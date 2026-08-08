# Cluster Split, Advisor & Upstream-Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure likbez into a five-plugin marketplace and add the new infrastructure: the `project-setup` advisor skill, the `docs/upstreams.md` sync registry, the repo-local `upstream-sync` dev skill, and `THIRD-PARTY-NOTICES.md`.

**Architecture:** The repo root `.claude-plugin/` keeps only `marketplace.json`; five plugins live under `plugins/<name>/` with their own manifests and (eventually) `skills/` trees. The advisor ships in the core plugin; the updater lives in the repo's own `.claude/skills/` and never ships. Skill *porting* (Phases 1–5) is NOT part of this plan — it continues per `docs/porting-plan.md`, into the paths this plan creates.

**Tech Stack:** Markdown + JSON only; no build system. Verification is `jq`, `grep`, `ls`, `git`. If `jq` is unavailable, substitute `python3 -m json.tool <file> > /dev/null` for validity checks and read fields by eye.

**Spec:** `docs/superpowers/specs/2026-08-07-cluster-split-advisor-upstream-sync-design.md`

## Global Constraints

- Commits: conventional commits, **subject line only, no trailers, no Co-Authored-By**.
- All content in English; **no absolute paths** anywhere in repo files (`../adguard-wallet` sibling convention only).
- Scrub gate after any change under `plugins/`: `grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard" plugins/` → no output, and `grep -rn "/Users/" plugins/` → no output.
- Lockstep version: all five `plugins/*/.claude-plugin/plugin.json` carry `"version": "0.1.0"` and must stay identical forever.
- Author block everywhere: `{"name": "Dmitry Seloustev", "email": "d.seloustev@adguard.com"}`; license `MIT`; homepage/repository `https://github.com/dseloustev/likbez`.
- Git identity is already configured locally; do not change git config.
- Keep `docs/porting-plan.md` checkboxes current: every task below that completes a Phase 5.5 item ticks its box in the same commit.

---

### Task 1: Five-plugin marketplace skeleton

