"""Parse a filled checklist (Markdown) into a Visit, and collect the pre-send warnings."""

from __future__ import annotations

import os
import re
from collections.abc import Callable
from pathlib import Path

from .model import PRIORITIES, PRIORITY_ALIASES, STATUSES, Item, Visit, Zone, plain

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
ITEM_RE = re.compile(r"^\s*- \[(.)\] (\S+)\s+(.*)$")
SUB_RE = re.compile(r"^\s+- (.*)$")
TAG_RE = re.compile(r"^(fait|done|photo|reco)(?:\s+(\w+))?\s*:\s*(.*)$", re.I)
FICHE_RE = re.compile(r"^\s*- ([^:]+?)\s*:\s*(.*)$")
ZONE_CODE_RE = re.compile(r"\s*\(([A-Za-z0-9]+)\)$")

# Front-matter keys: the French template's names map onto the canonical English ones.
META_ALIASES = {
    "cabinet": "office",
    "intervenant": "technician",
    "presents": "attendees",
    "arrivee": "arrival",
    "depart": "departure",
    "prochaine_visite": "next_visit",
}
SUMMARY_SECTIONS = ("synthese", "summary")
PRIVATE_SECTIONS = ("entretien", "interview", "notes")


def parse_checklist(path: Path) -> Visit:
    # Blank out the how-to-check hints but keep line numbers for warnings.
    text = COMMENT_RE.sub(lambda m: "\n" * m.group().count("\n"), path.read_text(encoding="utf-8"))
    lines = text.splitlines()
    visit = Visit(meta={})

    start = 0
    if lines and lines[0].strip() == "---":
        for n in range(1, len(lines)):
            if lines[n].strip() == "---":
                start = n + 1
                break
            key, sep, value = lines[n].partition(":")
            if sep:
                key = plain(key)
                visit.meta[META_ALIASES.get(key, key)] = value.strip()

    def warn(n: int, message: str) -> None:
        visit.warnings.append(f"line {n}: {message}")

    kind = sub = None
    zone: Zone | None = None
    item: Item | None = None
    summary: list[str] = []
    seen: set[str] = set()
    for n, line in enumerate(lines[start:], start + 1):
        if line.startswith("## "):
            title = line[3:].strip()
            key = plain(title)
            if key.startswith(SUMMARY_SECTIONS):
                kind = "summary"
            elif key.startswith(PRIVATE_SECTIONS):
                kind = "private"
            else:
                kind = "zone"
            zone = item = sub = None
            if kind == "zone":
                code = ZONE_CODE_RE.search(title)
                zone = Zone(title=ZONE_CODE_RE.sub("", title), code=code.group(1) if code else "")
                visit.zones.append(zone)
            continue
        if kind == "summary":
            summary.append(line)
            continue
        if zone is None or not line.strip():
            continue  # preamble, private sections, blank lines
        if line.startswith("### "):
            sub, item = plain(line[4:]), None
            continue
        if m := ITEM_RE.match(line):
            code, item_id, rest = m.groups()
            code = code.lower()
            if code not in STATUSES:
                warn(n, f"{item_id}: unknown code [{code}] (use x ~ ! - or a space), counted as not checked")
                code = " "
            if item_id in seen:
                warn(n, f"{item_id}: duplicate ID")
            seen.add(item_id)
            label, _, tail = rest.partition("::")
            value, _, note = tail.partition("::")
            item = Item(item_id, label.strip(), STATUSES[code][0], value.strip(), note.strip())
            zone.items.append(item)
            continue
        if item and (m := SUB_RE.match(line)):
            add_detail(item, m.group(1).strip(), lambda msg, n=n: warn(n, msg))
            continue
        if sub in ("fiche", "inventory") and (m := FICHE_RE.match(line)):
            zone.fiche.append((m.group(1).strip(), m.group(2).strip()))
            continue
        warn(n, f"not understood, left out of the report: {line.strip()[:70]}")

    visit.summary = "\n".join(summary).strip()
    return visit


def add_detail(item: Item, body: str, warn: Callable[[str], None]) -> None:
    """Attach a `fait:` / `reco …:` / `photo:` line to an item; anything else extends its note."""
    tag = TAG_RE.match(body)
    if not tag or (tag.group(2) and tag.group(1).lower() != "reco"):
        item.note = "; ".join(part for part in (item.note, body) if part)
        return
    kind, content = tag.group(1).lower(), tag.group(3).strip()
    if not content:
        return
    if kind in ("fait", "done"):
        item.done.append(content)
    elif kind == "photo":
        item.photos.append(content)
    else:
        priority = (tag.group(2) or "moyenne").lower()
        priority = PRIORITY_ALIASES.get(priority, priority)
        if priority not in PRIORITIES:
            warn(f"{item.id}: unknown priority '{priority}' (use haute, moyenne or basse), using moyenne")
            priority = "moyenne"
        item.recos.append((priority, content))


def check(visit: Visit, visit_dir: Path) -> None:
    """Add the pre-send warnings and resolve photo paths relative to the visit folder."""
    if not visit.summary:
        visit.warnings.append("the Synthèse is empty: write 4–5 sentences for the owner")
    for item in visit.items:
        if item.status == "fix" and not item.recos:
            visit.warnings.append(f"{item.id}: marked 🔴 but has no 'reco' line")
        found = []
        for photo in item.photos:
            path = next((p for p in (visit_dir / photo, visit_dir / "photos" / photo) if p.is_file()), None)
            if path is None:
                visit.warnings.append(f"{item.id}: photo not found: {photo}")
            else:
                found.append(Path(os.path.relpath(path, visit_dir)).as_posix())
        item.photos = found
    todo = [item.id for item in visit.items if item.status == "todo"]
    if todo:
        listed = ", ".join(todo[:6]) + (", …" if len(todo) > 6 else "")
        visit.warnings.append(f"{len(todo)} checkpoint(s) not checked yet: {listed}")


def load_visit(visit_dir: Path) -> Visit:
    """Parse and check `<visit_dir>/checklist.md`."""
    visit = parse_checklist(visit_dir / "checklist.md")
    check(visit, visit_dir)
    return visit
