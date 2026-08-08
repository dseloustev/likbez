---
name: flutter-conventions
description: >-
  Flutter convention checklist for the subset DCM/analyzer do NOT enforce.
  MANUAL/COMPOSED ONLY — loaded by the implementer before coding and by the
  reviewer's convention lens; not auto-fired.
argument-hint: "[optional: paths of a diff to check]"
disable-model-invocation: true
---

Composed by Read, not the Skill tool: `disable-model-invocation: true` hides this skill from
model-side Skill-tool invocation, and subagents do not inherit skills — agents consume it by
Read-ing this file and `checklist.md` by path in their prompts. User slash-command invocation
still works.

Load `checklist.md` (same directory) and apply it:

- **Implement time:** before proposing code, read `## must-read` and design so no item is violated.
- **Review time:** for each changed file in the diff, walk `## must-read`; every hit is a finding
  (convention-fit lens). `## dcm-caught` is informational — the analyzer/DCM gate already enforces
  those; do not re-report them manually.

Sources of truth (the checklist cites, never contradicts): the host project's `CLAUDE.md` and
convention/code-style docs. On any conflict, fix the checklist.
