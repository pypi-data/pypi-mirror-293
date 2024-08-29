"""Scaffold generator."""

import typing as t
from datetime import datetime
from pathlib import Path

from open_autonomy_compose.fsm.app import AbciAppSpecification
from open_autonomy_compose.fsm.base import WithParent
from open_autonomy_compose.fsm.scaffold.abci.generator import Scaffold as AbciScaffold


TEMPLATES = Path(__file__).parent / "templates"

CONSENSUS_BEHAVIOUR_PLACEHOLDER = "ScaffoldedConsensusBehaviour"
ABCI_APP_PLACEHOLDER = "ScaffoldedAbciApp"
ABCI_PLACEHOLDER = "__abci__"
NAME_PLACEHOLDER = "__name__"
AUHTOR_PLACEHOLDER = "__author__"
YEAR_PLACEHOLDER = "__year__"

CONSENSUS_BEHAVIOUR_TEMPLATE = "{name}ConsensusBehaviour"
ROUND_BEHAVIOUR_TEMPLATE = "{name}RoundBehaviour"
ABCI_APP_TEMPLATE = "{name}AbciApp"

DUMMY_HASH = "bafybei0000000000000000000000000000000000000000000000000000"


class AbciName:
    """Class to represent abci app name."""

    def __init__(self, name: str) -> None:
        """Initialize object."""
        self.name = name.replace("_abci", "")

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
        return CONSENSUS_BEHAVIOUR_TEMPLATE.format(name=self.name.title())

    @property
    def round_behaviour_name(self) -> str:
        """Round behaviour name."""
        return ROUND_BEHAVIOUR_TEMPLATE.format(name=self.name.title())


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
        return CONSENSUS_BEHAVIOUR_TEMPLATE.format(name=self.name.title())

    @property
    def vars(self) -> t.Dict[str, str]:
        """Vars."""
        return {
            CONSENSUS_BEHAVIOUR_PLACEHOLDER: self.consensus_behaviour_name,
            ABCI_APP_PLACEHOLDER: self.abci_app,
            ABCI_PLACEHOLDER: self.abci,
            NAME_PLACEHOLDER: self.name,
            AUHTOR_PLACEHOLDER: self.author,
            YEAR_PLACEHOLDER: self.year,
        }

    def sub(self, template: str) -> str:
        """Subtitute variables."""
        for var, val in self.vars.items():
            if var in template:
                template = template.replace(var, val)
        return template


class Scaffold:
    """Composition scaffold."""

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
        self.packages = packages
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

    def get_apps(self, specification: t.Dict) -> t.Dict[str, AbciAppSpecification]:
        """Get apps."""
        generated_apps = {}
        for app in specification["apps"]:
            author, name = app.split(".")
            spec = AbciAppSpecification.new(name=name, author=author)
            for initial_state in specification["initial_states"]:
                if initial_state.startswith(name):
                    spec.initial_states = list(
                        set([*spec.initial_states, WithParent.from_name(initial_state)])
                    )

            if len(spec.initial_states) == 0:
                raise ValueError(f"Not enough initial states for app '{author}.{name}'")

            if specification["start_state"].startswith(name):
                spec.start_state = WithParent.from_name(specification["start_state"])
                spec.initial_states = list(
                    set([*spec.initial_states, spec.start_state])
                )
            else:
                spec.start_state, *_ = spec.initial_states

            for final_state in specification["final_states"]:
                if final_state.startswith(name):
                    spec.final_states = list(
                        set([*spec.final_states, WithParent.from_name(final_state)])
                    )

            for state, transitions in specification["transitions"].items():
                if not state.startswith(name):
                    continue

                if "Finished" in state:
                    state_name = WithParent.from_name(state)
                    spec.transitions.transitions[state_name] = {}  # type: ignore[assignment]
                    spec.final_states = list(set([*spec.final_states, state_name]))
                    continue

                for event, next_state in transitions.items():
                    spec.add_transition(
                        from_state=WithParent.from_name(state),
                        to_state=WithParent.from_name(next_state),
                        event=event,
                    )
            generated_apps[name] = spec
        return generated_apps

    def _scaffold_app(self, name: str, speciification: t.Dict) -> None:
        """Scaffold app."""
        if name in (
            "registration_abci",
            "transaction_settlement_abci",
            "reset_pause_abci",
        ):
            return

        AbciScaffold(
            name=name,
            author=self.author,
            packages=self.packages,
        ).mkdir().write().hydrate(speciification=speciification)

    def hydrate(self, speciification: t.Dict) -> "Scaffold":
        """Hydrate the app with FSM speciification."""
        for name, spec in self.get_apps(specification=speciification).items():
            self._scaffold_app(
                name=name,
                speciification=spec.to_json(),
            )
        return self
