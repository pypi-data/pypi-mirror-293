# pylint: disable=too-few-public-methods, too-many-arguments, no-value-for-parameter
"""ABCI App helpers"""

import ast
import typing as t
from collections import OrderedDict
from pathlib import Path
from types import ModuleType

from open_autonomy_compose.fsm import modifiers
from open_autonomy_compose.fsm.base import Transitions, WithParent
from open_autonomy_compose.fsm.modifiers.base import Ast
from open_autonomy_compose.fsm.types import (
    AbciAppType,
    BaseRound,
    BehaviourType,
    EventsType,
    PayloadType,
    RoundBehaviourType,
    StatePosition,
    StateType,
)
from open_autonomy_compose.helpers.naming import snake_to_pascal_case
from open_autonomy_compose.helpers.package import load_module, load_package
from open_autonomy_compose.helpers.yaml import Yaml


class Payloads:
    """Payloads module."""

    def __init__(
        self,
        payloads: t.Dict[str, PayloadType],
        obj: ModuleType,
    ) -> None:
        """Initialize object."""
        self.payloads = payloads
        self.obj = obj

    @classmethod
    def from_path(cls, path: Path) -> "Payloads":
        """Load from path."""
        payloads = {}
        module = load_module(path=path, name="behaviours")
        for name in dir(module):
            obj = getattr(module, name)
            if not hasattr(obj, "__bases__"):
                continue
            if name.endswith("Payload"):
                payloads[name] = obj
        return cls(payloads, module)


class Behaviours:
    """Behaviours module."""

    def __init__(
        self,
        round_behaviour: RoundBehaviourType,
        behaviours: t.Dict[str, BehaviourType],
        obj: ModuleType,
    ) -> None:
        """Initialize object."""
        self.round_behaviour = round_behaviour
        self.behaviours = behaviours
        self.obj = obj

    @classmethod
    def from_path(cls, path: Path) -> "Behaviours":
        """Load from path."""
        round_behaviour = None
        behaviours = {}
        module = load_module(path=path, name="behaviours")
        for name in dir(module):
            obj = getattr(module, name)
            if not hasattr(obj, "__bases__"):
                continue
            for base in getattr(obj, "__bases__"):  # noqa: B009
                if base.__name__ == "AbstractRoundBehaviour":
                    obj.__name__ = name
                    round_behaviour = obj
                    break
            else:
                if name.endswith("Round"):
                    behaviours[name] = obj
        return cls(round_behaviour, behaviours, module)  # type: ignore[arg-type]


class Rounds:
    """Round module."""

    def __init__(
        self,
        abci_app: AbciAppType,
        rounds: t.Dict[str, StateType],
        events: EventsType,
        obj: ModuleType,
    ) -> None:
        """Initialize object."""
        self.abci_app = abci_app
        self.rounds = rounds
        self.events = events
        self.obj = obj

    @classmethod
    def from_path(cls, path: Path) -> "Payloads":
        """Load from path."""
        abci_app = None
        events = None
        rounds = {}
        module = load_module(path=path, name="rounds")
        for name in dir(module):
            obj = getattr(module, name)
            if not hasattr(obj, "__bases__"):
                continue
            if name == "Event":
                events = obj
                continue
            for base in getattr(obj, "__bases__"):  # noqa: B009
                if base.__name__ == "AbciApp":
                    obj.__name__ = name
                    abci_app = obj
                    break
            else:
                if name.endswith("Round"):
                    rounds[name] = obj
        return cls(abci_app, rounds, events, module)  # type: ignore[return-value, arg-type]


