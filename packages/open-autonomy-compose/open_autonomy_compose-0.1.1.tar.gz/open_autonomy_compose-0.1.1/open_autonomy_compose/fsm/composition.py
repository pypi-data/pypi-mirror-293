# pylint: disable=unused-import, too-many-arguments, inconsistent-return-statements, too-many-instance-attributes
"""FSM Composition helpers."""

import ast
import inspect
import re
import typing as t
from collections import OrderedDict
from enum import Enum
from pathlib import Path
from types import ModuleType

from open_autonomy_compose.fsm.app import (  # noqa: F401
    AbciApp,
    AbciAppSpecification,
    AbciAppType,
    EventsType,
)
from open_autonomy_compose.fsm.base import Transitions, WithParent
from open_autonomy_compose.helpers.naming import snake_to_pascal_case
from open_autonomy_compose.helpers.package import load_module, load_package
from open_autonomy_compose.helpers.yaml import Yaml


class Composition:
    """Composition module representation."""

    def __init__(
        self,
        name: str,
        app: AbciAppType,
        events: EventsType,
        apps: t.Dict[str, AbciAppType],
        module: ModuleType,
    ) -> None:
        """Composition module."""
        self.name = name
        self.app = app
        self.events = events
        self.apps = apps
        self.module = module

    @staticmethod
    def find_chain(module: ModuleType) -> ast.Assign:  # type: ignore[return]
        """Find chain definition"""
        for node in ast.parse(inspect.getsource(module)).body:
            if (
                isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "chain"
            ):
                return node

            if (
                isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Attribute)
                and "chain(" in ast.unparse(node.value.func)
            ):
                return node

    @classmethod
    def parse_chain(
        cls, module: ModuleType
    ) -> t.Tuple[str, AbciAppType, t.Dict[str, AbciAppType]]:
        """Find chain definition"""
        apps = {}
        node = cls.find_chain(module=module)
        code = ast.unparse(node.value)
        for abci_module, abci_app in re.findall(
            r"([A-Z][a-zA-Z0-9]+\.)?([A-Z][a-zA-Z0-9]+)", code
        ):
            if abci_app in ("TERMINATE", "TerminationAbciApp"):
                continue
            if len(abci_module) > 0:
                abci_module = abci_module.replace(".", "")
                apps[abci_app] = getattr(getattr(module, abci_module), abci_app)
            else:
                apps[abci_app] = getattr(module, abci_app)
        name = node.targets[0].id  # type: ignore[attr-defined]
        app = getattr(module, name)
        return name, app, apps

    @classmethod
    def from_path(cls, path: Path) -> "Composition":
        """Load from path."""
        load_package(
            ptype="skill",
            path=path,
            loaded=[],
        )
        module = load_module(path=path, name="composition")
        name, app, apps = cls.parse_chain(module=module)
        events = {"SENTINAL": "sentinal"}
        for transition in app.transition_function.values():
            for event in transition.keys():
                events[event.name] = event.value

        return cls(
            name=name,
            app=app,
            events=Enum("Event", events),  # type: ignore[arg-type]
            apps=apps,
            module=module,
        )