**Files:**
- Delete: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`, `CHANGELOG.md`
- Create: `plugins/likbez/.claude-plugin/plugin.json`, `plugins/likbez-ui/.claude-plugin/plugin.json`, `plugins/likbez-data/.claude-plugin/plugin.json`, `plugins/likbez-testing/.claude-plugin/plugin.json`, `plugins/likbez-tooling/.claude-plugin/plugin.json`

**Interfaces:**
- Produces: plugin names `likbez`, `likbez-ui`, `likbez-data`, `likbez-testing`, `likbez-tooling`; marketplace name `likbez`; plugin roots `plugins/<name>/` — every later task and all porting phases rely on these exact names and paths.

- [ ] **Step 1: Verify the starting state**

Run: `jq -r '.name' .claude-plugin/plugin.json && ls plugins 2>&1`
Expected: `likbez`, then `ls: plugins: No such file or directory`.

- [ ] **Step 2: Remove the root plugin manifest**

```bash
git rm .claude-plugin/plugin.json
```

- [ ] **Step 3: Create the five plugin manifests**

Create `plugins/likbez/.claude-plugin/plugin.json`:

```json
{
  "name": "likbez",
  "description": "Likbez core: project-setup advisor, ast-index search policy, Flutter architecture and convention skills.",
  "version": "0.1.0",
  "author": {
    "name": "Dmitry Seloustev",
    "email": "d.seloustev@adguard.com"
  },
  "homepage": "https://github.com/dseloustev/likbez",
  "repository": "https://github.com/dseloustev/likbez",
  "license": "MIT",
  "keywords": ["flutter", "dart", "architecture", "conventions", "skills"]
}
```

Create `plugins/likbez-ui/.claude-plugin/plugin.json` (same `author`/`homepage`/`repository`/`license`/`version` fields as above in every manifest below):

```json
{
  "name": "likbez-ui",
  "description": "Likbez UI cluster: adaptive and responsive layout, animations, widget previews, backend-driven UI, navigation and routing skills for Flutter.",
  "version": "0.1.0",
  "author": {
    "name": "Dmitry Seloustev",
    "email": "d.seloustev@adguard.com"
  },
  "homepage": "https://github.com/dseloustev/likbez",
  "repository": "https://github.com/dseloustev/likbez",
  "license": "MIT",
  "keywords": ["flutter", "ui", "layout", "animations", "navigation"]
}
```

Create `plugins/likbez-data/.claude-plugin/plugin.json`:

```json
{
  "name": "likbez-data",
  "description": "Likbez data cluster: networking, JSON serialization, internationalization, and Drift persistence skills for Flutter and Dart.",
  "version": "0.1.0",
  "author": {
    "name": "Dmitry Seloustev",
    "email": "d.seloustev@adguard.com"
  },
  "homepage": "https://github.com/dseloustev/likbez",
  "repository": "https://github.com/dseloustev/likbez",
  "license": "MIT",
  "keywords": ["flutter", "dart", "networking", "localization", "drift"]
}
```

Create `plugins/likbez-testing/.claude-plugin/plugin.json`:

```json
{
  "name": "likbez-testing",
  "description": "Likbez testing cluster: unit, widget, and integration testing, mocks, coverage, and static analysis skills for Flutter and Dart.",
  "version": "0.1.0",
  "author": {
    "name": "Dmitry Seloustev",
    "email": "d.seloustev@adguard.com"
  },
  "homepage": "https://github.com/dseloustev/likbez",
  "repository": "https://github.com/dseloustev/likbez",
  "license": "MIT",
  "keywords": ["flutter", "dart", "testing", "mocks", "coverage"]
}
```

Create `plugins/likbez-tooling/.claude-plugin/plugin.json`:

```json
{
  "name": "likbez-tooling",
  "description": "Likbez tooling cluster: runtime debugging, error fixing, Dart language idiom, CLI construction, and dependency management skills.",
  "version": "0.1.0",
  "author": {
    "name": "Dmitry Seloustev",
    "email": "d.seloustev@adguard.com"
  },
  "homepage": "https://github.com/dseloustev/likbez",
  "repository": "https://github.com/dseloustev/likbez",
  "license": "MIT",
  "keywords": ["dart", "flutter", "runtime", "cli", "dependencies"]
}
```

- [ ] **Step 4: Rewrite the marketplace file**

Replace the whole of `.claude-plugin/marketplace.json` with:

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
      "source": "./plugins/likbez",
      "description": "Core: project-setup advisor, ast-index policy, architecture and conventions."
    },
    {
      "name": "likbez-ui",
      "source": "./plugins/likbez-ui",
      "description": "UI: adaptive/responsive layout, animations, previews, BDUI, navigation."
    },
    {
      "name": "likbez-data",
      "source": "./plugins/likbez-data",
      "description": "Data: networking, serialization, localization, Drift persistence."
    },
    {
      "name": "likbez-testing",
      "source": "./plugins/likbez-testing",
      "description": "Testing: unit/widget/integration tests, mocks, coverage, static analysis."
    },
    {
      "name": "likbez-tooling",
      "source": "./plugins/likbez-tooling",
      "description": "Tooling: runtime debugging, error fixing, language idiom, CLI, dependencies."
    }
  ]
}
```

- [ ] **Step 5: Update the changelog**

In `CHANGELOG.md`, under `## [Unreleased]`, add:

```markdown
### Changed

- Restructured into a five-plugin marketplace (`likbez`, `likbez-ui`,
  `likbez-data`, `likbez-testing`, `likbez-tooling`) with lockstep versioning.
```

- [ ] **Step 6: Verify**

Run: `jq -r '.plugins[].name' .claude-plugin/marketplace.json`
Expected: the five names, in order: `likbez`, `likbez-ui`, `likbez-data`, `likbez-testing`, `likbez-tooling`.

Run: `for f in plugins/*/.claude-plugin/plugin.json; do jq -r '"\(.name) \(.version)"' "$f"; done`
Expected: five lines, each name with `0.1.0`; no JSON errors.

Run: `test -f .claude-plugin/plugin.json && echo STILL-THERE || echo GONE`
Expected: `GONE`.

- [ ] **Step 7: Commit**

```bash
git add -A .claude-plugin plugins CHANGELOG.md
git commit -m "chore: restructure into five-plugin marketplace skeleton"
```

---

### Task 2: Retarget docs to the cluster layout

**Files:**
- Modify: `CLAUDE.md`, `README.md`, `docs/design.md`, `docs/porting-plan.md`

**Interfaces:**
- Consumes: plugin names and `plugins/<name>/` roots from Task 1.
- Produces: porting-plan Phase 0.5 (marked done), Phase 5.5 section with five unticked checkboxes whose exact labels Tasks 3–6 tick: `project-setup`, `upstreams.md`, `upstream-sync`, `THIRD-PARTY-NOTICES.md`, `baseline reconciliation`.

- [ ] **Step 1: Update CLAUDE.md**

Apply these replacements (paragraph-for-paragraph):