class AbciApp:
    """Abci app class."""

    def __init__(
        self,
        name: str,
        rounds: Rounds,
        behaviours: Behaviours,
        payloads: Payloads,
        config: t.OrderedDict,
        author: t.Optional[str] = None,
    ) -> None:
        """Composition module."""
        self.name = name
        self.rounds = rounds
        self.behaviours = behaviours
        self.payloads = payloads
        self.author = author
        self.config = config

    @classmethod
    def from_path(cls, path: Path) -> "AbciApp":
        """Load from path."""
        load_package(
            ptype="skill",
            path=path,
            loaded=[],
        )
        *_, author, _, name = path.parts

        rounds = Rounds.from_path(path=path)
        behaviours = Behaviours.from_path(path=path)
        payloads = Payloads.from_path(path=path)
        with (path / "skill.yaml").open("r", encoding="utf-8") as stream:
            config = Yaml.load(stream=stream)
        return cls(
            name=name,
            rounds=rounds,  # type: ignore[arg-type]
            behaviours=behaviours,
            payloads=payloads,
            config=config,  # type: ignore[arg-type]
            author=author,
        )


class AbciAppSpecification:
    """FSM Specification representation."""

    def __init__(
        self,
        name: WithParent,
        events: t.List[str],
        start_state: WithParent,
        initial_states: t.List[WithParent],
        final_states: t.List[WithParent],
        transitions: Transitions,
        package: t.Optional[str] = None,
        author: t.Optional[str] = None,
    ) -> None:
        """Initialize object."""
        self.name = name
        self.events = events
        self.start_state = start_state
        self.initial_states = initial_states
        self.final_states = final_states
        self.transitions = transitions
        self.package = package
        self.author = author

    def add_transition(
        self,
        from_state: WithParent,
        to_state: WithParent,
        event: str,
    ) -> "AbciAppSpecification":
        """Add a new transition."""
        self.transitions.add(
            from_state=from_state,
            to_state=to_state,
            event=event,
        )
        self.events = list(set([event, *self.events]))
        return self

    @classmethod
    def new(
        cls,
        name: str,
        author: t.Optional[str] = None,
    ) -> "AbciAppSpecification":
        """Create a new specification."""
        return cls(
            name=WithParent(
                obj=None,
                name=f"{snake_to_pascal_case(name=name)}App",
                parent=name,
            ),
            events=[],
            start_state=WithParent(
                obj=None, name="InitialRound", parent="initial_abci"
            ),
            initial_states=[],
            final_states=[],
            transitions=Transitions(transitions=OrderedDict()),
            author=author,
        )

    def to_json(self) -> t.OrderedDict:
        """To JSON object."""
        return OrderedDict(
            name=self.name.name(),
            events=self.events,
            start_state=self.start_state.name(),
            initial_states=list(map(lambda x: x.name(), self.initial_states)),
            final_states=list(map(lambda x: x.name(), self.final_states)),
            transitions=self.transitions.to_json(),
        )

    def to_yaml(self, file: Path) -> None:
        """Dump to YAML file."""
        with file.open("w+") as fp:
            Yaml.dump(self.to_json(), fp)

    @classmethod
    def from_json(
        cls,
        obj: t.Dict,
        package: t.Optional[str] = None,
        author: t.Optional[str] = None,
    ) -> "AbciAppSpecification":
        """Load from a YAML file."""
        return cls(
            name=WithParent(name=obj["name"], parent=package),
            events=obj["events"],
            start_state=WithParent(obj=None, name=obj["start_state"], parent=package),
            initial_states=[
                WithParent(obj=None, name=name, parent=package)
                for name in obj["initial_states"]
            ],
            final_states=[
                WithParent(obj=None, name=name, parent=package)
                for name in obj["final_states"]
            ],
            transitions=Transitions.from_json(
                obj=obj["transitions"],
                parent=package,
            ),
            package=package,
            author=author,
        )

    @classmethod
    def from_yaml(
        cls,
        file: Path,
        package: t.Optional[str] = None,
        author: t.Optional[str] = None,
    ) -> "AbciAppSpecification":
        """Load from a YAML file."""
        with file.open("r", encoding="utf-8") as stream:
            obj = Yaml.load(stream=stream)
        return cls.from_json(
            obj=obj,
            package=package,
            author=author,
        )

    @classmethod
    def from_obj(cls, abci: AbciApp) -> "AbciAppSpecification":
        """Load from compostion."""
        return cls(
            name=WithParent(
                obj=abci.rounds.abci_app,
                name=abci.rounds.abci_app.__name__,  # type: ignore[attr-defined]
                parent=abci.name,
            ),
            events=[event.name for event in abci.rounds.events],  # type: ignore
            start_state=WithParent.from_cls(abci.rounds.abci_app.initial_round_cls),
            initial_states=[
                WithParent.from_cls(state)
                for state in getattr(abci.rounds.abci_app, "initial_states", [])
            ],
            final_states=[
                WithParent.from_cls(state)
                for state in getattr(abci.rounds.abci_app, "final_states", [])
            ],
            transitions=Transitions.from_function(
                function=abci.rounds.abci_app.transition_function,
            ),
            package=abci.name,
            author=abci.author,
        )

    def __getitem__(self, name: str) -> WithParent:
        """Get state name."""
        state = WithParent(name=name, parent=self.package)
        if self.transitions.get(state=state) is None:
            raise ValueError(f"State {name} does not exist on {self.package}")
        return state

    def __repr__(self) -> str:
        """String representation."""
        return f"<AbciAppSpecification name={self.name.name()}>"


