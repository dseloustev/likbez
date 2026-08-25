# Likbez — design

*Status: founding draft v0.1 · 2026-08-07*

## What this is

**Likbez** is a Claude Code plugin: a pure-knowledge pack of Flutter/Dart reference and
how-to skills. It is the companion to
**[artel](https://github.com/dseloustev/artel)** — the spec-driven autonomous
feature-development workflow plugin. The two were split out of the same source system
(a private Flutter wallet project): artel took the workflow (orchestrators, agents, hooks,
gates), likbez takes the knowledge the agents consult *while* developing.

The name pairing is era-matched: an *artel* is a workers' cooperative; *likbez*
(ликвидация безграмотности, "liquidation of illiteracy") was the literacy campaign that
educated it. **The crew works; likbez educates it.**

This repo is both the plugin and its own five-plugin marketplace
(`.claude-plugin/marketplace.json`), installable straight from GitHub — exactly like artel.

## Goals

1. **One-command install** — `/plugin marketplace add dseloustev/likbez` →
   `/plugin install likbez@likbez`, usable in any Flutter/Dart project.
2. **Complete v1 knowledge set** — all 31 informational skills from the source system,
   ported with their full `references/`, `assets/`, and `scripts/` subtrees intact.
3. **Generic Flutter/Dart, not wallet-flavored** — the knowledge reads as a general
   Flutter/Dart pack. Source-project literals (wallet paths, project launch flags, `make`
   targets) are genericized, never copied.

## Non-goals

- **No process.** Likbez contains no agents, no hooks, no orchestrator skills, no quality
  gates, no host-writable state, no config file. Every skill is self-contained knowledge:
  an agent (or human) loads it, reads it, applies it. The single recorded exception is the
  `project-setup` advisor (see decision log). If a future need for configuration
  arises, that is a new design decision — v1 explicitly has none.
- **No artel coupling.** Likbez installs and works standalone. Artel never becomes a
  dependency, and likbez never references artel's config, run state, or pipeline.
- **No internet-sourced extensions in v1.** The design decision that created likbez says
  "seeded from the source project and extended later from the internet" — the extension is
  post-v1 work (see open questions).

## Architecture

### Plugin layout

```
likbez/
├── .claude-plugin/
│   └── marketplace.json     # five-plugin marketplace (sources: ./plugins/<name>)
├── plugins/
│   ├── likbez/              # core: project-setup, conventions, architecture
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/<name>/   # SKILL.md + references/ assets/ scripts/
│   ├── likbez-ui/           # adaptive UI, layout, animations, previews, BDUI, navigation
│   ├── likbez-data/         # networking, serialization, l10n, Drift
│   ├── likbez-testing/      # unit/widget/integration tests, mocks, coverage, analysis
│   └── likbez-tooling/      # runtime, error fixing, idiom, CLI, dependencies
├── .claude/skills/          # repo-local dev tooling (upstream-sync, bump-version) — not shipped
├── docs/                    # design, porting plan, source inventory, upstreams registry
├── THIRD-PARTY-NOTICES.md
├── CLAUDE.md · README.md · LICENSE · CHANGELOG.md
```

Skills keep their source names and surface namespaced by their plugin:
`/likbez:flutter-architecture`, `/likbez-ui:flutter-navigation`, `/likbez-data:dart-drift`,
… The five plugins version in lockstep (one version, one CHANGELOG).

### Skill anatomy

Two shapes exist in the set, both preserved as-is:

- **Routed skills** (the big ones: `flutter-architecture`, `flutter-drift`,
  `flutter-testing`, …): a lean `SKILL.md` that routes to `references/<topic>.md` files
  and sometimes ships `assets/` starter code. The routing principle ("never write Drift
  from memory, route to references") is part of the knowledge — do not flatten these into
  single files.
- **Single-file how-tos** (the `flutter-add-*` / `dart-*` task guides): one `SKILL.md`
  with a step-by-step procedure.

Three skills ship a `scripts/verify-examples.sh` (`flutter-networking`, `flutter-testing`,
`dart-drift`) — skill-local helpers that validate the skill's own code examples. They port
unchanged.

### Why likbez ships no search policy

Likbez deliberately carries **no** code-search rules. The `ast-index` skill it shipped in
v0.1.0 — a port of the source system's `rules/ast-index.md` — was retired in 0.2.0 (see
the decision log, 2026-08-25). Three reasons, two of them invisible to the founding
design, the third a correction of it:

- **A standalone `ast-index` plugin owns the job.** It ships the full command reference
  for the current CLI and enforces the policy with hooks rather than prose, versioned in
  step with the tool.
- **The founding rationale was wrong about collision.** Plugin namespacing does *not*
  avoid it: both skills declare `name: ast-index`, so two competing descriptions load
  whenever both plugins are installed.
- **It was process, not knowledge.** Tool-choice policy for a third-party CLI that likbez
  cannot guarantee is installed, inside a pack whose charter is craft knowledge. Removing
  it restores the "No process" non-goal to a single recorded exception, `project-setup`.

The one Flutter/Dart fact worth keeping — codegen emits symbols a search index cannot see
until it is refreshed — moved to `flutter-conventions`' generated-files item, where it
belongs as a convention consequence. `project-setup` mentions the standalone plugin as
optional companion tooling. Nothing in likbez depends on it.

## Genericization

**The rule (inherited from artel):** port the structure and the knowledge; strip
source-project literals. Wallet paths, wallet-specific launch flags, `make` targets, and
project names become either generic phrasing or conditional advice ("projects using X
need…").

### Known wallet literals (complete scan, 2026-08-07)

A full scan of the 31 skills for `wallet|AW-[0-9]|aiguard|adguard` found **5 hits in
3 files** — the informational set is already nearly generic:

| File | Hit | Fix |
|---|---|---|
| `flutter-conventions/checklist.md` (title) | "Wallet convention checklist" | Retitle "Flutter convention checklist" |
| `flutter-conventions/checklist.md` (~L81) | Key material / `trust_wallet_core` call sites, MFA locker path `lib/data/storage/locker/` | Generalize: security-sensitive code paths (key material, credential storage, lockers) require explicit justification in the PR/plan |
| `flutter-conventions/checklist.md` (~L83) | "wallet identity derives from `mainAccount`, never…" | Generalize: identity/account derivation goes through the designated single source, never ad-hoc |
| `flutter-conventions/SKILL.md` (L4) | "Wallet convention checklist…" | "Flutter convention checklist…" |
| `flutter-runtime/SKILL.md` (L33) | "AdGuard Wallet requires `--dart-define-from-file=./config/dev.env`, so the user must launch from VS Code." | Conditionalize: "Projects launched with `--dart-define-from-file` (or other custom flags) can't use direct `launch_app` — use the VS Code DTD workflow instead." |

Found during Phase 1 porting (outside the grep pattern, same rule — make targets and
project names genericize):

| File | Hit | Fix |
|---|---|---|
| `flutter-conventions/checklist.md` (generated-files item) | `aw_api.json`; `make g` / `make ln` / `make vec` / `make codegen-api`; wallet-specific generated-tree paths | Generalize: "the source (annotated model, ARB file, SVG, API spec) followed by your project's codegen command" |
| `flutter-conventions/{SKILL.md,checklist.md}` | "the `verify` gate" (source-system gate name); sources-of-truth list naming wallet repo docs | Generalize: "the analyzer/DCM gate"; "the host project's `CLAUDE.md` and convention/code-style docs" |

`flutter-conventions` is the only skill needing real editorial rework (its checklist *is*
the wallet's); everything else is a copy with at most a one-line touch-up.

### Scrub gate

Mechanical acceptance check, run after every phase and again before publish:

```bash
grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard" plugins/ --exclude=plugin.json && echo "FAIL" || echo "CLEAN"
```

Must print `CLEAN`. Also: no absolute paths anywhere in the skill tree
(`grep -rn "/Users/" plugins/` must be empty; docs follow the same rule by convention —
the gate is scoped to `plugins/` so its own text doesn't trip it, and excludes
`plugin.json` manifests, whose author email legitimately contains the corporate domain).

## Attribution and licensing

Nine of the 31 skills carry third-party authorship in their frontmatter
(`metadata.author: Stanislav [MADTeacher] Chernyshev`): `flutter-adaptive-ui`,
`flutter-animations`, `flutter-architecture`, `flutter-drift`,
`flutter-internationalization`, `flutter-navigation`, `flutter-networking`,
`flutter-testing`, `dart-drift`.

Rules:

- **Preserve `metadata.author` verbatim** in every ported SKILL.md. Never strip or
  rewrite attribution.
- The repo's own license is MIT (matching artel), covering the original and
  likbez-authored content.
- **Open question (blocking public release):** verify the redistribution terms of the 9
  MADTeacher-authored skills. Until resolved, the GitHub repo stays **private**. Phase 6
  of the porting plan gates publishing on this.

## Relationship to artel

Loose by design. Likbez works standalone in any Flutter/Dart repo. When installed
alongside artel:

- Artel's agents run as subagents and **do not inherit skills** — the source system's
  pattern was "agents Read the skill by path" (e.g. the implementer reads
  `flutter-conventions` before coding). That pattern carries over: a host project's
  config or CLAUDE.md can point artel's crew at installed likbez skill paths. Nothing in
  likbez needs to know about this.
- The contracts and operator docs from the source system (`autonomous-run.md`,
  `orchestrator-common.md`, ticket-parsing, deviation-protocol, …) ship with **artel** —
  they document the workflow, not the craft. `rules/ast-index.md` was the single
  exception, ported here as a skill and retired in 0.2.0 (see the decision log).

## Conventions

- Skill names: kebab-case, directory name equals frontmatter `name`.
- All docs, skills, and commit messages in English.
- No absolute paths anywhere; source references use the sibling convention
  (`../adguard-wallet`, `../artel`).
- Commits: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`), subject line only.
- Versioning: semver; keep `CHANGELOG.md` and all five `plugins/*/.claude-plugin/plugin.json`
  versions in lockstep. Releases are cut with the `bump-version` dev skill
  (`.claude/skills/bump-version/`). First published tag: `v0.1.0`.
- Skills are knowledge, not process: a likbez skill never invokes agents, never writes
  host state, never orchestrates. The one exception, recorded in the decision log, is
  `project-setup`, which may write host config with explicit user consent. If a ported
  skill turns out to contain process, that is a porting error — flag it against the
  inventory.

## Versioning and publishing

Repo home: `https://github.com/dseloustev/likbez` (corporate account, **private until the
Phase 6 notices verification and go-public call (licensing itself is resolved — see
design.md decision log)**). `gh` operations need the corporate profile:
`GH_CONFIG_DIR=~/.config/gh-adguard gh …`. Git identity for commits: corporate
(`d.seloustev@adguard.com`, set in local git config).

Local smoke test: `/plugin marketplace add <path-to-this-repo>` then
`/plugin install likbez@likbez` (core); run `/likbez:project-setup` in a
sample project, install a recommended cluster, and confirm a routed skill
(e.g. `/likbez-data:flutter-drift`) can read its own `references/` files.
Full operator procedure with expected results: [smoke-test.md](smoke-test.md).

## Open questions

1. **Licensing of the 9 MADTeacher skills** — **resolved 2026-08-07**: the original
   distribution is `MADTeacher/mad-agents-skills` (MIT, © 2026 Stanislav Chernyshev);
   the unattributed how-tos trace to `flutter/agent-plugins` and `dart-lang/skills`
   (both BSD-3). Redistribution is permitted with notices retained — see the licensing
   decision below and `THIRD-PARTY-NOTICES.md` (added in Phase 5.5). Public release is
   unblocked; timing stays a Phase 6 call.
2. **Internet-sourced extensions (post-v1).** The founding decision says likbez will be
   "extended later from the internet" (official Flutter/Dart docs, community skill
   packs). Undecided: curation criteria, whether new skills join the existing `flutter-*`
   / `dart-*` prefixes or get their own, and how to track upstream freshness.
3. **Non-Flutter knowledge.** Likbez v1 is Flutter/Dart by content, but nothing in the
   name or layout forbids other stacks later. Out of scope until a concrete need appears.

## Decision log

- **2026-08-01 — Likbez exists (imported from artel's decision log, user-approved).** The
  informational/reference skills become a second plugin named **likbez** (era-matched
  pair to "artel"), seeded from the source project and extended later from the internet.
  `rules/ast-index.md` goes there too; orchestrator index-refresh steps in artel become
  an optional config hook. Separate repo.
- **2026-08-07 — Own single-plugin marketplace (user-approved).** Likbez mirrors artel's
  distribution: its repo is its own marketplace, installable straight from GitHub. No
  entry in artel's marketplace.json for now (may be added later as an external source —
  that would be artel's decision, not likbez's).
- **2026-08-07 — Repo home: `dseloustev/likbez` (user-approved).** Corporate account,
  matching artel; corporate git identity and `GH_CONFIG_DIR=~/.config/gh-adguard` for
  `gh`.
- **2026-08-07 — v1 scope: all 31 skills + ast-index (user-approved).** The complete
  informational inventory ports before `v0.1.0` is tagged. Internet-sourced extensions
  are post-v1.
- **2026-08-07 — Genericize, no config mechanism (user-approved).** Wallet literals are
  scrubbed to generic or conditional phrasing (5 known hits, listed above). No
  `.likbez/config.json` or host-injection mechanism in v1 — likbez stays configuration-free.
- **2026-08-07 — Founding docs: artel's 3-doc model (user-approved).** `design.md` +
  `porting-plan.md` + `source-inventory.md`, written so an agent can build the plugin
  from them without further input.
- **2026-08-07 — Cluster split: 5 plugins in one marketplace (user-approved).** The repo
  becomes a multi-plugin marketplace — `likbez` (core), `likbez-ui`, `likbez-data`,
  `likbez-testing`, `likbez-tooling` under `plugins/` — because Claude Code has no
  per-skill disable and 32 always-loaded skill descriptions cost real context, while
  per-project plugin enablement (`enabledPlugins`) exists. Lockstep versioning, one
  CHANGELOG. Restructure lands before porting (Phase 0.5). Full design:
  [superpowers/specs/2026-08-07-cluster-split-advisor-upstream-sync-design.md](superpowers/specs/2026-08-07-cluster-split-advisor-upstream-sync-design.md).
- **2026-08-07 — `project-setup` advisor skill (user-approved).** Core ships one
  deliberate **process carve-out**: a skill that analyzes the host project
  (`pubspec.yaml` etc.), recommends clusters with reasons, asks about planned
  technologies, and — only with explicit consent — writes `enabledPlugins` to the
  project's `.claude/settings.json` and/or a guidance note to the host CLAUDE.md.
  All other skills remain pure knowledge; the "no process" non-goal is amended by
  exactly this one skill.
- **2026-08-07 — `upstream-sync` dev skill + `docs/upstreams.md` registry
  (user-approved).** Skill updates flow from upstreams through a repo-local dev skill
  (`.claude/skills/upstream-sync/`, never shipped) driven by a per-skill registry
  (upstream repo/path, last-synced SHA, genericization deltas). Four upstreams:
  `MADTeacher/mad-agents-skills`, `flutter/agent-plugins`, `dart-lang/skills`
  (canonical for `dart-*`), and `../adguard-wallet` for the in-house trio. New upstream
  skills are proposed as candidates, never auto-added.
- **2026-08-07 — Third-party licensing resolved (user-approved).** All upstreams are
  permissively licensed (MIT / BSD-3). Add `THIRD-PARTY-NOTICES.md` with the three
  notices plus per-skill provenance via the registry; verify `flutter-duit-bdui`
  against MADTeacher's copy during its port and add attribution if derived. Open
  question 1 is closed; the repo may go public at Phase 6.
- **2026-08-08 — Scrub gate excludes plugin manifests (user-approved).** The gate
  command gains `--exclude=plugin.json`: the five manifests' `author.email`
  (`d.seloustev@adguard.com`) legitimately matches the `adguard` pattern and is
  the corporate identity, not a source-project literal. Skill content remains
  fully gated.
- **2026-08-23 — `bump-version` dev skill owns the release chore (user-approved).**
  Ported from artel's repo-local `bump-version` and adapted to likbez's six version
  carriers (`CHANGELOG.md` + five manifests): preflight adds a lockstep-drift check and
  uses the scrub gate in place of a test suite (likbez has none). A "finalize" rule
  covers the case where the manifests already name an untagged version — the first
  release, or a version pre-set in a sync commit — so the skill cuts that version as-is
  instead of demanding a strictly greater one. The skill stops at the annotated tag;
  push and GitHub release stay manual. `upstream-sync` no longer bumps manifests — the
  bump is sized from `[Unreleased]` at release time. Lives in
  `.claude/skills/bump-version/`, never shipped.
- **2026-08-25 — `ast-index` skill retired (user-approved).** Supersedes the 2026-08-07
  v1-scope decision for this one skill: `plugins/likbez/skills/ast-index/` is deleted, and
  the pack drops to 32 skills. A standalone `ast-index` plugin (CLI v3.50) ships the same
  policy with a current command reference and enforcement hooks, and both skills declared
  `name: ast-index` — the founding claim that plugin namespacing avoids collision does not
  hold. The skill was also the pack's only piece of pure tool policy, for a CLI likbez
  cannot assume is installed. Two lines survive, relocated by kind: the codegen-staleness
  fact (verified absent from the upstream plugin, which carries no codegen coverage at
  all) joins `flutter-conventions`' generated-files item, phrased tool-agnostically; and
  `project-setup` gains an optional-companion pointer. The remaining 32 skills are
  deliberately **not** wired to ast-index — that would push a third-party dependency into
  32 files of otherwise portable knowledge. Design:
  [superpowers/specs/2026-08-25-retire-ast-index-skill-design.md](superpowers/specs/2026-08-25-retire-ast-index-skill-design.md).
