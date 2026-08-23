# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

**Likbez** — a Claude Code plugin packaging a Flutter/Dart knowledge pack: 33 skills across five cluster
plugins — `likbez` (core), `likbez-ui`, `likbez-data`, `likbez-testing`,
`likbez-tooling` — including the `ast-index` search policy and the
`project-setup` advisor. Companion to
[artel](https://github.com/dseloustev/artel) (the workflow plugin): the crew works,
likbez educates it. This repo is both the plugin and its own five-plugin marketplace
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
`grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard" plugins/ --exclude=plugin.json` → no hits.

## Maintenance

Skill updates flow from upstream repos through the repo-local `upstream-sync`
dev skill (`.claude/skills/upstream-sync/`), driven by the registry in
[docs/upstreams.md](docs/upstreams.md). Releases are cut with the repo-local
`bump-version` dev skill (`.claude/skills/bump-version/`): it sizes the semver
bump from `[Unreleased]`, writes the five manifests and the CHANGELOG in
lockstep, commits, and tags — never pushes. Both are repo tooling — never ship
them under `plugins/`.

## Conventions

- Plugin layout: root `.claude-plugin/marketplace.json` lists five plugins; each
  plugin lives at `plugins/<plugin>/` with its own `.claude-plugin/plugin.json`
  and `skills/<name>/SKILL.md` (`references/`, `assets/`, `scripts/` subtrees
  preserved). Core skills surface as `/likbez:<name>`, cluster skills as
  `/likbez-ui:<name>` etc.
- Skills are **knowledge, not process** — no agents, no hooks, no orchestration, no host
  state, no config (single recorded exception: `project-setup` — see design.md decision
  log). If a skill seems to need any of those, stop and record a decision.
- Preserve `metadata.author` frontmatter verbatim — 9 skills carry third-party
  attribution (see design.md, "Attribution and licensing").
- All docs and commit messages in English. No absolute paths — repo-relative paths or
  the `../adguard-wallet` / `../artel` sibling convention only.
- Commits: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`). Subject line only,
  no trailers.
- Versioning: semver, **lockstep across all five plugins** — keep
  `CHANGELOG.md` and every `plugins/*/.claude-plugin/plugin.json` `version` in
  sync.

## Publishing

Repo home: `https://github.com/dseloustev/likbez` (corporate account, **private until
the Phase 6 notices verification and go-public call (licensing itself is resolved — see
design.md decision log)**). `gh` operations need the corporate profile:
`GH_CONFIG_DIR=~/.config/gh-adguard gh …`. Git identity for commits
here is the corporate one (`d.seloustev@adguard.com`, set in local git config).

## Testing a change

Local smoke test: `/plugin marketplace add <path-to-this-repo>` then
`/plugin install likbez@likbez` (core); run `/likbez:project-setup` in a
sample project, install a recommended cluster, and confirm a routed skill
(e.g. `/likbez-data:flutter-drift`) can read its own `references/` files.
Full step-by-step procedure with expected results:
[docs/smoke-test.md](docs/smoke-test.md).
