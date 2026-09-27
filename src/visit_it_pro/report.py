"""Render a parsed visit as the French Markdown report."""

from __future__ import annotations

import datetime as dt
import re
from collections.abc import Callable

from .config import Workspace
from .model import BADGE, EMOJI, PRIORITIES, PRIORITY_LABEL, Visit, plain

# Key-measurements table: item-id suffix -> column header (computer zones only).
MEASURES = {
    "espace": "Espace libre C:",
    "disque": "Disque",
    "stabilite": "Stabilité",
    "demarrage": "Démarrage",
    "internet": "Internet",
    "batterie": "Batterie",
}
NETWORK_MEASURES = {"debit": "débit mesuré", "stabilite": "stabilité"}
MONTHS = (
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
)
DASHBOARD_FILE = "tableau-de-bord.svg"


def french_date(value: str) -> str:
    try:
        date = dt.date.fromisoformat(value.strip())
    except ValueError:
        return value
    day = "1er" if date.day == 1 else str(date.day)
    return f"{day} {MONTHS[date.month - 1]} {date.year}"


def cell(text: str) -> str:
    return text.replace("|", "\\|")


def table(headers: list[str], rows: list[list[str]], widths: list[int], align: str = "") -> str:
    """Pipe table; dash counts set pandoc's relative column widths, 'c' in align centres."""
    rule = ["-" * w if align[k : k + 1] != "c" else ":" + "-" * (w - 2) + ":" for k, w in enumerate(widths)]
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(rule) + "|"]
    lines += ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def office_name(visit: Visit, ws: Workspace) -> str:
    return visit.meta.get("office") or ws.office


def footer_text(visit: Visit, ws: Workspace) -> str:
    date = french_date(visit.meta.get("date", ""))
    return f"{office_name(visit, ws)} — Bilan informatique du {date} — Confidentiel"


