"""Command-line interface: `visit-it-pro …`."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Annotated, NoReturn, Optional

import typer
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from . import __version__
from .checklist import copy_templates, count_checkpoints, create_visit, template_text
from .config import CONFIG_NAME, Workspace, WorkspaceError, is_date, load_workspace, write_config
from .dashboard import build_dashboard, export
from .model import BADGE, EMOJI, STATUS_KEYS, Visit
from .parser import load_visit
from .pdf import PdfError, build_pdf
from .report import DASHBOARD_FILE, footer_text, office_name, render_report
from .store import Store, StoreError

app = typer.Typer(
    name="visit-it-pro",
    help="Checklist-driven IT site visits: fill a Markdown checklist on site, get a PDF report, "
    "keep every visit in SQLite and follow it on a terminal dashboard.",
    no_args_is_help=True,
    rich_markup_mode="rich",
    add_completion=False,
)
console = Console()
err = Console(stderr=True)

VisitArg = Annotated[str, typer.Argument(help="Visit folder, or its date (YYYY-MM-DD) under visits/.")]


def version_callback(value: bool) -> None:
    if value:
        console.print(f"visit-it-pro {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    workspace: Annotated[
        Optional[Path],
        typer.Option(
            "--workspace",
            "-w",
            envvar="VISIT_IT_PRO_WORKSPACE",
            help=f"Client folder containing {CONFIG_NAME} (default: the current folder or a parent).",
        ),
    ] = None,
    version: Annotated[
        bool, typer.Option("--version", callback=version_callback, is_eager=True, help="Show the version and exit.")
    ] = False,
) -> None:
    ctx.obj = workspace


def fail(message: str) -> NoReturn:
    err.print(f"[bold red]Error:[/] {escape(message)}")
    raise typer.Exit(1)


def get_workspace(ctx: typer.Context) -> Workspace:
    try:
        return load_workspace(ctx.obj)
    except WorkspaceError as exc:
        fail(str(exc))


def shown(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def open_visit(ws: Workspace, ref: str) -> tuple[Path, Visit, str]:
    """Resolve, parse and check a visit; return its folder, the parsed visit and its date."""
    try:
        visit_dir = ws.visit_dir(ref)
    except WorkspaceError as exc:
        fail(str(exc))
    if not (visit_dir / "checklist.md").is_file():
        fail(f"{shown(visit_dir / 'checklist.md')} not found")
    visit = load_visit(visit_dir)
    date = visit.meta.get("date", "")
    if not is_date(date):
        if not is_date(visit_dir.name):
            fail("the checklist has no valid 'date:' (YYYY-MM-DD) in its front matter")
        date = visit_dir.name
    return visit_dir, visit, date


def print_warnings(visit: Visit) -> None:
    for warning in visit.warnings:
        console.print(f"[yellow]warning:[/] {escape(warning)}")


def status_summary(visit: Visit) -> str:
    counts = " · ".join(f"{n} {EMOJI[key]}" for key, n in visit.counts().items() if n)
    return f"{BADGE[visit.overall]} ({counts})"


@app.command()
def init(
    path: Annotated[Path, typer.Argument(help="Folder to turn into a workspace.")] = Path("."),
    office: Annotated[str, typer.Option(help="Office or client name, printed on reports.")] = "Mon client",
    technician: Annotated[str, typer.Option(help="Your name, printed on reports.")] = "",
    force: Annotated[bool, typer.Option(help=f"Overwrite an existing {CONFIG_NAME}.")] = False,
) -> None:
    """Turn a client folder into a workspace: writes visit-it-pro.toml and a visits/ folder."""
    try:
        config = write_config(path, office, technician, force)
    except WorkspaceError as exc:
        fail(str(exc))
    (path / "visits").mkdir(exist_ok=True)
    console.print(f"Created {shown(config)} and visits/")
    console.print("Next: list the client's computers in the file, then run [bold]visit-it-pro new[/].")


@app.command()
def new(
    ctx: typer.Context,
    date: Annotated[Optional[str], typer.Option(help="Visit date, YYYY-MM-DD (default: today).")] = None,
    force: Annotated[bool, typer.Option(help="Overwrite an existing checklist.")] = False,
) -> None:
    """Create visits/<date>/checklist.md (and photos/) for the next visit."""
    ws = get_workspace(ctx)
    date = date or dt.date.today().isoformat()
    if not is_date(date):
        fail(f"invalid date {date!r}: expected YYYY-MM-DD")
    try:
        checklist = create_visit(ws, date, force)
    except WorkspaceError as exc:
        fail(str(exc))
    count = count_checkpoints(checklist.read_text(encoding="utf-8"))
    console.print(f"Created {shown(checklist)} ({count} checkpoints) and photos/")
    console.print(f"After the visit: [bold]visit-it-pro report {date}[/]")


@app.command()
def check(ctx: typer.Context, visit: VisitArg) -> None:
    """Show a checklist's progress and warnings, without writing anything."""
    ws = get_workspace(ctx)
    _, parsed, date = open_visit(ws, visit)
    table = Table(title=f"Visit of {date}", title_justify="left")
    table.add_column("Zone")
    table.add_column("Checked", justify="right")
    for key in ("ok", "watch", "fix"):
        table.add_column(EMOJI[key], justify="right")
    table.add_column("Left", justify="right")
    for zone in parsed.zones:
        left = zone.count("todo")
        table.add_row(
            zone.title,
            f"{len(zone.items) - left}/{len(zone.items)}",
            str(zone.count("ok")),
            str(zone.count("watch")),
            str(zone.count("fix")),
            f"[yellow]{left}[/]" if left else "0",
        )
    console.print(table)
    print_warnings(parsed)
    console.print(f"Overall: {status_summary(parsed)}")


