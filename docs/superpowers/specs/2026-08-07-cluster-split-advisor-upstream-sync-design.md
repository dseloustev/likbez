# Likbez: cluster split, project-setup advisor, upstream-sync — design

*Status: approved 2026-08-07 · supplements [docs/design.md](../../design.md)*

## Context

Two capabilities were requested on top of the founding design:

1. **A skill updater** that tracks the upstream skill repositories and folds their
   changes back into likbez.
2. **A project-aware recommender**: users install likbez on different projects, and
   installing all 32 skills rarely makes sense — a skill should analyze the project,
   propose the relevant subset, ask what technologies are planned, and extend the
   proposal accordingly.

Research findings that shaped the design (verified 2026-08-07):

- Claude Code offers **no per-skill disable** — a plugin's skills are all-or-nothing,
  and every installed skill's name+description loads into context every turn
  (~2–3k tokens for 32 likbez-sized descriptions). `/doctor` flags unused skills for
  exactly this reason.
- One repo's `marketplace.json` **can define multiple plugins** sourced from
  subdirectories, and plugins **can be enabled per project** via `enabledPlugins` in the
  project's `.claude/settings.json`. Granularity therefore exists at plugin level.
- All three upstreams were located, with permissive licenses:
  - `MADTeacher/mad-agents-skills` — MIT (© 2026 Stanislav Chernyshev); the 9 attributed
    skills plus `flutter-duit-bdui`; last push 2026-05.
  - `flutter/agent-plugins` (renamed from `flutter/skills`) — BSD-3 (The Flutter
    Authors); the 10 unattributed `flutter-*` how-tos; very active.
  - `dart-lang/skills` — BSD-3 (Dart project authors); canonical home of the `dart-*`
    skills (9 of ours + 3 we don't carry); very active. `flutter/agent-plugins` carries
    copies of the `dart-*` set — those copies are ignored for sync purposes.
- Only three likbez skills are in-house: `flutter-conventions`, `flutter-runtime`,
  `ast-index`. Everything else has a public upstream.

## Approved decisions

1. **Split into 5 cluster plugins** in one marketplace, plus a `project-setup` advisor
   skill in the core plugin (chosen over: single plugin with advisory notes; split-later).
2. **Updater = repo-local dev skill** (`.claude/skills/upstream-sync/`), never shipped;
   tracks the 3 public upstreams plus `../adguard-wallet` for the in-house trio.
3. **Licensing resolved now**: add `THIRD-PARTY-NOTICES.md`, fix `flutter-duit-bdui`
   attribution during its port, mark design.md open question 1 resolved. Public release
   remains a Phase 6 call.

## 1. Repo restructure — multi-plugin marketplace

```
likbez/
├── .claude-plugin/marketplace.json      # marketplace "likbez", 5 plugin entries
├── plugins/
│   ├── likbez/                          # core — keeps the short name
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/<name>/...
│   ├── likbez-ui/
│   ├── likbez-data/
│   ├── likbez-testing/
│   └── likbez-tooling/
├── .claude/skills/upstream-sync/        # repo-local dev skill — NOT shipped
├── docs/                                # + upstreams.md registry
├── THIRD-PARTY-NOTICES.md
└── CLAUDE.md · README.md · LICENSE · CHANGELOG.md
```

Cluster contents (33 skills = 32 ported + the new advisor):

| Plugin | Skills |
|---|---|
| `likbez` (core, 5) | `project-setup` (new), `ast-index`, `flutter-conventions`, `flutter-architecture`, `flutter-apply-architecture-best-practices` |
| `likbez-ui` (8) | `flutter-adaptive-ui`, `flutter-build-responsive-layout`, `flutter-fix-layout-issues`, `flutter-animations`, `flutter-add-widget-preview`, `flutter-duit-bdui`, `flutter-navigation`, `flutter-setup-declarative-routing` |
| `likbez-data` (7) | `flutter-networking`, `flutter-use-http-package`, `flutter-implement-json-serialization`, `flutter-internationalization`, `flutter-setup-localization`, `flutter-drift`, `dart-drift` |
| `likbez-testing` (8) | `flutter-testing`, `flutter-add-widget-test`, `flutter-add-integration-test`, `dart-add-unit-test`, `dart-generate-test-mocks`, `dart-collect-coverage`, `dart-migrate-to-checks-package`, `dart-run-static-analysis` |
| `likbez-tooling` (5) | `flutter-runtime`, `dart-fix-runtime-errors`, `dart-use-pattern-matching`, `dart-build-cli-app`, `dart-resolve-package-conflicts` |

Rules:

- The root `.claude-plugin/` keeps only `marketplace.json`; each plugin carries its own
  `.claude-plugin/plugin.json`.
- **Lockstep versioning**: all five plugins share one version, bumped together; one
  CHANGELOG. First published tag stays `v0.1.0`.
- Skill namespaces: core skills surface as `/likbez:<name>`; cluster skills as
  `/likbez-ui:<name>` etc.
- Install UX: `/plugin marketplace add dseloustev/likbez` → `/plugin install
  likbez@likbez` (core) → `/likbez:project-setup` recommends the rest.
- The scrub gate becomes `grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard"
  plugins/ --exclude=plugin.json` (and `grep -rn "/Users/" plugins/` empty). CLAUDE.md, README, and
  design.md's architecture section are updated to the new layout and gate.
- Clusters align with porting phases: 1→core, 2→ui, 3→data, 4→testing, 5→tooling
  (`ast-index` lands in core during Phase 5).

## 2. `project-setup` advisor (ships in core)

Single-file how-to skill (SKILL.md, no references/) guiding this procedure:

1. **Detect** — read `pubspec.yaml`: Flutter SDK dep; `drift`/`drift_flutter`;
   `go_router`; `http`/`dio`/`retrofit`/`chopper`; `intl`/`flutter_localizations`;
   `flutter_duit`. Also: `l10n.yaml`, `test/`, `integration_test/`, `bin/` (CLI),
   `lib/` shape. Monorepos (multiple pubspecs / melos): union of detections, reported
   per package.
2. **Recommend** — a detection→cluster mapping table embedded in the skill produces the
   recommended set; present it as a table with the trigger for each recommendation
   (e.g. "`go_router` in pubspec → likbez-ui"). Baseline for any Flutter app project:
   core + `likbez-testing`; `likbez-tooling` when runtime-debugging or CLI signals
   appear; pure-Dart projects skip UI-flavored recommendations.
3. **Ask** — what technologies the user plans to add (database, deep links, BDUI,
   localization, CLI tooling, …); fold answers into the final set.
4. **Apply, with explicit consent** — offer both modes: (a) print the exact
   `/plugin install <cluster>@likbez` commands; (b) write `enabledPlugins` entries into
   the project's `.claude/settings.json`, optionally appending a short "Likbez skills in
   this project" note to the host CLAUDE.md so agents that read skills by path (e.g.
   artel's crew) know what to consult.

Guardrails: read-only until the user consents to writes; never modifies non-likbez
`enabledPlugins` entries; never disables the core plugin; if no `pubspec.yaml` exists,
say so and offer manual cluster selection. Exact dependency→cluster mapping is finalized
at implementation time; the table above is the contract's shape.

This is the **single process carve-out** in an otherwise knowledge-only plugin,
recorded in design.md's decision log.

## 3. `upstream-sync` dev skill + upstreams registry

**Registry** — `docs/upstreams.md`, one row per shipped skill:

| Column | Content |
|---|---|
| skill | plugin-relative path, e.g. `plugins/likbez-data/skills/flutter-drift` |
| upstream | repo + path, e.g. `MADTeacher/mad-agents-skills` `flutter-drift/` |
| last-synced | upstream commit SHA recorded at last sync |
| notes | genericization deltas to preserve, attribution requirements |

Upstreams: `MADTeacher/mad-agents-skills` (10 skills), `flutter/agent-plugins`
(`skills/`, 10), `dart-lang/skills` (`skills/`, 9), `../adguard-wallet`
(`.claude/skills/` + `.claude/rules/ast-index.md`, the in-house trio). The registry
doubles as the provenance table for THIRD-PARTY-NOTICES.md. Adding a future upstream is
one registry row plus its license notice.

**Skill** — `.claude/skills/upstream-sync/SKILL.md`, repo-local (dev tooling; ships
nothing). Procedure it encodes:

1. Shallow-clone (or update a cached clone of) each public upstream into the session
   scratchpad; `../adguard-wallet` is used in place.
2. Per registry row: `git diff <last-synced>..HEAD -- <path>` in the upstream; classify
   every mapped skill as unchanged / changed / removed; list upstream skills with no
   likbez counterpart as **new candidates**.
3. Present the digest to the operator (grouped: changes to apply, candidates to
   consider, removals to decide). Nothing is applied without operator approval;
   candidates are never auto-added — accepting one is a curation decision recorded in
   design.md.
4. For each accepted change: apply the upstream diff onto the likbez copy **through the
   standard port procedure** — re-genericize, preserve `metadata.author` verbatim, run
   the scrub gate and link check.
5. Record new SHAs in the registry, add a CHANGELOG entry, bump the lockstep version,
   commit.

**First run is a baseline reconciliation**: the wallet snapshot's upstream commits are
unknown, so content-diff each likbez skill against upstream HEAD, resolve differences,
and record HEAD SHAs as the baseline. Known candidates already waiting:
`dart-use-primary-constructors`, `dart-setup-ffi-assets`, `dart-use-ffigen`
(dart-lang/skills), `agents-md-generator` (MADTeacher).

Cadence: manual — run before releases or every few weeks. No scheduling in v1.

## 4. Licensing and attribution

- `THIRD-PARTY-NOTICES.md`: the MIT notice (© 2026 Stanislav Chernyshev), both BSD-3
  notices (The Flutter Authors; Dart project authors), and a pointer to the per-skill
  provenance in `docs/upstreams.md`.
- During the `flutter-duit-bdui` port: compare against MADTeacher's copy; if derived,
  add his `metadata.author` (making 10 attributed skills).
- design.md: open question 1 → resolved; README license section mentions the notices
  file. Going public stays a Phase 6 decision, now unblocked.

## 5. Impact on the porting plan

- **New Phase 0.5 — restructure**: create `plugins/` layout, five `plugin.json`
  manifests, rewritten `marketplace.json`, updated CLAUDE.md/README/design.md paths and
  scrub gate. Done **before** any skill porting so every skill is ported once, into its
  final home.
- **Phases 1–5**: content unchanged; target paths become
  `plugins/<cluster>/skills/<name>`.
- **New Phase 5.5 — advisor + sync infrastructure**: write `project-setup`,
  `docs/upstreams.md` (with baseline reconciliation as its first run),
  `.claude/skills/upstream-sync/`, `THIRD-PARTY-NOTICES.md`.
- **Phase 6**: smoke test becomes — marketplace add local path; install core + one
  cluster; `/likbez:project-setup` on a sample Flutter project produces sane
  recommendations; a routed skill reads its `references/`; scrub gate over `plugins/`.

## Error handling

- Advisor: missing/unparseable `pubspec.yaml` → report and fall back to manual
  selection; user declines writes → print-only mode; unknown dependencies → ignored
  (never block on unrecognized stack).
- Upstream-sync: unreachable upstream → skip it, report, continue with the rest; a
  recorded SHA no longer in upstream history (force-push) → fall back to content diff
  for that skill; scrub gate failure after a merge → the merge does not land.

## Out of scope (YAGNI)

- Scheduled/automated sync runs.
- Auto-adoption of new upstream skills.
- Per-skill (sub-plugin) granularity beyond the 5 clusters.
- Any config file in the shipped plugins — the advisor writes only host-project files,
  with consent.
