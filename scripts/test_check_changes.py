import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_changes  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_changes.py")

PROTECTED = """name: Protected checks

on:
  pull_request_target:
    branches: [main]

permissions:
  contents: read

jobs:
  stage-gate:
    name: Stage gate
    runs-on: ubuntu-latest
"""

CI = """name: CI

on:
  pull_request:
    branches: [main]

jobs:
  checks:
    name: Checks (Python ${{ matrix.python }})
    runs-on: ubuntu-24.04
"""


class Events(unittest.TestCase):
    def test_block_form_with_only_pull_request_target(self):
        self.assertEqual(check_changes.protected_events(PROTECTED), ["pull_request_target"])

    def test_other_events_are_listed(self):
        text = PROTECTED.replace("  pull_request_target:\n", "  pull_request_target:\n  pull_request:\n")
        self.assertEqual(check_changes.protected_events(text), ["pull_request_target", "pull_request"])

    def test_inline_form_is_not_read(self):
        self.assertIsNone(check_changes.protected_events(PROTECTED.replace("on:\n", "on: [push]\n")))
        self.assertIsNone(check_changes.protected_events("name: x\n"))

    def test_comment_inside_the_block_does_not_hide_an_event(self):
        text = PROTECTED.replace("  pull_request_target:\n", "  pull_request_target:\n# x\n  pull_request:\n")
        self.assertEqual(check_changes.protected_events(text), ["pull_request_target", "pull_request"])

    def test_quoted_event_key_is_read(self):
        text = PROTECTED.replace("  pull_request_target:\n", "  pull_request_target:\n  \"pull_request\":\n")
        self.assertEqual(check_changes.protected_events(text), ["pull_request_target", "pull_request"])

    def test_unreadable_event_line_is_not_read(self):
        self.assertIsNone(check_changes.protected_events(PROTECTED.replace("  pull_request_target:\n",
                                                                           "  pull_request_target:\n  [push]\n")))

    def test_quoted_on_key_is_read(self):
        self.assertEqual(check_changes.protected_events(PROTECTED.replace("on:", '"on":')), ["pull_request_target"])


class Script(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.write(".github/workflows/protected-checks.yml", PROTECTED)
        self.write(".github/workflows/ci.yml", CI)
        self.write("scripts/check.py", "print(1)\n")
        self.write("docs/a.md", "Text.\n")
        self.commit("base")
        self.git("checkout", "-q", "-b", "change")

    def git(self, *args):
        subprocess.run(["git"] + list(args), cwd=self.temp.name, check=True, stdout=subprocess.DEVNULL)

    def write(self, path, text):
        full = os.path.join(self.temp.name, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as file:
            file.write(text)

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def run_script(self, *args):
        return subprocess.run([sys.executable, SCRIPT, "main"] + list(args), cwd=self.temp.name,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    def test_change_without_check_files_passes_without_warnings(self):
        self.write("docs/a.md", "More text.\n")
        self.commit("docs")
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("::warning", result.stdout)

    def test_each_changed_check_file_gets_a_warning(self):
        for path in ["scripts/check.py", ".github/workflows/ci.yml", "hooks/guard.py", "reviewers/a.md",
                     ".claude/settings.json"]:
            self.write(path, "changed\n" if not path.endswith(".yml") else CI + "\n")
        self.commit("checks")
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        for path in ["scripts/check.py", ".github/workflows/ci.yml", "hooks/guard.py", "reviewers/a.md",
                     ".claude/settings.json"]:
            self.assertIn("::warning file={0},".format(path), result.stdout)

    def test_deleted_check_file_gets_a_warning(self):
        self.git("rm", "-q", "scripts/check.py")
        self.commit("delete")
        self.assertIn("::warning file=scripts/check.py,", self.run_script().stdout)

    def test_workflow_with_a_protected_job_name_fails(self):
        for name in ["PR metadata", "Stage gate", "Check changes"]:
            with self.subTest(name=name):
                self.write(".github/workflows/fake.yml", CI.replace("Checks (Python ${{ matrix.python }})", name))
                self.commit("fake " + name)
                result = self.run_script()
                self.assertEqual(result.returncode, 1)
                self.assertIn("protected job name", result.stdout)

    def test_only_name_values_count(self):
        text = CI + "      - name: Check changes in docs\n        run: echo 'Stage gate'\n# PR metadata\n"
        self.assertEqual(check_changes.protected_names(text), [])
        quoted = CI.replace("name: Checks (Python ${{ matrix.python }})", 'name: "Stage   gate"')
        self.assertEqual(check_changes.protected_names(quoted), ["Stage gate"])
        commented = CI.replace("name: Checks (Python ${{ matrix.python }})", "name: Stage gate # copied")
        self.assertEqual(check_changes.protected_names(commented), ["Stage gate"])
        step = CI + "      - name: PR metadata\n"
        self.assertEqual(check_changes.protected_names(step), ["PR metadata"])

    def test_protected_workflow_with_another_event_fails(self):
        for text in [PROTECTED.replace("  pull_request_target:\n", "  pull_request:\n"),
                     PROTECTED.replace("  pull_request_target:\n", "  pull_request_target:\n  push:\n"),
                     PROTECTED.replace("on:\n  pull_request_target:\n    branches: [main]\n", "on: [push]\n"),
                     PROTECTED.replace("  pull_request_target:\n", "  pull_request_target:\n# x\n  pull_request:\n")]:
            with self.subTest(text=text):
                self.write(".github/workflows/protected-checks.yml", text)
                self.commit("event")
                self.assertEqual(self.run_script().returncode, 1)

    def test_change_of_the_protected_workflow_that_keeps_its_event_passes(self):
        self.write(".github/workflows/protected-checks.yml", PROTECTED + "      - run: echo\n")
        self.commit("step")
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("::warning file=.github/workflows/protected-checks.yml,", result.stdout)

    def test_head_reads_another_commit(self):
        self.write(".github/workflows/fake.yml", CI.replace("Checks (Python ${{ matrix.python }})", "Stage gate"))
        self.commit("fake")
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.temp.name, check=True, stdout=subprocess.PIPE,
                              universal_newlines=True).stdout.strip()
        self.git("checkout", "-q", "main")
        self.assertEqual(self.run_script("--head", head).returncode, 1)

    def test_unknown_ref_exits_2(self):
        self.assertEqual(self.run_script("--head", "no-such-ref").returncode, 2)

    def test_annotation_values_are_escaped(self):
        self.assertEqual(check_changes.escape_property("a,b:c%\n"), "a%2Cb%3Ac%25%0A")
        self.assertEqual(check_changes.escape_data("a,b:c%\n"), "a,b:c%25%0A")

    def test_error_message_keeps_its_colons(self):
        self.write(".github/workflows/protected-checks.yml", PROTECTED.replace("pull_request_target:", "push:"))
        self.commit("event")
        self.assertIn("block form `on:`", self.run_script().stdout)


if __name__ == "__main__":
    unittest.main()
