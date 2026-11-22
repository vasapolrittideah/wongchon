import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_stage_gate  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_stage_gate.py")


def artifact(status, extra_lines=0):
    return "# Spec: Example\n\nAuthor: Kim Lee\n\nStatus: `{0}`\n".format(status) + "line\n" * extra_lines


class Artifacts(unittest.TestCase):
    def test_approved_intent_and_spec_pass(self):
        self.assertEqual(check_stage_gate.check_artifact("docs/intents/a.md", artifact("Approved")), [])
        self.assertEqual(check_stage_gate.check_artifact("docs/specs/a.md", artifact("Approved")), [])

    def test_draft_fails(self):
        findings = check_stage_gate.check_artifact("docs/specs/a.md", artifact("Draft"))
        self.assertEqual(len(findings), 1)
        self.assertIn('the status "Draft"', findings[0])

    def test_missing_or_unquoted_status_fails(self):
        for text in ["# Intent: Example\n", "Status: Approved\n"]:
            with self.subTest(text=text):
                findings = check_stage_gate.check_artifact("docs/intents/a.md", text)
                self.assertIn("has no Status line", findings[0])

    def test_first_status_line_counts(self):
        text = artifact("Draft") + "```markdown\nStatus: `Approved`\n```\n"
        self.assertIn('the status "Draft"', check_stage_gate.check_artifact("docs/specs/a.md", text)[0])

    def test_spec_of_200_lines_passes(self):
        text = artifact("Approved", 200 - 5)
        self.assertEqual(len(text.splitlines()), 200)
        self.assertEqual(check_stage_gate.check_artifact("docs/specs/a.md", text), [])

    def test_spec_of_201_lines_fails(self):
        findings = check_stage_gate.check_artifact("docs/specs/a.md", artifact("Approved", 201 - 5))
        self.assertEqual(findings, ["has 201 lines, more than 200"])

    def test_long_intent_passes(self):
        self.assertEqual(check_stage_gate.check_artifact("docs/intents/a.md", artifact("Approved", 300)), [])


class Script(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.write("docs/intents/old.md", artifact("Draft"))
        self.write("docs/specs/gone.md", artifact("Draft"))
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

    def run_script(self):
        return subprocess.run([sys.executable, SCRIPT, "main"], cwd=self.temp.name,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    def test_unchanged_drafts_and_other_files_pass(self):
        self.write("README.md", "Status: `Draft`\n")
        self.write("docs/plans/a.md", artifact("Draft"))
        self.git("rm", "-q", "docs/specs/gone.md")
        self.commit("change")
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("for 0 changed", result.stdout)

    def test_changed_draft_fails(self):
        self.write("docs/intents/old.md", artifact("Draft") + "more\n")
        self.write("docs/specs/new.md", artifact("Approved"))
        self.commit("change")
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("docs/intents/old.md has the status", result.stderr)
        self.assertNotIn("docs/specs/new.md", result.stderr)

    def test_unknown_base_exits_2(self):
        result = subprocess.run([sys.executable, SCRIPT, "no-such-ref"], cwd=self.temp.name,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
