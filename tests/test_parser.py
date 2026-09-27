from conftest import JULY, OCTOBER

from visit_it_pro.model import first_number
from visit_it_pro.parser import load_visit, parse_checklist


def test_october_counts_and_warnings(demo):
    visit = load_visit(demo.visits_dir / OCTOBER)
    assert visit.counts() == {"ok": 45, "watch": 21, "fix": 8, "todo": 1, "na": 0}
    assert visit.overall == "fix"
    assert visit.warnings == [
        "PC3-distance: marked 🔴 but has no 'reco' line",
        "1 checkpoint(s) not checked yet: NET-secours",
    ]
    assert visit.meta["technician"] == "Technicien Exemple"
    assert visit.meta["next_visit"] == "2026-11-06"


def test_july_is_complete(demo):
    visit = load_visit(demo.visits_dir / JULY)
    assert visit.counts() == {"ok": 36, "watch": 22, "fix": 17, "todo": 0, "na": 0}
    assert visit.warnings == []


def test_zones_items_and_details(demo):
    visit = load_visit(demo.visits_dir / OCTOBER)
    zones = {zone.code: zone for zone in visit.zones}
    assert list(zones) == ["BUR", "NET", "PC1", "PC2", "PC3", "SAV"]
    assert [z.code for z in visit.zones if z.is_computer] == ["PC1", "PC2", "PC3"]
    item = next(i for i in zones["PC1"].items if i.id == "PC1-chiffrement")
    assert (item.status, item.value, item.note) == ("fix", "Désactivé", "portable emporté chaque soir")
    assert item.recos == [("haute", "Activer BitLocker et conserver la clé de récupération en lieu sûr")]
    photo_item = next(i for i in zones["PC3"].items if i.id == "PC3-etat")
    assert photo_item.photos == ["photos/PC3-poussiere.png"]
    assert ("Débit contractuel (descendant / montant)", "100 / 50 Mb/s") in zones["NET"].fiche


def test_private_sections_are_not_parsed(demo):
    visit = load_visit(demo.visits_dir / OCTOBER)
    everything = repr(visit)
    assert "neveu" not in everything


def test_english_aliases_and_bad_input(tmp_path):
    path = tmp_path / "checklist.md"
    path.write_text(
        "---\noffice: Test\ndate: 2026-01-05\n---\n"
        "## Summary\n\nAll good.\n\n"
        "## Office (OFF)\n\n"
        "- [x] OFF-a First :: 12 % :: fine\n"
        "  - done: cleaned\n"
        "  - reco high: replace it\n"
        "- [v] OFF-b Second\n"
        "- [x] OFF-a Duplicate\n"
        "-[x] OFF-c Broken line\n",
        encoding="utf-8",
    )
    visit = parse_checklist(path)
    first = visit.zones[0].items[0]
    assert (first.done, first.recos) == (["cleaned"], [("haute", "replace it")])
    assert visit.summary == "All good."
    assert any("unknown code [v]" in w for w in visit.warnings)
    assert any("duplicate ID" in w for w in visit.warnings)
    assert any("not understood" in w for w in visit.warnings)


def test_first_number():
    assert first_number("8,7/10") == 8.7
    assert first_number("↓88 ↑45 Mb/s · 12 ms") == 88
    assert first_number("câble · ↓94 ↑48 Mb/s") == 94
    assert first_number("Aucun") is None
