"""Project representation."""

import typing as t
from enum import Enum
from pathlib import Path

from open_autonomy_compose import types
from open_autonomy_compose.helpers.git import GitSource
from open_autonomy_compose.helpers.yaml import Yaml
from open_autonomy_compose.studio.base import Resource
from open_autonomy_compose.studio.exceptions import NotFound, ResourceAlreadyExists


class ProjectManagement(Enum):
    """Project management style."""

    PIPFILE = "pipfile"
    POETRY = "poetry"


class Sources(
    Resource[
        t.List[types.GitRepoResource],
        types.GitRepoResource,
        types.GitRepoResource,
        types.GitRepoResource,
        types.GitRepoResource,
        types.GitRepoResource,
        types.GitRepoResource,
    ]
):
    """Sources helper."""

    def __init__(self, sources: t.List[GitSource]) -> None:
        """Initialize object."""
        self._sources = sources
        super().__init__()

    @property
    def json(self) -> t.List[types.GitRepoResource]:
        """JSON Serializable object."""
        return [source.json for source in self._sources]

    def __iter__(self) -> t.Iterator[GitSource]:
        """Iter over git sources"""
        yield from self._sources

    def create(self, data: types.GitRepoResource) -> types.GitRepoResource:
        """Add a new source."""
        source = GitSource(
            name=data["name"],
            author=data["author"],
            version=data["version"],
        )
        for _source in self._sources:
            if _source.author == source.author and _source.name == source.name:
                raise ResourceAlreadyExists(
                    f"Source '{source.repo}' already exists with version '{source.version}'"
                )
        self._sources.append(source)
        return source.json

    def update(self, data: types.GitRepoResource) -> types.GitRepoResource:
        """Update a source."""
        source = GitSource(
            name=data["name"],
            author=data["author"],
            version=data["version"],
        )
        sources = []
        found = False
        for _source in self._sources:
            if _source.author == source.author and _source.name == source.name:
                _source.version = source.version
                found = True
            sources.append(_source)
        if found:
            self._sources = sources
            return source.json
        raise NotFound(f"Source '{source.repo}' not found")

    def delete(self, data: types.GitRepoResource) -> types.GitRepoResource:
        """Remove a source."""
        source = GitSource(
            name=data["name"],
            author=data["author"],
            version=data["version"],
        )
        sources = []
        found = False
        for _source in self._sources:
            if _source.author == source.author and _source.name == source.name:
                found = True
                continue
            sources.append(_source)
        if found:
            self._sources = sources
            return source.json
        raise NotFound(f"Source '{source.repo}' not found")


class Project(Resource[types.ProjectResource, None, None, None, None, None, None]):
    """Project configuration."""

    def __init__(
        self,
        author: str,
        management: ProjectManagement,
        sources: Sources,
        path: Path,
    ) -> None:
        """Initialize object."""
        self.author = author
        self.management = management
        self.sources = sources
        self.path = path
        super().__init__()

    @property
    def json(self) -> types.ProjectResource:
        """To json object."""
        return types.ProjectResource(
            author=self.author,
            management=self.management.value,
            sources=self.sources.json,
        )

    @classmethod
    def load(cls, path: Path) -> "Project":
        """Load from directory."""
        with path.open("r", encoding="utf-8") as fp:
            config = Yaml.load(stream=fp)
        return cls(
            author=config["author"],
            management=ProjectManagement(config["management"]),
            sources=Sources([GitSource(**source) for source in config["sources"]]),
            path=path,
        )

    def dump(self) -> None:
        """Dump to a YAML file."""
        with self.path.open("w+", encoding="utf-8") as fp:
            Yaml.dump(data=self.json, stream=fp)  # type: ignore[arg-type]
