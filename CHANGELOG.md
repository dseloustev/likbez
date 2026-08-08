# Changelog

All notable changes to this project will be documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[semver](https://semver.org/).

## [Unreleased]

### Added

- `project-setup` advisor skill (core): recommends and enables likbez
  clusters per project.
- `docs/upstreams.md`: per-skill upstream registry (sync state + provenance).
- `upstream-sync` repo-local dev skill for folding upstream skill changes in.

### Changed

- Restructured into a five-plugin marketplace (`likbez`, `likbez-ui`,
  `likbez-data`, `likbez-testing`, `likbez-tooling`) with lockstep versioning.
