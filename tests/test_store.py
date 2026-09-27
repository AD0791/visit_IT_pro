import sqlite3

import pytest
from conftest import JULY, OCTOBER

from visit_it_pro.parser import load_visit
from visit_it_pro.store import SCHEMA_VERSION, Store, StoreError


def save_both(demo):
    store = Store(demo.db_path)
    for date in (JULY, OCTOBER):
        store.save_visit(load_visit(demo.visits_dir / date), date)
    return store


def test_visits_are_saved_in_date_order(demo):
    with save_both(demo) as store:
        visits = store.visits()
        assert [v["date"] for v in visits] == [JULY, OCTOBER]
        assert (visits[1]["n_ok"], visits[1]["n_fix"], visits[1]["n_todo"]) == (45, 8, 1)
        assert visits[1]["office"] == "Cabinet Exemple"
        assert [v["date"] for v in store.visits(until=JULY)] == [JULY]


def test_saving_again_replaces_the_visit(demo):
    with save_both(demo) as store:
        store.save_visit(load_visit(demo.visits_dir / OCTOBER), OCTOBER)
        assert len(store.visits()) == 2
        assert store.conn.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 150
        assert store.conn.execute("SELECT COUNT(*) FROM zones").fetchone()[0] == 12


def test_details_numbers_and_recommendations(demo):
    with save_both(demo) as store:
        october = store.visits()[-1]
        items = {row["check_id"]: row for row in store.items(october["id"])}
        assert items["PC1-stabilite"]["value_num"] == 8.7
        assert items["PC1-internet"]["value_num"] == 88
        recos = store.recommendations(october["id"])
        assert len(recos) == 21
        assert [r["priority"] for r in recos] == sorted(
            (r["priority"] for r in recos), key=["haute", "moyenne", "basse"].index
        )
        zones = store.zones(october["id"])
        assert [(z["code"], z["n_ok"], z["n_watch"], z["n_fix"]) for z in zones][0] == ("BUR", 3, 3, 1)
        actions = store.conn.execute(
            "SELECT COUNT(*) FROM actions a JOIN items i ON i.id = a.item_id WHERE i.visit_id = ?", (october["id"],)
        ).fetchone()[0]
        assert actions == 8


def test_newer_schema_is_refused(demo):
    Store(demo.db_path).close()
    conn = sqlite3.connect(demo.db_path)
    conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION + 1}")
    conn.close()
    with pytest.raises(StoreError):
        Store(demo.db_path)
