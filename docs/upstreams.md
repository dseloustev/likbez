# Upstream registry

*Maintained by the `upstream-sync` dev skill (`.opencode/skills/upstream-sync/`).
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
| `plugins/likbez/skills/flutter-conventions` | AW | `.claude/skills/flutter-conventions/` | 0876a4d31028f753da47e7e1f91965a7feecfd47 | retitled; key-material/locker and `mainAccount` items generalized; `aw_api.json`/make targets/`verify`-gate refs generalized (design.md known-literal table). Unreachable at the 2026-10-27 check: `.claude/skills/` is still absent from the sibling checkout (gitignored there, and no copy exists on disk anywhere in the wallet) — registry re-point pending |
| `plugins/likbez/skills/flutter-architecture` | MT | `flutter-architecture/` | 2fb67e384c6d91f32025bd96400d33b73f21bdc7 | preserve `metadata.author` |
| `plugins/likbez/skills/flutter-apply-architecture-best-practices` | FT | `skills/flutter-apply-architecture-best-practices/` | 90fa51dc9d1bd6694cee226397e08ec8193e9e69 | |
| `plugins/likbez-ui/skills/flutter-adaptive-ui` | MT | `flutter-adaptive-ui/` | 2fb67e384c6d91f32025bd96400d33b73f21bdc7 | preserve `metadata.author` |
| `plugins/likbez-ui/skills/flutter-build-responsive-layout` | FT | `skills/flutter-build-responsive-layout/` | 90fa51dc9d1bd6694cee226397e08ec8193e9e69 | |
| `plugins/likbez-ui/skills/flutter-fix-layout-issues` | FT | `skills/flutter-fix-layout-issues/` | 90fa51dc9d1bd6694cee226397e08ec8193e9e69 | |
| `plugins/likbez-ui/skills/flutter-animations` | MT | `flutter-animations/` | 2fb67e384c6d91f32025bd96400d33b73f21bdc7 | preserve `metadata.author` |
| `plugins/likbez-ui/skills/flutter-add-widget-preview` | FT | `skills/flutter-add-widget-preview/` | 90fa51dc9d1bd6694cee226397e08ec8193e9e69 | |
| `plugins/likbez-ui/skills/flutter-duit-bdui` | MT | `flutter-duit-bdui/` | 2fb67e384c6d91f32025bd96400d33b73f21bdc7 | no `metadata.author` upstream (verified at baseline); byte-identical copy |
| `plugins/likbez-ui/skills/flutter-navigation` | MT | `flutter-navigation/` | 2fb67e384c6d91f32025bd96400d33b73f21bdc7 | preserve `metadata.author` |
| `plugins/likbez-ui/skills/flutter-setup-declarative-routing` | FT | `skills/flutter-setup-declarative-routing/` | 90fa51dc9d1bd6694cee226397e08ec8193e9e69 | |
| `plugins/likbez-data/skills/flutter-networking` | MT | `flutter-networking/` | 2fb67e384c6d91f32025bd96400d33b73f21bdc7 | preserve `metadata.author` |
| `plugins/likbez-data/skills/flutter-use-http-package` | FT | `skills/flutter-use-http-package/` | 90fa51dc9d1bd6694cee226397e08ec8193e9e69 | keep `metadata.model: sonnet` (upstream retargeted to Gemini) |
| `plugins/likbez-data/skills/flutter-implement-json-serialization` | FT | `skills/flutter-implement-json-serialization/` | 90fa51dc9d1bd6694cee226397e08ec8193e9e69 | |
| `plugins/likbez-data/skills/flutter-internationalization` | MT | `flutter-internationalization/` | 2fb67e384c6d91f32025bd96400d33b73f21bdc7 | preserve `metadata.author` |
| `plugins/likbez-data/skills/flutter-setup-localization` | FT | `skills/flutter-setup-localization/` | 90fa51dc9d1bd6694cee226397e08ec8193e9e69 | |
| `plugins/likbez-data/skills/flutter-drift` | MT | `flutter-drift/` | 2fb67e384c6d91f32025bd96400d33b73f21bdc7 | preserve `metadata.author` |
| `plugins/likbez-data/skills/dart-drift` | MT | `dart-drift/` | 2fb67e384c6d91f32025bd96400d33b73f21bdc7 | preserve `metadata.author` |
| `plugins/likbez-testing/skills/flutter-testing` | MT | `flutter-testing/` | 2fb67e384c6d91f32025bd96400d33b73f21bdc7 | preserve `metadata.author` |
| `plugins/likbez-testing/skills/flutter-add-widget-test` | FT | `skills/flutter-add-widget-test/` | 90fa51dc9d1bd6694cee226397e08ec8193e9e69 | |
| `plugins/likbez-testing/skills/flutter-add-integration-test` | FT | `skills/flutter-add-integration-test/` | 90fa51dc9d1bd6694cee226397e08ec8193e9e69 | |
| `plugins/likbez-testing/skills/dart-add-unit-test` | DL | `skills/dart-add-unit-test/` | bf984f3ef223dd85e92036f934bbcb6bf301e4ce | keep vendored metadata (`model: sonnet`); upstream retargeted to Gemini |
| `plugins/likbez-testing/skills/dart-generate-test-mocks` | DL | `skills/dart-generate-test-mocks/` | bf984f3ef223dd85e92036f934bbcb6bf301e4ce | keep vendored metadata (`model: sonnet`); upstream retargeted to Gemini |
| `plugins/likbez-testing/skills/dart-collect-coverage` | DL | `skills/dart-collect-coverage/` | bf984f3ef223dd85e92036f934bbcb6bf301e4ce | keep vendored metadata (`model: sonnet`); upstream retargeted to Gemini |
| `plugins/likbez-testing/skills/dart-migrate-to-checks-package` | DL | `skills/dart-migrate-to-checks-package/` | bf984f3ef223dd85e92036f934bbcb6bf301e4ce | keep `metadata.model: sonnet`; trailing whitespace trimmed vs upstream |
| `plugins/likbez-testing/skills/dart-run-static-analysis` | DL | `skills/dart-run-static-analysis/` | bf984f3ef223dd85e92036f934bbcb6bf301e4ce | keep vendored metadata (`model: sonnet`); upstream retargeted to Gemini |
| `plugins/likbez-tooling/skills/flutter-runtime` | AW | `.claude/skills/flutter-runtime/` | 0876a4d31028f753da47e7e1f91965a7feecfd47 | launch-flag line conditionalized (design.md known-literal table). Unreachable at the 2026-10-27 check: `.claude/skills/` is still absent from the sibling checkout (gitignored there), and the former fallback `wallet-core/dart/.claude/skills/flutter-runtime/` is gone too — no source copy remains anywhere in the wallet; registry re-point pending |
| `plugins/likbez-tooling/skills/dart-fix-runtime-errors` | DL | `skills/dart-fix-runtime-errors/` | bf984f3ef223dd85e92036f934bbcb6bf301e4ce | keep vendored metadata (`model: opus`); upstream retargeted to Gemini |
| `plugins/likbez-tooling/skills/dart-use-pattern-matching` | DL | `skills/dart-use-pattern-matching/` | bf984f3ef223dd85e92036f934bbcb6bf301e4ce | keep vendored metadata (`model: sonnet`); upstream retargeted to Gemini |
| `plugins/likbez-tooling/skills/dart-build-cli-app` | DL | `skills/dart-build-cli-app/` | bf984f3ef223dd85e92036f934bbcb6bf301e4ce | keep vendored `metadata.model: sonnet`; upstream dropped its metadata block |
| `plugins/likbez-tooling/skills/dart-resolve-package-conflicts` | DL | `skills/dart-resolve-package-conflicts/` | bf984f3ef223dd85e92036f934bbcb6bf301e4ce | keep vendored metadata (`model: opus`); upstream retargeted to Gemini |

## Known candidates (not adopted)

Accepting a candidate is a curation decision — record it in design.md's
decision log and port it through the standard procedure.

| Skill | Upstream | Status |
|---|---|---|
| `dart-use-primary-constructors` | DL | proposed, undecided |
| `dart-setup-ffi-assets` | DL | proposed, undecided |
| `dart-use-ffigen` | DL | proposed, undecided |
| `dart-use-doc-examples` | DL | proposed, undecided |
| `dart-use-path-package` | DL | proposed, undecided |
| `dart-write-documentation` | DL | proposed, undecided |
| `agents-md-generator` | MT | proposed, undecided |
