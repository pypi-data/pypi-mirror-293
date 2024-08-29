# pylint: disable=import-error, no-self-argument
"""Base classes for FSM apps."""

import typing as t
from collections import OrderedDict

from open_autonomy_compose.fsm.types import EventsType, StateType


def _find_parent(obj: t.Any) -> str:
    """Find parent name to a obj class.."""
    # packages, author, skill, package_name, ...
    _, _, _, parent, *_ = obj.__module__.split(".")
    return parent


def _to_name(obj: t.Any, include_parent: bool = False) -> str:
    """State class to name."""
    name = obj.__name__
    if include_parent:
        name = f"{_find_parent(obj=obj)}.{name}"
    return name


class WithParent:
    """Named object with parent."""

    def __init__(
        self,
        name: str,
        parent: t.Optional[str] = None,
        obj: t.Optional[t.Any] = None,
    ) -> None:
        """Initialize object."""
        self.obj = obj
        self.parent = parent or ""
        self._name = name

    def __str__(self) -> str:
        """String representation."""
        return self.name(parent=True)

    def __repr__(self) -> str:
        """String representation."""
        return self.name(parent=True)

    def __eq__(self, __value: object) -> bool:
        """Check equivilance"""
        if not isinstance(__value, WithParent):
            return NotImplemented
        return self.name(parent=True) == __value.name(parent=True)

    def __hash__(self) -> int:
        """Calculate hash."""
        return hash((self._name, self.parent))

    @classmethod
    def from_cls(cls, obj: t.Any) -> "WithParent":
        """Parse from an object."""
        return cls(
            obj=obj,
            name=_to_name(obj=obj),
            parent=_find_parent(obj=obj),
        )

    @classmethod
    def from_name(cls, name: str) -> "WithParent":
        """Parse from name string."""
        parent, name = name.split(".")
        return cls(
            obj=None,
            name=name,
            parent=parent,
        )

    def with_parent(cls, parent: str) -> "WithParent":
        """With new parent name."""
        return WithParent(
            name=cls._name,
            parent=parent,
            obj=cls.obj,
        )

    def name(self, parent: bool = False) -> str:
        """State name with parent."""
        if parent:
            return f"{self.parent}.{self._name}"
        return self._name


class Transitions:
    """Transitions."""

    def __init__(
        self,
        transitions: t.OrderedDict[WithParent, t.OrderedDict[str, WithParent]],
    ) -> None:
        """Initialize object."""
        self.transitions = transitions

    def add(
        self,
        from_state: WithParent,
        to_state: WithParent,
        event: str,
    ) -> None:
        """Add/update a transition."""
        self.transitions[from_state] = OrderedDict(
            {
                **self.transitions.get(from_state, OrderedDict()),
                event: to_state,
            }
        )

    def get(self, state: WithParent) -> t.Optional[t.OrderedDict[str, WithParent]]:
        """Get transitions for a state."""
        for _state, transitions in self:
            if _state.name() == state.name() and _state.parent == state.parent:
                return transitions  # type: ignore[return-value]
        return None

    @classmethod
    def from_function(
        cls,
        function: t.OrderedDict[StateType, t.OrderedDict[EventsType, StateType]],
    ) -> "Transitions":
        """Parse from function."""
        transitions: t.OrderedDict[
            WithParent, t.OrderedDict[str, WithParent]
        ] = OrderedDict()
        for state, next_states in function.items():
            ns = WithParent.from_cls(obj=state)
            transitions[ns] = OrderedDict()
            for event, next_state in next_states.items():
                transitions[ns][event.name] = WithParent.from_cls(obj=next_state)
        return cls(
            transitions=transitions,
        )

    @classmethod
    def from_json(
        cls,
        obj: t.Dict[str, t.Dict[str, str]],
        parent: t.Optional[str] = None,
    ) -> "Transitions":
        """Parse from function."""
        transitions: t.OrderedDict[
            WithParent, t.OrderedDict[str, WithParent]
        ] = OrderedDict()
        for state, next_states in obj.items():
            ns = (
                WithParent.from_name(state)
                if "." in state
                else WithParent(obj=None, name=state, parent=parent)
            )
            transitions[ns] = OrderedDict()
            for event, next_state in next_states.items():
                transitions[ns][event] = (
                    WithParent.from_name(next_state)
                    if "." in next_state
                    else WithParent(obj=None, name=state, parent=parent)
                )
        return cls(
            transitions=transitions,
        )

    def to_json(
        self, include_parent: bool = False
    ) -> t.OrderedDict[str, t.OrderedDict[str, str]]:
        """To json object."""
        transitions: t.OrderedDict[str, t.OrderedDict[str, str]] = OrderedDict()
        for state, next_states in self.transitions.items():
            name = state.name(parent=include_parent)
            transitions[name] = OrderedDict()
            for event, next_state in next_states.items():
                transitions[name][event] = next_state.name(parent=include_parent)
        return transitions

    def __repr__(self) -> str:
        """String representation."""
        s = ""
        for state, exits in self.transitions.items():
            s += f"{state}:\n"
            for event, next_event in exits.items():
                s += f"    {event}: {next_event}\n"
        s = s[:-1]
        return s

    def __iter__(self) -> t.Iterator[t.Tuple[WithParent, t.Dict[str, WithParent]]]:
        """Iter over transitions."""
        yield from self.transitions.items()
