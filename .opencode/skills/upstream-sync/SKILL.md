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

       grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard" plugins/ --exclude=plugin.json   # no output
       grep -rn "/Users/" plugins/                                                                # no output

   and every relative link inside the skill resolves.
4. Commit: `feat: sync <skill> with upstream` (subject only).

## Step 5 — record the sync

1. Update the Last-synced column of every row checked this run — including
   unchanged ones ("checked at" is the meaning) — to the clone's
   `git rev-parse HEAD` (AW rows: the wallet SHA from step 1).
2. Add a CHANGELOG entry under Unreleased naming the synced skills.
3. Do not touch the `version` fields in `plugins/*/.claude-plugin/plugin.json`
   — the lockstep bump happens at release time via the `bump-version` dev
   skill, which reads the CHANGELOG entry from step 2 to size it.
4. Commit: `chore: record upstream sync`.

## Rules

- `dart-*` skills sync from `dart-lang/skills` only; the copies inside
  `flutter/agent-plugins` are ignored by design.
- Shipped skills carry no model pinning. Strip `metadata.model` and any
  top-level `model` from an incoming upstream change, and drop a `metadata:`
  block left holding nothing else. Every skill runs on the host session's
  model; upstream values (Claude aliases and Gemini ids alike) never land.
- Nothing is ever auto-added or auto-removed; every change under `plugins/`
  goes through operator approval.
- This skill is repo tooling — it must never be moved under `plugins/`.
