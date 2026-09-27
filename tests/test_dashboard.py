import io

from conftest import JULY, OCTOBER
from rich.console import Console

from visit_it_pro.dashboard import build_dashboard, export, sparkline
from visit_it_pro.parser import load_visit
from visit_it_pro.store import Store


def as_text(renderable) -> str:
    console = Console(file=io.StringIO(), width=120, color_system=None)
    console.print(renderable)
    return console.file.getvalue()


def test_dashboard_shows_history_trends_and_progress(demo):
    with Store(demo.db_path) as store:
        for date in (JULY, OCTOBER):
            store.save_visit(load_visit(demo.visits_dir / date), date)
        text = as_text(build_dashboard(store, demo.office))
        assert "Visite du 2 octobre 2026" in text
        assert "2 visite(s) enregistrée(s)" in text
        assert "10 point(s) corrigé(s) · 0 nouveau(x) point(s) à corriger" in text
        assert "62 % ▁█ +7" in text  # PC1 free space went from 55 % to 62 %
        assert "Recommandations ouvertes : 21 (12 haute · 5 moyenne · 4 basse)" in text

        as_of_july = as_text(build_dashboard(store, demo.office, JULY))
        assert "Visite du 3 juillet 2026" in as_of_july
        assert "Depuis la visite" not in as_of_july


def test_empty_store_and_export(demo, tmp_path):
    with Store(demo.db_path) as store:
        empty = build_dashboard(store, demo.office)
    assert "Aucune visite enregistrée" in as_text(empty)
    svg = export(empty, tmp_path / "d.svg")
    assert svg.read_text(encoding="utf-8").startswith("<svg")
    assert "@font-face" not in svg.read_text(encoding="utf-8")
    html = export(empty, tmp_path / "d.html")
    assert "<html" in html.read_text(encoding="utf-8").lower()


def test_sparkline():
    assert sparkline([1]) == ""
    assert sparkline([1, 2, 3]) == "▁▅█"
    assert sparkline([5, 5]) == "▄▄"
