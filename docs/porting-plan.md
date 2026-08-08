# Porting plan

*Status: draft v0.1 · 2026-08-07*

Source material lives in the originating project's `.claude/` directory, assumed available
as a sibling checkout at `../adguard-wallet`:

- `.claude/skills/{flutter-*,dart-*}` — the 31 informational skills (110 files)
- `.claude/rules/ast-index.md` — the ast-index search policy

Per-skill details (file census, authorship, scrub notes) live in
[source-inventory.md](source-inventory.md). Genericization rules and the known-literal
list live in [design.md](design.md#genericization). Each phase leaves the repo in a
coherent, committable state; keep the checkboxes current as work lands.

## Port procedure (applies to every skill)

1. **Copy the whole tree** into the skill's cluster (per the phase→cluster map
   below): `mkdir -p plugins/<cluster>/skills && cp -R
   ../adguard-wallet/.claude/skills/<name> plugins/<cluster>/skills/<name>` —
   including `references/`, `assets/`, `scripts/` subtrees. Never flatten a
   routed skill into a single file.

   | Phase | Cluster |
   |---|---|
   | 1 | `plugins/likbez` (core) |
   | 2 | `plugins/likbez-ui` |
   | 3 | `plugins/likbez-data` |
   | 4 | `plugins/likbez-testing` |
   | 5 | `plugins/likbez-tooling` (`ast-index` → `plugins/likbez`) |
2. **Scrub pass**: apply the skill's scrub notes from the inventory (most skills: none).
   Then check the skill individually:
   `grep -rniE "wallet|AW-[0-9]|aiguard|adguard" plugins/<cluster>/skills/<name>/` must return nothing.
3. **Frontmatter check**: `name` matches the directory (kebab-case), `description`
   present and accurate after scrubbing, `metadata.author` **preserved verbatim** where
   it exists (9 skills — see inventory).
4. **Link check**: relative links to `references/`/`assets/` files still resolve; no
   absolute paths anywhere in the tree.
5. Tick the checkbox here and commit (`feat: port <name> skill`).

## Phase 0 — skeleton

Repo scaffold, plugin manifest, marketplace file. Exact contents below — create verbatim,
then commit (`chore: repo skeleton and plugin manifest`). (Historical: these verbatim
blocks show the original single-plugin scaffold, superseded by Phase 0.5.)

- [x] `.claude-plugin/plugin.json`
- [x] `.claude-plugin/marketplace.json`
- [x] `CLAUDE.md`
- [x] `README.md`
- [x] `LICENSE` (MIT, standard text, copyright holder "Dmitry Seloustev")
- [x] `CHANGELOG.md`
- [x] `.gitignore`

`.claude-plugin/plugin.json`:

```json
{
  "name": "likbez",
  "description": "Flutter/Dart knowledge pack for Claude Code: reference and how-to skills that educate the crew — architecture, UI, navigation, data, testing, tooling.",
  "version": "0.1.0",
  "author": {
    "name": "Dmitry Seloustev",
    "email": "d.seloustev@adguard.com"
  },
  "homepage": "https://github.com/dseloustev/likbez",
  "repository": "https://github.com/dseloustev/likbez",
  "license": "MIT",
  "keywords": [
    "flutter",
    "dart",
    "knowledge",
    "reference",
    "how-to",
    "skills"
  ]
}
```

`.claude-plugin/marketplace.json`:

```json
{
  "name": "likbez",
  "owner": {
    "name": "Dmitry Seloustev",
    "email": "d.seloustev@adguard.com"
  },
  "plugins": [
    {
      "name": "likbez",
      "source": "./",
      "description": "Flutter/Dart knowledge pack: reference and how-to skills that educate the crew."
    }
  ]
}
```

`CLAUDE.md`:

