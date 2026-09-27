import re

import pytest

from visit_it_pro.checklist import build_checklist, copy_templates, count_checkpoints, create_visit
from visit_it_pro.config import WorkspaceError, load_workspace, write_config


def test_blank_checklist_has_every_zone_and_checkpoint(demo):
    text = build_checklist(demo, "2026-12-01")
    assert count_checkpoints(text) == 75
    zones = re.findall(r"^## (.+)$", text, re.M)
    assert zones == [
        "Synthèse",
        "Entretien",
        "Bureau et alimentation (BUR)",
        "Internet et réseau (NET)",
        "Poste 1 — Portable (PC1)",
        "Poste 2 — Bureau 1 (PC2)",
        "Poste 3 — Bureau 2 (PC3)",
        "Sauvegardes et données (SAV)",
        "Notes",
    ]
    assert "date: 2026-12-01" in text
    assert "intervenant: Technicien Exemple" in text


def test_laptop_only_items_and_unique_ids(demo):
    text = build_checklist(demo, "2026-12-01")
    ids = re.findall(r"^- \[ \] (\S+)", text, re.M)
    assert len(ids) == len(set(ids))
    assert [i for i in ids if i.endswith("-batterie")] == ["PC1-batterie"]
    assert not re.search(r"\{[A-Z]+\}|<!-- (if|endif)", text)


def test_create_visit_refuses_to_overwrite(demo):
    checklist = create_visit(demo, "2026-12-01")
    assert checklist.is_file() and (checklist.parent / "photos").is_dir()
    with pytest.raises(WorkspaceError):
        create_visit(demo, "2026-12-01")
    create_visit(demo, "2026-12-01", force=True)


def test_workspace_templates_override_builtin_ones(demo):
    copy_templates(demo)
    custom = demo.templates_dir / "checklist-computer.md"
    custom.write_text(
        custom.read_text(encoding="utf-8").replace("Version de Windows", "Version du système"), encoding="utf-8"
    )
    assert "Version du système" in build_checklist(demo, "2026-12-01")


def test_init_config_round_trip(tmp_path):
    write_config(tmp_path, 'Étude "Test"', "Alex")
    ws = load_workspace(tmp_path)
    assert ws.office == 'Étude "Test"'
    assert [c.kind for c in ws.computers] == ["laptop", "desktop"]
    with pytest.raises(WorkspaceError):
        write_config(tmp_path, "Autre", "Alex")


def test_invalid_computer_kind_is_rejected(tmp_path):
    (tmp_path / "visit-it-pro.toml").write_text(
        '[office]\nname = "X"\n[[computers]]\nid = "PC1"\nname = "A"\nkind = "tablet"\n', encoding="utf-8"
    )
    with pytest.raises(WorkspaceError, match="laptop"):
        load_workspace(tmp_path)
