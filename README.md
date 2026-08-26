# likbez

A Claude Code plugin: a Flutter/Dart knowledge pack of 32 skills in five installable cluster
plugins — core (architecture, conventions, the `project-setup` advisor), UI,
data, testing, and tooling.

Companion to [artel](https://github.com/dseloustev/artel), the spec-driven autonomous
feature-development workflow plugin. The names are an era-matched pair: an *artel* is a
workers' cooperative; *likbez* was the literacy campaign that educated it. **The crew
works; likbez educates it.**

## Install

    /plugin marketplace add dseloustev/likbez
    /plugin install likbez@likbez

Then run `/likbez:project-setup` inside your project: it detects your stack,
recommends the matching clusters (`likbez-ui`, `likbez-data`,
`likbez-testing`, `likbez-tooling`), and installs them with your approval.
Core skills surface as `/likbez:<name>`, cluster skills as
`/likbez-ui:<name>` etc.

### OpenCode

From a likbez checkout:

```bash
scripts/install-opencode.sh
```

Restart OpenCode; every skill is available as `likbez-<skill>` with its reference
material alongside. Uninstall with `scripts/install-opencode.sh --remove`. Details and
host differences: [docs/opencode.md](docs/opencode.md).

## What's inside

### likbez (core)

| Skill | Purpose |
|---|---|
| `project-setup` | Analyzes the host project and recommends/enables the matching likbez clusters |
| `flutter-architecture` | MVVM, layered UI/Data/optional Domain boundaries, feature-first structure, Result & Command patterns |
| `flutter-apply-architecture-best-practices` | The official layered-approach primer for structuring or refactoring a project |
| `flutter-conventions` | Convention checklist for the subset DCM/analyzer do not enforce |

### likbez-ui

| Skill | Purpose |
|---|---|
| `flutter-adaptive-ui` | Constraint-based adaptive design: breakpoints, `MediaQuery` vs `LayoutBuilder`, state preservation across resize/fold |
| `flutter-build-responsive-layout` | Layout techniques: constraints-down/sizes-up, `Expanded`/`Flexible`, lazy `.builder` lists |
| `flutter-fix-layout-issues` | Diagnostic map from layout error signatures to conditional fixes |
| `flutter-animations` | Picking the smallest sufficient animation model with controller lifecycle discipline |
| `flutter-add-widget-preview` | Adding `@Preview` widget previews |
| `flutter-duit-bdui` | Backend-driven UI with `flutter_duit` |
| `flutter-navigation` | Choosing the smallest routing model (`Navigator` vs `go_router`), route data, URL/tab/back behavior |
| `flutter-setup-declarative-routing` | Bootstrap for `MaterialApp.router` + `go_router` |

### likbez-data

| Skill | Purpose |
|---|---|
| `flutter-networking` | Networking contract: client stacks, typed decoders, explicit timeouts, services own endpoints |
| `flutter-use-http-package` | Narrow how-to for the `http` package |
| `flutter-implement-json-serialization` | Manual `fromJson`/`toJson` with `dart:convert`, `compute()` offloading |
| `flutter-internationalization` | The l10n decision guide: gen-l10n, ARB management, plural/select, RTL |
| `flutter-setup-localization` | Initial l10n bootstrap checklist |
| `flutter-drift` | Routed Drift-in-Flutter reference |
| `dart-drift` | Drift for CLI/server/desktop Dart (SQLite or PostgreSQL) |

### likbez-testing

| Skill | Purpose |
|---|---|
| `flutter-testing` | Umbrella testing reference: choosing the correct layer, goldens, flakiness, CI |
| `flutter-add-widget-test` | `WidgetTester`/`Finder`/`Matcher` walkthrough |
| `flutter-add-integration-test` | Setting up `integration_test` and converting live-app exploration into tests |
| `dart-add-unit-test` | Unit-test structure and conventions |
| `dart-generate-test-mocks` | Mockito + build_runner mocks |
| `dart-collect-coverage` | Coverage collection and LCOV reports |
| `dart-migrate-to-checks-package` | Migrating `expect()` assertions to `package:checks` |
| `dart-run-static-analysis` | `analysis_options.yaml`, suppressions, `dart analyze` / `dart fix` workflows |

### likbez-tooling

| Skill | Purpose |
|---|---|
| `flutter-runtime` | The Dart MCP runtime tools and connection workflows; hot reload, widget tree inspection, log reading |
| `dart-fix-runtime-errors` | Type-soundness/null-safety knowledge plus the locate-fix-verify loop |
| `dart-use-pattern-matching` | Dart 3 pattern-matching idiom |
| `dart-build-cli-app` | CLI construction: ArgParser vs CommandRunner, POSIX exit codes, distribution |
| `dart-resolve-package-conflicts` | Dependency management and conflict-resolution workflows |

## Development

Maintainer docs live in [docs/](docs/): [design](docs/design.md) (architecture
and decision log), [porting plan](docs/porting-plan.md),
[source inventory](docs/source-inventory.md),
[upstream registry](docs/upstreams.md), and the
[local smoke test](docs/smoke-test.md) run before each release.

## License

MIT for likbez itself. Ported skills originate from third-party repositories
under MIT and BSD 3-Clause — see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)
and the per-skill provenance in [docs/upstreams.md](docs/upstreams.md). Nine+
skills also carry author attribution in their frontmatter (see
[docs/design.md](docs/design.md), "Attribution and licensing").
