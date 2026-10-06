---
name: bump-version
description: "Use when cutting a release of likbez itself — bumping the lockstep version across the five plugin manifests, dating the CHANGELOG, committing, and tagging. Repo tooling only, never shipped under plugins/."
metadata:
  opencode/autoinvoke: false
---

## Overview

`bump-version` performs **this repository's own release chore**. It is repo-local by design: its
logic is specific to likbez's six version carriers — `CHANGELOG.md` plus the five
`plugins/<plugin>/.claude-plugin/plugin.json` manifests (`likbez`, `likbez-ui`, `likbez-data`,
`likbez-testing`, `likbez-tooling`), which version in **lockstep** — and it is not part of the
shipped plugins. It never runs against a host project.

It is a **worker that runs inline** — plain `git` and file edits, no agent delegation. Because it
writes files, commits, and tags, it is user-invoked only: `metadata.opencode/autoinvoke: false`
keeps it out of the model's skill list, so load it explicitly — mention `@bump-version` in the
request, carrying the optional bump when there is one (e.g. `@bump-version patch`).

The skill stops at the tag. Pushing and publishing a GitHub release stay a deliberate manual step.
The local smoke test ([docs/smoke-test.md](../../../docs/smoke-test.md)) is the operator's
pre-release check; this skill does not run it.

## Steps

Run the steps in order. Each later step assumes the previous one succeeded.

### Step 1: Preflight

Every check except the branch check (3) is **fatal**. Run all five before reporting — the user
should see every failure in one pass — then report what failed and stop, changing nothing:

1. **Right repo.** `grep -c '"source": "./plugins/' .claude-plugin/marketplace.json` prints `5`,
   the five `plugins/*/.claude-plugin/plugin.json` manifests exist, and `CHANGELOG.md` exists at
   the repo root. If not, this is not the likbez checkout.
2. **Clean tree.** `git status --porcelain` is empty. A release commit must contain only the bump;
   never stash, never commit someone else's work-in-progress alongside it. If the tree is dirty,
   list what is uncommitted and let the user decide.
3. **On `main`.** `git rev-parse --abbrev-ref HEAD` is `main`. If it is not, **ask** before
   continuing rather than refusing outright — a release from another branch is unusual but the
   user's call. This is the one preflight check the user can wave through.
4. **Lockstep intact.** `grep -ho '"version": *"[^"]*"' plugins/*/.claude-plugin/plugin.json | sort -u`
   prints exactly one line. Drift between the five manifests is fatal: print all five values and
   stop. Repairing drift is its own commit, never folded into a release.
5. **Scrub gate passes.**
   `grep -rniE "wallet|AW-[0-9]|aiguard|adguard|mcp__aiguard" plugins/ --exclude=plugin.json`
   prints nothing (exit status 1). Any hit is a source-project literal that must not ship; list the
   hits and halt the release. This is likbez's release gate — the repo has no test suite.

### Step 2: Read the current state

1. `CURRENT_VERSION` — the shared `version` value of the five manifests (identical after Step 1).
   These are the **only** files in the repo carrying a version: `.claude-plugin/marketplace.json`
   has no `version` field, so there is nothing to keep in sync there. Do not add one.
2. `CURRENT_TAGGED` — whether `git tag -l "v<CURRENT_VERSION>"` prints anything. Empty means the
   version the manifests already carry has never been cut.
3. `UNRELEASED_BODY` — everything in `CHANGELOG.md` between the `## [Unreleased]` heading and the
   next `## [` heading (or end of file). Note which `### ` subsections it contains
   (`Added`, `Changed`, `Fixed`, `Removed`, …).
4. If `UNRELEASED_BODY` has no entries, **stop**: there is nothing to release. Say so plainly
   rather than cutting an empty version.
5. `DATE` — the output of `date +%F`. Read the date from the system, never from memory or an
   assumption about today.

### Step 3: Decide the new version

**Requested bump:** the version or bump word carried by the request that led here — `x.y.z`,
`major`, `minor`, or `patch` — blank when the request named none. It decides how `NEW_VERSION`
is reached:

| Argument | Behaviour |
|----------|-----------|
| `x.y.z` | Used verbatim. Validate: well-formed semver, and strictly greater than `CURRENT_VERSION` — **or equal to it when `CURRENT_TAGGED` is false** (finalize, below). Either check failing is fatal. |
| `major` / `minor` / `patch` | Computed from `CURRENT_VERSION`. Honoured **verbatim, including pre-1.0** — an explicit `major` on `0.x` yields `1.0.0`. That is the user overriding the inference below, on purpose. |
| *(blank)* | Inferred: finalize if `CURRENT_TAGGED` is false, otherwise from `UNRELEASED_BODY` per the table below. |

**Finalize mode** — `CURRENT_TAGGED` is false and no argument was given: `NEW_VERSION` **is**
`CURRENT_VERSION`. The manifests already name the version to cut (the first release, or a version
pre-set in a sync commit); the release only dates the CHANGELOG, and the manifests are left
untouched. Say explicitly that this is what is happening.

**Inference** — `CURRENT_TAGGED` is true and no argument was given:

- **`CURRENT_VERSION` is `0.x`**: a `Removed` section or any entry describing a breaking change →
  **minor**; an `Added` section → **minor**; only `Changed` / `Fixed` / documentation entries →
  **patch**. Pre-1.0, breaking changes ride a minor bump — semver's own convention.
- **`CURRENT_VERSION` is `1.0.0` or later**: `Removed`/breaking → **major**; `Added` → **minor**;
  otherwise → **patch**.

