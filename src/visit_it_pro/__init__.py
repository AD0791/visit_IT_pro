"""visit-it-pro: checklist-driven IT site visits with PDF reports, a SQLite history and a terminal dashboard."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("visit-it-pro")
except PackageNotFoundError:  # running from a source tree that is not installed
    __version__ = "0.0.0"
