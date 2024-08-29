# pylint: disable=import-error
"""FSM Helpers."""

import json
from enum import Enum
from pathlib import Path

from clea import ChoiceByFlag, Directory, File  # type: ignore[import]
from typing_extensions import Annotated

from open_autonomy_compose.cli import compose
from open_autonomy_compose.fsm.app import AbciApp, AbciAppSpecification
from open_autonomy_compose.fsm.composition import Composition, CompositionSpecification
from open_autonomy_compose.helpers.package import load_packages


class OutputType(Enum):
    """Output types."""

    JSON = "json"
    YAML = "yaml"


@compose.group
def fsm() -> None:
    """FSM Helpers."""


@fsm.command(name="from-app")
def _from_app(
    app: Annotated[Path, Directory(exists=True, resolve=True)],
    output_type: Annotated[
        OutputType,
        ChoiceByFlag(
            enum=OutputType, default=OutputType.YAML, help="File output type."
        ),
    ],
    output: Annotated[Path, File(help="Path to output file.", short_flag="-o")],
) -> None:
    """Generate specification from an ABCI app."""
    load_packages(packages=app.parent.parent.parent)
    try:
        spec = CompositionSpecification.from_obj(
            composition=Composition.from_path(
                path=app,
            ),
        )
    except (FileNotFoundError, ModuleNotFoundError):
        spec = AbciAppSpecification.from_obj(  # type: ignore[assignment]
            abci=AbciApp.from_path(
                path=app,
            ),
        )

    if output_type == OutputType.YAML:
        spec.to_yaml(file=output or Path("fsm.yaml"))
    else:
        data = spec.to_json()
        with (output or Path("fsm.json")).open("w+", encoding="utf-8") as fp:
            json.dump(data, fp=fp, indent=2)
