# pylint: disable=arguments-renamed, no-member, no-value-for-parameter, unexpected-keyword-arg
"""Behaviours.py modifier."""

import ast
import inspect
import typing as t
from pathlib import Path

from open_autonomy_compose.fsm.modifiers.base import Ast, ClassModifier, Modifier
from open_autonomy_compose.fsm.types import BehaviourType, StatePosition
from open_autonomy_compose.helpers.package import load_module


def async_act_node(
    payload_class: str,
    payload_value: t.Any,
) -> ast.FunctionDef:
    """Async act function definition."""
    return ast.FunctionDef(
        name="async_act",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="self")],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[
            ast.Expr(value=ast.Constant(value="Do the action.")),
            ast.With(
                items=[
                    ast.withitem(
                        context_expr=ast.Call(
                            func=ast.Attribute(
                                value=ast.Call(
                                    func=ast.Attribute(
                                        value=ast.Attribute(
                                            value=ast.Attribute(
                                                value=ast.Name(
                                                    id="self", ctx=ast.Load()
                                                ),
                                                attr="context",
                                                ctx=ast.Load(),
                                            ),
                                            attr="benchmark_tool",
                                            ctx=ast.Load(),
                                        ),
                                        attr="measure",
                                        ctx=ast.Load(),
                                    ),
                                    args=[
                                        ast.Attribute(
                                            value=ast.Name(id="self", ctx=ast.Load()),
                                            attr="behaviour_id",
                                            ctx=ast.Load(),
                                        )
                                    ],
                                    keywords=[],
                                ),
                                attr="local",
                                ctx=ast.Load(),
                            ),
                            args=[],
                            keywords=[],
                        )
                    )
                ],
                body=[
                    ast.Assign(
                        targets=[ast.Name(id="payload", ctx=ast.Store())],
                        value=ast.Call(
                            func=ast.Name(id=payload_class, ctx=ast.Load()),
                            args=[
                                ast.Attribute(
                                    value=ast.Attribute(
                                        value=ast.Name(id="self", ctx=ast.Load()),
                                        attr="context",
                                        ctx=ast.Load(),
                                    ),
                                    attr="agent_address",
                                    ctx=ast.Load(),
                                ),
                                ast.Constant(value=payload_value),
                            ],
                            keywords=[],
                        ),
                        lineno=0,
                    )
                ],
                lineno=0,
            ),
            ast.With(
                items=[
                    ast.withitem(
                        context_expr=ast.Call(
                            func=ast.Attribute(
                                value=ast.Call(
                                    func=ast.Attribute(
                                        value=ast.Attribute(
                                            value=ast.Attribute(
                                                value=ast.Name(
                                                    id="self", ctx=ast.Load()
                                                ),
                                                attr="context",
                                                ctx=ast.Load(),
                                            ),
                                            attr="benchmark_tool",
                                            ctx=ast.Load(),
                                        ),
                                        attr="measure",
                                        ctx=ast.Load(),
                                    ),
                                    args=[
                                        ast.Attribute(
                                            value=ast.Name(id="self", ctx=ast.Load()),
                                            attr="behaviour_id",
                                            ctx=ast.Load(),
                                        )
                                    ],
                                    keywords=[],
                                ),
                                attr="consensus",
                                ctx=ast.Load(),
                            ),
                            args=[],
                            keywords=[],
                        )
                    )
                ],
                body=[
                    ast.Expr(
                        value=ast.YieldFrom(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id="self", ctx=ast.Load()),
                                    attr="send_a2a_transaction",
                                    ctx=ast.Load(),
                                ),
                                args=[ast.Name(id="payload", ctx=ast.Load())],
                                keywords=[],
                            )
                        )
                    ),
                    ast.Expr(
                        value=ast.YieldFrom(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id="self", ctx=ast.Load()),
                                    attr="wait_until_round_end",
                                    ctx=ast.Load(),
                                ),
                                args=[],
                                keywords=[],
                            )
                        )
                    ),
                ],
                lineno=0,
            ),
            ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="self", ctx=ast.Load()),
                        attr="set_done",
                        ctx=ast.Load(),
                    ),
                    args=[],
                    keywords=[],
                )
            ),
        ],
        decorator_list=[],
        returns=ast.Attribute(
            value=ast.Name(id="t", ctx=ast.Load()), attr="Generator", ctx=ast.Load()
        ),
        lineno=0,
    )