@app.command()
def report(
    ctx: typer.Context,
    visit: VisitArg,
    pdf: Annotated[bool, typer.Option("--pdf/--no-pdf", help="Also build the PDF (needs pandoc and Chrome).")] = True,
    save: Annotated[bool, typer.Option("--save/--no-save", help="Save the visit into the database.")] = True,
    dashboard: Annotated[
        Optional[bool],
        typer.Option(
            "--dashboard/--no-dashboard",
            help="Add the dashboard snapshot to the report (default: [report] dashboard in the config).",
        ),
    ] = None,
) -> None:
    """Build rapport-<date>.md and .pdf from a filled checklist, and save the visit."""
    ws = get_workspace(ctx)
    visit_dir, parsed, date = open_visit(ws, visit)
    office = office_name(parsed, ws)
    include_dashboard = ws.dashboard_in_report if dashboard is None else dashboard
    if include_dashboard and not save:
        console.print(
            "[yellow]note:[/] the dashboard is left out because --no-save keeps this visit out of "
            "the database it is built from"
        )
        include_dashboard = False

    outputs = []
    dashboard_file = None
    if save or include_dashboard:
        try:
            with Store(ws.db_path) as store:
                if save:
                    store.save_visit(parsed, date, visit_dir / "checklist.md")
                if include_dashboard:
                    export(
                        build_dashboard(store, office, date),
                        visit_dir / DASHBOARD_FILE,
                        title=f"visit-it-pro · {office}",
                    )
                    dashboard_file = DASHBOARD_FILE
                    outputs.append(visit_dir / DASHBOARD_FILE)
        except StoreError as exc:
            fail(str(exc))

    md_path = visit_dir / f"rapport-{date}.md"
    md_path.write_text(render_report(parsed, ws, dashboard=dashboard_file), encoding="utf-8")
    outputs.insert(0, md_path)

    pdf_error = None
    if pdf:
        try:
            produced = build_pdf(
                lambda resource: render_report(parsed, ws, resource, dashboard_file),
                visit_dir,
                visit_dir / f"rapport-{date}.pdf",
                footer_text(parsed, ws),
                f"Bilan informatique — {office}",
                template_text(ws, "report.css"),
            )
            outputs.append(produced)
            if produced.suffix == ".html":
                console.print(
                    "[yellow]note:[/] no Chrome, Chromium or Edge found: open the .html file in a "
                    "browser and print it to PDF (or set VISIT_IT_PRO_CHROME)"
                )
        except PdfError as exc:
            pdf_error = str(exc)

    print_warnings(parsed)
    console.print(f"Overall: {status_summary(parsed)}")
    if save:
        console.print(f"Saved in {shown(ws.db_path)}")
    for path in outputs:
        console.print(f"Wrote {shown(path)}")
    if pdf_error:
        fail(f"PDF not built: {pdf_error}")


