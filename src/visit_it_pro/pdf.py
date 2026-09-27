"""Markdown -> HTML (pandoc) -> PDF (headless Chrome, Chromium or Edge)."""

from __future__ import annotations

import os
import re
import shutil
import signal
import subprocess
import tempfile
import time
from collections.abc import Callable
from pathlib import Path

CHROME_ENV = "VISIT_IT_PRO_CHROME"
CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
)
CHROME_NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge")


class PdfError(Exception):
    """The PDF could not be produced; the message says why and what to do."""


def find_chrome() -> str | None:
    if configured := os.environ.get(CHROME_ENV):
        return configured
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    for name in CHROME_NAMES:
        if found := shutil.which(name):
            return found
    return None


def web_image(src: Path, tmp: Path) -> str:
    """Path to use in the PDF: SVGs as they are; photos as JPEG ≤ 1600 px via macOS `sips`
    (which also converts iPhone HEIC), or the original when `sips` is not available."""
    sips = shutil.which("sips")
    if src.suffix.lower() == ".svg" or not sips:
        return str(src.resolve())
    out_dir = tmp / "photos"
    out_dir.mkdir(exist_ok=True)
    dst = out_dir / f"{len(list(out_dir.iterdir())):02d}-{src.stem}.jpg"
    info = subprocess.run(
        [sips, "-g", "pixelWidth", "-g", "pixelHeight", str(src)], capture_output=True, text=True
    ).stdout
    sizes = [int(v) for v in re.findall(r"pixel(?:Width|Height): (\d+)", info)]
    resize = ["-Z", "1600"] if sizes and max(sizes) > 1600 else []
    result = subprocess.run(
        [sips, "-s", "format", "jpeg", "-s", "formatOptions", "80", *resize, str(src), "--out", str(dst)],
        capture_output=True,
    )
    return str(dst) if result.returncode == 0 and dst.is_file() else str(src.resolve())


def build_pdf(
    render: Callable[[Callable[[str], str]], str], visit_dir: Path, pdf_path: Path, footer: str, title: str, css: str
) -> Path:
    """Build the PDF. `render(resource)` returns the report Markdown with image paths mapped by `resource`.
    Returns the PDF path, or the HTML path when no browser is available (print it by hand)."""
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise PdfError(
            "pandoc not found: install it from https://pandoc.org/installing.html (macOS: brew install pandoc)"
        )
    with tempfile.TemporaryDirectory(prefix="visit-it-pro-", ignore_cleanup_errors=True) as tmp_name:
        tmp = Path(tmp_name)
        (tmp / "report.md").write_text(render(lambda p: web_image(visit_dir / p, tmp)), encoding="utf-8")
        css = css.replace("__PIED__", footer.replace("\\", "\\\\").replace('"', '\\"'))
        (tmp / "report.css").write_text(css, encoding="utf-8")
        result = subprocess.run(
            [
                pandoc,
                "report.md",
                "--from",
                "markdown",
                "--to",
                "html5",
                "--standalone",
                "--embed-resources",
                "--css",
                "report.css",
                "--columns",
                "20",
                "--metadata",
                f"pagetitle={title}",
                "--metadata",
                "lang=fr",
                "--output",
                "report.html",
            ],
            cwd=tmp,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise PdfError(f"pandoc failed: {result.stderr.strip()}")
        html = tmp / "report.html"
        chrome = find_chrome()
        if not chrome:
            fallback = pdf_path.with_suffix(".html")
            shutil.copyfile(html, fallback)
            return fallback
        print_pdf(chrome, html, pdf_path, tmp)
    return pdf_path


def print_pdf(chrome: str, html: Path, pdf_path: Path, tmp: Path, timeout: float = 90) -> None:
    """Print html to pdf_path with a headless Chromium-based browser.

    Chrome writes the PDF but may never exit on its own (seen with Chrome 153 on macOS), and
    subprocess timeouts did not fire reliably, so wait for its "written to file" log line and
    then stop its whole process group. The log goes to a file: a pipe would be held open by
    Chrome's helper processes.
    """
    log_path = tmp / "chrome.log"
    pdf_path.unlink(missing_ok=True)
    args = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--use-mock-keychain",
        "--no-pdf-header-footer",
        f"--user-data-dir={tmp / 'chrome-profile'}",
        f"--print-to-pdf={pdf_path}",
        html.as_uri(),
    ]
    with log_path.open("wb") as log:
        if os.name == "nt":
            proc = subprocess.Popen(args, stdout=log, stderr=log, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            proc = subprocess.Popen(args, stdout=log, stderr=log, start_new_session=True)
    deadline = time.monotonic() + timeout
    try:
        while time.monotonic() < deadline and proc.poll() is None:
            if b"written to file" in log_path.read_bytes():
                break
            time.sleep(0.2)
    finally:
        stop_browser(proc)
    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        tail = log_path.read_text(errors="replace").strip().splitlines()[-5:]
        raise PdfError("the browser did not produce the PDF. Its log ends with:\n  " + "\n  ".join(tail))


def stop_browser(proc: subprocess.Popen) -> None:
    """Stop the browser and its helpers, waiting until the whole group is gone so the
    temporary profile can be deleted cleanly."""
    if os.name == "nt":
        if proc.poll() is None:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        return
    for sig in (signal.SIGTERM, signal.SIGKILL):
        if not group_alive(proc):
            return
        try:
            os.killpg(proc.pid, sig)
        except ProcessLookupError:
            return
        for _ in range(50):
            if not group_alive(proc):
                return
            time.sleep(0.1)


def group_alive(proc: subprocess.Popen) -> bool:
    """True while any process of proc's process group is still running (reaps proc itself)."""
    proc.poll()
    try:
        os.killpg(proc.pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    return True
