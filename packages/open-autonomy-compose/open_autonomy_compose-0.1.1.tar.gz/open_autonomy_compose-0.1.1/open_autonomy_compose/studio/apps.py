# pylint: disable=import-error
"""Apps helpers."""

import typing as t

from aea.configurations.data_types import PackageType  # type: ignore[import]

import open_autonomy_compose.types as rt
from open_autonomy_compose.fsm.scaffold.abci.generator import Scaffold as AbciScaffold
from open_autonomy_compose.fsm.scaffold.composition.generator import (
    Scaffold as CompositionScaffold,
)
from open_autonomy_compose.studio.base import Resource
from open_autonomy_compose.studio.packages import Packages
from open_autonomy_compose.studio.project import Project


class Apps(
    Resource[
        t.List[rt.AppResource],
        rt.AppResource,
        rt.AppResource,
        rt.AppResource,
        rt.AppResource,
        rt.AppResource,
        rt.AppResource,
    ]
):
    """Apps helper."""

    _apps: t.List[rt.AppResource]

    def __init__(
        self,
        packages: Packages,
        project: Project,
    ) -> None:
        """Initialize object."""
        self.packages = packages
        self.project = project
        super().__init__()

    def _find_apps(self) -> t.List[rt.AppResource]:
        """Find apps"""
        apps = []
        for package in self.packages.manager.dev_packages:
            if package.package_type != PackageType.SKILL:
                continue
            package_path = self.packages.manager.package_path_from_package_id(
                package_id=package
            )
            ptype = (
                rt.AppType.Composition
                if (package_path / "composition.py").exists()
                else rt.AppType.Abci
            )
            apps.append(
                rt.AppResource(  # type: ignore[typeddict-item]
                    name=package.name,
                    type=ptype,
                    third_party=False,
                )
            )
        for package in self.packages.manager.third_party_packages:
            if package.package_type != PackageType.SKILL:
                continue
            package_path = self.packages.manager.package_path_from_package_id(
                package_id=package
            )
            ptype = (
                rt.AppType.Composition
                if (package_path / "composition.py").exists()
                else rt.AppType.Abci
            )
            apps.append(
                rt.AppResource(  # type: ignore[typeddict-item]
                    name=package.name,
                    type=ptype,
                    third_party=True,
                )
            )
        return apps

    @property
    def json(self) -> t.List[rt.AppResource]:
        """Return JSON representation of the resource."""
        return self._find_apps()

    def _create(self, data: rt.AppResource) -> rt.AppResource:
        """Create a new app"""
        Scaffold = (
            AbciScaffold if data["type"] == rt.AppType.Abci else CompositionScaffold
        )
        package_path = (
            Scaffold(  # type: ignore[attr-defined]
                name=data["name"],
                author=self.project.author,
                packages=self.packages.path,
            )
            .mkdir()
            .write()
            .path
        )
        self.packages.manager.register(
            package_path=package_path,
            package_type=PackageType.SKILL,
        )
        self.packages.manager.dump()
        return data

    def create(self, data: rt.AppResource) -> rt.AppResource:
        """POST /api/apps"""
        return self._create(data=data).json  # type: ignore[attr-defined]

    def update(self, data: rt.AppResource) -> rt.AppResource:
        """PUT /api/apps"""
        return data

    def delete(self, data: rt.AppResource) -> rt.AppResource:
        """DELETE /api/apps"""
        return data