Next, verify `git tag -l "v<NEW_VERSION>"` is empty (already established in finalize mode). An
existing tag for that version is fatal.

Then, before writing anything: **present the proposed version and the reasoning that produced it**
— finalize vs. explicit argument vs. which inference rule fired, which subsections were seen,
whether the five manifests will change, and the `DATE` about to be stamped — and **wait for an
explicit yes**. This is the skill's only pause, and it is not optional, including when the argument
named the version explicitly (confirming a typo'd `1.2.3` costs one line; an unwanted tag costs
more). Anything other than an explicit yes — a no, a question, no answer at all — means stop with
nothing written.

### Step 4: Write the carriers

1. **The five manifests** — only when `NEW_VERSION` differs from `CURRENT_VERSION`: replace the
   `version` value in each `plugins/*/.claude-plugin/plugin.json` with `NEW_VERSION`. A targeted
   edit of that one field per file: preserve key order, indentation, and trailing newline. Do not
   reformat the JSON. In finalize mode the manifests are not touched at all.
2. **`CHANGELOG.md`** — retitle the existing `## [Unreleased]` heading to
   `## [<NEW_VERSION>] - <DATE>` (the `DATE` read in Step 2), and insert a fresh
   `## [Unreleased]` heading above it, followed by a blank line and no placeholder subsections.
   - The released section's body is untouched: the entries move under the version heading exactly
     as written.
   - This CHANGELOG carries **no link-reference definitions** at the bottom (no `[Unreleased]: …`
     compare links, no `[x.y.z]: …` tag links). Do not invent them.

Nothing else is edited in this step — not `docs/porting-plan.md` checkboxes, not the decision log,
not the README. Those are separate commits if they are due at all.

### Step 5: Verify, then commit

1. Re-read the carriers. Confirm `grep -h '"version"' plugins/*/.claude-plugin/plugin.json | sort -u`
   prints exactly one line carrying `NEW_VERSION`, that `CHANGELOG.md` now has exactly one
   `## [<NEW_VERSION>] - <DATE>` heading and one empty `## [Unreleased]` above it, and that no
   other content moved.
2. Show the user `git diff`.
3. Stage exactly the carriers and commit them together:
   `git add CHANGELOG.md plugins/*/.claude-plugin/plugin.json` (in finalize mode only
   `CHANGELOG.md` has changed; the glob is harmless) then
   `git commit -m "chore(release): v<NEW_VERSION>"`.
   Name the paths explicitly rather than using `git add -A` or `git commit -a` — the tree was clean
   at Step 1, so the two are equivalent today, but an explicit stage keeps that true if a later
   step ever writes something else. **Subject line only, no trailers** — the repo's commit
   convention (`CLAUDE.md`, "Conventions") overrides any harness default of appending co-author
   trailers.

### Step 6: Tag

`git tag -a "v<NEW_VERSION>" -m "v<NEW_VERSION>"` — annotated, on the commit just made.

If tagging fails after the commit landed, say so explicitly: the release commit exists and only the
tag is missing, which the user fixes with a single command. Do not attempt to unwind the commit.

### Step 7: Report

Print a concise summary:

- `CURRENT_VERSION` → `NEW_VERSION`, and how it was decided (finalize, explicit argument, or which
  inference rule fired).
- The release date stamped into the CHANGELOG, and how many entries (list items) moved under it.
- Which carriers changed (six, or only the CHANGELOG in finalize mode).
- The commit SHA and the tag name.
- The manual follow-up, as a command to copy — **printed, not run**:
  `git push origin main --follow-tags`
- A reminder that publishing a GitHub release is separate, and that `gh` against this repo needs the
  corporate profile: `GH_CONFIG_DIR=~/.config/gh-adguard gh …`.

## Rules

- **Never push, never publish.** The skill's last action is the tag. Pushing to `origin` and
  creating a GitHub release are outward-facing and stay with the user.
- **One pause, always.** Step 3 confirms the version before any file is written. Everything before
  that pause is read-only; everything after it is mechanical.
- **The CHANGELOG is the source of truth for the bump size.** The inference reads what is actually
  written in `[Unreleased]` — it does not re-derive the release's significance from `git log`.
- **Six carriers, no more.** The five manifests and `CHANGELOG.md`. If a seventh file ever starts
  carrying the version, this skill is where that gets added — and `marketplace.json` deliberately
  is not one.
- **The release commit carries only the carriers.** No doc updates, no checkbox ticks, no decision
  log entries ride along.
- **Fail loudly, change nothing.** Every preflight failure and every validation failure stops the
  skill before the first write. There is no partial release.
- **Not idempotent — do not re-run blindly.** A second run on an unchanged tree stops at Step 2's
  empty-`[Unreleased]` check, and a re-run after adding entries would cut a further version. To
  redo a botched release, undo the commit and tag first.

## Examples

- `@bump-version` with the manifests at `0.1.0` and no `v0.1.0` tag — finalize: propose
  `0.1.0 → 0.1.0`, confirm, date the CHANGELOG, commit, tag. Manifests untouched.
- `@bump-version` after `v0.1.0` is tagged and `[Unreleased]` has an `Added` section — propose
  `0.1.0 → 0.2.0`, confirm, then write all six carriers, commit, tag.
- `@bump-version patch` — force `0.1.0 → 0.1.1` regardless of what the section contains.
- `@bump-version 1.0.0` — the first stable release: validated as semver and greater than current,
  then confirmed like any other.
