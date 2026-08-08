---
name: ast-index
description: >-
  Mandatory-first code search policy for projects with the ast-index CLI:
  ast-index before Grep, outline before reading large files, index-freshness
  rules, scope filters, empty-result triage, and a verbatim prompt block to
  paste into subagent prompts (subagents do not inherit these rules). Use when
  searching code, finding symbols/usages/implementations, or spawning a
  code-search subagent in an ast-index-enabled project.
---

# ast-index Rules

## Keep the index up to date

Run `ast-index update` after `git pull` / merge / rebase, and after completing a plan that changed Dart code — it
reindexes only changed files (seconds, not minutes). For a fresh clone, run `ast-index rebuild` once.

## Mandatory search rules

1. **ALWAYS use ast-index FIRST** for any code-search task.
2. **NEVER duplicate results** — if ast-index returned hits, that IS the complete answer. Do not re-run grep to
   "double-check".
3. Use the Grep tool **only when** ast-index returned empty, or for regex / string-literal patterns that are not
   symbol names, or for matches inside comments.

## Mandatory read rules

1. **Before `Read`-ing any file over 500 lines, run `ast-index outline <file>` first.**
2. Use the outline to locate the specific symbol / line range you need, then `Read` that slice via `offset` / `limit`.
3. Never bulk-read large files without an outline — it wastes the agent's context window and produces worse answers.

## Rules for subagents

When you spawn a subagent for code search (via the Agent / Task tool), the subagent does **not** inherit this file.
Include the block below verbatim in the subagent's prompt:

```
Use `ast-index` via Bash for code search (NOT grep / the Grep tool):
  ast-index search "query"           — universal search
  ast-index file "Name"              — find a file by name fragment
  ast-index symbol "Name"            — find a symbol definition
  ast-index class "Name"             — find a class / mixin / interface
  ast-index usages "Name"            — every usage of a symbol
  ast-index callers "func"           — functions that call this one
  ast-index implementations "Iface"  — concrete implementers of an interface
  ast-index refs "Name"              — cross-references (defs + imports + usages)
Use Grep ONLY if ast-index returned empty, for regex, or for string literals / comments.

Before Read-ing any file over 500 lines, FIRST run
  ast-index outline <file>
to get its structure, then Read only the targeted slice via offset/limit.
Never bulk-read large files.
```

## Why ast-index

ast-index is 17–69× faster than grep (1–10ms vs 200ms–3s) and returns structured, accurate results.

## Command cheat sheet

Full command list and flags: `ast-index --help`. Beyond the subagent block above, note `call-tree`, `hierarchy`,
`deps`/`dependents`, `changed` (branch vs trunk — useful for PR descriptions), and `todo`.

## Scoping searches

All symbol-returning commands accept scope filters — use them to kill noise:

```bash
ast-index usages "Config" --module lib/data            # only within one module
ast-index search "retry" --in-file http_client.dart    # only inside this file
ast-index symbol "User" --type class                   # only class-kind symbols
```

## When ast-index returns empty

Legitimate reasons:

- Symbol genuinely doesn't exist in the codebase.
- Index is stale — run `ast-index update` and retry.
- Generated symbol behind `part`/codegen (freezed, json_serializable, drift, openapi). After your project's codegen
  command, run `ast-index update` so generated `.g.dart` / `.freezed.dart` parts are reindexed.
- You're searching for a string literal, content inside a comment, or a regex pattern — use Grep instead.

Do **not** fall back to bulk `Read` of files in these cases. Use Grep with a specific pattern.

## Index management

- `ast-index rebuild` — full reindex (run once after clone).
- `ast-index update` — incremental reindex; run after pull/merge/rebase or after completing a plan that changed Dart
  code.
- `ast-index stats` — show index statistics.
