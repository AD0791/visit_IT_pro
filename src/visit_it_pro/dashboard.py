"""Terminal dashboard (Rich) built from the SQLite store; exportable as SVG or HTML for the report."""

from __future__ import annotations

import io
import re
import sqlite3
from pathlib import Path

from rich import box
from rich.console import Console, Group, RenderableType
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .model import LABEL, PRIORITY_LABEL
from .report import french_date
from .store import Store

STYLE = {"ok": "green3", "watch": "dark_orange", "fix": "red1", "todo": "grey62", "na": "grey62"}
DOT = "●"
SPARK = "▁▂▃▄▅▆▇█"
HISTORY = 6  # visits shown in the history columns
# Trend columns: (checkpoint suffix, header, unit, higher is better).
TRENDS = (
    ("espace", "Espace libre", " %", True),
    ("stabilite", "Stabilité", "/10", True),
    ("demarrage", "Démarrage", " s", False),
    ("batterie", "Batterie", " %", True),
    ("internet", "Internet ↓", " Mb/s", True),
)
FONT_FACE_RE = re.compile(r"@font-face\s*\{[^}]*\}", re.S)
LOCAL_MONO = "Menlo, Consolas, 'DejaVu Sans Mono', monospace"


def status_text(status: str) -> Text:
    return Text.assemble((DOT + " ", STYLE[status]), LABEL[status])


def fr_number(value: float, signed: bool = False) -> str:
    text = f"{value:+.1f}" if signed else f"{value:.1f}"
    if text.endswith(".0"):
        text = text[:-2]
    return text.replace(".", ",").replace("-", "−")


def sparkline(values: list[float]) -> str:
    if len(values) < 2:
        return ""
    low, high = min(values), max(values)
    if high == low:
        return SPARK[3] * len(values)
    return "".join(SPARK[round((v - low) / (high - low) * (len(SPARK) - 1))] for v in values)


def build_dashboard(store: Store, office: str, date: str | None = None) -> RenderableType:
    """The dashboard as of `date` (default: the latest saved visit)."""
    visits = store.visits(until=date)
    if not visits:
        return Panel(
            "Aucune visite enregistrée.\nLancez [bold]visit-it-pro report <visite>[/] pour en enregistrer une.",
            title=f"{escape(office)} · Tableau de bord",
            border_style="grey62",
        )
    current = visits[-1]
    previous = visits[-2] if len(visits) > 1 else None
    recent = visits[-HISTORY:]
    parts = [
        header(current, len(visits), office),
        zones_table(store, current, recent),
        trends_table(store, current),
        recommendations_table(store, current),
        progress(store, current, previous),
        history_table(recent),
    ]
    return Group(*[part for part in parts if part is not None])


def header(current: sqlite3.Row, n_visits: int, office: str) -> Panel:
    counts = Text.assemble(
        f"{current['n_ok'] + current['n_watch'] + current['n_fix'] + current['n_todo'] + current['n_na']} points : ",
        (DOT, STYLE["ok"]),
        f" {current['n_ok']} bons · ",
        (DOT, STYLE["watch"]),
        f" {current['n_watch']} à surveiller · ",
        (DOT, STYLE["fix"]),
        f" {current['n_fix']} à corriger",
        f" · {current['n_todo']} non vérifié(s)" if current["n_todo"] else "",
    )
    body = Text.assemble(
        "Visite du ",
        (french_date(current["date"]), "bold"),
        "   État général : ",
        status_text(current["overall"]),
        f"   {n_visits} visite(s) enregistrée(s)\n",
        counts,
    )
    return Panel(
        body, title=f"[bold]{escape(office)}[/] · Tableau de bord", title_align="left", border_style="steel_blue"
    )


def zones_table(store: Store, current: sqlite3.Row, recent: list[sqlite3.Row]) -> Table:
    history = store.zone_statuses([visit["id"] for visit in recent])
    table = Table(title="Zones", title_justify="left", title_style="bold", box=box.SIMPLE_HEAD, expand=True)
    table.add_column("Zone")
    table.add_column("État")
    for status, header_text in (("ok", "Bon"), ("watch", "À surv."), ("fix", "À corr.")):
        table.add_column(Text(header_text, style=STYLE[status]), justify="right")
    table.add_column(f"Historique ({len(recent)} visites)" if len(recent) > 1 else "Historique")
    for zone in store.zones(current["id"]):
        key = zone["code"] or zone["title"]
        dots = Text(" ").join(
            Text(DOT, style=STYLE[history[(v["id"], key)]]) if (v["id"], key) in history else Text("·", "grey50")
            for v in recent
        )
        table.add_row(
            zone["title"],
            status_text(zone["status"]),
            str(zone["n_ok"] or 0),
            str(zone["n_watch"] or 0),
            str(zone["n_fix"] or 0),
            dots,
        )
    return table


