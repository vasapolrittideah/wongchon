import os
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

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


def plan(status="Approved", spec="[`docs/specs/x.md`](../specs/x.md)", tasks=1, milestone=False):
    tracking = "Tasks are tracked in the Project"
    if milestone:
        tracking += " under the [x](https://github.com/o/r/milestone/2) milestone"
    items = ["{0}. [#{0} Add task](https://github.com/o/r/issues/{0})".format(n) for n in range(1, tasks + 1)]
    return "\n".join(["# Plan: X", "", "Author: Kim Lee", "", "Status: `{0}`".format(status), "",
                      "Spec: " + spec, "", "## Tasks", "", tracking + ".", ""] + items + [""])


def body(*paths):
    return "## Related artifacts\n\n" + "".join(
        "- [`{0}`](https://github.com/o/r/blob/main/{0})\n".format(path) for path in paths) + "\n## Related issues\n"


class Plans(unittest.TestCase):
    def setUp(self):
        self.milestones = []

    def run_check(self, milestone):
        self.milestones.append(milestone)
        return ["fails"] if milestone == "bad" else []

    def check(self, path, text):
        return check_stage_gate.check_artifact(path, text, self.run_check)

    def test_approved_plan_with_a_spec_checks_the_issues_of_its_milestone(self):
        self.assertEqual(self.check("docs/plans/good.md", plan(milestone=True)), [])
        self.assertEqual(self.check("docs/plans/bad.md", plan(milestone=True, tasks=3)), ["fails"])
        self.assertEqual(self.milestones, ["good", "bad"])

    def test_draft_plan_fails_without_a_check_of_issues(self):
        findings = self.check("docs/plans/good.md", plan(status="Draft"))
        self.assertIn("has the status", findings[0])
        self.assertEqual(self.milestones, [])

    def test_small_change_with_1_task_passes_without_a_check_of_issues(self):
        self.assertEqual(self.check("docs/plans/small.md", plan(spec="None")), [])
        self.assertEqual(self.milestones, [])

    def test_small_change_with_0_or_2_tasks_or_a_milestone_fails(self):
        self.assertIn("with 0 tasks", self.check("docs/plans/small.md", plan(spec="None", tasks=0))[0])
        self.assertIn("with 2 tasks", self.check("docs/plans/small.md", plan(spec="None", tasks=2))[0])
        self.assertIn("links a milestone", self.check("docs/plans/small.md", plan(spec="None", milestone=True))[0])

    def test_plan_without_a_spec_line_fails(self):
        text = plan().replace("Spec: [`docs/specs/x.md`](../specs/x.md)\n", "")
        self.assertEqual(self.check("docs/plans/x.md", text), ["has no Spec line"])

    def run_plan_issues(self, script):
        with tempfile.TemporaryDirectory() as folder:
            gh = os.path.join(folder, "gh")
            with open(gh, "w", encoding="utf-8") as file:
                file.write("#!{0}\n{1}".format(sys.executable, script))
            os.chmod(gh, os.stat(gh).st_mode | stat.S_IEXEC)
            with mock.patch.dict(os.environ, {"PATH": folder + os.pathsep + os.environ["PATH"]}):
                return check_stage_gate.run_plan_issues("x")

    def test_issue_check_failure_is_a_finding(self):
        findings = self.run_plan_issues("import sys\nsys.stderr.write('HTTP 401\\n')\nsys.exit(1)\n")
        self.assertEqual(len(findings), 1)
        self.assertIn('fails the check of the Issues of the milestone "x"', findings[0])
        self.assertIn("HTTP 401", findings[0])

    def test_issue_check_pass_gives_no_finding(self):
        script = ("import json, sys\n"
                  "if sys.argv[1] == 'issue':\n"
                  "    print(json.dumps([{'number': 1, 'title': 'Add a', 'body': '## Files\\n\\n- `a.py`'}]))\n"
                  "else:\n"
                  "    print('[]')\n")
        self.assertEqual(self.run_plan_issues(script), [])


