"""Build a blank visit checklist from the templates and the workspace configuration."""

from __future__ import annotations

import re
from importlib import resources
from pathlib import Path

from .config import Workspace, WorkspaceError

TEMPLATE_NAMES = ("checklist-site.md", "checklist-computer.md", "report.css")
COND_RE = re.compile(r"^<!-- if (\w+) -->\n(.*?)^<!-- endif -->\n", re.M | re.S)
CHECKPOINT_RE = re.compile(r"^- \[ \] ", re.M)


def template_text(ws: Workspace | None, name: str) -> str:
    """A template from the workspace's `templates/` folder if present, else the built-in one."""
    if ws is not None and (custom := ws.templates_dir / name).is_file():
        return custom.read_text(encoding="utf-8")
    return resources.files("visit_it_pro").joinpath("templates", name).read_text(encoding="utf-8")


def build_checklist(ws: Workspace, date: str) -> str:
    computer_template = template_text(ws, "checklist-computer.md")
    blocks = []
    for n, computer in enumerate(ws.computers, 1):
        block = COND_RE.sub(lambda m, kind=computer.kind: m.group(2) if m.group(1) == kind else "", computer_template)
        for key, value in {"{N}": str(n), "{ID}": computer.id, "{NAME}": computer.name}.items():
            block = block.replace(key, value)
        blocks.append(block)

    text = template_text(ws, "checklist-site.md")
    replacements = {
        "{COMPUTERS}\n": "".join(blocks),
        "{OFFICE}": ws.office,
        "{DATE}": date,
        "{TECHNICIAN}": ws.technician.get("name", ""),
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def count_checkpoints(text: str) -> int:
    return len(CHECKPOINT_RE.findall(text))


def create_visit(ws: Workspace, date: str, force: bool = False) -> Path:
    """Write `visits/<date>/checklist.md` and an empty `photos/` folder; return the checklist path."""
    visit_dir = ws.visits_dir / date
    checklist = visit_dir / "checklist.md"
    if checklist.exists() and not force:
        raise WorkspaceError(f"{checklist} already exists (add --force to overwrite it)")
    text = build_checklist(ws, date)
    (visit_dir / "photos").mkdir(parents=True, exist_ok=True)
    checklist.write_text(text, encoding="utf-8")
    return checklist


def copy_templates(ws: Workspace, force: bool = False) -> list[Path]:
    """Copy the built-in templates into the workspace so they can be customised."""
    ws.templates_dir.mkdir(exist_ok=True)
    written = []
    for name in TEMPLATE_NAMES:
        target = ws.templates_dir / name
        if target.exists() and not force:
            continue
        target.write_text(template_text(None, name), encoding="utf-8")
        written.append(target)
    return written