1. In `## Project`, replace the sentence fragment `packaging a Flutter/Dart knowledge pack: 31 reference
and how-to skills plus the `ast-index` search policy.` with `packaging a Flutter/Dart knowledge pack: 33 skills across five cluster
plugins — `likbez` (core), `likbez-ui`, `likbez-data`, `likbez-testing`,
`likbez-tooling` — including the `ast-index` search policy and the
`project-setup` advisor.` and replace `its own single-plugin marketplace` with `its own five-plugin marketplace`.
2. In `## Source material`, replace the scrub-gate command's target `skills/` with `plugins/` (the command becomes `grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard" plugins/` → no hits).
3. In `## Conventions`, replace the bullet starting `- Plugin layout:` with:

```markdown
- Plugin layout: root `.claude-plugin/marketplace.json` lists five plugins; each
  plugin lives at `plugins/<plugin>/` with its own `.claude-plugin/plugin.json`
  and `skills/<name>/SKILL.md` (`references/`, `assets/`, `scripts/` subtrees
  preserved). Core skills surface as `/likbez:<name>`, cluster skills as
  `/likbez-ui:<name>` etc.
```

4. In `## Conventions`, replace the versioning bullet with:

```markdown
- Versioning: semver, **lockstep across all five plugins** — keep
  `CHANGELOG.md` and every `plugins/*/.claude-plugin/plugin.json` `version` in
  sync.
```

5. After the `## Source material` section, add a new section:

```markdown
## Maintenance

Skill updates flow from upstream repos through the repo-local `upstream-sync`
dev skill (`.claude/skills/upstream-sync/`), driven by the registry in
[docs/upstreams.md](docs/upstreams.md). It is repo tooling — never ship it
under `plugins/`.
```

6. Replace the body of `## Testing a change` with:

```markdown
Local smoke test: `/plugin marketplace add <path-to-this-repo>` then
`/plugin install likbez@likbez` (core); run `/likbez:project-setup` in a
sample project, install a recommended cluster, and confirm a routed skill
(e.g. `/likbez-data:flutter-drift`) can read its own `references/` files.
```

- [ ] **Step 2: Update README.md**

1. Replace the first paragraph's `a Flutter/Dart knowledge pack of 32 reference and how-to skills` with `a Flutter/Dart knowledge pack of 33 skills in five installable cluster
plugins — core (architecture, conventions, `ast-index`, the `project-setup`
advisor), UI, data, testing, and tooling`.
2. Replace the `## Install` section body with:

```markdown
    /plugin marketplace add dseloustev/likbez
    /plugin install likbez@likbez

Then run `/likbez:project-setup` inside your project: it detects your stack,
recommends the matching clusters (`likbez-ui`, `likbez-data`,
`likbez-testing`, `likbez-tooling`), and installs them with your approval.
Core skills surface as `/likbez:<name>`, cluster skills as
`/likbez-ui:<name>` etc.
```

3. In the `## What's inside` HTML comment, replace `one table per cluster` guidance with `one table per plugin (likbez core, likbez-ui, likbez-data, likbez-testing, likbez-tooling)` — the comment stays a comment (catalog is filled in Phase 6).

- [ ] **Step 3: Update docs/design.md**

1. Replace the `### Plugin layout` code block with:

```
likbez/
├── .claude-plugin/
│   └── marketplace.json     # five-plugin marketplace (sources: ./plugins/<name>)
├── plugins/
│   ├── likbez/              # core: project-setup, ast-index, conventions, architecture
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/<name>/   # SKILL.md + references/ assets/ scripts/
│   ├── likbez-ui/           # adaptive UI, layout, animations, previews, BDUI, navigation
│   ├── likbez-data/         # networking, serialization, l10n, Drift
│   ├── likbez-testing/      # unit/widget/integration tests, mocks, coverage, analysis
│   └── likbez-tooling/      # runtime, error fixing, idiom, CLI, dependencies
├── .claude/skills/          # repo-local dev tooling (upstream-sync) — not shipped
├── docs/                    # design, porting plan, source inventory, upstreams registry
├── THIRD-PARTY-NOTICES.md
├── CLAUDE.md · README.md · LICENSE · CHANGELOG.md
```

and after that block replace the paragraph starting `Skills keep their source names` so it reads:

```markdown
Skills keep their source names and surface namespaced by their plugin:
`/likbez:ast-index`, `/likbez-ui:flutter-navigation`, `/likbez-data:dart-drift`,
… The five plugins version in lockstep (one version, one CHANGELOG).
```

2. In `### The ast-index skill`, replace `ports
as a 32nd skill, `skills/ast-index/SKILL.md`` with `ports
as a core skill, `plugins/likbez/skills/ast-index/SKILL.md``.
3. In `### Scrub gate`, replace both commands and the scoping note: gate command target `skills/` → `plugins/`, `grep -rn "/Users/" skills/` → `grep -rn "/Users/" plugins/`, and `the gate is scoped to `skills/`` → `the gate is scoped to `plugins/``.
4. In `## Conventions`, replace the versioning bullet's `keep `CHANGELOG.md` and `.claude-plugin/plugin.json` `version` in
  sync` with `keep `CHANGELOG.md` and all five `plugins/*/.claude-plugin/plugin.json`
  versions in lockstep`.
