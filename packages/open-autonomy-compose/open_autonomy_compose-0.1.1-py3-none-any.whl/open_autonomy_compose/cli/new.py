# mypy: disable-error-code="import"
# pylint: disable=import-error, unnecessary-comprehension, consider-using-with, too-many-statements, too-many-locals

"""Create new compose project."""

import logging
import shutil
import subprocess
import sys
import typing as t
from pathlib import Path

from aea.configurations.constants import PACKAGES  # type: ignore[import]
from aea.configurations.data_types import (
    Dependency as PyPiDependency,  # type: ignore[import]
)
from aea.configurations.data_types import PackageId  # type: ignore[import]
from aea.package_manager.v1 import PackageManagerV1  # type: ignore[import]
from clea import ChoiceByFlag, String  # type: ignore[import]
from clea.exceptions import CleaException  # type: ignore[import]
from typing_extensions import Annotated

from open_autonomy_compose.cli import compose
from open_autonomy_compose.constants import COMPOSE_YAML
from open_autonomy_compose.helpers.git import (
    GitSource,
    fetch_latest_tag,
    fetch_packages_json,
)
from open_autonomy_compose.helpers.pipfile import PIPFILE, init_pipfile
from open_autonomy_compose.helpers.pyproject import PYPROJECT_TOML, init_pyproject_toml
from open_autonomy_compose.helpers.scripts import SCRIPTS
from open_autonomy_compose.helpers.tox import TOX_INI, init_tox_ini
from open_autonomy_compose.helpers.workflow import install_workflow
from open_autonomy_compose.studio.project import Project, ProjectManagement, Sources


GIT_SOURCE_OPEN_AEA = GitSource(name="open-aea", author="valory-xyz")
GIT_SOURCE_OPEN_AUTONOMY = GitSource(name="open-autonomy", author="valory-xyz")
GIT_SOURCE_TOMTE = GitSource(name="tomte", author="valory-xyz")

CORE_DEPENDENCIES = (
    (
        "open-aea",
        GIT_SOURCE_OPEN_AEA,
        [
            "all",
        ],
    ),
    ("open-aea-ledger-ethereum", GIT_SOURCE_OPEN_AEA, None),
    ("open-aea-ledger-cosmos", GIT_SOURCE_OPEN_AEA, None),
    (
        "open-autonomy",
        GIT_SOURCE_OPEN_AUTONOMY,
        [
            "all",
        ],
    ),
    ("open-aea-test-autonomy", GIT_SOURCE_OPEN_AUTONOMY, None),
    ("tomte", GIT_SOURCE_TOMTE, ["cli", "tests"]),
)
CORE_PACKAGES = [
    PackageId.from_uri_path("protocol/open_aea/signing/latest"),
    PackageId.from_uri_path("protocol/valory/abci/latest"),
    PackageId.from_uri_path("protocol/valory/acn/latest"),
    PackageId.from_uri_path("protocol/valory/http/latest"),
    PackageId.from_uri_path("protocol/valory/ipfs/latest"),
    PackageId.from_uri_path("protocol/valory/ledger_api/latest"),
    PackageId.from_uri_path("protocol/valory/tendermint/latest"),
    PackageId.from_uri_path("protocol/valory/contract_api/latest"),
    PackageId.from_uri_path("contract/valory/gnosis_safe/latest"),
    PackageId.from_uri_path("contract/valory/gnosis_safe_proxy_factory/latest"),
    PackageId.from_uri_path("contract/valory/service_registry/latest"),
    PackageId.from_uri_path("contract/valory/multisend/latest"),
    PackageId.from_uri_path("connection/valory/abci/latest"),
    PackageId.from_uri_path("connection/valory/http_client/latest"),
    PackageId.from_uri_path("connection/valory/ipfs/latest"),
    PackageId.from_uri_path("connection/valory/ledger/latest"),
    PackageId.from_uri_path("connection/valory/p2p_libp2p_client/latest"),
    PackageId.from_uri_path("skill/valory/abstract_abci/latest"),
    PackageId.from_uri_path("skill/valory/abstract_round_abci/latest"),
    PackageId.from_uri_path("skill/valory/registration_abci/latest"),
    PackageId.from_uri_path("skill/valory/transaction_settlement_abci/latest"),
    PackageId.from_uri_path("skill/valory/reset_pause_abci/latest"),
]