```markdown
# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

**Likbez** — a Claude Code plugin packaging a Flutter/Dart knowledge pack: 31 reference
and how-to skills plus the `ast-index` search policy. Companion to
[artel](https://github.com/dseloustev/artel) (the workflow plugin): the crew works,
likbez educates it. This repo is both the plugin and its own single-plugin marketplace
(`.claude-plugin/marketplace.json`), installable straight from GitHub.

Read these before making changes:

- [docs/design.md](docs/design.md) — architecture, genericization rules, attribution
  policy, decision log. **Record notable decisions in its decision log.**
- [docs/porting-plan.md](docs/porting-plan.md) — phased plan. Keep checkboxes current.
- [docs/source-inventory.md](docs/source-inventory.md) — per-skill source paths, file
  census, and scrub notes.

## Source material

The skills originate from a **sibling checkout** of the source project (private Flutter
repo), normally at `../adguard-wallet`: `.claude/skills/{flutter-*,dart-*}` and
`.claude/rules/ast-index.md`.

When porting, **genericize** — never copy project literals (wallet paths, launch flags,
`make` targets, project names). The complete known-literal list is in design.md. After
any skill change, the scrub gate must pass:
`grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard" skills/` → no hits.

## Conventions

- Plugin layout: `.claude-plugin/plugin.json` (manifest), `skills/<name>/SKILL.md` with
  `references/`, `assets/`, `scripts/` subtrees preserved. Installed skills surface as
  `/likbez:<name>`.
- Skills are **knowledge, not process** — no agents, no hooks, no orchestration, no host
  state, no config. If a skill seems to need any of those, stop and record a decision.
- Preserve `metadata.author` frontmatter verbatim — 9 skills carry third-party
  attribution (see design.md, "Attribution and licensing").
- All docs and commit messages in English. No absolute paths — repo-relative paths or
  the `../adguard-wallet` / `../artel` sibling convention only.
- Commits: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`). Subject line only,
  no trailers.
- Versioning: semver; keep `CHANGELOG.md` and `.claude-plugin/plugin.json` `version` in
  sync.

## Publishing

Repo home: `https://github.com/dseloustev/likbez` (corporate account, **private until
the third-party licensing question in design.md is resolved**). `gh` operations need the
corporate profile: `GH_CONFIG_DIR=~/.config/gh-adguard gh …`. Git identity for commits
here is the corporate one (`d.seloustev@adguard.com`, set in local git config).

## Testing a change

Local smoke test: `/plugin marketplace add <path-to-this-repo>` then
`/plugin install likbez@likbez`; confirm skills appear under the `likbez:` namespace and
a routed skill (e.g. `/likbez:flutter-drift`) can read its own `references/` files.
```

`README.md`:

```markdown
# likbez

A Claude Code plugin: a Flutter/Dart knowledge pack of 32 reference and how-to skills —
architecture, UI and layout, navigation, networking, localization, persistence, testing,
runtime debugging, language idiom, and the `ast-index` code-search policy.

