# pylint: disable=too-many-locals
"""Scaffold generator."""

import ast
import typing as t
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

from open_autonomy_compose.fsm import modifiers
from open_autonomy_compose.fsm.modifiers.base import Ast
from open_autonomy_compose.fsm.scaffold.base import Modifier, get_event_enum
from open_autonomy_compose.fsm.types import BaseRound


TEMPLATES = Path(__file__).parent / "templates"

ROUND_BEHAVIOUR_PLACEHOLDER = "ScaffoldedRoundBehaviour"
ABCI_APP_PLACEHOLDER = "ScaffoldedAbciApp"
ABCI_PLACEHOLDER = "__abci__"
NAME_PLACEHOLDER = "__name__"
AUTHOR_PLACEHOLDER = "__author__"
YEAR_PLACEHOLDER = "__year__"

CONSENSUS_BEHAVIOUR_TEMPLATE = "{name}RoundBehaviour"
ABCI_APP_TEMPLATE = "{name}AbciApp"


class Vars:
    """FSM template vars."""

    def __init__(
        self,
        name: str,
        author: str,
    ) -> None:
        """Initialize object."""
        self.author = author
        self.name = name.replace("_abci", "")
        self.year = str(datetime.now().year)

    @property
    def abci(self) -> str:
        """ABCI name"""
        return self.name + "_abci"

    @property
    def abci_app(self) -> str:
        """Abci App name"""
        return ABCI_APP_TEMPLATE.format(
            name="".join(map(lambda x: x.title(), self.name.split("_")))
        )

    @property
    def consensus_behaviour_name(self) -> str:
        """Consensus behaviour name."""
        return CONSENSUS_BEHAVIOUR_TEMPLATE.format(
            name="".join(map(lambda x: x.title(), self.name.split("_")))
        )

    @property
    def vars(self) -> t.Dict[str, str]:
        """Vars."""
        return {
            ROUND_BEHAVIOUR_PLACEHOLDER: self.consensus_behaviour_name,
            ABCI_APP_PLACEHOLDER: self.abci_app,
            ABCI_PLACEHOLDER: self.abci,
            NAME_PLACEHOLDER: self.name,
            AUTHOR_PLACEHOLDER: self.author,
            YEAR_PLACEHOLDER: self.year,
        }

    def sub(self, template: str) -> str:
        """Subtitute variables."""
        for var, val in self.vars.items():
            if var in template:
                template = template.replace(var, val)
        return template


