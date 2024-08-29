# pylint: disable=unused-import, super-init-not-called
"""Payloads.py modifier."""

import ast
import typing as t
from pathlib import Path

from open_autonomy_compose.fsm.modifiers.base import Ast, ClassModifier, Modifier
from open_autonomy_compose.fsm.types import PayloadType
from open_autonomy_compose.helpers.package import (  # noqa: F401
    load_into_sys_modules,
    load_module,
)


class Payload(ClassModifier):
    """Payload class."""

    def __init__(self, obj: PayloadType) -> None:
        """Initialize object."""
        self._obj = obj

    @staticmethod
    def new(name: str, attributes: t.Dict[str, str]) -> ast.ClassDef:
        """Create a new payload class."""
        return Ast.cls(
            name=name,
            bases=["BaseTxPayload"],
            body=[
                Ast.expr(
                    value=Ast.constant(
                        f"""{name} class.""",
                    )
                ),
                *[
                    Ast.ann_assign(target, annotation)
                    for target, annotation in attributes.items()
                ],
            ],
            decorator_list=[
                Ast.call(
                    func="dataclass",
                    keywords=[
                        Ast.keyword(arg="frozen", value=Ast.constant(True)),  # type: ignore[list-item]
                    ],
                )
            ],
        )


class Payloads(Modifier):
    """Payloads module modifier."""

    def __init__(self, payloads: t.Dict[str, Payload], path: Path) -> None:
        """Initialize object."""
        super().__init__(path=path)
        self.payloads = payloads

    def create(
        self,
        name: str,
        attributes: t.Dict[str, str],
        reload: bool = False,
    ) -> "Payloads":
        """Create new payload class."""
        node = Payload.new(name=name, attributes=attributes)
        self.add(node=node)
        if reload:
            return self.reload()
        return self

    def reload(self) -> "Payloads":
        """Reload module."""
        return self.from_path(path=self.path.parent)

    @classmethod
    def from_path(cls, path: Path) -> "Payloads":
        """Load from path."""
        if not (path / "payloads.py").exists():
            raise FileNotFoundError(f"Cannot find the payloads module for {path}")

        payloads = {}
        module = load_module(path=path, name="payloads")
        for name in dir(module):
            obj = getattr(module, name)
            try:
                if obj.__name__.endswith("Payload"):
                    payloads[obj.__name__] = Payload(obj)
                    continue
            except AttributeError:
                continue
        return cls(payloads=payloads, path=path)
