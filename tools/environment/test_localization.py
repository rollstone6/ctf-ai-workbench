"""Regression checks for human feedback without changing machine contracts."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]

class ChineseFeedbackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = Path(self.temp.name) / 'graph'
        self.run_cli('init', '--goal', '阅读项目：project: error 原始证据')

    def run_cli(self, *args, lang='zh', check=True):
        return subprocess.run([str(ROOT / 'bin/sapper'), '--store', str(self.store), *args],
                              env={**os.environ, 'SAPPER_LANG': lang},
                              capture_output=True, text=True, check=check)

    def test_chinese_status_preserves_user_content(self):
        result = self.run_cli('status').stdout
        self.assertIn('目标：阅读项目：project: error 原始证据', result)
        self.assertIn('暂无待办任务', result)
        self.assertIn('事实图校验通过', self.run_cli('validate').stdout)

    def test_english_fallback(self):
        self.assertIn('project:', self.run_cli('status', lang='en').stdout)
        self.assertIn('graph valid:', self.run_cli('validate', lang='en').stdout)

    def test_json_and_id_protocols_unchanged(self):
        fact = self.run_cli('fact', '中文事实').stdout.strip()
        self.assertRegex(fact, r'^f\d+$')
        zh = json.loads(self.run_cli('graph', '--format', 'json').stdout)
        en = json.loads(self.run_cli('graph', '--format', 'json', lang='en').stdout)
        self.assertEqual(zh, en)
        self.assertEqual(zh['project']['status'], 'active')
        self.assertIn('facts', zh)

    def test_failure_keeps_nonzero_exit_and_diagnostics(self):
        self.store = Path(self.temp.name) / 'missing'
        result = self.run_cli('status', check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn('操作失败', result.stderr)
        self.assertIn('sapper init', result.stderr)
