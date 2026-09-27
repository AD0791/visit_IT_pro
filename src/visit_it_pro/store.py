"""SQLite store: every saved visit, for history, trends and the dashboard."""

from __future__ import annotations

import datetime as dt
import sqlite3
from pathlib import Path

from .model import Visit, first_number

SCHEMA_VERSION = 1
SCHEMA = """
CREATE TABLE visits (
    id          INTEGER PRIMARY KEY,
    date        TEXT NOT NULL UNIQUE,          -- ISO date; one visit per day per workspace
    office      TEXT NOT NULL,
    technician  TEXT NOT NULL DEFAULT '',
    attendees   TEXT NOT NULL DEFAULT '',
    arrival     TEXT NOT NULL DEFAULT '',
    departure   TEXT NOT NULL DEFAULT '',
    next_visit  TEXT NOT NULL DEFAULT '',
    summary     TEXT NOT NULL DEFAULT '',
    overall     TEXT NOT NULL,                 -- ok | watch | fix | todo
    n_ok        INTEGER NOT NULL,
    n_watch     INTEGER NOT NULL,
    n_fix       INTEGER NOT NULL,
    n_todo      INTEGER NOT NULL,
    n_na        INTEGER NOT NULL,
    checklist   TEXT NOT NULL DEFAULT '',      -- path of the source checklist.md
    saved_at    TEXT NOT NULL
);
CREATE TABLE zones (
    id          INTEGER PRIMARY KEY,
    visit_id    INTEGER NOT NULL REFERENCES visits(id) ON DELETE CASCADE,
    position    INTEGER NOT NULL,
    code        TEXT NOT NULL DEFAULT '',      -- BUR, NET, PC1, … (from "## Title (CODE)")
    title       TEXT NOT NULL,
    status      TEXT NOT NULL,
    is_computer INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE items (
    id          INTEGER PRIMARY KEY,
    visit_id    INTEGER NOT NULL REFERENCES visits(id) ON DELETE CASCADE,
    zone_id     INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    position    INTEGER NOT NULL,
    check_id    TEXT NOT NULL,                 -- stable across visits: PC1-espace, NET-stabilite…
    label       TEXT NOT NULL,
    status      TEXT NOT NULL,                 -- ok | watch | fix | todo | na
    value       TEXT NOT NULL DEFAULT '',
    value_num   REAL,                          -- first number in value, for trends
    note        TEXT NOT NULL DEFAULT ''
);
CREATE TABLE actions (
    id          INTEGER PRIMARY KEY,
    item_id     INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    text        TEXT NOT NULL
);
CREATE TABLE recommendations (
    id          INTEGER PRIMARY KEY,
    item_id     INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    priority    TEXT NOT NULL,                 -- haute | moyenne | basse
    text        TEXT NOT NULL
);
CREATE TABLE photos (
    id          INTEGER PRIMARY KEY,
    item_id     INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    path        TEXT NOT NULL
);
CREATE TABLE inventory (
    id          INTEGER PRIMARY KEY,
    zone_id     INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    key         TEXT NOT NULL,
    value       TEXT NOT NULL
);
CREATE INDEX items_by_visit ON items(visit_id);
CREATE INDEX items_by_check ON items(check_id);
"""

PRIORITY_ORDER = "CASE r.priority WHEN 'haute' THEN 0 WHEN 'moyenne' THEN 1 ELSE 2 END"


class StoreError(Exception):
    """The database cannot be used by this version of visit-it-pro."""


