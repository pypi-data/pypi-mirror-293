# pylint: disable=import-error
"""Compsoe studio."""

from pathlib import Path
from typing import Any

from aea.configurations.constants import PACKAGES  # type: ignore[import]
from starlette.responses import HTMLResponse  # type: ignore[import]
from starlette.types import Receive, Scope, Send  # type: ignore[import]

from open_autonomy_compose.constants import COMPOSE_YAML
from open_autonomy_compose.data import DATA_DIR
from open_autonomy_compose.studio.apps import Apps
from open_autonomy_compose.studio.inspect import Inspect
from open_autonomy_compose.studio.packages import Packages
from open_autonomy_compose.studio.project import Project


class Studio:
    """Class to represent studio config."""

    def __init__(
        self,
        packages: Packages,
        project: Project,
        inspect: Inspect,
        apps: Apps,
        path: Path,
    ) -> None:
        """Initialize object."""
        self.path = path
        self.packages = packages
        self.project = project
        self.inspect = inspect
        self.apps = apps

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> Any:
        """Web handler."""
        response = HTMLResponse(
            content=(DATA_DIR / "site" / "index.html").read_text(encoding="utf-8")
        )
        await response(scope=scope, receive=receive, send=send)

    @classmethod
    def load(cls, path: Path) -> "Studio":
        """Load from directory."""
        packages = Packages.load(path=path / PACKAGES)
        project = Project.load(path=path / COMPOSE_YAML)
        inspect = Inspect(project=path)
        apps = Apps(packages=packages, project=project)
        return cls(
            packages=packages,
            project=project,
            inspect=inspect,
            apps=apps,
            path=path,
        )
