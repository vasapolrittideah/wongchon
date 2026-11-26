import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_plan_issues  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_plan_issues.py")

FAKE_GH = """#!{python}
import json, os, sys
data = json.load(open(os.environ["FAKE_ISSUES"]))
if os.environ.get("FAKE_FAIL"):
    sys.stderr.write("HTTP 401\\n")
    sys.exit(1)
args = sys.argv[1:]
if args[:2] == ["issue", "list"]:
    print(json.dumps([{{k: issue[k] for k in ("number", "title", "body")}} for issue in data]))
else:
    assert args[1].endswith("/dependencies/blocked_by?per_page=100"), args[1]
    number = int(args[1].split("/")[4])
    issue = next(issue for issue in data if issue["number"] == number)
    print(json.dumps([{{"number": blocker}} for blocker in issue["blocked_by"]]))
"""


def body(*paths):
    lines = ["Plan: [`docs/plans/x.md`](https://example.com)", "", "## Result", "", "Text.", "", "## Files", ""]
    lines += ["- `{0}`".format(path) for path in paths] or ["- None"]
    return "\n".join(lines + ["", "## Proof", "", "- [ ] Review the CI results on the PR."])


def issue(number, paths, blocked_by=(), title=None):
    return {"number": number, "title": title or "Add task {0}".format(number), "body": body(*paths),
            "blocked_by": list(blocked_by)}


class Files(unittest.TestCase):
    def test_reads_each_path_of_the_files_section(self):
        text = body("a.py", "b.md").replace("- `b.md`", "- `b.md` (new)")
        self.assertEqual(check_plan_issues.files(text), ["a.py", "b.md"])

    def test_none_and_other_sections_give_no_path(self):
        self.assertEqual(check_plan_issues.files(body()), [])
        self.assertEqual(check_plan_issues.files("## Result\n\n- `a.py`\n"), [])
        self.assertEqual(check_plan_issues.files(None), [])

    def test_folder_overlaps_its_files(self):
        self.assertTrue(check_plan_issues.overlap("skills/plan/", "skills/plan/SKILL.md"))
        self.assertTrue(check_plan_issues.overlap("skills/plan/SKILL.md", "skills/plan/"))
        self.assertTrue(check_plan_issues.overlap("a.py", "a.py"))
        self.assertFalse(check_plan_issues.overlap("skills/plan", "skills/plan-x.md"))
        self.assertFalse(check_plan_issues.overlap("a.py", "b.py"))


class Check(unittest.TestCase):
    def test_shared_file_without_blocked_by_fails(self):
        findings = check_plan_issues.check([issue(1, ["a.py"]), issue(2, ["a.py", "b.py"])])
        self.assertEqual(len(findings), 1)
        self.assertIn("#1 and #2 both change a.py", findings[0])

    def test_direct_or_chained_blocked_by_passes(self):
        self.assertEqual(check_plan_issues.check([issue(1, ["a.py"]), issue(2, ["a.py"], [1])]), [])
        self.assertEqual(check_plan_issues.check([issue(1, ["a.py"]), issue(2, ["b.py"], [1]),
                                                  issue(3, ["a.py"], [2])]), [])

    def test_blocked_by_in_the_other_direction_passes(self):
        self.assertEqual(check_plan_issues.check([issue(1, ["a.py"], [2]), issue(2, ["a.py"])]), [])

    def test_cycle_of_blocked_by_ends(self):
        findings = check_plan_issues.check([issue(1, ["a.py"], [3]), issue(2, ["a.py"]), issue(3, ["b.py"], [1])])
        self.assertEqual(len(findings), 1)
        self.assertIn("#1 and #2", findings[0])

    def test_new_file_in_a_shared_folder_fails(self):
        findings = check_plan_issues.check([issue(1, ["skills/plan/"]), issue(2, ["skills/plan/SKILL.md"])])
        self.assertIn("skills/plan/", findings[0])

    def test_long_title_fails(self):
        findings = check_plan_issues.check([issue(1, [], title="a" * 73), issue(2, [], title="a" * 72)])
        self.assertEqual(findings, ["#1 has a title of 73 characters, more than 72"])


class Script(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        gh = os.path.join(self.folder, "gh")
        with open(gh, "w", encoding="utf-8") as file:
            file.write(FAKE_GH.format(python=sys.executable))
        os.chmod(gh, os.stat(gh).st_mode | stat.S_IEXEC)
        self.data = os.path.join(self.folder, "issues.json")

    def tearDown(self):
        shutil.rmtree(self.folder)

    def run_script(self, issues, **env):
        with open(self.data, "w", encoding="utf-8") as file:
            json.dump(issues, file)
        env = dict(os.environ, PATH=self.folder + os.pathsep + os.environ["PATH"], FAKE_ISSUES=self.data, **env)
        return subprocess.run([sys.executable, SCRIPT, "change"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True, env=env)

    def test_ordered_issues_pass(self):
        result = self.run_script([issue(1, ["a.py"]), issue(2, ["a.py"], [1])])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("The 2 Issues", result.stdout)

    def test_unordered_issues_fail(self):
        result = self.run_script([issue(1, ["a.py"]), issue(2, ["a.py"])])
        self.assertEqual(result.returncode, 1)
        self.assertIn("#1 and #2 both change a.py", result.stderr)

    def test_failed_gh_or_empty_milestone_is_an_error(self):
        for issues, env in [([issue(1, [])], {"FAKE_FAIL": "1"}), ([], {})]:
            with self.subTest(issues=issues, env=env):
                result = self.run_script(issues, **env)
                self.assertEqual(result.returncode, 2)
                self.assertIn("Cannot read the Issues", result.stderr)

    def test_milestone_at_the_limit_is_an_error(self):
        limit = check_plan_issues.MAX_ISSUES
        check_plan_issues.MAX_ISSUES = 2
        try:
            with self.assertRaises(check_plan_issues.IssueError):
                with open(self.data, "w", encoding="utf-8") as file:
                    json.dump([issue(1, []), issue(2, [])], file)
                path = os.environ["PATH"]
                os.environ["PATH"] = self.folder + os.pathsep + path
                os.environ["FAKE_ISSUES"] = self.data
                try:
                    check_plan_issues.load("change")
                finally:
                    os.environ["PATH"] = path
                    del os.environ["FAKE_ISSUES"]
        finally:
            check_plan_issues.MAX_ISSUES = limit

    def test_missing_gh_is_an_error(self):
        os.remove(os.path.join(self.folder, "gh"))
        with open(self.data, "w", encoding="utf-8") as file:
            json.dump([], file)
        result = subprocess.run([sys.executable, SCRIPT, "change"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, env=dict(os.environ, PATH=self.folder))
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot run gh", result.stderr)

    def test_output_that_is_not_json_is_an_error(self):
        with open(os.path.join(self.folder, "gh"), "w", encoding="utf-8") as file:
            file.write("#!{0}\nprint('not json')\n".format(sys.executable))
        result = self.run_script([])
        self.assertEqual(result.returncode, 2)
        self.assertIn("did not return JSON", result.stderr)


if __name__ == "__main__":
    unittest.main()
