# pylint: disable=import-error, import-outside-toplevel, unused-import, cyclic-import
"""CLI Module."""

import typing as t

from clea import group, run  # type: ignore[import]


@group
def compose() -> None:
    """Composer - A CLI tool for working with FSM applications."""


def main(argv: t.Optional[t.List[str]] = None) -> None:
    """Run compose CLI module."""
    from open_autonomy_compose.cli.check import check  # noqa: F401
    from open_autonomy_compose.cli.fsm import fsm  # noqa: F401
    from open_autonomy_compose.cli.inspect import inspect  # noqa: F401
    from open_autonomy_compose.cli.new import new  # noqa: F401
    from open_autonomy_compose.cli.scaffold import scaffold  # noqa: F401

    run(
        cli=compose,
        argv=argv,
        isolated=False,
    )


if __name__ == "__main__":
    main()
