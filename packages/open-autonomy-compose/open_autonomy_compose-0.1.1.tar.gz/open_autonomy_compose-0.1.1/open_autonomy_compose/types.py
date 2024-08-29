"""Resource types."""

import typing as t
from enum import IntEnum

from typing_extensions import TypedDict


class GitRepoResource(TypedDict):
    """Git resource type."""

    author: str
    name: str
    version: str


class ComponentResource(TypedDict):
    """Component resource type."""

    type: str
    author: str
    name: str
    hash: str


class AppType(IntEnum):
    """App type enum."""

    Abci = 0
    Composition = 1


class AppResource(TypedDict):
    """Create app payload."""

    name: str
    description: t.Optional[str]
    type: AppType
    third_party: bool


class ProjectResource(TypedDict):
    """Project type"""

    author: str
    management: str
    sources: t.List[GitRepoResource]
