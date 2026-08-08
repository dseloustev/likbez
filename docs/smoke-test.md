# Local marketplace smoke test

The Phase 6 install gate: verifies the five-plugin marketplace installs from a
local checkout and that skills load, route, and read their own files. All
`/plugin` and `/likbez:*` commands are interactive host commands — run them
yourself in a Claude Code session; an agent cannot run them for you.

## Prerequisites

- Claude Code with plugin support.
- This repo checked out locally — `<likbez-repo>` below stands for its path.
- A sample Flutter project (e.g. `flutter create smoke_sample`). A bare app
  triggers only the Flutter baseline recommendation (`likbez-ui`,
  `likbez-testing`); add a dependency from the `project-setup` signal table
  (e.g. `dart pub add http` or `drift`) so a data-cluster recommendation can
  be checked too.

## Steps

Each step lists the expected result; any deviation is a finding.

1. **Add the marketplace**

       /plugin marketplace add <likbez-repo>

   Expect: the marketplace registers with all five plugins listed — `likbez`,
   `likbez-ui`, `likbez-data`, `likbez-testing`, `likbez-tooling`.

2. **Install the core plugin**

       /plugin install likbez@likbez

   Expect: core skills appear under the `likbez:` namespace —
   `project-setup`, `ast-index`, `flutter-architecture`,
   `flutter-apply-architecture-best-practices`, `flutter-conventions`.
   Note: `flutter-conventions` is manual/composed-only
   (`disable-model-invocation: true`) — it won't auto-fire, but invoking it
   as a slash command must still work.

3. **Run the advisor in the sample project**

       /likbez:project-setup

   Expect, in order: a detection table naming the exact pubspec/path signal
   per recommended cluster; non-recommended clusters listed as "no signal
   found"; one question about planned technologies; then the three apply
   modes (print commands / write `.claude/settings.json` / CLAUDE.md note),
   each gated on explicit consent. Sane recommendations for the sample: the
   Flutter baseline plus whatever signal dependency was added. Nothing is
   written without approval.

4. **Install one recommended cluster**

       /plugin install likbez-data@likbez

   Expect: cluster skills appear under the `likbez-data:` namespace.

5. **Spot-check a routed skill** — invoke `/likbez-data:flutter-drift` and
   ask a topic question (e.g. "How do I set up Drift migrations?").
   Expect: the skill Reads its own `references/` files from the installed
   plugin directory (watch for Read calls into
   `…/skills/flutter-drift/references/`) instead of answering from memory.

6. **Spot-check a single-file skill** — e.g.
   `/likbez-data:flutter-use-http-package`. Expect: the skill body loads and
   visibly shapes the answer (platform permissions, background parsing).

7. **Spot-check the search policy** — `/likbez:ast-index`. Expect: the full
   policy loads, including the verbatim subagent prompt block.

8. **Cleanup (optional)** — uninstall the test plugins and remove the
   marketplace entry; revert the sample project's `.claude/settings.json` /
   `CLAUDE.md` if apply modes 2–3 were exercised in step 3.

## Recording the result

On a full pass, tick the smoke-test checkbox in
[porting-plan.md](porting-plan.md) Phase 6. On any failure, fix the skill or
manifest, commit, and rerun from step 1 (marketplace add picks up the new
state of the checkout).