class Store:
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        version = self.conn.execute("PRAGMA user_version").fetchone()[0]
        if version == 0:
            self.conn.executescript(SCHEMA)
            self.conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            self.conn.commit()
        elif version > SCHEMA_VERSION:
            raise StoreError(f"{path} was written by a newer visit-it-pro (schema {version}); upgrade the package")

    def __enter__(self) -> Store:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        self.conn.close()

    # --- writing -------------------------------------------------------------

    def save_visit(self, visit: Visit, date: str, checklist: Path | str = "") -> int:
        """Insert the visit, replacing any visit already saved for the same date. Returns its id."""
        meta, counts = visit.meta, visit.counts()
        with self.conn:
            self.conn.execute("DELETE FROM visits WHERE date = ?", (date,))
            visit_id = self.conn.execute(
                "INSERT INTO visits (date, office, technician, attendees, arrival, departure, next_visit,"
                " summary, overall, n_ok, n_watch, n_fix, n_todo, n_na, checklist, saved_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    date,
                    meta.get("office", ""),
                    meta.get("technician", ""),
                    meta.get("attendees", ""),
                    meta.get("arrival", ""),
                    meta.get("departure", ""),
                    meta.get("next_visit", ""),
                    visit.summary,
                    visit.overall,
                    counts["ok"],
                    counts["watch"],
                    counts["fix"],
                    counts["todo"],
                    counts["na"],
                    str(checklist),
                    dt.datetime.now().isoformat(timespec="seconds"),
                ),
            ).lastrowid
            for z, zone in enumerate(visit.zones):
                zone_id = self.conn.execute(
                    "INSERT INTO zones (visit_id, position, code, title, status, is_computer)"
                    " VALUES (?, ?, ?, ?, ?, ?)",
                    (visit_id, z, zone.code, zone.title, zone.status, int(zone.is_computer)),
                ).lastrowid
                self.conn.executemany(
                    "INSERT INTO inventory (zone_id, key, value) VALUES (?, ?, ?)",
                    [(zone_id, k, v) for k, v in zone.fiche if v],
                )
                for i, item in enumerate(zone.items):
                    item_id = self.conn.execute(
                        "INSERT INTO items (visit_id, zone_id, position, check_id, label, status, value,"
                        " value_num, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            visit_id,
                            zone_id,
                            i,
                            item.id,
                            item.label,
                            item.status,
                            item.value,
                            first_number(item.value),
                            item.note,
                        ),
                    ).lastrowid
                    self.conn.executemany(
                        "INSERT INTO actions (item_id, text) VALUES (?, ?)", [(item_id, text) for text in item.done]
                    )
                    self.conn.executemany(
                        "INSERT INTO recommendations (item_id, priority, text) VALUES (?, ?, ?)",
                        [(item_id, p, text) for p, text in item.recos],
                    )
                    self.conn.executemany(
                        "INSERT INTO photos (item_id, path) VALUES (?, ?)", [(item_id, path) for path in item.photos]
                    )
        return visit_id

    # --- reading -------------------------------------------------------------

    def visits(self, until: str | None = None) -> list[sqlite3.Row]:
        """Saved visits in date order, optionally up to and including `until`."""
        if until:
            return self.conn.execute("SELECT * FROM visits WHERE date <= ? ORDER BY date", (until,)).fetchall()
        return self.conn.execute("SELECT * FROM visits ORDER BY date").fetchall()

    def zones(self, visit_id: int) -> list[sqlite3.Row]:
        """Zones of a visit with their status counts."""
        return self.conn.execute(
            "SELECT z.*, SUM(i.status = 'ok') AS n_ok, SUM(i.status = 'watch') AS n_watch,"
            " SUM(i.status = 'fix') AS n_fix, SUM(i.status = 'todo') AS n_todo"
            " FROM zones z LEFT JOIN items i ON i.zone_id = z.id"
            " WHERE z.visit_id = ? GROUP BY z.id ORDER BY z.position",
            (visit_id,),
        ).fetchall()

    def zone_statuses(self, visit_ids: list[int]) -> dict[tuple[int, str], str]:
        """(visit id, zone key) -> status, where the key is the zone code or, failing that, its title."""
        if not visit_ids:
            return {}
        marks = ",".join("?" * len(visit_ids))
        rows = self.conn.execute(
            f"SELECT visit_id, code, title, status FROM zones WHERE visit_id IN ({marks})", visit_ids
        )
        return {(row["visit_id"], row["code"] or row["title"]): row["status"] for row in rows}

    def items(self, visit_id: int) -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT i.*, z.code AS zone_code, z.title AS zone_title FROM items i"
            " JOIN zones z ON z.id = i.zone_id WHERE i.visit_id = ? ORDER BY z.position, i.position",
            (visit_id,),
        ).fetchall()

    def recommendations(self, visit_id: int) -> list[sqlite3.Row]:
        """Recommendations of a visit, highest priority first, then checklist order."""
        return self.conn.execute(
            "SELECT r.priority, r.text, i.check_id, i.label, i.status, z.title AS zone_title"
            " FROM recommendations r JOIN items i ON i.id = r.item_id JOIN zones z ON z.id = i.zone_id"
            f" WHERE i.visit_id = ? ORDER BY {PRIORITY_ORDER}, z.position, i.position, r.id",
            (visit_id,),
        ).fetchall()

    def computer_measures(self, until: str | None = None) -> list[sqlite3.Row]:
        """Every checkpoint of computer zones, oldest visit first: the raw material for trends."""
        return self.conn.execute(
            "SELECT v.date, z.code AS zone_code, z.title AS zone_title, i.check_id, i.value,"
            " i.value_num, i.status FROM items i JOIN zones z ON z.id = i.zone_id"
            " JOIN visits v ON v.id = i.visit_id"
            " WHERE z.is_computer = 1 AND (? IS NULL OR v.date <= ?) ORDER BY v.date, z.position, i.position",
            (until, until),
        ).fetchall()
