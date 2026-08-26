# OpenCode host

Likbez runs on OpenCode as a generated build: the canonical Claude Code plugin tree is
transformed by `scripts/build_opencode.py` and placed into OpenCode's discovery
directories by `scripts/install-opencode.sh`. This doc is the operator guide for that
host; everything else in `docs/` describes the knowledge itself, which is identical on
both hosts.

## Install

From a likbez checkout:

```bash
scripts/install-opencode.sh           # install / refresh
scripts/install-opencode.sh --remove  # uninstall
```

This generates the OpenCode build into `<checkout>/opencode/dist/` (gitignored) and
places it into `~/.config/opencode/skills/likbez-<skill>/` — one directory per skill,
each with its `references/`, `assets/` and `scripts/` subtrees. Restart OpenCode after
installing. Respects `XDG_CONFIG_HOME`.

There is no marketplace and no namespace on OpenCode: skills surface as
`likbez-<skill>` (TUI: `/likbez-<skill>` is available once a matching command wrapper
exists — otherwise load them with the `skill` tool). The cluster grouping
(`/likbez-ui:<skill>` on Claude Code) is flattened: every skill is `likbez-<skill>`.

## How it works

The generator makes three transformations per skill and nothing else:

1. **Prefixing** — `flutter-drift` becomes `likbez-flutter-drift`, safe against other
   packs in OpenCode's shared flat directory.
2. **Frontmatter remap** — `name` is prefixed; `description` is folded to one quoted
   line (≤ 1024 chars); Claude-behavioral keys (`argument-hint`,
   `disable-model-invocation`, `allowed-tools`, `model`) are dropped, and so are
   Claude-only keys booked inside `metadata:` (e.g. `metadata.model`); the rest of
   the `metadata:` block (`metadata.author`, `version`, `last_modified`) is preserved
   verbatim — nine skills carry third-party `metadata.author`
   attribution that must survive any port (see design.md, "Attribution and licensing").
3. **Host glossary** — a short `<OPENCODE-HOST-NOTES>` block is prepended to every
   body, mapping the Claude Code dialect (`/likbez:<skill>` commands, `CLAUDE.md`)
   onto OpenCode equivalents.

`project-setup` additionally carries a host note: its advice to write
`.claude/settings.json` / `enabledPlugins` is Claude Code-specific, so on OpenCode the
skill recommends the repository README instead of host config writes.

Claude Code operation is unchanged by construction: the generator never writes outside
its `--out` directory, and the canonical `plugins/` tree is untouched.

## Differences from Claude Code

| Aspect | Claude Code | OpenCode |
|---|---|---|
| Installation | `/plugin marketplace add` + `/plugin install <cluster>@likbez` | `scripts/install-opencode.sh` |
| Invocation | `/likbez:<skill>` per cluster | the `likbez-<skill>` skill (flat) |
| Selective clusters | enable only the clusters you want | all 32 skills install together |
| `project-setup` | recommends clusters and enables them in host config | recommends only; points at the README |

## Troubleshooting

- **A skill does not appear** — check `~/.config/opencode/skills/likbez-<skill>/SKILL.md`
  exists, its frontmatter `name` matches the directory, and restart OpenCode.
- **Stale skills after an update** — re-run `scripts/install-opencode.sh`; it replaces
  every `likbez-*` directory.
