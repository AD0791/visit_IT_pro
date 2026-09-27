"""Core data model: checkpoint statuses, items, zones and visits."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass, field

# Checklist code -> (status key, emoji, French label).
STATUSES = {
    "x": ("ok", "🟢", "Bon"),
    "~": ("watch", "🟠", "À surveiller"),
    "!": ("fix", "🔴", "À corriger"),
    "-": ("na", "➖", "Sans objet"),
    " ": ("todo", "⚪", "Non vérifié"),
}
STATUS_KEYS = ("ok", "watch", "fix", "todo", "na")
EMOJI = {key: emoji for key, emoji, _ in STATUSES.values()}
LABEL = {key: label for key, _, label in STATUSES.values()}
BADGE = {key: f"{EMOJI[key]} {LABEL[key]}" for key in STATUS_KEYS}
# Severity for "worst of" roll-ups; "na" and "todo" never count.
RANK = {"ok": 1, "watch": 2, "fix": 3}

# Recommendation priorities, highest first. English aliases are accepted in checklists.
PRIORITIES = ("haute", "moyenne", "basse")
PRIORITY_LABEL = {"haute": "Haute", "moyenne": "Moyenne", "basse": "Basse"}
PRIORITY_ALIASES = {"high": "haute", "medium": "moyenne", "low": "basse"}

NUMBER_RE = re.compile(r"-?\d+(?:[.,]\d+)?")


def worst(statuses: Iterable[str]) -> str:
    ranked = [status for status in statuses if status in RANK]
    return max(ranked, key=RANK.__getitem__) if ranked else "todo"


def plain(text: str) -> str:
    """Lowercase ASCII form of a heading or key, for matching names written with or without accents."""
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().strip().lower()


def first_number(text: str) -> float | None:
    """First number in a free-text value ("8,7/10" -> 8.7, "↓88 ↑45 Mb/s" -> 88), used for trends."""
    match = NUMBER_RE.search(text or "")
    return float(match.group().replace(",", ".")) if match else None


@dataclass
class Item:
    id: str
    label: str
    status: str
    value: str = ""
    note: str = ""
    done: list[str] = field(default_factory=list)
    recos: list[tuple[str, str]] = field(default_factory=list)
    photos: list[str] = field(default_factory=list)

    @property
    def suffix(self) -> str:
        return self.id.split("-", 1)[-1]

    @property
    def observation(self) -> str:
        return " — ".join(part for part in (self.value, self.note) if part)


@dataclass
class Zone:
    title: str
    code: str = ""
    fiche: list[tuple[str, str]] = field(default_factory=list)
    items: list[Item] = field(default_factory=list)

    def count(self, status: str) -> int:
        return sum(item.status == status for item in self.items)

    @property
    def status(self) -> str:
        return worst(item.status for item in self.items)

    @property
    def is_computer(self) -> bool:
        return any(item.suffix == "windows" for item in self.items)


@dataclass
class Visit:
    meta: dict[str, str]
    summary: str = ""
    zones: list[Zone] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def items(self) -> list[Item]:
        return [item for zone in self.zones for item in zone.items]

    @property
    def overall(self) -> str:
        return worst(zone.status for zone in self.zones)

    def counts(self) -> dict[str, int]:
        return {key: sum(item.status == key for item in self.items) for key in STATUS_KEYS}
