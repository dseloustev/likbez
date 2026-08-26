"""The OpenCode build generator: every canonical skill becomes a `likbez-<name>`
skill directory with a host glossary and OpenCode-legal frontmatter. Guards the
zero-regression promise by asserting what the generated files contain (and omit):
a generated skill that still carries `disable-model-invocation` or lost its
`metadata.author` attribution breaks in a session nobody is watching.
"""
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / 'scripts' / 'build_opencode.py'

VALID_NAME = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
GLOSSARY_MARKER = '<OPENCODE-HOST-NOTES>'
MAX_DESCRIPTION = 1024
# Skills carrying third-party attribution that must survive the port verbatim.
ATTRIBUTED = {
    'dart-drift', 'flutter-drift', 'flutter-internationalization',
    'flutter-networking', 'flutter-testing', 'flutter-adaptive-ui',
    'flutter-animations', 'flutter-navigation', 'flutter-architecture',
}


def source_skills():
    """Every shipped skill, by folder name (folder names are unique across plugins)."""
    return sorted(p.parent.name for p in ROOT.glob('plugins/*/skills/*/SKILL.md'))


class BuildBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls._tmp.name)
        cls.out = tmp / 'dist'
        proc = subprocess.run(
            [sys.executable, str(BUILD), '--out', str(cls.out)],
            capture_output=True, text=True)
        if proc.returncode != 0:
            raise AssertionError('build failed: ' + proc.stderr)
        cls.proc = proc

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()


class TestSkillBuild(BuildBase):
    def test_build_succeeds_and_reports_the_count(self):
        self.assertEqual(self.proc.returncode, 0)
        self.assertIn('{} skills'.format(len(source_skills())), self.proc.stdout)

    def test_every_skill_is_built_prefixed(self):
        for name in source_skills():
            path = self.out / 'skills' / ('likbez-' + name) / 'SKILL.md'
            self.assertTrue(path.is_file(), 'missing ' + str(path))

    def test_generated_names_are_opencode_legal(self):
        for path in sorted((self.out / 'skills').glob('*/SKILL.md')):
            self.assertRegex(path.parent.name, VALID_NAME)

    def test_frontmatter_drops_claude_only_keys(self):
        for path in sorted((self.out / 'skills').glob('*/SKILL.md')):
            head = path.read_text(encoding='utf-8').split('---')[1]
            for field in ('argument-hint:', 'model:',
                          'disable-model-invocation:', 'allowed-tools:'):
                self.assertNotIn(field, head,
                                 path.parent.name + ' keeps Claude-only ' + field)

    def test_description_is_single_line_quoted_and_within_limit(self):
        for path in sorted((self.out / 'skills').glob('*/SKILL.md')):
            head = path.read_text(encoding='utf-8').split('---')[1]
            lines = [l for l in head.splitlines() if l.startswith('description: ')]
            self.assertEqual(len(lines), 1,
                             path.parent.name + ' description is not one line')
            self.assertTrue(lines[0].startswith('description: "'),
                            path.parent.name + ' description is not quoted')
            self.assertLessEqual(len(lines[0]), len('description: ') + MAX_DESCRIPTION,
                                 path.parent.name + ' description too long')

    def test_every_generated_skill_carries_the_host_glossary(self):
        for path in sorted((self.out / 'skills').glob('*/SKILL.md')):
            self.assertIn(GLOSSARY_MARKER, path.read_text(encoding='utf-8'),
                          path.parent.name + ' has no glossary')

    def test_attribution_survives_verbatim(self):
        for name in ATTRIBUTED:
            src = next(ROOT.glob('plugins/*/skills/' + name + '/SKILL.md'))
            gen = self.out / 'skills' / ('likbez-' + name) / 'SKILL.md'
            src_author = [l for l in src.read_text(encoding='utf-8').splitlines()
                          if l.strip().startswith('author:')]
            gen_author = [l for l in gen.read_text(encoding='utf-8').splitlines()
                          if l.strip().startswith('author:')]
            self.assertEqual(src_author, gen_author,
                             name + ' lost or altered its metadata.author')

    def test_unattributed_skills_gain_no_author(self):
        for path in sorted((self.out / 'skills').glob('*/SKILL.md')):
            name = path.parent.name[len('likbez-'):]
            if name in ATTRIBUTED:
                continue
            self.assertNotIn('author:', path.read_text(encoding='utf-8'),
                             name + ' grew an author it never had')


class TestSubtreeCopy(BuildBase):
    def test_scripts_subtree_is_copied(self):
        path = self.out / 'skills' / 'likbez-dart-drift' / 'scripts' / 'verify-examples.sh'
        self.assertTrue(path.is_file(), 'missing ' + str(path))

    def test_assets_subtree_is_copied(self):
        base = self.out / 'skills' / 'likbez-flutter-internationalization' / 'assets'
        self.assertTrue(base.is_dir() and any(base.iterdir()),
                        'likbez-flutter-internationalization assets missing')

    def test_canonical_tree_is_untouched_by_generation(self):
        # The generator must never write outside --out: the source tree keeps
        # exactly the files git knows about.
        proc = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT,
                              capture_output=True, text=True)
        self.assertEqual(proc.stdout.strip(), '',
                         'generation dirtied the canonical tree')


class TestDeterminism(BuildBase):
    def test_rebuild_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as second:
            out2 = Path(second) / 'dist'
            proc = subprocess.run(
                [sys.executable, str(BUILD), '--out', str(out2)],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            for path in sorted((self.out / 'skills').glob('*/SKILL.md')):
                twin = out2 / 'skills' / path.parent.name / 'SKILL.md'
                self.assertTrue(twin.is_file(), 'second build missed ' + path.parent.name)
                self.assertEqual(path.read_text(encoding='utf-8'),
                                 twin.read_text(encoding='utf-8'),
                                 path.parent.name + ' differs between builds')


if __name__ == '__main__':
    unittest.main()
