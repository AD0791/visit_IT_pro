# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow
[Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-09-27

First release.

### Added

- `visit-it-pro init`: turn a client folder into a workspace (`visit-it-pro.toml` + `visits/`).
- `visit-it-pro new`: generate a visit checklist (Markdown, French) from the office's list of computers:
  26 office, network and backup checkpoints plus 16 per desktop and 17 per laptop, each with a
  how-to-check hint using built-in Windows tools.
- `visit-it-pro check`: progress per zone and pre-send warnings, without writing anything.
- `visit-it-pro report`: French report as Markdown and A4 PDF (pandoc + headless Chrome/Chromium/Edge),
  with dashboard, work done, prioritised recommendations, key measurements and appendices.
- SQLite store (`visit-it-pro.db`): every saved visit with zones, checkpoints, numeric values,
  actions, recommendations, photos and inventory; `visit-it-pro save` and `visit-it-pro list`.
- `visit-it-pro dashboard`: Rich terminal dashboard (zone history, trends with sparklines,
  open recommendations, progress since the previous visit, visit history), exportable as SVG
  or HTML and inserted into the report as a snapshot.
- `visit-it-pro templates`: copy the built-in templates into the workspace to customise them.
- Demo workspace (`examples/demo`, fictional office) used by the tests and the README.
