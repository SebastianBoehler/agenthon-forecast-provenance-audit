"""Executive summary: reject escaping manifest paths and corrupted public-bank identities."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_public_repository.py'
spec = importlib.util.spec_from_file_location('public_check', SCRIPT)
public_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(public_check)


class ManifestPathTests(unittest.TestCase):
    def test_existing_relative_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ((root / 'evidence.json').resolve()).write_text('{}')
            self.assertEqual(public_check.contained(root, 'evidence.json'), (root / 'evidence.json').resolve())

    def test_absolute_parent_and_missing_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            for name in ('/etc/passwd', '../outside.json', 'missing.json'):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    public_check.contained(Path(temp), name)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'escape').symlink_to('/etc/passwd')
            with self.assertRaises(ValueError):
                public_check.contained(root, 'escape')

    def test_public_evidence_identities(self):
        self.assertEqual(public_check.check()['status'], 'PASS')