5. In `## Versioning and publishing`, replace the smoke-test sentence with the same wording as CLAUDE.md's new `## Testing a change` body (core install → `/likbez:project-setup` → cluster → routed skill reads `references/`).

- [ ] **Step 4: Update docs/porting-plan.md**

1. After the `## Phase 0 — skeleton` section (after its `.gitignore` block), insert:

```markdown
## Phase 0.5 — cluster restructure

Done 2026-08-08 (see docs/superpowers/specs/2026-08-07-cluster-split-advisor-upstream-sync-design.md):

- [x] Five plugin manifests under `plugins/<name>/.claude-plugin/plugin.json`
      (`likbez`, `likbez-ui`, `likbez-data`, `likbez-testing`, `likbez-tooling`),
      lockstep version 0.1.0; root manifest removed.
- [x] `marketplace.json` rewritten to five entries with `./plugins/<name>` sources.
- [x] CLAUDE.md, README.md, design.md, and this plan retargeted to the cluster
      layout; scrub gate now scoped to `plugins/`.
```

2. In `## Port procedure`, replace step 1 with:

```markdown
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
```

3. In `## Port procedure` step 2, replace `grep -rniE "wallet|AW-[0-9]|aiguard|adguard" skills/<name>/` with `grep -rniE "wallet|AW-[0-9]|aiguard|adguard" plugins/<cluster>/skills/<name>/`.
4. Append the target cluster to each phase heading: `## Phase 1 — architecture & conventions (→ plugins/likbez/skills/)`, `## Phase 2 — UI, layout, navigation (→ plugins/likbez-ui/skills/)`, `## Phase 3 — data: networking, serialization, localization, persistence (→ plugins/likbez-data/skills/)`, `## Phase 4 — testing & quality (→ plugins/likbez-testing/skills/)`, `## Phase 5 — runtime, tooling, ast-index (→ plugins/likbez-tooling/skills/, ast-index → plugins/likbez/skills/)`.
5. In the Phase 5 ast-index item, replace `→
      `skills/ast-index/SKILL.md`` with `→
      `plugins/likbez/skills/ast-index/SKILL.md``.
6. After the Phase 5 section, insert:

```markdown
## Phase 5.5 — advisor & sync infrastructure

Designed in docs/superpowers/specs/2026-08-07-cluster-split-advisor-upstream-sync-design.md.

- [ ] `project-setup` advisor skill in `plugins/likbez/skills/project-setup/`.
- [ ] `docs/upstreams.md` registry (per-skill upstream, path, last-synced SHA, notes).
- [ ] `upstream-sync` dev skill in `.claude/skills/upstream-sync/` (repo-local, not shipped).
- [ ] `THIRD-PARTY-NOTICES.md` with the MIT and BSD-3 notices, verbatim from upstream LICENSE files.
- [ ] Baseline reconciliation: first `upstream-sync` run after Phases 1–5 —
      content-diff every skill against upstream HEAD, record starting SHAs in
      the registry.
```

7. In `## Phase 6 — publish`: replace the scrub-gate item's `skills/` targets with `plugins/` (both greps); replace the smoke-test item with `- [ ] Local marketplace smoke test: `/plugin marketplace add <path>` +
      `/plugin install likbez@likbez`; run `/likbez:project-setup` on a sample
      Flutter project (sane recommendations); install one recommended cluster;
      spot-check one routed skill (`/likbez-data:flutter-drift` reads its
      `references/`), one single-file skill, and `/likbez:ast-index`.`; replace the `**Resolve the MADTeacher licensing question**` item with `- [ ] Verify `THIRD-PARTY-NOTICES.md` matches the upstream LICENSE files
      (licensing resolved 2026-08-07 — see design.md decision log). Repo may go
      public once verified.`; replace `Fill README's skill catalog from the inventory clusters.` with `Fill README's skill catalog: one table per plugin.`
8. In `## Source → plugin map`, change the `Likbez` column values from `skills/` to the cluster path per the phase→cluster table (e.g. Phase 1 rows → `plugins/likbez/skills/`, Phase 2 rows → `plugins/likbez-ui/skills/`, Phase 3 → `plugins/likbez-data/skills/`, Phase 4 → `plugins/likbez-testing/skills/`, Phase 5 dart rows → `plugins/likbez-tooling/skills/`, ast-index row → `plugins/likbez/skills/ast-index/`).

