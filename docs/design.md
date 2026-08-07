# Likbez — design

*Status: founding draft v0.1 · 2026-08-07*

## What this is

**Likbez** is a Claude Code plugin: a pure-knowledge pack of Flutter/Dart reference and
how-to skills, plus the `ast-index` search policy. It is the companion to
**[artel](https://github.com/dseloustev/artel)** — the spec-driven autonomous
feature-development workflow plugin. The two were split out of the same source system
(a private Flutter wallet project): artel took the workflow (orchestrators, agents, hooks,
gates), likbez takes the knowledge the agents consult *while* developing.

The name pairing is era-matched: an *artel* is a workers' cooperative; *likbez*
(ликвидация безграмотности, "liquidation of illiteracy") was the literacy campaign that
educated it. **The crew works; likbez educates it.**

This repo is both the plugin and its own single-plugin marketplace
(`.claude-plugin/marketplace.json`), installable straight from GitHub — exactly like artel.

## Goals

1. **One-command install** — `/plugin marketplace add dseloustev/likbez` →
   `/plugin install likbez@likbez`, usable in any Flutter/Dart project.
2. **Complete v1 knowledge set** — all 31 informational skills from the source system plus
   the `ast-index` policy, ported with their full `references/`, `assets/`, and `scripts/`
   subtrees intact.
3. **Generic Flutter/Dart, not wallet-flavored** — the knowledge reads as a general
   Flutter/Dart pack. Source-project literals (wallet paths, project launch flags, `make`
   targets) are genericized, never copied.

## Non-goals

- **No process.** Likbez contains no agents, no hooks, no orchestrator skills, no quality
  gates, no host-writable state, no config file. Every skill is self-contained knowledge:
  an agent (or human) loads it, reads it, applies it. If a future need for configuration
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
│   ├── plugin.json          # manifest: name, version, author, license
│   └── marketplace.json     # single-plugin marketplace (source: "./")
├── skills/
│   └── <name>/
│       ├── SKILL.md         # entry point with YAML frontmatter
│       ├── references/      # per-topic deep-dive files (routed skills)
│       ├── assets/          # starter code the skill tells the reader to copy
│       └── scripts/         # skill-local helpers (example verifiers)
├── docs/                    # this design, the porting plan, the source inventory
├── CLAUDE.md · README.md · LICENSE · CHANGELOG.md
```

Skills keep their source names — `flutter-architecture`, `dart-drift`, … — and surface as
`/likbez:flutter-architecture` etc. once installed. No renames are needed: the `flutter-*`
/ `dart-*` prefixes are the catalog's organizing principle, not project residue.

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

### The ast-index skill

The source system's `rules/ast-index.md` — the policy making `ast-index` the mandatory
first tool for code search, with a verbatim block to paste into subagent prompts — ports
as a 32nd skill, `skills/ast-index/SKILL.md`. Rationale:

- Skills are a plugin's delivery mechanism; a loose doc in the plugin directory is not
  discoverable or loadable by a host session.
- Plugin namespacing (`/likbez:ast-index`) avoids collision with any standalone ast-index
  tooling the host may have installed.
- Agents that don't inherit skills can still `Read` it by path (see "Relationship to
  artel" below).

Its `make g` / `make codegen` literals genericize to "your project's codegen command".

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

`flutter-conventions` is the only skill needing real editorial rework (its checklist *is*
the wallet's); everything else is a copy with at most a one-line touch-up. The ast-index
skill additionally drops its `make g` / `make codegen` references (see above).

### Scrub gate

Mechanical acceptance check, run after every phase and again before publish:

```bash
grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard" skills/ && echo "FAIL" || echo "CLEAN"
```

Must print `CLEAN`. Also: no absolute paths anywhere in the skill tree
(`grep -rn "/Users/" skills/` must be empty; docs follow the same rule by convention —
the gate is scoped to `skills/` so its own text doesn't trip it).

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
  they document the workflow, not the craft. The single exception, `rules/ast-index.md`,
  ships here as the `ast-index` skill.

## Conventions

- Skill names: kebab-case, directory name equals frontmatter `name`.
- All docs, skills, and commit messages in English.
- No absolute paths anywhere; source references use the sibling convention
  (`../adguard-wallet`, `../artel`).
- Commits: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`), subject line only.
- Versioning: semver; `CHANGELOG.md` and `.claude-plugin/plugin.json` `version` stay in
  sync. First published tag: `v0.1.0`.
- Skills are knowledge, not process: a likbez skill never invokes agents, never writes
  host state, never orchestrates. If a ported skill turns out to contain process, that is
  a porting error — flag it against the inventory.

## Versioning and publishing

Repo home: `https://github.com/dseloustev/likbez` (corporate account, **private until the
licensing question resolves**). `gh` operations need the corporate profile:
`GH_CONFIG_DIR=~/.config/gh-adguard gh …`. Git identity for commits: corporate
(`d.seloustev@adguard.com`, set in local git config).

Local smoke test: `/plugin marketplace add <path-to-this-repo>` →
`/plugin install likbez@likbez` → confirm skills appear under the `likbez:` namespace and
a routed skill (e.g. `/likbez:flutter-drift`) can read its own `references/` files.

## Open questions

1. **Licensing of the 9 MADTeacher skills** (blocking public release; see above). Resolve
   by locating the original distribution and its license, or obtaining permission.
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