class CompositionSpecification:
    """FSM Specification representation."""

    def __init__(
        self,
        name: WithParent,
        events: t.List[WithParent],
        apps: t.List[WithParent],
        start_state: WithParent,
        initial_states: t.List[WithParent],
        final_states: t.List[WithParent],
        transitions: Transitions,
        author: t.Optional[str] = None,
    ) -> None:
        """Initialize object."""
        self.name = name
        self.events = events
        self.apps = apps
        self.start_state = start_state
        self.initial_states = initial_states
        self.final_states = final_states
        self.transitions = transitions
        self.package = name.parent
        self.author = author

    def app_exists(self, app: WithParent) -> bool:
        """Get app specification."""
        for _app in self.apps:
            if _app.name() == app.name() and _app.parent == app.parent:
                return True
        return False

    def add_app(
        self,
        app: AbciAppSpecification,
        author: t.Optional[str] = None,
    ) -> "CompositionSpecification":
        """Add new app."""
        name = WithParent(
            obj=None,
            name=app.name.parent,
            parent=author or app.author,
        )
        if self.app_exists(name):
            return self

        self.apps.append(name)
        self.initial_states.extend(
            [
                WithParent(name=state.name(parent=False), parent=app.name.parent)
                for state in app.initial_states
            ]
        )
        self.final_states.extend(
            [
                WithParent(name=state.name(parent=False), parent=app.name.parent)
                for state in app.final_states
            ]
        )
        return self

    def set_start_state(self, state: WithParent) -> "CompositionSpecification":
        """Set start state."""
        self.start_state = state
        return self

    def add_transition(
        self,
        from_state: WithParent,
        to_state: WithParent,
        event: str,
    ) -> "CompositionSpecification":
        """Add a new transition."""
        self.transitions.add(
            from_state=from_state,
            to_state=to_state,
            event=event,
        )
        self.events = list(set([event, *self.events]))  # type: ignore[list-item]
        return self

    @classmethod
    def new(
        cls,
        name: str,
        author: t.Optional[str] = None,
    ) -> "CompositionSpecification":
        """Create a new specification."""
        return cls(
            name=WithParent(
                obj=None,
                name=f"{snake_to_pascal_case(name=name)}App",
                parent=name,
            ),
            events=[],
            apps=[],
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
            name=self.name.name(parent=True),
            events=self.events,
            apps=list(map(lambda x: x.name(parent=True), self.apps)),
            start_state=self.start_state.name(parent=True),
            initial_states=list(
                map(lambda x: x.name(parent=True), self.initial_states)
            ),
            final_states=list(map(lambda x: x.name(parent=True), self.final_states)),
            transitions=self.transitions.to_json(include_parent=True),
        )

    def to_yaml(self, file: Path) -> None:
        """Dump to YAML file."""
        with file.open("w+") as fp:
            Yaml.dump(self.to_json(), fp)

    @classmethod
    def from_json(
        cls,
        obj: t.Dict,
        author: t.Optional[str] = None,
    ) -> "CompositionSpecification":
        """Load from a YAML file."""
        return cls(
            name=WithParent.from_name(obj["name"]),
            events=obj["events"],
            apps=[WithParent.from_name(name=name) for name in obj["apps"]],
            start_state=WithParent.from_name(name=obj["start_state"]),
            initial_states=[
                WithParent.from_name(name=name) for name in obj["initial_states"]
            ],
            final_states=[
                WithParent.from_name(name=name) for name in obj["final_states"]
            ],
            transitions=Transitions.from_json(obj=obj["transitions"]),
            author=author,
        )

    @classmethod
    def from_yaml(
        cls,
        file: Path,
        author: t.Optional[str] = None,
    ) -> "CompositionSpecification":
        """Load from a YAML file."""
        with file.open("r", encoding="utf-8") as stream:
            obj = Yaml.load(stream=stream)
        return cls.from_json(
            obj=obj,
            author=author,
        )

    @classmethod
    def from_obj(cls, composition: Composition) -> "CompositionSpecification":
        """Load from compostion."""
        _, author, _, skill_name, *_ = composition.module.__name__.split(".")
        apps = []
        initial_states = set()
        final_states = set()  # type: ignore[var-annotated]
        for app in composition.apps.values():
            _author, _name, *_ = (
                app.__module__.replace("packages.", "")
                .replace("skills.", "")
                .replace(".rounds", "")
                .split(".")
            )
            apps.append(WithParent(obj=app, name=_name, parent=_author))
            initial_states.add(WithParent.from_cls(app.initial_round_cls))
            initial_states.update(map(WithParent.from_cls, app.initial_states))
            final_states.update(map(WithParent.from_cls, app.final_states))

        return cls(
            name=WithParent(
                obj=composition.app,
                name=composition.name,
                parent=skill_name,
            ),
            apps=apps,
            events=[event.name for event in composition.events],  # type: ignore[attr-defined]
            start_state=WithParent.from_cls(composition.app.initial_round_cls),
            initial_states=list(initial_states),
            final_states=list(final_states),
            transitions=Transitions.from_function(
                function=composition.app.transition_function,
            ),
            author=author,
        )

    def __repr__(self) -> str:
        """String representation."""
        return f"<CompositionSpecification name={self.name.name()}>"