- [ ] **Step 5: Verify**

Run: `grep -rn "skills/ast-index" docs/design.md docs/porting-plan.md CLAUDE.md README.md | grep -v "plugins/likbez"`
Expected: no output (all references retargeted).

Run: `grep -c "plugins/" docs/porting-plan.md`
Expected: a number ≥ 10 (retargeting present).

Run: `grep -n "Phase 0.5\|Phase 5.5" docs/porting-plan.md`
Expected: both headings present.

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md README.md docs/design.md docs/porting-plan.md
git commit -m "docs: retarget plan and conventions to the cluster layout"
```

---

### Task 3: `project-setup` advisor skill

**Files:**
- Create: `plugins/likbez/skills/project-setup/SKILL.md`
- Modify: `CHANGELOG.md`, `docs/porting-plan.md` (tick the Phase 5.5 `project-setup` box)

**Interfaces:**
- Consumes: plugin names from Task 1.
- Produces: skill name `project-setup` (surfaces as `/likbez:project-setup`) — referenced by README, CLAUDE.md (already written in Task 2), and Phase 6 smoke test.

- [ ] **Step 1: Create the skill**

Create `plugins/likbez/skills/project-setup/SKILL.md` with exactly this content:

````markdown
---
name: project-setup
description: >-
  Analyze a Dart/Flutter project and recommend which likbez cluster plugins
  (likbez-ui, likbez-data, likbez-testing, likbez-tooling) to enable for it.
  Use when the user asks to set up likbez, pick likbez skills for a project,
  configure likbez, or asks which likbez plugins their project needs. Detects
  the stack from pubspec.yaml and the project tree, asks what technologies
  are planned, then applies the choice only with explicit consent.
---

# Likbez project setup

Recommend the smallest useful set of likbez cluster plugins for the current
project, then apply it only after the user approves. Stay read-only until the
apply step.

## Step 1 — detect the stack

Collect signals. Missing files are signals too — never fail on them.

1. Find every `pubspec.yaml` outside hidden, build, and tool-cache
   directories. More than one means a monorepo: evaluate each package and
   union the results, noting which package triggered what.
2. For each pubspec, read `dependencies` and `dev_dependencies`.
3. Check for `l10n.yaml`, `test/`, `integration_test/`, and `bin/` next to
   each pubspec.

| Signal | Cluster | Reason shown to the user |
|---|---|---|
| `flutter` in `dependencies` | `likbez-ui`, `likbez-testing` | Flutter app baseline |
| no `flutter` dependency | `likbez-tooling` | pure-Dart baseline (CLI/server) |
| `drift`, `drift_flutter`, `drift_postgres`, or `drift_dev` | `likbez-data` | Drift persistence skills |
| `go_router` | `likbez-ui` | navigation and routing skills |
| `http`, `dio`, `retrofit`, or `chopper` | `likbez-data` | networking skills |
| `intl`, `flutter_localizations`, or an `l10n.yaml` file | `likbez-data` | localization skills |
| `flutter_duit` | `likbez-ui` | backend-driven UI skills |
| `test/` or `integration_test/` present; `mockito`, `checks`, or `coverage` | `likbez-testing` | testing skills |
| `bin/` containing `.dart` entrypoints | `likbez-tooling` | CLI construction skills |

The core plugin (`likbez`) is always part of the set — it is the plugin this
skill ships in, and its architecture, convention, and `ast-index` skills apply
to every Dart/Flutter project.

Dependencies not in the table are ignored — never block on an unrecognized
stack. If no `pubspec.yaml` exists, say this doesn't look like a Dart/Flutter
project and offer the cluster list for manual selection instead of a detected
recommendation.

## Step 2 — show the recommendation

Before asking anything, present a table: each recommended cluster, the exact
signals that triggered it (dependency name or path — with the package
qualifier in monorepos), and one line on what the cluster teaches. List the
non-recommended clusters too, marked "no signal found", so the user sees the
full menu.

## Step 3 — ask about planned technology

Ask one question: which of these does the user plan to add — a database, deep
links or web URLs, backend-driven UI, localization, HTTP APIs, CLI tooling,
or none? Map the answers through the same signal table and extend the
recommendation, marking those rows "planned" rather than "detected".

## Step 4 — apply, with explicit consent

Show the final set and offer exactly these modes:

1. **Print commands** — output one line per recommended cluster:

       /plugin install likbez-ui@likbez

2. **Write project settings** — after a separate confirmation, edit the host
   project's `.claude/settings.json`: under `enabledPlugins`, set
   `"<cluster>@likbez": true` for each chosen cluster and `false` for likbez
   clusters the user explicitly declined. Rules:
   - touch only keys ending in `@likbez`; never modify other plugins' entries;
   - never set the core `"likbez@likbez"` entry to `false`;
   - create the file or the `enabledPlugins` key if missing, preserving all
     existing content.
3. **Optional note** — after another confirmation, append to the host
   project's `CLAUDE.md`:

       ## Likbez skills

       This project uses likbez clusters: <list>. Consult the relevant
       `/likbez:<skill>` and `/<cluster>:<skill>` skills before implementing
       in their areas. Agents that don't inherit skills can read them by path
       under the installed plugin directories.

Afterwards report exactly what was changed. If the user declines writes,
mode 1's printed commands are the deliverable.

## Guardrails

- Read-only until the user approves an apply mode.
- Never uninstall or disable anything except explicitly declined `@likbez`
  clusters.
- Never edit `.claude/settings.local.json` or user-level settings.
- Recommendations are hints — the user's selection always wins.
````

- [ ] **Step 2: Verify**

Run: `head -3 plugins/likbez/skills/project-setup/SKILL.md`
Expected: `---`, `name: project-setup`, `description: >-`.

Run: `grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard" plugins/ ; grep -rn "/Users/" plugins/`
Expected: no output from either grep.