class Scaffold:
    """ABCI skill scaffold."""

    def __init__(
        self,
        name: str,
        author: str,
        packages: Path,
    ) -> None:
        """Initialize object."""
        self.name = name
        self.author = author
        self.vars = Vars(name=name, author=author)
        self.path = packages / self.author / "skills" / self.vars.abci

    def mkdir(self) -> "Scaffold":
        """Make directory."""
        if self.path.exists():
            raise FileExistsError(f"A skill package already exist @ {self.path}")
        self.path.mkdir(parents=True)
        return self

    def write(self) -> "Scaffold":
        """Write modules."""
        for file in TEMPLATES.iterdir():
            if not file.is_file():
                continue
            output = self.path / file.name
            content = self.vars.sub(template=file.read_text())
            output.write_text(data=content, encoding="utf-8")
        return self

    def hydrate(self, speciification: t.Dict) -> "Scaffold":
        """Hydrate the app with FSM speciification."""
        app = Path.cwd() / "packages" / self.author / "skills" / self.vars.abci
        rounds = Modifier(app / "rounds.py")
        payloads = Modifier(app / "payloads.py")
        behaviours = Modifier(app / "behaviours.py")

        payload_nodes = []
        behaviour_nodes = []
        state_nodes = []

        event_class = get_event_enum(events=speciification["events"])

        states = set(speciification["transitions"])
        for state in states:
            if state.startswith("Finished"):
                state_nodes.append(
                    modifiers.rounds.Round.new(
                        name=state,
                        base=BaseRound.DegenerateRound,
                    )
                )
                continue
            prefix = state.replace("Round", "")
            payload_class = f"{prefix}Payload"
            behaviour_class = f"{prefix}Behaviour"
            state_nodes.append(
                modifiers.rounds.Round.new(
                    name=state,
                    base=BaseRound.CollectDifferentUntilThresholdRound,
                    payload_class=payload_class,
                    selection_key="content",
                    collection_key="content",
                )
            )
            payload_nodes.append(
                modifiers.payloads.Payload.new(
                    name=payload_class, attributes={"content": "str"}
                )
            )
            behaviour_nodes.append(
                modifiers.behaviours.Behaviour.new(
                    name=behaviour_class,
                    matching_round=state,
                    payload_class=payload_class,
                    payload_value="content",
                )
            )

        abci_app_ast = rounds.objects[self.vars.abci_app]
        for node in abci_app_ast.body:
            if not isinstance(node, ast.AnnAssign):
                continue
            if t.cast(ast.Name, node.target).id == "initial_round_cls":
                node.value = Ast.name(
                    value=speciification["start_state"], ctx=ast.Load()
                )

            if t.cast(ast.Name, node.target).id == "initial_states":
                node.value = (
                    ast.Set(
                        elts=[
                            Ast.name(value=state, ctx=ast.Load())
                            for state in speciification["initial_states"]
                        ]
                    )
                    if len(speciification["initial_states"]) > 0
                    else Ast.call(func="set")
                )

            if t.cast(ast.Name, node.target).id == "transition_function":
                node.value = ast.Dict(
                    keys=[
                        Ast.name(value=state, ctx=ast.Load())
                        for state in speciification["transitions"]
                    ],
                    values=[
                        ast.Dict(
                            keys=[
                                ast.Attribute(
                                    value=Ast.name("Event", ctx=ast.Load()),
                                    attr=_event,
                                    ctx=ast.Load(),
                                )
                                for _event in _transitions
                            ],
                            values=[
                                Ast.name(value=_state, ctx=ast.Load())
                                for _state in _transitions.values()
                            ],
                        )
                        for _transitions in speciification["transitions"].values()
                    ],
                )

            if t.cast(ast.Name, node.target).id == "final_states":
                node.value = (
                    ast.Set(
                        elts=[
                            Ast.name(value=state, ctx=ast.Load())
                            for state in speciification["final_states"]
                        ]
                    )
                    if len(speciification["final_states"]) > 0
                    else Ast.call(func="set")
                )

            if t.cast(ast.Name, node.target).id == "db_pre_conditions":
                node.value = ast.Dict(
                    keys=[
                        Ast.name(value=state, ctx=ast.Load())
                        for state in speciification["initial_states"]
                    ],
                    values=[
                        Ast.call(func="set") for _ in speciification["initial_states"]
                    ],
                )

            if t.cast(ast.Name, node.target).id == "db_post_conditions":
                node.value = ast.Dict(
                    keys=[
                        Ast.name(value=state, ctx=ast.Load())
                        for state in speciification["final_states"]
                    ],
                    values=[
                        # TOFIX: Port from genie
                        Ast.call(func="set")
                        for _ in set(speciification["final_states"])
                    ],
                )

        round_behaviour_ast = behaviours.objects[self.vars.consensus_behaviour_name]
        for node in round_behaviour_ast.body:
            if isinstance(node, ast.Assign):
                if t.cast(ast.Name, node.targets[0]).id == "initial_behaviour_cls":
                    node.value = Ast.name(
                        value=speciification["start_state"].replace(
                            "Round", "Behaviour"
                        ),
                        ctx=ast.Load(),
                    )

            if isinstance(node, ast.AnnAssign):
                if t.cast(ast.Name, node.target).id == "behaviours":
                    node.value = (
                        ast.Set(
                            elts=[
                                Ast.name(value=node.name, ctx=ast.Load())
                                for node in behaviour_nodes
                            ]
                        )
                        if len(behaviour_nodes) > 0
                        else Ast.call(func="set")
                    )

        payloads.objects = OrderedDict(
            {node.name: node for node in payload_nodes},
        )
        rounds.objects = OrderedDict(
            {
                event_class.name: event_class,
                "SynchronizedData": rounds.objects["SynchronizedData"],
                **{node.name: node for node in state_nodes},
                abci_app_ast.name: abci_app_ast,
            }
        )
        rounds.imports.append(
            Ast.import_from(
                module=payloads.module, names=[node.name for node in payload_nodes]
            )
        )
        behaviours.objects = OrderedDict(
            {
                "BaseBehaviour": behaviours.objects["BaseBehaviour"],
                **{node.name: node for node in behaviour_nodes},
                round_behaviour_ast.name: round_behaviour_ast,
            }
        )
        behaviours.imports.append(
            Ast.import_from(
                rounds.module,
                names=[
                    node.name
                    for node in state_nodes
                    if not node.name.startswith("Finished")
                ],
            )
        )
        behaviours.imports.append(
            Ast.import_from(
                module=payloads.module, names=[node.name for node in payload_nodes]
            )
        )

        payloads.write()
        rounds.write()
        behaviours.write()

        return self
