# pylint: disable=import-error
"""Git helpers."""

import os
import time
import typing as t
from pathlib import Path

import requests  # type: ignore[import]
from aea.package_manager.v1 import PackageManagerV1  # type: ignore[import]
from autonomy.cli.helpers.ipfs_hash import load_configuration  # type: ignore[import]

from open_autonomy_compose.types import GitRepoResource


TAG_LATEST = "latest"
TAGS_URL = "https://api.github.com/repos/{repo}/tags"
PACKAGE_FILE_REMOTE_URL = (
    "https://raw.githubusercontent.com/{repo}/{tag}/packages/packages.json"
)
GITIGNORE = ".gitignore"


class Tag:
    """Tag version."""

    def __init__(
        self,
        major: int,
        minor: int,
        patch: int,
        post: t.Optional[int] = None,
    ) -> None:
        """Initialize object."""
        self.major = major
        self.minor = minor
        self.patch = patch
        self.post = post or -1

    @classmethod
    def parse(cls, string: str) -> "Tag":
        """Parse tag string."""
        string = string.replace("v", "")
        parts = string.split(".")
        if len(parts) == 3:
            return cls(
                major=int(parts[0]),
                minor=int(parts[1]),
                patch=int(parts[2]),
            )
        return cls(
            major=int(parts[0]),
            minor=int(parts[1]),
            patch=int(parts[2]),
            post=int(parts[3].replace("post", "")),
        )

    def __str__(self) -> str:
        """To string."""
        if self.post > -1:
            return f"v{self.major}.{self.minor}.{self.patch}.post{self.post}"
        return f"v{self.major}.{self.minor}.{self.patch}"

    def __repr__(self) -> str:
        """To string."""
        return str(self)

    def __lt__(self, other: "Tag") -> int:
        """Less than."""
        if not isinstance(other, Tag):
            return NotImplemented
        return (
            self.major < other.major
            and self.minor < other.minor
            and self.patch < other.patch
            and self.post < other.post
        )


def add_to_gitignore(obj: t.Any, wd: t.Optional[Path] = None) -> None:
    """Add to .gitignore"""
    obj = str(obj)
    wd = wd or Path.cwd()
    gitignore = wd / GITIGNORE
    gitignore.touch(exist_ok=True)
    content = gitignore.read_text()
    if obj in content:
        return
    content += f"{obj}\n"
    gitignore.write_text(content, encoding="utf-8")


class GitSource:
    """Github repo as source."""

    def __init__(
        self,
        name: str,
        author: str,
        version: str = TAG_LATEST,
    ) -> None:
        """Initialize object"""
        self.name = name
        self.author = author
        self.version = version

    @property
    def repo(self) -> str:
        """As repo name."""
        return f"{self.author}/{self.name}"

    @property
    def json(self) -> GitRepoResource:
        """To json object."""
        return GitRepoResource(
            name=self.name,
            author=self.author,
            version=self.version,
        )

    def with_version(self, version: str) -> "GitSource":
        """With new version string."""
        return GitSource(
            name=self.name,
            author=self.author,
            version=version,
        )

    def to_string(self) -> str:
        """To string."""
        return f"{self.author}/{self.name}:{self.version}"

    @classmethod
    def from_string(cls, string: str) -> "GitSource":
        """Load from string."""
        repo, *_version = string.split(":")
        if len(_version) > 0:
            (version,) = _version
        else:
            version = TAG_LATEST
        author, name = repo.split("/")
        return cls(
            name=name,
            author=author,
            version=version,
        )


def make_git_request(url: str) -> requests.Response:
    """Make git request"""
    auth = os.environ.get("GITHUB_AUTH")
    while True:
        try:
            if auth is None or auth == "":
                return requests.get(url=url)
            return requests.get(url=url, headers={"Authorization": f"Bearer {auth}"})
        except requests.ConnectionError as e:
            print(e, url)
            time.sleep(1)


def fetch_latest_tag(repo: str) -> str:
    """Fetch latest git tag."""
    response = make_git_request(TAGS_URL.format(repo=repo))
    if response.status_code != 200:
        raise ValueError(
            f"Fetching tags from `{repo}` failed with message '"
            + response.json()["message"]
            + "'"
        )
    # TODO: Fix sorting
    tags = list(reversed(sorted([Tag.parse(tag["name"]) for tag in response.json()])))  # type: ignore[type-var]
    return str(tags[-1])


def fetch_packages_json(repo: str, tag: str) -> t.Dict[str, t.Dict[str, str]]:
    """Get `packages.json`."""
    response = make_git_request(PACKAGE_FILE_REMOTE_URL.format(repo=repo, tag=tag))
    if response.status_code != 200:
        raise ValueError(
            f"Fetching packages from `{repo}` failed with message '"
            + response.text
            + "'"
        )
    return response.json()


def load_packages_from_git_source(source: GitSource) -> PackageManagerV1:
    """Load package manager from git source."""
    version = (
        fetch_latest_tag(repo=source.repo)
        if source.version == TAG_LATEST
        else source.version
    )
    packages = fetch_packages_json(
        repo=source.repo,
        tag=version,
    )
    return PackageManagerV1.from_json(
        packages=packages,
        config_loader=load_configuration,
    )