class AbciModifier:
    """AbciApp modifier."""

    def __init__(self, app: Path) -> None:
        """Initialize object."""
        self.app = app
        self.payloads = modifiers.payloads.Payloads({}, path=app / "payloads.py")
        self.behaviours = modifiers.behaviours.Behaviours(
            {},
            round_behaviour=modifiers.behaviours.RoundBehaviour(path=app),  # type: ignore[call-arg]
            path=app,
        )
        self.rounds = modifiers.rounds.Rounds(app=modifiers.rounds.AbciApp())  # type: ignore[call-arg]

    def create_new_state(
        self,
        name: str,
        base: BaseRound,
        state_pos: StatePosition,
        payload_attributes: t.Optional[t.Dict[str, str]] = None,
        selection_key: t.Optional[str] = None,
        collection_key: t.Optional[str] = None,
        pre_conditions: t.Optional[
            t.List[t.Union[ast.Constant, ast.Name, ast.Attribute]]
        ] = None,
        post_conditions: t.Optional[
            t.List[t.Union[ast.Constant, ast.Name, ast.Attribute]]
        ] = None,
    ) -> None:
        """Create new round."""
        payload_class = f"{name}Payload"
        round_class = f"{name}Round"
        behaviour_class = f"{name}Behaviour"

        self.payloads = self.payloads.create(
            name=payload_class, attributes=payload_attributes or {}
        )
        self.rounds.modifier.add(  # type: ignore[attr-defined]
            Ast.import_from(
                module=self.payloads.module,
                names=[payload_class],
            ),
            index=1,
        )
        self.rounds.modifier.add(  # type: ignore[attr-defined]
            Ast.import_from(
                module="packages.valory.skills.abstract_round_abci.base",
                names=[base.name],
            ),
            index=1,
        )
        self.rounds = self.rounds.create(
            name=round_class,
            state_pos=state_pos,
            base=base,
            payload_class=payload_class,
            selection_key=selection_key,
            collection_key=collection_key,
            pre_conditions=pre_conditions,
            post_conditions=post_conditions,
        )
        self.behaviours.modifier.add(  # type: ignore[attr-defined]
            Ast.import_from(
                module=self.payloads.module,
                names=[payload_class],
            ),
            index=1,
        )
        self.behaviours.modifier.add(  # type: ignore[attr-defined]
            Ast.import_from(
                module=self.rounds.module,
                names=[round_class],
            ),
            index=1,
        )
        self.behaviours = self.behaviours.create(
            name=behaviour_class,
            matching_round=round_class,
            payload_class=payload_class,
            payload_value="content",
            state_pos=state_pos,
        )
