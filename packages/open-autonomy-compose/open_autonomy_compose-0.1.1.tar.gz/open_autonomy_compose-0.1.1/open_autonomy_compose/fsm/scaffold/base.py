# pylint: disable=import-error, unused-import
"""Base classes."""

import ast
import typing as t
from collections import OrderedDict
from pathlib import Path

from black import Mode  # type: ignore[import]
from black import format_str as black_format  # type: ignore[import]
from isort.api import sort_file  # type: ignore[import]
from isort.settings import Config as IsortConfig  # type: ignore[import]

from open_autonomy_compose.fsm import modifiers  # noqa: F401
from open_autonomy_compose.fsm.modifiers.base import Ast


def get_event_enum(events: t.List[str]) -> ast.ClassDef:
    """Get Event enum class def"""
    return Ast.cls(
        name="Event",
        bases=["Enum"],
        keywords=[],
        body=[
            Ast.expr(value=Ast.constant(value="Event enum for state transitions.")),
            *[
                Ast.assign(
                    name=event,
                    value=ast.Constant(value=event.lower()),
                    ctx=ast.Store(),
                )
                for event in events
            ],
        ],
    )


class Modifier:
    """Modifier"""

    def __init__(self, path: Path) -> None:
        """Initialize object."""
        self.path = path
        module = path.resolve().relative_to(Path.cwd())
        self.module = ".".join([*module.parent.parts, module.name.replace(".py", "")])
        self.load()

    def load(self) -> "Modifier":
        """Load module."""
        self.tree = ast.parse(self.path.read_text())
        self.copyright = self.tree.body[0]
        self.imports = []
        self.objects: t.OrderedDict[str, t.Any] = OrderedDict()
        for node in self.tree.body[1:]:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                self.imports.append(node)
                continue
            if isinstance(node, ast.ClassDef):
                self.objects[node.name] = node
                continue
            if isinstance(node, ast.Assign):
                self.objects[t.cast(ast.Name, node.targets[0]).id] = node
                continue
            if isinstance(node, ast.AnnAssign):
                self.objects[t.cast(ast.Name, node.target).id] = node
                continue
        return self

    def add(
        self, node: t.Union[ast.ClassDef, ast.Import, ast.ImportFrom]
    ) -> "Modifier":
        """Add a new node."""
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            self.imports.append(node)
        if isinstance(node, ast.ClassDef):
            self.objects.pop(node.name)
            self.objects[node.name] = node
        return self

    def write(self) -> "Modifier":
        """Write tree object to file"""
        self.tree.body = [
            self.copyright,
            *self.imports,
            *self.objects.values(),
        ]
        code = black_format(ast.unparse(self.tree), mode=Mode())
        self.path.write_text(code, encoding="utf-8")
        sort_file(
            self.path,
            config=IsortConfig(
                quiet=True,
                multi_line_output=3,
                include_trailing_comma=True,
                force_grid_wrap=0,
                use_parentheses=True,
                ensure_newline_before_comments=True,
                line_length=88,
                order_by_type=False,
                case_sensitive=True,
                lines_after_imports=2,
            ),
        )
        return self