_source_caches = {}


def get_latest_dependencies() -> t.Dict[str, PyPiDependency]:
    """Get a list of latest dependencies."""
    deps: t.Dict[str, PyPiDependency] = {}
    for name, source, extras in CORE_DEPENDENCIES:
        version = fetch_latest_tag(repo=source.repo)
        _source_caches[source] = version
        version = version.removeprefix("v")
        dep = PyPiDependency(name=name, version=f"=={version}", extras=extras)
        deps[name] = dep
    return deps


@compose.command()
def new(
    author: Annotated[str, String(long_flag="--author")],
    pms: Annotated[
        ProjectManagement,
        ChoiceByFlag(ProjectManagement, help="Choose project management style"),
    ] = ProjectManagement.PIPFILE,
) -> None:
    """Create a new compose project."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    cwd = Path.cwd()
    project_file = cwd / COMPOSE_YAML
    if project_file.exists():
        raise CleaException(f"Compose project already exitst @ {project_file}")

    if author is None:
        author = input("[-] Author: ")

    logger.info("Fetching latest core dependency versions")
    core_dependencies = get_latest_dependencies()
    management = None
    if (cwd / PYPROJECT_TOML).exists():
        management = ProjectManagement.POETRY

    if (cwd / PIPFILE).exists():
        management = ProjectManagement.PIPFILE

    core_dependencies_list = [dep for dep in core_dependencies.values()]
    if management is None:
        if pms == ProjectManagement.PIPFILE:
            init_pipfile(
                wd=cwd,
                core_dependencies=core_dependencies_list,
            )
        else:
            init_pyproject_toml(
                wd=cwd,
                core_dependencies=core_dependencies_list,
            )
        management = pms
        logger.info(f"Using {management.value} for managing the project")

    if not (cwd / TOX_INI).exists():
        logger.info("Creating tox.ini")
        init_tox_ini(
            wd=cwd,
            core_dependencies=core_dependencies_list,
        )

    logger.info(f"Creating compose project @ {cwd}")
    Project(
        author=author,
        management=management,
        sources=Sources(
            [
                GIT_SOURCE_OPEN_AEA.with_version(
                    core_dependencies[GIT_SOURCE_OPEN_AEA.name].version.replace(
                        "==", "v"
                    )
                ),
                GIT_SOURCE_OPEN_AUTONOMY.with_version(
                    core_dependencies[GIT_SOURCE_OPEN_AUTONOMY.name].version.replace(
                        "==", "v"
                    )
                ),
            ]
        ),
        path=project_file,
    ).dump()

    packages = cwd / PACKAGES
    if not packages.exists():
        logger.info(f"Initializing repository @ {packages}")
        packages.mkdir()
        PackageManagerV1(path=packages).dump()

    logger.info("Fetching latest core packages")
    pm = PackageManagerV1(
        path=packages,
        logger=logger,
    )
    for source in (GIT_SOURCE_OPEN_AEA, GIT_SOURCE_OPEN_AUTONOMY):
        packages_json = fetch_packages_json(
            repo=source.repo, tag=_source_caches[source]
        )
        source_manager = PackageManagerV1.from_json(packages_json)
        for dependency in CORE_PACKAGES:
            for remote in source_manager.dev_packages:
                if (
                    remote.package_type == dependency.package_type
                    and remote.public_id.to_any() == dependency.public_id.to_any()
                ):
                    pm.third_party_packages[remote] = source_manager.dev_packages[
                        remote
                    ]
    pm.sync().dump()

    logger.info("Copying helper scripts")
    scripts = cwd / "scripts"
    if not scripts.exists():
        scripts.mkdir()

    for script in SCRIPTS.iterdir():
        if not script.is_file():
            continue
        shutil.copy(script, scripts / script.name)

    logger.info("Setting up development dependenies")
    proc = subprocess.Popen(
        args=[sys.executable, str(scripts / "dependencies.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    proc.wait()

    logger.info("Installing dependencies")
    proc = subprocess.Popen(
        args=[
            str(
                (
                    shutil.which("pipenv")
                    if pms == ProjectManagement.PIPFILE
                    else shutil.which("poetry")
                ),
            ),
            "install",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    proc.wait()

    # Add workflow.yml if it does not exist
    logger.info("Setting up workflow")
    install_workflow(wd=cwd)

    logger.info("Done")
