"""AEA Package helpers."""

import importlib.util
import os
import sys
import types
import typing as t
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType

from open_autonomy_compose.helpers.yaml import Yaml


PACKAGES = "packages"
PACKAGE_TYPES = (
    "protocols",
    "contracts",
    "connections",
    "skills",
)


def load_module(path: Path, name: str) -> ModuleType:
    """Import module."""
    root_dir = os.path.abspath(os.curdir)
    if str(path).startswith(root_dir):
        path = path.relative_to(root_dir)
    import_name = ".".join((path / name).parts)
    return importlib.import_module(import_name)


def parse_public_id(pubstr: str) -> t.Tuple[str, str]:
    """Parse public ID for author and package name."""
    pubstr, _ = pubstr.split(":", maxsplit=1)
    author, package = pubstr.split("/")
    return author, package


def load_into_sys_modules(path: Path) -> None:  # pylint: disable=too-many-locals
    """Load the AEA package from values provided."""
    *_, author, ptype_plural, package = path.parts
    prefix_root = PACKAGES
    prefix_author = prefix_root + f".{author}"
    prefix_pkg_type = prefix_author + f".{ptype_plural}"

    prefix_root_module = types.ModuleType(prefix_root)
    prefix_root_module.__path__ = None  # type: ignore
    sys.modules[prefix_root] = sys.modules.get(prefix_root, prefix_root_module)
    author_module = types.ModuleType(prefix_author)
    author_module.__path__ = None  # type: ignore
    sys.modules[prefix_author] = sys.modules.get(prefix_author, author_module)
    prefix_pkg_type_module = types.ModuleType(prefix_pkg_type)
    prefix_pkg_type_module.__path__ = None  # type: ignore
    sys.modules[prefix_pkg_type] = sys.modules.get(
        prefix_pkg_type, prefix_pkg_type_module
    )

    prefix_pkg = prefix_pkg_type + f".{package}"
    for subpackage_init_file in path.rglob("__init__.py"):
        if subpackage_init_file.parent.name == "tests":
            continue
        parent_dir = subpackage_init_file.parent
        relative_parent_dir = parent_dir.relative_to(path)
        if relative_parent_dir == Path("."):
            import_path = prefix_pkg
        else:
            import_path = prefix_pkg + "." + ".".join(relative_parent_dir.parts)
        spec = importlib.util.spec_from_file_location(import_path, subpackage_init_file)
        module = importlib.util.module_from_spec(t.cast(ModuleSpec, spec))
        sys.modules[import_path] = module
        spec.loader.exec_module(module)  # type: ignore


def collect_dependencies(config: t.Dict) -> t.List[t.Tuple[str, Path]]:
    """Merge package dependencies."""
    dependencies = []
    for ptype in PACKAGE_TYPES:
        for pubstr in config.get(ptype, []):
            author, package = parse_public_id(pubstr=pubstr)
            dependencies.append((ptype[:-1], Path("packages", author, ptype, package)))
    return dependencies


def load_package(ptype: str, path: Path, loaded: t.List[Path]) -> None:
    """Load package."""
    yaml = path / f"{ptype}.yaml"
    with yaml.open("r", encoding="utf-8") as fp:
        config = Yaml.load(stream=fp)
    dependencies = collect_dependencies(config=config)
    for dptype, dpath in dependencies:
        if dpath in loaded:
            continue
        load_package(ptype=dptype, path=dpath, loaded=loaded)
    load_into_sys_modules(path=path)
    loaded.append(path)


def load_packages(packages: Path) -> None:
    """Load packages into sys.modules"""
    paths = []
    for ptype in PACKAGE_TYPES:
        paths += list(
            map(
                lambda x: (ptype[:-1], x),  # pylint: disable=cell-var-from-loop
                filter(
                    lambda x: x.is_dir() and x.name != "__pycache__",
                    packages.glob(f"*/{ptype}/*"),
                ),
            )
        )

    loaded: t.List[Path] = []
    for ptype, path in paths:
        if path in loaded:
            continue
        load_package(ptype=ptype, path=path, loaded=loaded)
