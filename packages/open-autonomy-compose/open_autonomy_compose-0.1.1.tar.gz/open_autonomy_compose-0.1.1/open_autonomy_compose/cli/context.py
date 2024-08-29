# pylint: disable=import-error,too-few-public-methods, super-init-not-called
"""Compose CLI context."""

import typing as t
from pathlib import Path

from clea import Context as BaseContext  # type: ignore

from open_autonomy_compose.constants import COMPOSE_CACHE


class ComposeCLICache:
    """Compose global cache."""


class ComposeCLIConfig:
    """Compose CLI global config."""

    def __init__(self, path: Path) -> None:
        """Initialize object."""
        self.path = path

    @classmethod
    def from_dir(cls, path: Path) -> "ComposeCLIConfig":
        """Load from directory."""
        if path.exists():
            return cls(path=path)
        path.mkdir()
        return cls(path=path)


class Context(BaseContext):
    """Compose context."""

    _config: t.Optional[ComposeCLIConfig]
    _cache: t.Optional[ComposeCLICache]

    def __init__(self) -> None:
        """Initialize context object."""
        self._config = None
        self._cache = None

    @property
    def config(self) -> ComposeCLIConfig:
        """Global configuration."""
        if self._config is None:
            self._config = ComposeCLIConfig.from_dir(path=Path.home() / COMPOSE_CACHE)
        return self._config

    @property
    def cache(self) -> ComposeCLICache:  # type: ignore
        """Global cache."""
