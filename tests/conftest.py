from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from visit_it_pro.config import Workspace, load_workspace

DEMO = Path(__file__).resolve().parent.parent / "examples" / "demo"
JULY, OCTOBER = "2026-07-03", "2026-10-02"


@pytest.fixture
def demo(tmp_path: Path) -> Workspace:
    """A private copy of the demo workspace: config, the two checklists and the photo, no outputs."""
    root = tmp_path / "demo"
    shutil.copytree(DEMO, root, ignore=shutil.ignore_patterns("*.db", "rapport-*", "tableau-de-bord.*"))
    return load_workspace(root)
