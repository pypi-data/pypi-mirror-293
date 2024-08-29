# pylint: disable=import-error, no-self-use
"""Inspect an AbciApp in web-view"""

import asyncio
import typing as t
from pathlib import Path

from starlette.requests import Request  # type: ignore[import]
from starlette.responses import JSONResponse  # type: ignore[import]

from open_autonomy_compose.fsm.composition import Composition, CompositionSpecification
from open_autonomy_compose.helpers.package import load_packages


class Inspect:
    """View-Controller for inspect tool."""

    def __init__(self, project: Path) -> None:
        """Initialize object."""
        self.project = project

    def _get_apps(self, author: t.Optional[str] = None) -> t.List[t.Dict[str, str]]:
        """List available apps."""
        apps = []
        author = author or "*"
        glob = (self.project / "packages").glob(f"**/{author}/skills/*/composition.py")
        for package in glob:
            *_, author, _, app, _ = package.parts
            apps.append(
                {
                    "author": author,
                    "app": app,
                }
            )
        return apps

    def _get_spec(self, path: Path) -> CompositionSpecification:
        """Load FSM spec."""
        asyncio.set_event_loop(asyncio.new_event_loop())  # Patch for AEA multiplexer
        load_packages(path.parent.parent.parent)
        return CompositionSpecification.from_obj(
            composition=Composition.from_path(
                path=path,
            ),
        )

    def get_apps(self, request: Request) -> JSONResponse:
        """View for /inspect"""
        return JSONResponse({"apps": self._get_apps(request.path_params.get("author"))})

    def get_app(self, request: Request) -> JSONResponse:
        """Returns FSM as json."""
        app = (
            self.project
            / "packages"
            / request.path_params["author"]
            / "skills"
            / request.path_params["app"]
        )
        if not app.exists():
            return JSONResponse(
                content={"message": "Cannot find " + request.path_params["app"]},
                status_code=404,
            )
        spec = self._get_spec(path=app)
        return JSONResponse(content=spec.to_json())  # type: ignore[call-arg]