Companion to [artel](https://github.com/dseloustev/artel), the spec-driven autonomous
feature-development workflow plugin. The names are an era-matched pair: an *artel* is a
workers' cooperative; *likbez* was the literacy campaign that educated it. **The crew
works; likbez educates it.**

## Install

    /plugin marketplace add dseloustev/likbez
    /plugin install likbez@likbez

Skills surface under the `likbez:` namespace, e.g. `/likbez:flutter-architecture`.

## What's inside

<!-- Generate this catalog from docs/source-inventory.md cluster headings once skills
     land: one table per cluster (Architecture & conventions, UI & layout, Navigation,
     Networking & serialization, Localization, Persistence, Testing & quality,
     Runtime & debugging, Language & tooling, Search policy), columns: skill, one-line
     purpose. -->

## License

MIT. Nine skills carry third-party author attribution in their frontmatter — see
[docs/design.md](docs/design.md) "Attribution and licensing".
```

`CHANGELOG.md`:

```markdown
# Changelog

All notable changes to this project will be documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[semver](https://semver.org/).

## [Unreleased]
```

`.gitignore`:

```
.DS_Store
```

## Phase 0.5 — cluster restructure

Done 2026-08-08 (see docs/superpowers/specs/2026-08-07-cluster-split-advisor-upstream-sync-design.md):

- [x] Five plugin manifests under `plugins/<name>/.claude-plugin/plugin.json`
      (`likbez`, `likbez-ui`, `likbez-data`, `likbez-testing`, `likbez-tooling`),
      lockstep version 0.1.0; root manifest removed.
- [x] `marketplace.json` rewritten to five entries with `./plugins/<name>` sources.
- [x] CLAUDE.md, README.md, design.md, and this plan retargeted to the cluster
      layout; scrub gate now scoped to `plugins/`.

## Phase 1 — architecture & conventions (→ plugins/likbez/skills/)

The only phase with real editorial work: `flutter-conventions` is the wallet's checklist
and must be rewritten as a generic Flutter checklist (scrub notes in the inventory and
design.md's known-literal table).

- [x] Port `flutter-architecture` (5 refs, 3 assets; author: MADTeacher — preserve).
- [x] Port `flutter-apply-architecture-best-practices` (single-file).
- [x] Port + genericize `flutter-conventions` (SKILL.md + checklist.md): retitle
      "Flutter convention checklist"; generalize the key-material / locker-path /
      `mainAccount` items to stack-neutral security guidance. (Also scrubbed literals
      the known-literal scan missed — `aw_api.json`, `make` targets, `verify`-gate
      references; recorded in design.md's known-literal table.)

## Phase 2 — UI, layout, navigation (→ plugins/likbez-ui/skills/)

- [x] Port `flutter-adaptive-ui` (6 refs, 2 assets; MADTeacher).
- [x] Port `flutter-build-responsive-layout` (single-file).
- [x] Port `flutter-fix-layout-issues` (single-file).
- [x] Port `flutter-animations` (6 refs, 4 assets; MADTeacher).
- [x] Port `flutter-add-widget-preview` (single-file).
- [x] Port `flutter-duit-bdui` (4 refs).
- [x] Port `flutter-navigation` (4 refs, 4 assets; MADTeacher).
- [x] Port `flutter-setup-declarative-routing` (single-file).

## Phase 3 — data: networking, serialization, localization, persistence (→ plugins/likbez-data/skills/)

- [x] Port `flutter-networking` (5 refs, 7 assets, 1 script; MADTeacher).
- [x] Port `flutter-use-http-package` (single-file).
- [x] Port `flutter-implement-json-serialization` (single-file).
- [x] Port `flutter-internationalization` (3 refs, 2 assets; MADTeacher).
- [x] Port `flutter-setup-localization` (single-file).
- [x] Port `flutter-drift` (7 refs; MADTeacher).
- [x] Port `dart-drift` (7 refs, 1 script; MADTeacher).

## Phase 4 — testing & quality (→ plugins/likbez-testing/skills/)

- [x] Port `flutter-testing` (6 refs, 1 script; MADTeacher).
- [x] Port `flutter-add-widget-test` (single-file).
- [x] Port `flutter-add-integration-test` (single-file).
- [x] Port `dart-add-unit-test` (single-file).
- [x] Port `dart-generate-test-mocks` (single-file).
- [x] Port `dart-collect-coverage` (single-file).
- [x] Port `dart-migrate-to-checks-package` (single-file).
- [x] Port `dart-run-static-analysis` (single-file).

## Phase 5 — runtime, tooling, ast-index (→ plugins/likbez-tooling/skills/, ast-index → plugins/likbez/skills/)

- [x] Port + genericize `flutter-runtime` (single-file): conditionalize the
      `--dart-define-from-file` line (design.md known-literal table).
- [x] Port `dart-fix-runtime-errors` (single-file).
- [x] Port `dart-use-pattern-matching` (single-file).
- [x] Port `dart-build-cli-app` (single-file).
- [x] Port `dart-resolve-package-conflicts` (single-file).
- [ ] Port + genericize `../adguard-wallet/.claude/rules/ast-index.md` →
      `plugins/likbez/skills/ast-index/SKILL.md`: add frontmatter (`name: ast-index`, description
      covering "mandatory-first code search policy + subagent prompt block"), replace
      `make g` / `make codegen` with "your project's codegen command". Keep the verbatim
      subagent block, read rules, scoping examples, and empty-result triage intact.

## Phase 5.5 — advisor & sync infrastructure

Designed in docs/superpowers/specs/2026-08-07-cluster-split-advisor-upstream-sync-design.md.

- [x] `project-setup` advisor skill in `plugins/likbez/skills/project-setup/`.
- [x] `docs/upstreams.md` registry (per-skill upstream, path, last-synced SHA, notes).
- [x] `upstream-sync` dev skill in `.claude/skills/upstream-sync/` (repo-local, not shipped).
- [x] `THIRD-PARTY-NOTICES.md` with the MIT and BSD-3 notices, verbatim from upstream LICENSE files.
- [ ] Baseline reconciliation: first `upstream-sync` run after Phases 1–5 —
      content-diff every skill against upstream HEAD, record starting SHAs in
      the registry.

## Phase 6 — publish

- [ ] Run the scrub gate over the full tree (design.md) — `CLEAN` required. Also
      `grep -rn "/Users/" plugins/` → empty.
- [ ] Local marketplace smoke test: `/plugin marketplace add <path>` +
      `/plugin install likbez@likbez`; run `/likbez:project-setup` on a sample
      Flutter project (sane recommendations); install one recommended cluster;
      spot-check one routed skill (`/likbez-data:flutter-drift` reads its
      `references/`), one single-file skill, and `/likbez:ast-index`.
- [ ] Fill README's skill catalog: one table per plugin.
- [ ] Verify `THIRD-PARTY-NOTICES.md` matches the upstream LICENSE files
      (licensing resolved 2026-08-07 — see design.md decision log). Repo may go
      public once verified.
- [ ] Create `dseloustev/likbez` (private) with the corporate profile
      (`GH_CONFIG_DIR=~/.config/gh-adguard gh repo create …`), push, verify the install
      path from GitHub.
- [ ] Update CHANGELOG (`0.1.0` entry), confirm plugin.json version matches, tag
      `v0.1.0`.

## Source → plugin map

| Source (`../adguard-wallet/.claude/…`) | Likbez | Action |
|---|---|---|
| `skills/{flutter-architecture,flutter-apply-architecture-best-practices}` | `plugins/likbez/skills/` | copy (Phase 1) |
| `skills/flutter-conventions` | `plugins/likbez/skills/` | port + genericize checklist (Phase 1) |
| `skills/{flutter-adaptive-ui,flutter-build-responsive-layout,flutter-fix-layout-issues,flutter-animations,flutter-add-widget-preview,flutter-duit-bdui,flutter-navigation,flutter-setup-declarative-routing}` | `plugins/likbez-ui/skills/` | copy (Phase 2) |
| `skills/{flutter-networking,flutter-use-http-package,flutter-implement-json-serialization,flutter-internationalization,flutter-setup-localization,flutter-drift,dart-drift}` | `plugins/likbez-data/skills/` | copy (Phase 3) |
| `skills/{flutter-testing,flutter-add-widget-test,flutter-add-integration-test,dart-add-unit-test,dart-generate-test-mocks,dart-collect-coverage,dart-migrate-to-checks-package,dart-run-static-analysis}` | `plugins/likbez-testing/skills/` | copy (Phase 4) |
| `skills/flutter-runtime` | `plugins/likbez-tooling/skills/` | port + conditionalize launch note (Phase 5) |
| `skills/{dart-fix-runtime-errors,dart-use-pattern-matching,dart-build-cli-app,dart-resolve-package-conflicts}` | `plugins/likbez-tooling/skills/` | copy (Phase 5) |
| `rules/ast-index.md` | `plugins/likbez/skills/ast-index/` | port + frontmatter + genericize codegen refs (Phase 5) |
| everything else in `.claude/` (workflow skills, agents, hooks, contracts, operator docs) | — | out of scope: artel's domain (or already ported there) |