- [ ] **Step 3: Tick the Phase 5.5 box and update the changelog**

In `docs/porting-plan.md`, change `- [ ] \`project-setup\` advisor skill` to `- [x]`. In `CHANGELOG.md` under `## [Unreleased]`, add an `### Added` heading (if not present) with:

```markdown
- `project-setup` advisor skill (core): recommends and enables likbez
  clusters per project.
```

- [ ] **Step 4: Commit**

```bash
git add plugins/likbez/skills/project-setup/SKILL.md docs/porting-plan.md CHANGELOG.md
git commit -m "feat: add project-setup advisor skill"
```

---

### Task 4: `docs/upstreams.md` registry

**Files:**
- Create: `docs/upstreams.md`
- Modify: `CHANGELOG.md`, `docs/porting-plan.md` (tick the Phase 5.5 `upstreams.md` box)

**Interfaces:**
- Produces: upstream ids `MT`, `FT`, `DL`, `AW`; the `—` sentinel meaning "baseline pending"; table columns `Skill | Upstream | Upstream path | Last-synced | Notes` — the `upstream-sync` skill (Task 5) and `THIRD-PARTY-NOTICES.md` (Task 6) reference this file and these conventions.

- [ ] **Step 1: Create the registry**

Create `docs/upstreams.md` with exactly this content:

````markdown
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
````

- [ ] **Step 2: Verify**

Run: `grep -c "^| \`plugins/" docs/upstreams.md`
Expected: `33` (32 ported + project-setup).

Run: `grep -c "| MT |" docs/upstreams.md && grep -c "| FT |" docs/upstreams.md && grep -c "| DL |" docs/upstreams.md && grep -c "| AW |" docs/upstreams.md`
Expected: counts including the header tables: MT 11 (1 upstream row + 10 skills), FT 11 (1 + 10), DL 10 (1 + 9), AW 4 (1 + 3).

- [ ] **Step 3: Tick the Phase 5.5 box and update the changelog**

In `docs/porting-plan.md`, tick the `docs/upstreams.md` registry box. In `CHANGELOG.md` under `### Added`, add:

```markdown
- `docs/upstreams.md`: per-skill upstream registry (sync state + provenance).
```

- [ ] **Step 4: Commit**

```bash
git add docs/upstreams.md docs/porting-plan.md CHANGELOG.md
git commit -m "docs: add upstream sync registry"
```

---

### Task 5: `upstream-sync` dev skill

**Files:**
- Create: `.claude/skills/upstream-sync/SKILL.md`
- Modify: `CHANGELOG.md`, `docs/porting-plan.md` (tick the Phase 5.5 `upstream-sync` box)

