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