class DesignLinks(unittest.TestCase):
    def test_design_file_without_a_spec_link_fails(self):
        for path in ["docs/adrs/0001-x.md", "ARCHITECTURE.md", "CONSTRAINTS.md"]:
            with self.subTest(path=path):
                findings = check_stage_gate.check_design_links([path], body("docs/plans/x.md"))
                self.assertIn("links no spec", findings[0])

    def test_design_file_with_a_spec_link_passes(self):
        self.assertEqual(check_stage_gate.check_design_links(["docs/adrs/0001-x.md"], body("docs/specs/x.md")), [])

    def test_spec_link_outside_related_artifacts_does_not_count(self):
        text = "## Why\n\n- [`docs/specs/x.md`](https://github.com/o/r/blob/main/docs/specs/x.md)\n" + body()
        self.assertEqual(len(check_stage_gate.check_design_links(["CONSTRAINTS.md"], text)), 1)

    def test_other_files_need_no_spec_link(self):
        self.assertEqual(check_stage_gate.check_design_links(["docs/conventions/x.md", "docs/adrs.md"], body()), [])


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

    def run_script(self, **env):
        return subprocess.run([sys.executable, SCRIPT, "main"], cwd=self.temp.name,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                              env=dict({k: v for k, v in os.environ.items() if k != "PR_BODY"}, **env))

    def test_changed_draft_plan_fails(self):
        self.write("docs/plans/new.md", plan(status="Draft"))
        self.commit("plan")
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("docs/plans/new.md has the status", result.stderr)

    def test_design_file_needs_a_spec_link_only_with_a_pr_body(self):
        self.write("CONSTRAINTS.md", "# Constraints\n")
        self.commit("constraints")
        self.assertEqual(self.run_script().returncode, 0)
        result = self.run_script(PR_BODY=body())
        self.assertEqual(result.returncode, 1)
        self.assertIn("CONSTRAINTS.md", result.stderr)
        self.assertEqual(self.run_script(PR_BODY=body("docs/specs/x.md")).returncode, 0)

    def test_deleted_design_file_needs_a_spec_link(self):
        self.write("CONSTRAINTS.md", "# Constraints\n")
        self.git("checkout", "-q", "main")
        self.commit("constraints")
        self.git("checkout", "-q", "change")
        self.git("merge", "-q", "main")
        self.git("rm", "-q", "CONSTRAINTS.md")
        self.commit("remove")
        result = self.run_script(PR_BODY=body())
        self.assertEqual(result.returncode, 1)
        self.assertIn("CONSTRAINTS.md", result.stderr)

    def test_unchanged_drafts_and_other_files_pass(self):
        self.write("README.md", "Status: `Draft`\n")
        self.write("docs/evidence/a.md", artifact("Draft"))
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

    def test_head_reads_the_artifacts_of_that_commit(self):
        self.write("docs/specs/new.md", artifact("Draft"))
        self.commit("draft")
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.temp.name, check=True, stdout=subprocess.PIPE,
                              universal_newlines=True).stdout.strip()
        self.git("checkout", "-q", "main")
        result = subprocess.run([sys.executable, SCRIPT, "main", "--head", head], cwd=self.temp.name,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("docs/specs/new.md has the status", result.stderr)

    def test_missing_artifact_at_the_head_cannot_be_read(self):
        cwd = os.getcwd()
        os.chdir(self.temp.name)
        try:
            with self.assertRaises(subprocess.CalledProcessError):
                check_stage_gate.read_artifact("docs/specs/missing.md", "HEAD")
        finally:
            os.chdir(cwd)

    def test_unknown_head_exits_2(self):
        result = subprocess.run([sys.executable, SCRIPT, "main", "--head", "no-such-ref"], cwd=self.temp.name,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.assertEqual(result.returncode, 2)

    def test_unknown_base_exits_2(self):
        result = subprocess.run([sys.executable, SCRIPT, "no-such-ref"], cwd=self.temp.name,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