def trends_table(store: Store, current: sqlite3.Row) -> Table | None:
    series: dict[tuple[str, str], list[sqlite3.Row]] = {}
    titles: dict[str, str] = {}
    current_zones = []
    for row in store.computer_measures(until=current["date"]):
        zone_key = row["zone_code"] or row["zone_title"]
        suffix = row["check_id"].split("-", 1)[-1]
        series.setdefault((zone_key, suffix), []).append(row)
        if row["date"] == current["date"] and zone_key not in titles:
            titles[zone_key] = row["zone_title"]
            current_zones.append(zone_key)
    if not current_zones:
        return None
    table = Table(
        title="Mesures clés (valeur actuelle · tendance · écart avec la visite précédente)",
        title_justify="left",
        title_style="bold",
        box=box.SIMPLE_HEAD,
        expand=True,
    )
    table.add_column("Poste")
    for _, header_text, _, _ in TRENDS:
        table.add_column(header_text)
    for zone_key in current_zones:
        cells: list[Text | str] = [titles[zone_key]]
        for suffix, _, unit, higher_is_better in TRENDS:
            rows = [r for r in series.get((zone_key, suffix), [])]
            latest = rows[-1] if rows and rows[-1]["date"] == current["date"] else None
            if latest is None or latest["value_num"] is None:
                cells.append(Text("—", "grey50"))
                continue
            numbers = [r["value_num"] for r in rows if r["value_num"] is not None]
            cell = Text(fr_number(latest["value_num"]) + unit, style=STYLE[latest["status"]])
            if spark := sparkline(numbers[-HISTORY:]):
                cell.append(" " + spark, style="steel_blue")
            if len(numbers) > 1 and (delta := numbers[-1] - numbers[-2]):
                better = (delta > 0) == higher_is_better
                cell.append(" " + fr_number(delta, signed=True), style="green3" if better else "red1")
            cells.append(cell)
        table.add_row(*cells)
    return table


def recommendations_table(store: Store, current: sqlite3.Row, limit: int = 8) -> Table | None:
    recos = store.recommendations(current["id"])
    if not recos:
        return None
    by_priority = {p: sum(r["priority"] == p for r in recos) for p in PRIORITY_LABEL}
    summary = " · ".join(f"{n} {PRIORITY_LABEL[p].lower()}" for p, n in by_priority.items() if n)
    table = Table(
        title=f"Recommandations ouvertes : {len(recos)} ({summary})",
        title_justify="left",
        title_style="bold",
        box=box.SIMPLE_HEAD,
        expand=True,
    )
    table.add_column("Priorité", no_wrap=True)
    table.add_column("Zone", no_wrap=True)
    table.add_column("Action recommandée", ratio=1)
    for reco in recos[:limit]:
        style = "bold red1" if reco["priority"] == "haute" else ""
        table.add_row(Text(PRIORITY_LABEL[reco["priority"]], style=style), reco["zone_title"], reco["text"])
    if len(recos) > limit:
        table.add_row("", "", Text(f"… et {len(recos) - limit} autre(s) dans le rapport", "grey50"))
    return table


def progress(store: Store, current: sqlite3.Row, previous: sqlite3.Row | None) -> Panel | None:
    if previous is None:
        return None
    before = {row["check_id"]: row["status"] for row in store.items(previous["id"])}
    now = store.items(current["id"])
    fixed = [row for row in now if before.get(row["check_id"]) in ("watch", "fix") and row["status"] == "ok"]
    new_issues = [row for row in now if row["status"] == "fix" and before.get(row["check_id"]) != "fix"]
    lines = Text.assemble(
        (f"{len(fixed)} point(s) corrigé(s)", "green3"),
        " · ",
        (f"{len(new_issues)} nouveau(x) point(s) à corriger", "red1" if new_issues else "grey50"),
    )
    for row in fixed[:6]:
        lines.append(f"\n  {DOT} ", style=STYLE["ok"])
        lines.append(f"{row['zone_title']} · {row['label']}")
    if len(fixed) > 6:
        lines.append(f"\n  … et {len(fixed) - 6} autre(s)", style="grey50")
    return Panel(
        lines, title=f"Depuis la visite du {french_date(previous['date'])}", title_align="left", border_style="grey50"
    )


def history_table(recent: list[sqlite3.Row]) -> Table:
    table = Table(
        title="Historique des visites", title_justify="left", title_style="bold", box=box.SIMPLE_HEAD, expand=True
    )
    table.add_column("Date")
    table.add_column("État général")
    for status, header_text in (("ok", "Bon"), ("watch", "À surv."), ("fix", "À corr."), ("todo", "Non vér.")):
        table.add_column(Text(header_text, style=STYLE[status]), justify="right")
    for visit in reversed(recent):
        table.add_row(
            french_date(visit["date"]),
            status_text(visit["overall"]),
            str(visit["n_ok"]),
            str(visit["n_watch"]),
            str(visit["n_fix"]),
            str(visit["n_todo"]),
        )
    return table


def export(renderable: RenderableType, path: Path, width: int = 100, title: str = "visit-it-pro") -> Path:
    """Save the dashboard as .svg (terminal snapshot, used in reports) or .html."""
    console = Console(record=True, width=width, file=io.StringIO(), force_terminal=True, color_system="truecolor")
    console.print(renderable)
    if path.suffix.lower() == ".html":
        path.write_text(console.export_html(inline_styles=True), encoding="utf-8")
        return path
    svg = console.export_svg(title=title)
    # Rich links a web font; use local monospace fonts so the snapshot renders offline.
    svg = FONT_FACE_RE.sub("", svg).replace("Fira Code", LOCAL_MONO.split(",")[0])
    path.write_text(svg, encoding="utf-8")
    return path
