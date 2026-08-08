# Upstream registry

*Maintained by the `upstream-sync` dev skill (`.claude/skills/upstream-sync/`).
`Last-synced` is the upstream commit this skill's content was last reconciled
against; `—` means the baseline reconciliation has not run yet. This file is
also the per-skill provenance table referenced by `THIRD-PARTY-NOTICES.md`.*

## Upstreams

| Id | Repo | Skills path | License |
|---|---|---|---|
| MT | `MADTeacher/mad-agents-skills` | repo root, `<skill>/` | MIT (© 2026 Stanislav Chernyshev) |
| FT | `flutter/agent-plugins` | `skills/<skill>/` | BSD 3-Clause (The Flutter Authors) |
| DL | `dart-lang/skills` | `skills/<skill>/` | BSD 3-Clause (Dart project authors) |
| AW | `../adguard-wallet` (sibling checkout) | `.claude/skills/<skill>/`, `.claude/rules/` | in-house |

`dart-*` skills sync from DL only — the copies of them inside
`flutter/agent-plugins` are ignored by design.

## Skills

| Skill | Upstream | Upstream path | Last-synced | Notes |
|---|---|---|---|---|
| `plugins/likbez/skills/project-setup` | — | — | — | likbez original, no upstream |
| `plugins/likbez/skills/ast-index` | AW | `.claude/rules/ast-index.md` | — | frontmatter added; `make g`/`make codegen` → generic codegen phrasing |
| `plugins/likbez/skills/flutter-conventions` | AW | `.claude/skills/flutter-conventions/` | — | retitled; key-material/locker and `mainAccount` items generalized |
| `plugins/likbez/skills/flutter-architecture` | MT | `flutter-architecture/` | — | preserve `metadata.author` |
| `plugins/likbez/skills/flutter-apply-architecture-best-practices` | FT | `skills/flutter-apply-architecture-best-practices/` | — | |
| `plugins/likbez-ui/skills/flutter-adaptive-ui` | MT | `flutter-adaptive-ui/` | — | preserve `metadata.author` |
| `plugins/likbez-ui/skills/flutter-build-responsive-layout` | FT | `skills/flutter-build-responsive-layout/` | — | |
| `plugins/likbez-ui/skills/flutter-fix-layout-issues` | FT | `skills/flutter-fix-layout-issues/` | — | |
| `plugins/likbez-ui/skills/flutter-animations` | MT | `flutter-animations/` | — | preserve `metadata.author` |
| `plugins/likbez-ui/skills/flutter-add-widget-preview` | FT | `skills/flutter-add-widget-preview/` | — | |
| `plugins/likbez-ui/skills/flutter-duit-bdui` | MT | `flutter-duit-bdui/` | — | attribution pending verification against the MT copy |
| `plugins/likbez-ui/skills/flutter-navigation` | MT | `flutter-navigation/` | — | preserve `metadata.author` |
| `plugins/likbez-ui/skills/flutter-setup-declarative-routing` | FT | `skills/flutter-setup-declarative-routing/` | — | |
| `plugins/likbez-data/skills/flutter-networking` | MT | `flutter-networking/` | — | preserve `metadata.author` |
| `plugins/likbez-data/skills/flutter-use-http-package` | FT | `skills/flutter-use-http-package/` | — | |
| `plugins/likbez-data/skills/flutter-implement-json-serialization` | FT | `skills/flutter-implement-json-serialization/` | — | |
| `plugins/likbez-data/skills/flutter-internationalization` | MT | `flutter-internationalization/` | — | preserve `metadata.author` |
| `plugins/likbez-data/skills/flutter-setup-localization` | FT | `skills/flutter-setup-localization/` | — | |
| `plugins/likbez-data/skills/flutter-drift` | MT | `flutter-drift/` | — | preserve `metadata.author` |
| `plugins/likbez-data/skills/dart-drift` | MT | `dart-drift/` | — | preserve `metadata.author` |
| `plugins/likbez-testing/skills/flutter-testing` | MT | `flutter-testing/` | — | preserve `metadata.author` |
| `plugins/likbez-testing/skills/flutter-add-widget-test` | FT | `skills/flutter-add-widget-test/` | — | |
| `plugins/likbez-testing/skills/flutter-add-integration-test` | FT | `skills/flutter-add-integration-test/` | — | |
| `plugins/likbez-testing/skills/dart-add-unit-test` | DL | `skills/dart-add-unit-test/` | — | |
| `plugins/likbez-testing/skills/dart-generate-test-mocks` | DL | `skills/dart-generate-test-mocks/` | — | |
| `plugins/likbez-testing/skills/dart-collect-coverage` | DL | `skills/dart-collect-coverage/` | — | |
| `plugins/likbez-testing/skills/dart-migrate-to-checks-package` | DL | `skills/dart-migrate-to-checks-package/` | — | |
| `plugins/likbez-testing/skills/dart-run-static-analysis` | DL | `skills/dart-run-static-analysis/` | — | |
| `plugins/likbez-tooling/skills/flutter-runtime` | AW | `.claude/skills/flutter-runtime/` | — | launch-flag line conditionalized (design.md known-literal table) |
| `plugins/likbez-tooling/skills/dart-fix-runtime-errors` | DL | `skills/dart-fix-runtime-errors/` | — | |
| `plugins/likbez-tooling/skills/dart-use-pattern-matching` | DL | `skills/dart-use-pattern-matching/` | — | |
| `plugins/likbez-tooling/skills/dart-build-cli-app` | DL | `skills/dart-build-cli-app/` | — | |
| `plugins/likbez-tooling/skills/dart-resolve-package-conflicts` | DL | `skills/dart-resolve-package-conflicts/` | — | |

## Known candidates (not adopted)

Accepting a candidate is a curation decision — record it in design.md's
decision log and port it through the standard procedure.

| Skill | Upstream | Status |
|---|---|---|
| `dart-use-primary-constructors` | DL | proposed, undecided |
| `dart-setup-ffi-assets` | DL | proposed, undecided |
| `dart-use-ffigen` | DL | proposed, undecided |
| `agents-md-generator` | MT | proposed, undecided |
