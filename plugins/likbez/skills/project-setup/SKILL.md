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
links or web URLs, backend-driven UI, localization, HTTP APIs, runtime debugging, CLI tooling,
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
