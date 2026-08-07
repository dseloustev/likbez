# Source inventory — the likbez skill set

*Adapted 2026-08-07 from artel's `docs/source-inventory-informational.md` (compiled
2026-08-01 from the sibling checkout `../adguard-wallet/.claude/`), extended with per-skill
file census, authorship, target phase, and scrub notes.*

Everything here is **knowledge, not process**: reference and how-to skills an agent
consults *while* developing. None of them orchestrate agents or drive a pipeline — the
workflow material became the [artel](https://github.com/dseloustev/artel) plugin. Note:
`flutter-inner-loop` is deliberately absent — despite the prefix it is a pipeline verify
stage and lives in artel (as `inner-loop`).

Each entry: source purpose, then an annotation line —
**Files** (beyond SKILL.md) · **Author** (frontmatter `metadata.author` to preserve; "—"
means none) · **Phase** (porting-plan phase) · **Scrub** (edits needed; "none" = verbatim
copy). Source path for every skill: `../adguard-wallet/.claude/skills/<name>/`.

Totals: **31 skills (110 files) + 1 policy doc → 32 likbez skills.** Only
`flutter-conventions`, `flutter-runtime`, and `ast-index` need any editing; the other 29
are verbatim copies.

## Architecture & conventions

- **`flutter-architecture`** — Deep architecture contract: MVVM, layered UI/Data/optional
  Domain, feature-first vs layer-first selection, repositories/services/DI, Result &
  Command patterns; for reviews, reports layer violations before style advice.
  **Files:** 5 references, 3 assets (`command.dart`, `result.dart`, examples) ·
  **Author:** MADTeacher · **Phase:** 1 · **Scrub:** none
- **`flutter-apply-architecture-best-practices`** — The official layered-approach primer
  (lean Views, ChangeNotifier ViewModels, Repository/Service data layer, hybrid
  `lib/data|domain|ui` structure) for structuring or refactoring a project.
  **Files:** single-file · **Author:** — · **Phase:** 1 · **Scrub:** none
- **`flutter-conventions`** — Convention checklist for the subset DCM/analyzer do *not*
  enforce; in the source system the implementer reads it before coding and the reviewer's
  convention lens reads it by path. Manual/composed only.
  **Files:** `checklist.md` (95 lines) · **Author:** — · **Phase:** 1 ·
  **Scrub:** the only deep rework in the set — retitle "Wallet convention checklist" →
  "Flutter convention checklist" (checklist.md L1, SKILL.md L4); generalize the
  key-material / `trust_wallet_core` / MFA-locker-path item (~L81) to "security-sensitive
  code paths (key material, credential storage, lockers) require explicit justification
  in the PR/plan"; generalize the `mainAccount` identity rule (~L83) to "identity/account
  derivation goes through the designated single source, never ad-hoc". Everything else in
  the checklist is generic Flutter/Dart and stays.

## UI & layout

- **`flutter-adaptive-ui`** — Constraint-based adaptive design: compact/medium/expanded
  breakpoints (600/840), `MediaQuery.sizeOf` vs `LayoutBuilder`, state preservation
  across resize/fold, Capability/Policy patterns for platform branching.
  **Files:** 6 references, 2 assets · **Author:** MADTeacher · **Phase:** 2 ·
  **Scrub:** none
- **`flutter-build-responsive-layout`** — Narrower layout-technique guide: measuring
  available space, constraints-down/sizes-up, `Expanded`/`Flexible`, lazy `.builder`
  lists. **Files:** single-file · **Author:** — · **Phase:** 2 · **Scrub:** none
- **`flutter-fix-layout-issues`** — Diagnostic map from layout error signatures
  ("RenderFlex overflowed", unbounded viewport height, …) to conditional fixes, verified
  via hot reload. **Files:** single-file · **Author:** — · **Phase:** 2 · **Scrub:** none
- **`flutter-animations`** — Picking the smallest sufficient animation model (implicit /
  explicit / Hero / staggered / physics) with controller lifecycle discipline.
  **Files:** 6 references, 4 assets · **Author:** MADTeacher · **Phase:** 2 ·
  **Scrub:** none
- **`flutter-add-widget-preview`** — How to add `@Preview` widget previews (valid
  targets, MultiPreview, previewer limitations).
  **Files:** single-file · **Author:** — · **Phase:** 2 · **Scrub:** none
- **`flutter-duit-bdui`** — Backend-driven UI with `flutter_duit`: version-first (public
  API changed across majors), `XDriver.remote` vs `.static`, custom widgets and
  capability delegates only when built-ins can't.
  **Files:** 4 references · **Author:** — · **Phase:** 2 · **Scrub:** none

## Navigation & routing

- **`flutter-navigation`** — Navigation as user state: choose the smallest routing model
  (`Navigator` for local flows, `go_router` for deep links/web/redirects/shells), model
  route data deliberately, preserve URLs/tab state/back behavior.
  **Files:** 4 references, 4 assets · **Author:** MADTeacher · **Phase:** 2 ·
  **Scrub:** none
- **`flutter-setup-declarative-routing`** — Bootstrap guide for `MaterialApp.router` +
  `go_router` (ShellRoute, URL strategy, platform deep-link setup).
  **Files:** single-file · **Author:** — · **Phase:** 2 · **Scrub:** none

## Networking & serialization

- **`flutter-networking`** — Networking contract: adapt to the project's existing client
  stack (http/Dio/Retrofit/Chopper), typed decoders, explicit timeouts and status
  handling, services own endpoints / repositories own data policy; review lens for leaked
  clients, unsafe token storage, UI-thread parsing.
  **Files:** 5 references, 7 assets, 1 script (`verify-examples.sh`) ·
  **Author:** MADTeacher · **Phase:** 3 · **Scrub:** none
- **`flutter-use-http-package`** — Narrow how-to for the `http` package: platform
  permissions/entitlements, request execution rules, background parsing.
  **Files:** single-file · **Author:** — · **Phase:** 3 · **Scrub:** none
- **`flutter-implement-json-serialization`** — Manual `fromJson`/`toJson` with
  `dart:convert`, `compute()` offloading for large parses, throw-don't-return-null on
  HTTP errors. **Files:** single-file · **Author:** — · **Phase:** 3 · **Scrub:** none

## Localization

- **`flutter-internationalization`** — The l10n decision guide: gen-l10n by default, ARB
  management, plural/select, RTL, migration off `package:flutter_gen`, generation
  troubleshooting. **Files:** 3 references, 2 assets · **Author:** MADTeacher ·
  **Phase:** 3 · **Scrub:** none
- **`flutter-setup-localization`** — The initial bootstrap checklist
  (`flutter_localizations` + `intl`, `generate: true`, `l10n.yaml`, MaterialApp wiring).
  **Files:** single-file · **Author:** — · **Phase:** 3 · **Scrub:** none

## Persistence

- **`flutter-drift`** — Routed Drift-in-Flutter reference: `drift_flutter` setup,
  type-safe tables/queries/streams, `drift_dev make-migrations`, Riverpod/StreamBuilder
  wiring, per-topic reference files.
  **Files:** 7 references · **Author:** MADTeacher · **Phase:** 3 · **Scrub:** none
- **`dart-drift`** — The non-Flutter sibling (CLI/server/desktop): SQLite via
  `drift/native.dart` or PostgreSQL via `drift_postgres`, same "never write Drift from
  memory, route to references" principle.
  **Files:** 7 references, 1 script (`verify-examples.sh`) · **Author:** MADTeacher ·
  **Phase:** 3 · **Scrub:** none

## Testing & quality

- **`flutter-testing`** — Umbrella testing reference: choose the correct layer (unit /
  widget / integration / plugin-channel mocking), golden and accessibility checks,
  flakiness, CI commands; routes to per-topic references.
  **Files:** 6 references, 1 script (`verify-examples.sh`) · **Author:** MADTeacher ·
  **Phase:** 4 · **Scrub:** none
- **`flutter-add-widget-test`** — `WidgetTester`/`Finder`/`Matcher` walkthrough with a
  9-step checklist from `pumpWidget` to a run-fix-rerun loop.
  **Files:** single-file · **Author:** — · **Phase:** 4 · **Scrub:** none
- **`flutter-add-integration-test`** — Setting up `integration_test`, exploring the live
  app via Dart MCP tools, then converting the actions into permanent test files.
  **Files:** single-file · **Author:** — · **Phase:** 4 · **Scrub:** none
- **`dart-add-unit-test`** — Unit-test structure and conventions: `test/` mirroring
  `lib/`, `group()`/`test()`/`expect()`, setUp/tearDown, `dart test` vs `flutter test`.
  **Files:** single-file · **Author:** — · **Phase:** 4 · **Scrub:** none
- **`dart-generate-test-mocks`** — Mockito + build_runner mocks: `@GenerateNiceMocks`,
  stubbing/verifying, `thenAnswer` for async.
  **Files:** single-file · **Author:** — · **Phase:** 4 · **Scrub:** none
- **`dart-collect-coverage`** — Coverage collection and LCOV reports, incl.
  `coverage:ignore` directives.
  **Files:** single-file · **Author:** — · **Phase:** 4 · **Scrub:** none
- **`dart-migrate-to-checks-package`** — Assertion migration table from
  `package:matcher` `expect(...)` to `package:checks` `check(...)`.
  **Files:** single-file · **Author:** — · **Phase:** 4 · **Scrub:** none
- **`dart-run-static-analysis`** — `analysis_options.yaml` configuration, suppression
  mechanisms, `dart analyze` + `dart fix --apply` workflows.
  **Files:** single-file · **Author:** — · **Phase:** 4 · **Scrub:** none

## Runtime & debugging

- **`flutter-runtime`** — The 12 Dart MCP runtime tools and the two connection workflows
  (direct `launch_app` vs VS Code DTD); hot reload, widget tree inspection, log reading.
  **Files:** single-file (133 lines) · **Author:** — · **Phase:** 5 ·
  **Scrub:** one line (L33): replace the source-project statement ("AdGuard Wallet
  requires `--dart-define-from-file=./config/dev.env`, so the user must launch from VS
  Code") with conditional advice: projects launched with `--dart-define-from-file` (or
  other custom flags) can't use direct `launch_app` — use the VS Code DTD workflow
  instead.
- **`dart-fix-runtime-errors`** — Type-soundness/null-safety knowledge plus the
  locate-fix-verify loop for runtime and analyzer errors.
  **Files:** single-file · **Author:** — · **Phase:** 5 · **Scrub:** none

## Language & tooling

- **`dart-use-pattern-matching`** — Dart 3 pattern-matching idiom: which pattern kind for
  which job, switch statement vs expression.
  **Files:** single-file · **Author:** — · **Phase:** 5 · **Scrub:** none
- **`dart-build-cli-app`** — CLI construction: `bin/` vs `lib/src/`, ArgParser vs
  CommandRunner, POSIX exit codes, CLI integration testing, compilation/distribution.
  **Files:** single-file · **Author:** — · **Phase:** 5 · **Scrub:** none
- **`dart-resolve-package-conflicts`** — Dependency management: single-version rule,
  caret constraints, reading `dart pub outdated`, conflict-resolution workflows.
  **Files:** single-file · **Author:** — · **Phase:** 5 · **Scrub:** none

## Search policy (from `rules/`, becomes a skill)

- **`ast-index`** ← `../adguard-wallet/.claude/rules/ast-index.md` — Policy making
  `ast-index` the mandatory first tool for code search: index-freshness rules
  (`update` after pull/merge/rebase, `rebuild` after clone), search rules (ast-index
  first, Grep only on empty/regex/literals), read rules (`outline` before reading any
  500+ line file, then targeted slices), a **verbatim prompt block for subagents** (they
  don't inherit the rules), scope filters, empty-result triage, command cheat sheet.
  **Files:** becomes `skills/ast-index/SKILL.md` · **Author:** — · **Phase:** 5 ·
  **Scrub:** add YAML frontmatter (`name: ast-index`, description); replace `make g` /
  `make codegen` in the empty-result triage section with "your project's codegen
  command". Keep everything else — especially the verbatim subagent block — intact.

## What deliberately does NOT come to likbez

- The workflow skills, agent crew, hooks, and gates — artel's domain, already ported or
  planned there.
- The contracts & operator docs (`autonomous-run.md`, `orchestrator-common.md`,
  `skills-reference.md`, `workflow-guide.md`, `ticket-parsing.md`,
  `deviation-protocol.md`, `path-conventions.md`) — they document the workflow system
  and ship with artel. `rules/ast-index.md` is the single exception, ported here.
- `rules/sensitive-paths.json` — input to artel's `sensitive_guard` hook, not knowledge.