@app.command()
def save(ctx: typer.Context, visit: VisitArg) -> None:
    """Save a visit into the database without building its report (e.g. to import past visits)."""
    ws = get_workspace(ctx)
    visit_dir, parsed, date = open_visit(ws, visit)
    try:
        with Store(ws.db_path) as store:
            store.save_visit(parsed, date, visit_dir / "checklist.md")
    except StoreError as exc:
        fail(str(exc))
    print_warnings(parsed)
    console.print(f"Saved the visit of {date} in {shown(ws.db_path)}: {status_summary(parsed)}")


@app.command("list")
def list_visits(ctx: typer.Context) -> None:
    """List the visits saved in the database."""
    ws = get_workspace(ctx)
    with Store(ws.db_path) as store:
        visits = store.visits()
        recos = {v["id"]: len(store.recommendations(v["id"])) for v in visits}
    if not visits:
        console.print("No visit saved yet: run [bold]visit-it-pro report <visit>[/] after a visit.")
        return
    table = Table(title=f"{ws.office}: {len(visits)} visit(s)", title_justify="left")
    table.add_column("Date", no_wrap=True)
    table.add_column("Overall", no_wrap=True)
    for key in STATUS_KEYS[:4]:
        table.add_column(EMOJI[key], justify="right")
    table.add_column("Recos", justify="right")
    table.add_column("Technician")
    for v in visits:
        table.add_row(
            v["date"],
            BADGE[v["overall"]],
            str(v["n_ok"]),
            str(v["n_watch"]),
            str(v["n_fix"]),
            str(v["n_todo"]),
            str(recos[v["id"]]),
            v["technician"],
        )
    console.print(table)


@app.command("dashboard")
def show_dashboard(
    ctx: typer.Context,
    date: Annotated[
        Optional[str], typer.Option(help="Show the dashboard as of this visit date (default: latest).")
    ] = None,
    export_to: Annotated[
        Optional[Path], typer.Option("--export", help="Also save it as .svg (terminal snapshot) or .html.")
    ] = None,
    width: Annotated[int, typer.Option(help="Width in characters of the exported file.")] = 100,
) -> None:
    """Show the terminal dashboard: zone history, trends, open recommendations, progress."""
    ws = get_workspace(ctx)
    if date and not is_date(date):
        fail(f"invalid date {date!r}: expected YYYY-MM-DD")
    with Store(ws.db_path) as store:
        renderable = build_dashboard(store, ws.office, date)
    console.print(renderable)
    if export_to:
        export(renderable, export_to, width, title=f"visit-it-pro · {ws.office}")
        console.print(f"Wrote {shown(export_to)}")


@app.command()
def templates(
    ctx: typer.Context,
    force: Annotated[bool, typer.Option(help="Overwrite templates already copied.")] = False,
) -> None:
    """Copy the built-in templates into <workspace>/templates/ so you can customise them."""
    ws = get_workspace(ctx)
    written = copy_templates(ws, force)
    for path in written:
        console.print(f"Wrote {shown(path)}")
    if not written:
        console.print("Nothing copied: the templates are already there (add --force to overwrite).")
    else:
        console.print("Edit them freely: files in templates/ take precedence over the built-in ones.")
