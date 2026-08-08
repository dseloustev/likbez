# Changelog

All notable changes to this project will be documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[semver](https://semver.org/).

## [Unreleased]

### Added

- All 32 knowledge skills ported from the source project across the five
  cluster plugins (Phases 1–5 of the porting plan): 3 core (plus `ast-index`
  from the search-policy doc), 8 UI, 7 data, 8 testing, 5 tooling.
- `project-setup` advisor skill (core): recommends and enables likbez
  clusters per project.
- `docs/upstreams.md`: per-skill upstream registry (sync state + provenance).
- `upstream-sync` repo-local dev skill for folding upstream skill changes in.
- `THIRD-PARTY-NOTICES.md` with the upstream MIT and BSD-3 license texts.

### Changed

- Restructured into a five-plugin marketplace (`likbez`, `likbez-ui`,
  `likbez-data`, `likbez-testing`, `likbez-tooling`) with lockstep versioning.
- Baseline upstream reconciliation recorded in `docs/upstreams.md`: starting
  SHAs for all 32 tracked skills; `metadata.model` kept as vendored (upstream
  retargeted to Gemini); `dart-migrate-to-checks-package` upstream rewrite
  noted as pending adoption. No shipped skill content changed.
