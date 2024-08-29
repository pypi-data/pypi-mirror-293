# pylint: disable=import-error
"""Packages helper."""

import typing as t
from pathlib import Path

from aea.configurations.data_types import (  # type: ignore[import]
    PackageId,
    PackageType,
    PublicId,
)
from aea.package_manager.v1 import PackageManagerV1  # type: ignore[import]
from aea_cli_ipfs.registry import fetch_ipfs  # type: ignore[import]
from autonomy.cli.helpers.ipfs_hash import load_configuration  # type: ignore[import]

from open_autonomy_compose import types as rt
from open_autonomy_compose.helpers.git import add_to_gitignore
from open_autonomy_compose.studio.base import Resource
from open_autonomy_compose.studio.exceptions import BadRequest


class Packages(
    Resource[
        t.Dict[str, t.List[rt.ComponentResource]],
        rt.ComponentResource,
        rt.ComponentResource,
        rt.ComponentResource,
        rt.ComponentResource,
        rt.ComponentResource,
        rt.ComponentResource,
    ]
):
    """Packages handler."""

    def __init__(
        self,
        path: Path,
    ) -> None:
        """Initialize object."""
        self.path = path
        self.manager = PackageManagerV1.from_dir(
            packages_dir=path,
            config_loader=load_configuration,
        )
        super().__init__()

    @classmethod
    def load(cls, path: Path) -> "Packages":
        """Load from directory."""
        return cls(
            path=path,
        )

    def dump(self) -> None:
        """Dump packages info."""
        self.manager.dump()

    @property
    def json(self) -> t.Dict[str, t.List[rt.ComponentResource]]:
        """Return JSON representation."""
        obj: t.Dict[str, t.List[rt.ComponentResource]] = {"dev": [], "third_party": []}
        for component, chash in self.manager.dev_packages.items():
            obj["dev"].append(
                rt.ComponentResource(
                    name=component.name,
                    author=component.author,
                    type=component.package_type.name,
                    hash=chash,
                )
            )
        for component, chash in self.manager.third_party_packages.items():
            obj["third_party"].append(
                rt.ComponentResource(
                    name=component.name,
                    author=component.author,
                    type=component.package_type.name,
                    hash=chash,
                )
            )
        return obj

    def create(self, data: rt.ComponentResource) -> rt.ComponentResource:
        """Add a new third party package"""
        package_id = PackageId(
            package_type=PackageType(data["type"]),
            public_id=PublicId(
                author=data["author"],
                name=data["name"],
                package_hash=data["hash"],
            ),
        )
        self.add(package_id=package_id)
        return data

    def add(self, package_id: PackageId) -> Path:
        """Add a new third party package."""
        package_hash = self.manager.get_package_hash(package_id=package_id)
        if package_hash is not None:
            raise BadRequest(f"Package already exists with hash {package_hash}")
        dest = self.manager.package_path_from_package_id(package_id=package_id)
        fetch_ipfs(
            item_type=package_id.package_type.value,
            public_id=package_id.public_id,
            dest=dest,
        )
        self.manager.third_party_packages[package_id] = package_id.package_hash
        self.manager.dump()
        add_to_gitignore(dest)
        return dest
