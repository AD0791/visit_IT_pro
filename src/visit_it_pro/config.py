"""Workspace configuration: the `visit-it-pro.toml` file at the root of a client folder."""

from __future__ import annotations

import datetime as dt
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

CONFIG_NAME = "visit-it-pro.toml"
KINDS = ("laptop", "desktop")
ID_RE = re.compile(r"^[A-Za-z0-9]+$")


class WorkspaceError(Exception):
    """A problem with the workspace or its configuration, shown to the user as-is."""


@dataclass
class Computer:
    id: str
    name: str
    kind: str


@dataclass
class Workspace:
    root: Path
    office: str
    technician: dict[str, str]
    computers: list[Computer]
    visits_dir: Path
    db_path: Path
    dashboard_in_report: bool = True

    @property
    def config_path(self) -> Path:
        return self.root / CONFIG_NAME

    @property
    def templates_dir(self) -> Path:
        """Optional folder of customised templates; files found here override the built-in ones."""
        return self.root / "templates"

    def visit_dir(self, ref: str) -> Path:
        """Resolve a visit reference: an existing folder, or a date meaning `visits/<date>`."""
        candidate = Path(ref).expanduser()
        if candidate.is_dir():
            return candidate.resolve()
        if is_date(ref):
            return self.visits_dir / ref
        raise WorkspaceError(f"{ref!r} is neither a visit folder nor a date (YYYY-MM-DD)")


def is_date(text: str) -> bool:
    try:
        dt.date.fromisoformat(text.strip())
    except ValueError:
        return False
    return True


def find_root(start: Path) -> Path:
    for folder in (start, *start.parents):
        if (folder / CONFIG_NAME).is_file():
            return folder
    raise WorkspaceError(
        f"No {CONFIG_NAME} found in {start} or its parent folders. "
        "Run `visit-it-pro init` in the client folder, or pass --workspace."
    )


def load_workspace(start: Path | None = None) -> Workspace:
    root = find_root((start or Path.cwd()).expanduser().resolve())
    path = root / CONFIG_NAME
    try:
        with path.open("rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as exc:
        raise WorkspaceError(f"{path}: {exc}") from exc

    office = str(data.get("office", {}).get("name", "")).strip()
    if not office:
        raise WorkspaceError(f"{path}: [office] needs a name")
    technician = {key: str(value) for key, value in data.get("technician", {}).items()}

    computers: list[Computer] = []
    for entry in data.get("computers", []):
        computer = Computer(str(entry.get("id", "")), str(entry.get("name", "")), str(entry.get("kind", "")))
        if not ID_RE.match(computer.id):
            raise WorkspaceError(f"{path}: computer id {computer.id!r} must use only letters and digits")
        if computer.kind not in KINDS:
            raise WorkspaceError(f'{path}: computer {computer.id} needs kind = "laptop" or "desktop"')
        if any(c.id == computer.id for c in computers):
            raise WorkspaceError(f"{path}: computer id {computer.id} is used twice")
        computers.append(computer)

    paths = data.get("paths", {})
    return Workspace(
        root=root,
        office=office,
        technician=technician,
        computers=computers,
        visits_dir=root / paths.get("visits", "visits"),
        db_path=root / paths.get("database", "visit-it-pro.db"),
        dashboard_in_report=bool(data.get("report", {}).get("dashboard", True)),
    )


def toml_string(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


CONFIG_TEMPLATE = """\
# visit-it-pro workspace configuration.
# Every command run in this folder (or a sub-folder) uses this file.

[office]
name = {office}

[technician]
# Printed in the report header and closing line.
name = {technician}
phone = ""
email = ""

[report]
# Add the terminal dashboard (history of all saved visits) to every report.
dashboard = true

# Optional: where visits and the database live, relative to this file.
# [paths]
# visits = "visits"
# database = "visit-it-pro.db"

# One [[computers]] block per computer; kind = "laptop" or "desktop".
# The id (letters and digits only) prefixes every checkpoint ID: PC1-espace, PC1-batterie…
[[computers]]
id = "PC1"
name = "Portable"
kind = "laptop"

[[computers]]
id = "PC2"
name = "Bureau 1"
kind = "desktop"
"""


def write_config(root: Path, office: str, technician: str, force: bool = False) -> Path:
    path = root / CONFIG_NAME
    if path.exists() and not force:
        raise WorkspaceError(f"{path} already exists (add --force to overwrite it)")
    root.mkdir(parents=True, exist_ok=True)
    path.write_text(
        CONFIG_TEMPLATE.format(office=toml_string(office), technician=toml_string(technician)), encoding="utf-8"
    )
    return path
