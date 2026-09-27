import shutil

import pytest
from conftest import JULY, OCTOBER
from typer.testing import CliRunner

from visit_it_pro.cli import app
from visit_it_pro.pdf import find_chrome

runner = CliRunner()


def run(*args):
    return runner.invoke(app, [str(a) for a in args])


def test_version():
    result = run("--version")
    assert result.exit_code == 0 and result.stdout.startswith("visit-it-pro ")


def test_full_cycle_in_a_new_workspace(tmp_path):
    ws = tmp_path / "client"
    assert run("init", ws, "--office", "Étude Test", "--technician", "Alex").exit_code == 0
    assert run("-w", ws, "new", "--date", "2026-12-01").exit_code == 0
    assert (ws / "visits" / "2026-12-01" / "checklist.md").is_file()
    assert run("-w", ws, "new", "--date", "2026-12-01").exit_code == 1  # no silent overwrite

    check = run("-w", ws, "check", "2026-12-01")
    assert check.exit_code == 0 and "checkpoint(s) not checked yet" in check.stdout

    report = run("-w", ws, "report", "2026-12-01", "--no-pdf")
    assert report.exit_code == 0, report.stdout
    assert (ws / "visits" / "2026-12-01" / "rapport-2026-12-01.md").is_file()
    assert (ws / "visits" / "2026-12-01" / "tableau-de-bord.svg").is_file()
    assert (ws / "visit-it-pro.db").is_file()
    assert "2026-12-01" in run("-w", ws, "list").stdout


def test_demo_reports_and_dashboard(demo, tmp_path):
    for date in (JULY, OCTOBER):
        result = run("-w", demo.root, "report", date, "--no-pdf")
        assert result.exit_code == 0, result.stdout
    assert "PC3-distance: marked 🔴 but has no 'reco' line" in result.stdout
    report = (demo.visits_dir / OCTOBER / f"rapport-{OCTOBER}.md").read_text(encoding="utf-8")
    assert "## Suivi dans le temps" in report and "neveu" not in report

    export = tmp_path / "board.svg"
    dashboard = run("-w", demo.root, "dashboard", "--export", export)
    assert dashboard.exit_code == 0 and export.read_text(encoding="utf-8").startswith("<svg")


def test_no_save_leaves_the_database_alone(demo):
    result = run("-w", demo.root, "report", OCTOBER, "--no-pdf", "--no-save")
    assert result.exit_code == 0 and "dashboard is left out" in result.stdout
    assert not demo.db_path.exists()


def test_errors_are_reported_cleanly(tmp_path):
    result = run("-w", tmp_path, "new")
    assert result.exit_code == 1 and "visit-it-pro.toml" in result.output
    assert run("-w", tmp_path, "new", "--date", "tomorrow").exit_code == 1


@pytest.mark.skipif(not (shutil.which("pandoc") and find_chrome()), reason="needs pandoc and Chrome")
def test_pdf_is_a4(demo):
    result = run("-w", demo.root, "report", OCTOBER)
    assert result.exit_code == 0, result.output
    pdf = (demo.visits_dir / OCTOBER / f"rapport-{OCTOBER}.pdf").read_bytes()
    assert pdf.startswith(b"%PDF")
    assert b"/MediaBox [0 0 594.95996 841.91998]" in pdf
