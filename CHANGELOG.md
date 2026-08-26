# Changelog

All notable changes to this project will be documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[semver](https://semver.org/).

## [Unreleased]

### Added

- OpenCode host support. `scripts/build_opencode.py` generates `likbez-`-prefixed skill
  directories (host glossary prepended, frontmatter remapped, attribution and
  `references/`/`assets/`/`scripts/` subtrees preserved);
  `scripts/install-opencode.sh` installs/uninstalls into `~/.config/opencode/skills/`.
  Claude Code operation is unchanged: the canonical `plugins/` tree is untouched.
  See `docs/opencode.md`.

## [0.2.0] - 2026-08-25

### Removed

- `ast-index` skill (core), in favour of the standalone `ast-index` plugin:
  it ships a command reference current with the CLI plus enforcement hooks,
  and both skills declared `name: ast-index`, so the two collided whenever
  both were installed. The one Flutter/Dart fact likbez carried alone —
  codegen emits symbols a search index cannot see until it is refreshed —
  moved to `flutter-conventions`' generated-files item; `project-setup` now
  mentions the standalone plugin as optional companion tooling. No likbez
  skill depends on it. Core drops to four skills, the pack to 32.

## [0.1.0] - 2026-08-23

### Added

- All 32 knowledge skills ported from the source project across the five
  cluster plugins (Phases 1–5 of the porting plan): 3 core (plus `ast-index`
  from the search-policy doc), 8 UI, 7 data, 8 testing, 5 tooling.
- `project-setup` advisor skill (core): recommends and enables likbez
  clusters per project.
- `docs/upstreams.md`: per-skill upstream registry (sync state + provenance).
- `upstream-sync` repo-local dev skill for folding upstream skill changes in.
- `bump-version` repo-local dev skill for cutting releases: lockstep manifest
  bump, dated CHANGELOG section, `chore(release)` commit and annotated tag.
- `THIRD-PARTY-NOTICES.md` with the upstream MIT and BSD-3 license texts.

### Changed

- Restructured into a five-plugin marketplace (`likbez`, `likbez-ui`,
  `likbez-data`, `likbez-testing`, `likbez-tooling`) with lockstep versioning.
- Baseline upstream reconciliation recorded in `docs/upstreams.md`: starting
  SHAs for all 32 tracked skills; `metadata.model` kept as vendored (upstream
  retargeted to Gemini); `dart-migrate-to-checks-package` upstream rewrite
  noted as pending adoption. No shipped skill content changed.
