# mypy: disable-error-code="import"
# pylint: disable=import-error, too-few-public-methods
"""tox.ini helpers."""

import typing as t
from pathlib import Path

from aea.configurations.data_types import (
    Dependency as PyPiDependency,  # type: ignore[import]
)

from open_autonomy_compose.data import TEMPLATES_DIR


TOX_INI = "tox.ini"


def init_tox_ini(wd: Path, core_dependencies: t.List[PyPiDependency]) -> None:
    """Initialize tox.ini"""
    mapping = {dep.name.replace("-", "_"): dep.version for dep in core_dependencies}
    content = (TEMPLATES_DIR / "tox.ini").read_text(encoding="utf-8")
    content = content.format(**mapping)
    (wd / TOX_INI).write_text(content, encoding="utf-8")
    (wd / ".pylintrc").write_text(
        (TEMPLATES_DIR / "pylintrc").read_text(encoding="utf-8"),
        encoding="utf-8",
    )


class ToxIni:
    """Tox.ini helper"""
