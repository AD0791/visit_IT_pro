import re

from conftest import OCTOBER

from visit_it_pro.parser import load_visit
from visit_it_pro.report import french_date, render_report


def render(demo, **kwargs):
    return render_report(load_visit(demo.visits_dir / OCTOBER), demo, **kwargs)


def test_report_sections_and_privacy(demo):
    text = render(demo)
    headings = re.findall(r"^## (.+)$", text, re.M)
    assert headings == [
        "État général : 🔴 À corriger",
        "Tableau de bord",
        "Interventions réalisées pendant la visite",
        "Recommandations",
        "Mesures clés",
        "Annexe A — Inventaire du parc",
        "Annexe B — Détail des contrôles",
        "Annexe C — Photos",
    ]
    assert "neveu" not in text
    assert "<!--" not in text
    assert "75 points de contrôle : 45 🟢 Bon · 21 🟠 À surveiller · 8 🔴 À corriger · 1 ⚪ Non vérifié." in text


def test_recommendations_sorted_by_priority(demo):
    text = render(demo)
    rows = [
        line
        for line in text.splitlines()
        if line.startswith("| **Haute**") or line.startswith("| Moyenne") or line.startswith("| Basse")
    ]
    order = [0 if "Haute" in r.split("|")[1] else 1 if "Moyenne" in r.split("|")[1] else 2 for r in rows]
    assert order == sorted(order) and len(rows) == 21


def test_dashboard_section_only_when_requested(demo):
    assert "Suivi dans le temps" not in render(demo)
    text = render(demo, dashboard="tableau-de-bord.svg")
    assert "## Suivi dans le temps" in text
    assert "![Tableau de bord de suivi](<tableau-de-bord.svg>)" in text


def test_contact_details_belong_to_the_configured_technician(demo):
    demo.technician.update(phone="+000", email="tech@example.com")
    assert "par Technicien Exemple · +000 · tech@example.com." in render(demo)
    demo.technician["name"] = "Quelqu'un d'autre"
    assert "+000" not in render(demo)


def test_french_date():
    assert french_date("2026-10-02") == "2 octobre 2026"
    assert french_date("2026-08-01") == "1er août 2026"
    assert french_date("bientôt") == "bientôt"