**Interfaces:**
- Consumes: `docs/upstreams.md` columns and the `—` sentinel from Task 4; upstream ids MT/FT/DL/AW.
- Produces: the maintainer workflow later used for the baseline reconciliation (Phase 5.5's last box, which stays unticked until after Phases 1–5).

- [ ] **Step 1: Create the skill**

Create `.claude/skills/upstream-sync/SKILL.md` with exactly this content:

````markdown
---
name: upstream-sync
description: >-
  Maintainer skill for the likbez repo: sync shipped skills with their
  upstream repositories (MADTeacher/mad-agents-skills, flutter/agent-plugins,
  dart-lang/skills, and the ../adguard-wallet sibling). Use when asked to
  check upstreams for skill updates, run a skills sync, or run the baseline
  reconciliation. Repo tooling only — never ships in the plugin.
---

# Upstream sync

Fold upstream skill changes into likbez under operator control. The registry
at `docs/upstreams.md` is the single source of truth: per shipped skill — its
upstream, the last-synced upstream commit, and the genericization deltas that
must survive every merge.

## Step 1 — prepare upstream checkouts

In the session scratchpad (never inside this repo):

    git clone --filter=blob:none https://github.com/MADTeacher/mad-agents-skills
    git clone --filter=blob:none https://github.com/flutter/agent-plugins
    git clone --filter=blob:none https://github.com/dart-lang/skills

`../adguard-wallet` is used in place (no clone); record its current commit
with `git -C ../adguard-wallet rev-parse HEAD`. If a clone fails, skip that
upstream, mark its rows "unreachable" in the digest, and continue with the
rest.

## Step 2 — classify every registry row

For each row of `docs/upstreams.md` (skip rows whose Upstream is `—`):

- **Last-synced is `—` (baseline pending):** compare full content —
  `diff -r <clone>/<upstream-path> <skill-path>` — and sort every difference
  into either a genericization delta (record it in the Notes column) or an
  upstream change to adopt. This is baseline-reconciliation mode.
- **Last-synced is a SHA:** run
  `git -C <clone> diff <last-synced>..HEAD -- <upstream-path>`.
  Empty output → unchanged. Non-empty → changed. Path absent at HEAD →
  removed. If the recorded SHA is unknown to the clone (force-push), fall
  back to the full content diff and say so in the digest.

Also list **candidates**: upstream skill directories with no registry row.

## Step 3 — present the digest

One report, grouped: changed (skill, upstream, diff summary), candidates
(name + one-line description from its SKILL.md), removed, unreachable, and
unchanged (count only). Apply nothing yet. Candidates and removals are
curation decisions for the operator: accepting one requires a design.md
decision-log entry and its own port through the standard procedure — never
part of the same sync commit.

## Step 4 — apply approved changes

Per approved skill, in its own commit:

1. Apply the upstream diff onto the likbez copy by hand — never `cp -R` over
   it. Re-apply every genericization delta listed in the Notes column.
2. Keep `metadata.author` frontmatter byte-identical where the Notes require
   preserving it.
3. Gates — all must pass, or the merge does not land (revert the skill and
   report):

       grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard" plugins/   # no output
       grep -rn "/Users/" plugins/                                          # no output

   and every relative link inside the skill resolves.
4. Commit: `feat: sync <skill> with upstream` (subject only).

## Step 5 — record the sync

1. Update the Last-synced column of every row checked this run — including
   unchanged ones ("checked at" is the meaning) — to the clone's
   `git rev-parse HEAD` (AW rows: the wallet SHA from step 1).
2. Add a CHANGELOG entry under Unreleased naming the synced skills.
3. If any shipped skill changed, bump the lockstep version in all five
   `plugins/*/.claude-plugin/plugin.json` files — they must stay identical.
4. Commit: `chore: record upstream sync`.

## Rules

- `dart-*` skills sync from `dart-lang/skills` only; the copies inside
  `flutter/agent-plugins` are ignored by design.
- Nothing is ever auto-added or auto-removed; every change under `plugins/`
  goes through operator approval.
- This skill is repo tooling — it must never be moved under `plugins/`.
````

- [ ] **Step 2: Verify**

Run: `head -2 .claude/skills/upstream-sync/SKILL.md && grep -c "docs/upstreams.md" .claude/skills/upstream-sync/SKILL.md`
Expected: `---` + `name: upstream-sync`, then a count ≥ 2.

Run: `git check-ignore .claude/skills/upstream-sync/SKILL.md ; echo "ignored=$?"`
Expected: `ignored=1` (NOT gitignored).

- [ ] **Step 3: Tick the Phase 5.5 box and update the changelog**

In `docs/porting-plan.md`, tick the `upstream-sync` box. In `CHANGELOG.md` under `### Added`, add:

```markdown
- `upstream-sync` repo-local dev skill for folding upstream skill changes in.
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/upstream-sync/SKILL.md docs/porting-plan.md CHANGELOG.md
git commit -m "feat: add upstream-sync dev skill"
```

---

### Task 6: `THIRD-PARTY-NOTICES.md`

**Files:**
- Create: `THIRD-PARTY-NOTICES.md`
- Modify: `README.md` (license section), `CHANGELOG.md`, `docs/porting-plan.md` (tick the Phase 5.5 notices box)

**Interfaces:**
- Consumes: `docs/upstreams.md` as the provenance table (Task 4).
- Produces: the notices file Phase 6 verifies before going public.

- [ ] **Step 1: Fetch the upstream license texts verbatim**

The notices must carry the upstreams' license texts **byte-for-byte**, not from memory:

```bash
cd "$SCRATCHPAD"   # any scratch dir outside the repo
curl -sfL https://raw.githubusercontent.com/MADTeacher/mad-agents-skills/HEAD/LICENSE -o mt-LICENSE
curl -sfL https://raw.githubusercontent.com/flutter/agent-plugins/HEAD/LICENSE -o ft-LICENSE
curl -sfL https://raw.githubusercontent.com/dart-lang/skills/HEAD/LICENSE -o dl-LICENSE
head -3 mt-LICENSE ft-LICENSE dl-LICENSE
```

Expected: MIT header with `Stanislav Chernyshev`; BSD headers with `The Flutter Authors` / `the Dart project authors`. If a fetch fails, clone the repo (`git clone --depth 1`) and copy its `LICENSE` file instead. If a fetched text contradicts the expectations above, STOP and report — do not guess.

- [ ] **Step 2: Create the notices file**

Create `THIRD-PARTY-NOTICES.md`:

````markdown
# Third-party notices

Likbez redistributes skills that originate from third-party repositories, in
genericized form. Per-skill provenance — which skill came from which upstream
— is tracked in [docs/upstreams.md](docs/upstreams.md); skills with
third-party authorship additionally carry `metadata.author` in their
frontmatter. The upstream license texts follow verbatim.

## MADTeacher/mad-agents-skills — MIT License

<verbatim content of mt-LICENSE>

## flutter/agent-plugins — BSD 3-Clause License

<verbatim content of ft-LICENSE>

## dart-lang/skills — BSD 3-Clause License

<verbatim content of dl-LICENSE>
````

where each `<verbatim content of …>` placeholder is replaced by the exact text fetched in Step 1 (no reformatting, no re-wrapping).

- [ ] **Step 3: Point README at the notices**

In `README.md`, replace the `## License` section body with:

```markdown
MIT for likbez itself. Ported skills originate from third-party repositories
under MIT and BSD 3-Clause — see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)
and the per-skill provenance in [docs/upstreams.md](docs/upstreams.md). Nine+
skills also carry author attribution in their frontmatter (see
[docs/design.md](docs/design.md), "Attribution and licensing").
```

- [ ] **Step 4: Verify**

Run: `grep -c "License" THIRD-PARTY-NOTICES.md && grep -n "Chernyshev\|Flutter Authors\|Dart project authors" THIRD-PARTY-NOTICES.md | head -5`
Expected: all three copyright holders present.

Run: `grep -n "THIRD-PARTY-NOTICES" README.md`
Expected: one hit in the License section.

- [ ] **Step 5: Tick the Phase 5.5 box and update the changelog**

In `docs/porting-plan.md`, tick the `THIRD-PARTY-NOTICES.md` box. In `CHANGELOG.md` under `### Added`, add:

```markdown
- `THIRD-PARTY-NOTICES.md` with the upstream MIT and BSD-3 license texts.
```

- [ ] **Step 6: Commit**

```bash
git add THIRD-PARTY-NOTICES.md README.md docs/porting-plan.md CHANGELOG.md
git commit -m "docs: add third-party notices"
```

---

## Not in this plan

- **Phases 1–5 (porting the 31 skills + ast-index)** — governed by `docs/porting-plan.md`, now retargeted to `plugins/<cluster>/skills/`.
- **Baseline reconciliation** (Phase 5.5's last box) — the first `upstream-sync` run; requires the ported skills, so it happens after Phases 1–5.
- **README skill catalog, smoke test, going public** — Phase 6.
