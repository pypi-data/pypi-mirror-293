# pylint: disable=arguments-renamed, no-member, no-value-for-parameter, unexpected-keyword-arg, too-many-arguments
"""Rounds.py modifier."""

import ast
import inspect
import typing as t
from pathlib import Path

from open_autonomy_compose.fsm.modifiers.base import Ast, ClassModifier, Modifier
from open_autonomy_compose.fsm.types import (
    AbciAppType,
    BaseRound,
    EventsType,
    StatePosition,
    StateType,
)
from open_autonomy_compose.helpers.package import load_module


class Events(ClassModifier):
    """Events modifier."""

    def __init__(self, enum: EventsType, path: Path) -> None:
        """Initialize object."""
        super().__init__(enum, path)


class Round(ClassModifier):
    """Round modifier."""

    def __init__(self, obj: StateType, path: Path) -> None:
        """Initialize object."""
        super().__init__(obj, path)

    @staticmethod
    def new(
        name: str,
        base: BaseRound,
        payload_class: t.Optional[str] = None,
        selection_key: t.Optional[str] = None,
        collection_key: t.Optional[str] = None,
    ) -> ast.ClassDef:
        """Create new round class."""
        body = [
            Ast.expr(Ast.constant(f"""{name} round implementation.""")),
            Ast.assign(
                name="synchronized_data_class",
                value=Ast.name("SynchronizedData", ctx=ast.Load()),
            ),
            Ast.assign(
                name="done_event",
                value=ast.Attribute(  # type: ignore[arg-type]
                    value=ast.Name(id="Event", ctx=ast.Load()),
                    attr="DONE",
                    ctx=ast.Load(),
                ),
            ),
        ]
        if payload_class is not None:
            body.append(
                Ast.assign(
                    name="payload_class",
                    value=Ast.name(payload_class, ctx=ast.Load()),
                )
            )
        if selection_key is not None:
            body.append(
                Ast.assign(
                    name="selection_key",
                    value=Ast.constant(selection_key),
                )
            )
        if collection_key is not None:
            body.append(
                Ast.assign(
                    name="collection_key",
                    value=Ast.constant(collection_key),
                )
            )
        return Ast.cls(
            name=name,
            bases=[base.value],
            body=body,
        )


class AbciApp(ClassModifier):
    """AbciApp modifier."""

    def __init__(self, obj: AbciAppType, path: Path) -> None:  # type: ignore
        """Initialize object."""
        super().__init__(obj, path)

    def add(  # type: ignore[override]
        self,
        name: str,
        state_pos: StatePosition,
        pre_conditions: t.Optional[
            t.List[t.Union[ast.Constant, ast.Name, ast.Attribute]]
        ] = None,
        post_conditions: t.Optional[
            t.List[t.Union[ast.Constant, ast.Name, ast.Attribute]]
        ] = None,
    ) -> ast.ClassDef:
        """Add new state to the AbciApp definition."""
        (node,) = ast.parse(inspect.getsource(self.app)).body  # type: ignore[attr-defined]
        for expr in node.body:  # type: ignore[attr-defined]
            if not isinstance(expr, ast.AnnAssign):
                continue

            expr = t.cast(ast.AnnAssign, expr)
            if (
                state_pos == StatePosition.START
                and expr.target.id == "initial_round_cls"  # type: ignore[attr-defined]
            ):
                expr.value = Ast.name(name, ctx=ast.Load())

            if state_pos == StatePosition.START and expr.target.id == "initial_states":  # type: ignore[attr-defined]
                expr.value.elts = [  # type: ignore[union-attr]
                    *expr.value.elts,  # type: ignore[union-attr]
                    Ast.name(name, ctx=ast.Load()),
                ]

            if (
                state_pos == StatePosition.INITIAL
                and expr.target.id == "initial_states"  # type: ignore[attr-defined]
            ):
                expr.value.elts = [  # type: ignore[union-attr]
                    *expr.value.elts,  # type: ignore[union-attr]
                    Ast.name(name, ctx=ast.Load()),
                ]

            if state_pos == StatePosition.FINAL and expr.target.id == "final_states":  # type: ignore[attr-defined]
                expr.value.elts = [  # type: ignore[union-attr]
                    *expr.value.elts,  # type: ignore[union-attr]
                    Ast.name(name, ctx=ast.Load()),
                ]

            if expr.target.id == "transition_function":  # type: ignore[attr-defined]
                transition_function = t.cast(ast.Dict, expr.value)
                transition_function.keys.append(Ast.name(name, ctx=ast.Load()))
                transition_function.values.append(
                    ast.Dict(
                        keys=[],
                        values=[],
                    )
                )

            if expr.target.id == "db_pre_conditions" and pre_conditions:  # type: ignore[attr-defined]
                db_pre_conditions = t.cast(ast.Dict, expr.value)
                db_pre_conditions.keys.append(Ast.name(name, ctx=ast.Load()))
                db_pre_conditions.values.append(ast.Set(elts=pre_conditions))

            if expr.target.id == "db_post_conditions" and post_conditions:  # type: ignore[attr-defined]
                db_post_conditions = t.cast(ast.Dict, expr.value)
                db_post_conditions.keys.append(Ast.name(name, ctx=ast.Load()))
                db_post_conditions.values.append(ast.Set(elts=post_conditions))
        return node  # type: ignore[return-value]


class Rounds(Modifier):
    """Rounds.py modifier."""

    def __init__(
        self,
        app: AbciApp,
        events: Events,
        rounds: t.Dict[str, Round],
        path: Path,
    ) -> None:
        """Initialize object."""
        super().__init__(path=path)

        self.app = app
        self.events = events
        self.rounds = rounds

    def create(
        self,
        name: str,
        base: BaseRound,
        state_pos: StatePosition,
        payload_class: str,
        selection_key: t.Optional[str] = None,
        collection_key: t.Optional[str] = None,
        pre_conditions: t.Optional[
            t.List[t.Union[ast.Constant, ast.Name, ast.Attribute]]
        ] = None,
        post_conditions: t.Optional[
            t.List[t.Union[ast.Constant, ast.Name, ast.Attribute]]
        ] = None,
    ) -> "Rounds":
        """Create a new round."""
        self.add(
            node=Round.new(
                name=name,
                base=base,
                payload_class=payload_class,
                selection_key=selection_key,
                collection_key=collection_key,
            )
        )
        self.update(
            self.app.add(
                name=name,
                state_pos=state_pos,
                pre_conditions=pre_conditions,
                post_conditions=post_conditions,
            )
        )
        return self.from_path(path=self.path)

    @classmethod
    def from_path(cls, path: Path) -> "Rounds":
        """Load from path."""
        if not (path / "rounds.py").exists():
            raise FileNotFoundError(f"Cannot find the rounds module module for {path}")

        rounds = {}
        event_cls = None
        abci_app_cls = None
        module = load_module(path=path, name="rounds")
        for name in dir(module):
            obj = getattr(module, name)
            try:
                if obj.__name__ == "Event":
                    event_cls = obj
                    continue

                if obj.__name__.endswith("Round"):
                    rounds[obj.__name__] = Round(obj)  # type: ignore[call-arg]
                    continue

                for base in obj.__bases__:
                    if base.__name__ == "AbciApp":
                        obj.__name__ = name
                        abci_app_cls = obj
            except AttributeError:
                continue

        return cls(  # type: ignore[call-arg]
            app=AbciApp(app=abci_app_cls),  # type: ignore[call-arg]
            events=Events(enum=event_cls),  # type: ignore
            rounds=rounds,
            modifier=Modifier(path=path / "rounds.py"),
            path=path,
        )
