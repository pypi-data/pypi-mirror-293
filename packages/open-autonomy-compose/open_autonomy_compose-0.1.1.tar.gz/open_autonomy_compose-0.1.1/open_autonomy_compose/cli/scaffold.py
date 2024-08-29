# pylint: disable=import-error, redefined-outer-name
"""Scaffold CLI command."""

from enum import Enum
from pathlib import Path

from aea.package_manager.v1 import PackageManagerV1  # type: ignore[import]
from clea import ChoiceByFlag, CleaException, File, String  # type: ignore[import]
from typing_extensions import Annotated

from open_autonomy_compose.cli import compose
from open_autonomy_compose.constants import COMPOSE_YAML
from open_autonomy_compose.fsm.base import WithParent
from open_autonomy_compose.fsm.scaffold.abci.generator import Scaffold as AbciScaffold
from open_autonomy_compose.fsm.scaffold.composition.generator import (
    Scaffold as CompositionScaffold,
)
from open_autonomy_compose.helpers.package import PACKAGES
from open_autonomy_compose.helpers.yaml import Yaml
from open_autonomy_compose.studio.project import Project


class ScaffoldType(Enum):
    """Scaffold type enum."""

    ABCI = "abci"
    COMPOSITION = "composition"


@compose.command(name="scaffold")
def scaffold(
    name: Annotated[str, String(long_flag="--name", help="Name of the application")],
    stype: Annotated[
        ScaffoldType,
        ChoiceByFlag(ScaffoldType, default=ScaffoldType.ABCI, help="Scaffold type."),
    ],
    spec: Annotated[
        Path,
        File(long_flag="--spec", help="FSM specification to use for scaffolding"),
    ],
) -> None:
    """Scaffold a new ABCI app."""
    packages = Path(PACKAGES)
    project = Project.load(path=Path(COMPOSE_YAML))

    if spec is None and name is None:
        raise CleaException("Provide name or specification file")

    if spec is not None:
        with spec.open("r", encoding="utf-8") as stream:
            specification = Yaml.load(stream=stream)
        name = WithParent.from_name(specification["name"]).parent

    scaffold = (
        (  # type: ignore[attr-defined]
            AbciScaffold(name=name, author=project.author, packages=packages)
            if stype == ScaffoldType.ABCI
            else CompositionScaffold(
                name=name, author=project.author, packages=packages
            )
        )
        .mkdir()
        .write()
    )

    if spec is not None:
        scaffold.hydrate(speciification=specification)

    PackageManagerV1.from_dir(packages_dir=packages).register(
        package_path=scaffold.path
    ).dump()