def render_report(
    visit: Visit, ws: Workspace, resource: Callable[[str], str] = lambda p: p, dashboard: str | None = None
) -> str:
    """The report as Markdown. `resource` maps photo/image paths (relative to the visit folder);
    `dashboard` is the dashboard image to include, if any."""
    meta, zones, items = visit.meta, visit.zones, visit.items
    office = office_name(visit, ws)
    who = meta.get("technician") or ws.technician.get("name", "")
    out = [f"# Bilan informatique — {office}", ""]

    header = [f"**Date de la visite :** {french_date(meta.get('date', ''))}"]
    hours = " – ".join(v for v in (meta.get("arrival", ""), meta.get("departure", "")) if v)
    if hours:
        header[0] += f" ({hours})"
    if who:
        header.append(f"**Intervenant :** {who}")
    if meta.get("attendees"):
        header.append(f"**Personnes présentes :** {meta['attendees']}")
    if meta.get("next_visit"):
        header.append(f"**Prochaine visite :** {french_date(meta['next_visit'])}")
    out += ["\\\n".join(header), ""]

    # Overall status and the hand-written summary.
    out += [f"## État général : {BADGE[visit.overall]}", ""]
    counts = [f"{n} {BADGE[key]}" for key, n in visit.counts().items() if n]
    out += [f"{len(items)} points de contrôle : " + " · ".join(counts) + ".", ""]
    out += [visit.summary or "_Synthèse à rédiger._", ""]

    # Dashboard.
    show_todo = any(item.status == "todo" for item in items)
    headers = ["Zone", "État", "🟢", "🟠", "🔴"] + (["⚪"] if show_todo else [])
    rows = []
    for zone in zones:
        row = [zone.title, BADGE[zone.status]] + [str(zone.count(s)) for s in ("ok", "watch", "fix")]
        rows.append(row + ([str(zone.count("todo"))] if show_todo else []))
    out += [
        "## Tableau de bord",
        "",
        table(headers, rows, [40, 24, 7, 7, 7, 7][: len(headers)], "llcccc"),
        "",
        "Légende : 🟢 Bon · 🟠 À surveiller · 🔴 À corriger · ⚪ Non vérifié · ➖ Sans objet. "
        "L'état d'une zone est celui de son point le moins bon.",
        "",
    ]

    # Work done on site.
    done = [
        f"- **{zone.title}** · {item.label} : {text}" for zone in zones for item in zone.items for text in item.done
    ]
    out += ["## Interventions réalisées pendant la visite", ""]
    out += (done or ["_Aucune intervention lors de cette visite._"]) + [""]

    # Recommendations, highest priority first, then checklist order.
    recos = [
        (PRIORITIES.index(priority), z, i, priority, zone, item, text)
        for z, zone in enumerate(zones)
        for i, item in enumerate(zone.items)
        for priority, text in item.recos
    ]
    out += ["## Recommandations", ""]
    if recos:
        rows = []
        for *_, priority, zone, item, text in sorted(recos, key=lambda r: r[:3]):
            finding = f"{EMOJI[item.status]} {item.label}" + (f" : {item.observation}" if item.observation else "")
            label = PRIORITY_LABEL[priority]
            rows.append([f"**{label}**" if priority == "haute" else label, zone.title, finding, text])
        out += [
            "Classées par priorité — **Haute** : dès que possible · **Moyenne** : dans les "
            "prochaines semaines · **Basse** : à planifier.",
            "",
            table(["Priorité", "Zone", "Constat", "Action recommandée"], rows, [10, 18, 36, 36]),
            "",
        ]
    else:
        out += ["_Aucune recommandation._", ""]

    # Key measurements: one row per computer, plus the internet line.
    rows = []
    for zone in zones:
        if not zone.is_computer:
            continue
        by_suffix = {item.suffix: item for item in zone.items}
        row = [zone.title]
        for suffix in MEASURES:
            item = by_suffix.get(suffix)
            row.append("—" if item is None else f"{EMOJI[item.status]} {item.value}".strip())
        rows.append(row)
    network = []
    for zone in zones:
        if not any(item.id.startswith("NET-") for item in zone.items):
            continue
        contract = next((v for k, v in zone.fiche if plain(k).startswith("debit contractuel") and v), "")
        if contract:
            network.append(f"débit contractuel : {contract}")
        network += [
            f"{NETWORK_MEASURES[item.suffix]} : {EMOJI[item.status]} {item.value}"
            for item in zone.items
            if item.suffix in NETWORK_MEASURES and item.value
        ]
    if rows or network:
        out += ["## Mesures clés", ""]
        if rows:
            out += [table(["Poste", *MEASURES.values()], rows, [15, 11, 15, 11, 11, 26, 11]), ""]
        if network:
            out += ["**Connexion Internet** — " + " · ".join(network) + ".", ""]
        out += ["_Ces valeurs servent de référence pour suivre l'évolution d'une visite à l'autre._", ""]

    # Terminal dashboard snapshot (history of saved visits).
    if dashboard:
        out += [
            "## Suivi dans le temps",
            "",
            "Tableau de bord établi à partir de l'historique des visites enregistrées.",
            "",
            '<div class="tableau-de-bord">',
            "",
            f"![Tableau de bord de suivi](<{resource(dashboard)}>)",
            "",
            "</div>",
            "",
        ]

    # Appendix A: inventory (fiche lines that were filled in).
    out += ["## Annexe A — Inventaire du parc", ""]
    inventory = False
    for zone in zones:
        entries = [[re.sub(r"\s+\([^)]*\)$", "", k), v] for k, v in zone.fiche if v]
        if entries:
            inventory = True
            out += [f"### {zone.title}", "", table(["Élément", "Détail"], entries, [30, 70]), ""]
    if not inventory:
        out += ["_Inventaire à compléter._", ""]

    # Appendix B: every checkpoint.
    out += ["## Annexe B — Détail des contrôles", ""]
    for zone in zones:
        rows = [[item.label, BADGE[item.status], item.observation] for item in zone.items]
        out += [f"### {zone.title}", "", table(["Point de contrôle", "État", "Observation"], rows, [34, 18, 48]), ""]

    # Appendix C: photos.
    photos = [(zone, item, p) for zone in zones for item in zone.items for p in item.photos]
    if photos:
        out += ["## Annexe C — Photos", ""]
        for zone, item, p in photos:
            out += [f"![{zone.title} · {item.label}](<{resource(p)}>)", ""]

    # Phone and email belong to the configured technician only.
    contact = [who]
    if who == ws.technician.get("name", ""):
        contact += [ws.technician.get("phone", ""), ws.technician.get("email", "")]
    contact_text = " · ".join(v for v in contact if v)
    out += [
        "---",
        "",
        f"_Document confidentiel établi pour {office}" + (f" par {contact_text}" if contact_text else "") + "._",
        "",
    ]
    return "\n".join(out)
