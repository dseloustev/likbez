#!/usr/bin/env python3
"""Generate the OpenCode build of likbez: `likbez-`-prefixed skill directories
under <out> (default <source>/opencode/dist).

OpenCode discovers skills from flat config directories (~/.config/opencode/skills)
with no plugin namespace, so every generated skill directory is prefixed `likbez-`.
Each generated SKILL.md keeps the canonical body with a prepended host glossary and
a remapped frontmatter: name is prefixed, description is folded to one quoted line,
Claude-behavioral keys (argument-hint, disable-model-invocation, allowed-tools,
model) are dropped — including Claude-only keys booked inside `metadata:` — and the
`metadata:` block is otherwise preserved verbatim (nine skills carry third-party
attribution — see docs/design.md, "Attribution and licensing").
references/, assets/, scripts/ and examples/ subtrees are copied alongside unchanged.
Canonical sources are never modified. Contract: docs/opencode.md.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

GLOSSARY = """
<OPENCODE-HOST-NOTES>
This is the OpenCode build of the likbez knowledge pack. The body below is written in
artel's Claude Code dialect; this glossary translates it. Apply it throughout:

- A `/likbez:<skill>` or `/<cluster>:<skill>` command — the `likbez-<skill>` skill
  (this very skill if the name matches yours), loaded with the `skill` tool
  (TUI: `/likbez-<skill>`).
- Paths like `references/...`, `assets/...`, `scripts/...`, `examples/...` — relative
  to this skill's own directory.
- `CLAUDE.md` — the host project's conventions doc (on OpenCode usually `AGENTS.md`).
- "Claude" in the prose below — you, the agent reading this.
</OPENCODE-HOST-NOTES>
"""

# project-setup advises host-state writes (.claude/settings.json enabledPlugins)
# that only exist on Claude Code; the note redirects them instead of dropping the
# skill (decision recorded in docs/design.md, 2026-08-26).
PROJECT_SETUP_NOTE = """
OpenCode note: this skill's steps that edit `.claude/settings.json`,
`.claude/settings.local.json` or `enabledPlugins` are Claude Code-specific. On
OpenCode there is no plugin marketplace: present the cluster recommendation, then
point the user at this pack's repository README for manual installation instead of
offering to write host config files.
"""

VALID_NAME = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
BLOCK_SCALAR = re.compile(r'^[>|][+-]?\d*[+-]?$')
DROPPED_KEYS = ('argument-hint', 'disable-model-invocation', 'allowed-tools', 'model')
SUBTREES = ('references', 'assets', 'scripts', 'examples')
MAX_DESCRIPTION = 1024
# The 1024-char budget is asserted on the whole emitted line (`description: `
# plus quotes), so the value itself is clipped 2 chars short of MAX_DESCRIPTION;
# the value therefore also honors the documented "descriptions ≤ 1024 chars".
MAX_DESCRIPTION_VALUE = MAX_DESCRIPTION - 2


def split_frontmatter(text):
    """(header_lines, body_text): the raw lines between the leading `---` markers,
    and the body after them verbatim. Files without frontmatter come back
    as ([], text)."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != '---':
        return [], text
    for index in range(1, len(lines)):
        if lines[index].strip() == '---':
            header = [line.rstrip('\n') for line in lines[1:index]]
            return header, ''.join(lines[index + 1:])
    return [], text


def _continuation(header_lines, index):
    """The indented continuation lines of a block scalar starting after `index`."""
    collected = []
    for line in header_lines[index + 1:]:
        if not line.strip():
            collected.append('')
            continue
        if line[0] in ' \t':
            collected.append(line.strip())
            continue
        break
    while collected and not collected[-1]:
        collected.pop()
    return collected


def scalar_value(header_lines, key):
    """The value of `key` as a single string: plain/quoted scalars directly,
    `>`-style folded blocks joined with spaces. None when the key is absent."""
    for index, line in enumerate(header_lines):
        if not line.startswith(key + ':'):
            continue
        rest = line[len(key) + 1:].strip()
        if BLOCK_SCALAR.match(rest):
            return ' '.join(_continuation(header_lines, index))
        return rest.strip('"\'')
    return None


def _is_dropped_key(line):
    stripped = line.strip()
    return any(stripped.startswith(key + ':') for key in DROPPED_KEYS)


def metadata_block(header_lines):
    """The raw lines of the `metadata:` block (the key line plus its indented
    children), ready to be re-emitted verbatim — except Claude-only keys
    (`model` et al.) that Claude Code books inside metadata, which are dropped
    like their top-level twins. Empty when absent."""
    started = False
    collected = []
    for line in header_lines:
        if line.startswith('metadata:'):
            started = True
            collected.append(line)
            continue
        if started:
            if not line.strip() or line[0] in ' \t':
                if not _is_dropped_key(line):
                    collected.append(line)
            else:
                break
    while collected and not collected[-1].strip():
        collected.pop()
    return collected


def yaml_quote(value):
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def clip(value, limit):
    value = ' '.join(value.split())
    return value if len(value) <= limit else value[:limit - 3] + '...'


def build_skill(src_text, folder_name):
    """(dir_name, frontmatter_lines, body_text) for one canonical SKILL.md."""
    header, body = split_frontmatter(src_text)
    name = 'likbez-' + folder_name
    frontmatter = [
        'name: ' + name,
        'description: ' + yaml_quote(clip(scalar_value(header, 'description') or '',
                                          MAX_DESCRIPTION_VALUE)),
    ]
    frontmatter.extend(metadata_block(header))
    if folder_name == 'project-setup':
        body = body.rstrip('\n') + '\n\n' + PROJECT_SETUP_NOTE.strip() + '\n'
    return name, frontmatter, body


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Generate the OpenCode build of likbez.')
    parser.add_argument('--source', default=str(REPO_ROOT),
                        help='checkout to read plugins/ from (default: this repo)')
    parser.add_argument('--out', default=None,
                        help='output directory (default: <source>/opencode/dist)')
    args = parser.parse_args(argv)

    source = Path(args.source).resolve()
    out = Path(args.out).resolve() if args.out else source / 'opencode' / 'dist'

    skill_files = sorted(source.glob('plugins/*/skills/*/SKILL.md'))
    if not skill_files:
        print('build_opencode: no skills under {}'.format(source), file=sys.stderr)
        return 2

    for skill_path in skill_files:
        folder = skill_path.parent.name
        name, frontmatter, body = build_skill(
            skill_path.read_text(encoding='utf-8'), folder)
        if not VALID_NAME.match(name):
            print('build_opencode: {} is not a legal OpenCode name'.format(name),
                  file=sys.stderr)
            return 2
        dest = out / 'skills' / name
        # Rebuilds into an existing --out must be idempotent: copytree cannot
        # merge into an existing subtree, so wipe any previous build first.
        shutil.rmtree(dest, ignore_errors=True)
        dest.mkdir(parents=True, exist_ok=True)
        parts = ['---'] + frontmatter + ['---', '', GLOSSARY.strip(),
                                         body.strip('\n') + '\n']
        (dest / 'SKILL.md').write_text('\n'.join(parts), encoding='utf-8')
        for subtree in SUBTREES:
            src_dir = skill_path.parent / subtree
            if src_dir.is_dir():
                shutil.copytree(src_dir, dest / subtree)

    print('build_opencode: {} skills -> {}'.format(len(skill_files), out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
