# pylint: disable=import-error
"""Base definitions."""

import ast
import typing as t
from pathlib import Path

from black import Mode  # type: ignore[import]
from black import format_str as black_format  # type: ignore[import]
from isort.api import sort_file  # type: ignore[import]
from isort.settings import Config as IsortConfig  # type: ignore[import]


class Ast:
    """Ast helpers."""

    @classmethod
    def import_from(
        cls, module: str, names: t.Union[t.List[t.Tuple[str, str]], t.List[str]]
    ) -> ast.ImportFrom:
        """Creates ast.ImportFrom node."""
        if isinstance(names[0], tuple):
            return ast.ImportFrom(
                module=module,
                names=[ast.alias(name=name, asname=asname) for name, asname in names],  # type: ignore[misc]
                level=0,
            )
        return ast.ImportFrom(
            module=module,
            names=[ast.alias(name=name) for name in names],
            level=0,
        )

    @classmethod
    def constant(cls, value: t.Any) -> ast.Constant:
        """Create ast.Constant node."""
        return ast.Constant(value=value)

    @classmethod
    def expr(cls, value: ast.Constant) -> ast.Expr:
        """Create ast.Expr node."""
        return ast.Expr(value=value)

    @classmethod
    def name(
        cls,
        value: str,
        ctx: t.Optional[ast.expr_context] = None,
    ) -> ast.Name:
        """Create ast.Expr node."""
        return ast.Name(id=value, ctx=ctx)

    @classmethod
    def keyword(
        cls,
        arg: str,
        value: t.Optional[t.Union[ast.Constant, ast.Name]] = None,
    ) -> ast.Name:
        """Create ast.Expr node."""
        return ast.keyword(  # type: ignore[return-value]
            arg=arg,
            value=value,
        )

    @classmethod
    def assign(
        cls,
        name: str,
        value: t.Union[ast.Constant, ast.Name],
        ctx: t.Optional[ast.expr_context] = None,
    ) -> ast.Assign:
        """Create ast.Assign node."""
        return ast.Assign(
            targets=[
                cls.name(
                    value=name,
                    ctx=ctx or ast.Store(),
                )
            ],
            value=value,
            lineno=0,
        )

    @classmethod
    def ann_assign(
        cls,
        target: str,
        annotation: str,
        simple: int = 1,
    ) -> ast.Assign:
        """Create ast.Assign node."""
        return ast.AnnAssign(  # type: ignore[return-value]
            target=cls.name(target),
            annotation=cls.name(annotation),
            simple=simple,
        )

    @classmethod
    def call(
        cls,
        func: str,
        args: t.Optional[t.List[t.Union[ast.Name, ast.Constant]]] = None,
        keywords: t.Optional[t.List[ast.keyword]] = None,
    ) -> ast.Call:
        """Create an ast.Call node."""
        return ast.Call(
            func=cls.name(value=func),
            args=args or [],
            keywords=keywords or [],
        )

    @classmethod
    def cls(
        cls,
        name: str,
        bases: t.Optional[t.List[str]] = None,
        keywords: t.Optional[t.List] = None,
        body: t.Optional[t.List] = None,
        decorator_list: t.Optional[t.List] = None,
    ) -> ast.ClassDef:
        """Create a ast.ClassDef node."""
        return ast.ClassDef(
            name=name,
            bases=list(map(cls.name, bases)) or [],  # type: ignore[arg-type]
            keywords=keywords or [],
            body=body or [cls.expr(cls.constant(f"""{name} class."""))],
            decorator_list=decorator_list or [],
        )


class Modifier:
    """Ast modifier for a module."""

    def __init__(self, path: Path) -> None:
        """Initialize object."""
        self.path = path
        self.module = ".".join([*path.parent.parts, path.name.replace(".py", "")])

    def load(self) -> ast.Module:
        """Load tree."""
        return ast.parse(self.path.read_text(encoding="utf-8"))

    def dump(self, tree: ast.Module) -> None:
        """Load tree."""
        code = black_format(ast.unparse(tree), mode=Mode())
        self.path.write_text(code, encoding="utf-8")
        sort_file(self.path, config=IsortConfig(quiet=True))

    def update(self, node: ast.ClassDef) -> None:
        """Add a new node."""
        tree = self.load()
        body = []
        for cdef in tree.body:
            if not isinstance(cdef, ast.ClassDef):
                body.append(cdef)
                continue
            if cdef.name == node.name:
                body.append(node)
                continue
            body.append(cdef)
        tree.body = body
        self.dump(tree=tree)

    def add(self, node: ast.AST, index: int = -1) -> None:
        """Add a new node."""
        tree = self.load()
        if index == -1:
            tree.body.append(node)  # type: ignore[arg-type]
        else:
            tree.body.insert(index, node)  # type: ignore[arg-type]
        self.dump(tree=tree)


class ClassModifier(Modifier):
    """Class modifier."""

    def __init__(self, obj: t.Any, path: Path) -> None:
        """Initialize object."""
        super().__init__(path)
        self.obj = obj
