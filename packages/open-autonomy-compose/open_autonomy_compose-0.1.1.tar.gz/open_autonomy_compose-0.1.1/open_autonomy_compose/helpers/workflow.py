"""Workflow helpers."""

from pathlib import Path

from open_autonomy_compose.data import TEMPLATES_DIR


WORKFLOW_YML = "workflow.yml"


def install_workflow(wd: Path) -> None:
    """Install workflow."""
    workflow_dir = wd / ".github" / "workflows"
    if workflow_dir.exists():
        return
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / WORKFLOW_YML).write_text(
        (TEMPLATES_DIR / WORKFLOW_YML).read_text(encoding="utf-8"),
        encoding="utf-8",
    )