class Behaviour(ClassModifier):
    """Class to represent Behaviour object"""

    def __init__(self, obj: BehaviourType, path: Path) -> None:
        """Initialize object."""
        super().__init__(obj, path)

    @staticmethod
    def new(
        name: str,
        matching_round: str,
        payload_class: str,
        payload_value: t.Any,
    ) -> ast.ClassDef:
        """Create a new behaviour."""
        body = [
            Ast.expr(Ast.constant(f"""{name} behaviour implementation.""")),
            Ast.assign(
                name="matching_round",
                value=Ast.name(matching_round, ctx=ast.Load()),
            ),
            async_act_node(payload_class=payload_class, payload_value=payload_value),
        ]
        return Ast.cls(
            name=name,
            bases=["BaseBehaviour"],
            body=body,
        )


class RoundBehaviour(ClassModifier):
    """Class to represent Behaviour object"""

    def add(self, name: str, state_pos: StatePosition) -> ast.ClassDef:  # type: ignore[override]
        """Add new behaviour."""
        tree = ast.parse(inspect.getsource(self._obj))  # type: ignore[attr-defined]
        (cls,) = tree.body
        for node in cls.body:  # type: ignore[attr-defined]
            if state_pos == StatePosition.START and isinstance(node, ast.Assign):
                (target,) = node.targets
                if target.id != "initial_behaviour_cls":  # type: ignore[attr-defined]
                    continue
                node.value = Ast.name(name, ctx=ast.Load())
            if not isinstance(node, ast.AnnAssign):
                continue
            if node.target.id != "behaviours":  # type: ignore[attr-defined]
                continue
            node.value.elts = [*node.value.elts, Ast.name(name, ctx=ast.Load())]  # type: ignore[union-attr]
        return cls  # type: ignore[return-value]


class Behaviours(Modifier):
    """Class to represent behaviours.py"""

    def __init__(
        self,
        behaviours: t.Dict[str, Behaviour],
        round_behaviour: RoundBehaviour,
        path: Path,
    ) -> None:
        """Initialize object."""
        super().__init__(path=path)
        self.behaviours = behaviours
        self.round_behaviour = round_behaviour

    def create(
        self,
        name: str,
        matching_round: str,
        payload_class: str,
        payload_value: t.Any,
        state_pos: "StatePosition",
    ) -> "Behaviours":
        """Create a new behaviour."""
        self.add(
            node=Behaviour.new(
                name=name,
                matching_round=matching_round,
                payload_class=payload_class,
                payload_value=payload_value,
            )
        )
        self.update(
            self.round_behaviour.add_behaviour(  # type: ignore[attr-defined]
                name=name,
                state_pos=state_pos,
            )
        )
        return self.from_path(path=self.path)

    @classmethod
    def from_path(cls, path: Path) -> "Behaviours":
        """Load from path."""
        if not (path / "behaviours.py").exists():
            raise FileNotFoundError(f"Cannot find the rounds module module for {path}")

        behaviours = {}
        round_behaviour_cls = None
        module = load_module(path=path, name="behaviours")
        for name in dir(module):
            obj = getattr(module, name)
            try:
                if obj.__name__.endswith("RoundBehaviour"):
                    round_behaviour_cls = obj
                    continue
                if obj.__name__.endswith("Behaviour"):
                    behaviours[obj.__name__] = Behaviour(obj)  # type: ignore[call-arg]
                    continue
            except AttributeError:
                continue

        return cls(  # type: ignore[call-arg]
            behaviours=behaviours,
            round_behaviour=RoundBehaviour(round_behaviour_cls),  # type: ignore[call-arg]
            modifier=Modifier(path=path / "behaviours.py"),
            path=path,
        )
