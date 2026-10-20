import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.focus_contract import parse_strategy


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'strategies/explore/STRATEGY.md'


def run_cli(*paths):
    return subprocess.run(
        [sys.executable, '-m', 'tools.validate', *map(str, paths)],
        cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
        env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
    )


class CatalogTests(unittest.TestCase):
    def test_catalog_and_template_pass_real_cli(self):
        result = run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Validated', result.stdout)

    def test_all_strategies_have_three_review_scenarios(self):
        scenarios = json.loads((ROOT / 'tests/scenarios.json').read_text(encoding='utf-8'))
        ids = {parse_strategy(path.read_text(encoding='utf-8')).metadata.id
               for path in (ROOT / 'strategies').glob('*/STRATEGY.md')}
        self.assertTrue(ids)
        self.assertEqual(set(scenarios), ids)
        for identity, cases in scenarios.items():
            with self.subTest(identity=identity):
                self.assertEqual(set(cases), {'applicable', 'inapplicable', 'feedback'})
                for case in cases.values():
                    self.assertEqual(set(case), {'input', 'expectation'})
                    self.assertIsInstance(case['input'], str)
                    self.assertIsInstance(case['expectation'], str)
                    self.assertTrue(case['input'].strip())
                    self.assertTrue(case['expectation'].strip())


class CliIntegrationTests(unittest.TestCase):
    def test_duplicate_ids_fail_and_name_both_files(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            for name in ('first', 'second'):
                destination = folder / name / 'STRATEGY.md'
                destination.parent.mkdir()
                destination.write_bytes(EXAMPLE.read_bytes())
            result = run_cli(folder)
            self.assertEqual(result.returncode, 1)
            self.assertIn('duplicate id', result.stdout)
            self.assertIn('first', result.stdout)
            self.assertIn('second', result.stdout)

    def test_invalid_file_fails_and_valid_input_is_still_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'STRATEGY.md'
            path.write_text('No frontmatter', encoding='utf-8')
            result = run_cli(path, EXAMPLE)
            self.assertEqual(result.returncode, 1)
            self.assertIn('2 file(s)', result.stdout)
            self.assertIn('STRATEGY.md', result.stdout)

    def test_invalid_utf8_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'STRATEGY.md'
            path.write_bytes(b'\xff\xfe')
            result = run_cli(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn('ERROR:', result.stdout)
            self.assertNotIn('Traceback', result.stderr)

    def test_missing_and_empty_inputs_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            for path in (Path(temp), Path(temp) / 'missing'):
                with self.subTest(path=path):
                    result = run_cli(path)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn('ERROR:', result.stdout)

    def test_overlapping_paths_are_not_duplicate_strategies(self):
        result = run_cli(EXAMPLE.parent, EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('1 Strategy file(s)', result.stdout)


if __name__ == '__main__':
    unittest.main()
