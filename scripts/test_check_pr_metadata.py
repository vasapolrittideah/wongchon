import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_pr_metadata  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
SCRIPT = os.path.join(ROOT, "scripts", "check_pr_metadata.py")
HEADINGS = ["Result", "What changed", "Why", "Breaking changes", "Verification", "Risks or limitations",
            "Follow-up tasks", "Related artifacts", "Related issues"]
GOOD_BODY = "\n\n".join("## {0}\n\nn/a".format(heading) for heading in HEADINGS)
TYPES = {"feat", "fix", "docs", "build", "ci", "revert"}
SCOPES = {"intent", "build", "plugin"}


class Titles(unittest.TestCase):
    def assert_passes(self, titles):
        for title in titles:
            with self.subTest(title=title):
                self.assertEqual(check_pr_metadata.check_title(title, TYPES, SCOPES), [])

    def assert_fails(self, titles, expected):
        for title in titles:
            with self.subTest(title=title):
                findings = check_pr_metadata.check_title(title, TYPES, SCOPES)
                self.assertTrue(any(expected in finding for finding in findings), findings)

    def test_valid_titles_pass(self):
        self.assert_passes([
            "feat(intent): ask for the affected systems in the intent template",
            "ci: check pull request titles",
            "feat!: read commit scopes from .wongchon/config.json",
            "fix(build)!: keep multiline PR descriptions in the plan hook",
            "build(build): pin Python to 3.9",
            "revert(intent): ask for the affected systems in the intent template",
            "docs: " + "a" * 66,
        ])

    def test_bad_form_fails(self):
        self.assert_fails([
            "add a CI gate",
            "feat:add a CI gate",
            "feat : add a CI gate",
            "feat !: add a CI gate",
            "feat(intent) : add a CI gate",
            "feat(intent)!:  add a CI gate",
            "feat(intent: add a CI gate",
            "feat(): ",
        ], "does not have the form")

    def test_unknown_type_fails(self):
        self.assert_fails(["feature: add a CI gate", "Feat: add a CI gate", "wip: add a CI gate"],
                          "is not in the Types table")

    def test_unknown_or_combined_scope_fails(self):
        self.assert_fails([
            "feat(stage): add a CI gate",
            "feat(intent,build): add a CI gate",
            "feat(intent, build): add a CI gate",
            "feat(): add a CI gate",
        ], "is not in commit.scopes")

    def test_description_must_start_lowercase(self):
        self.assert_fails(["feat: Add a CI gate", "feat: 3 checks in CI"], "lowercase letter")

    def test_description_must_not_end_with_period(self):
        self.assert_fails(["feat: add a CI gate."], "ends with a period")

    def test_description_must_be_plain_text(self):
        self.assert_fails([
            "feat: add the `check_pr_title.py` script",
            "docs: link the [playbook](https://example.com)",
            "docs: link https://example.com in the roadmap",
        ], "Write plain text")

    def test_long_title_fails(self):
        self.assert_fails(["docs: " + "a" * 67], "more than 72")



class Descriptions(unittest.TestCase):
    def findings(self, body):
        return check_pr_metadata.check_body(body, HEADINGS)

    def test_template_headings_pass(self):
        self.assertEqual(self.findings(GOOD_BODY), [])

    def test_crlf_line_endings_pass(self):
        self.assertEqual(self.findings(GOOD_BODY.replace("\n", "\r\n")), [])

    def test_headings_in_code_blocks_and_lower_levels_do_not_count(self):
        body = GOOD_BODY.replace("## Verification\n", "## Verification\n\n```text\n## Why\n```\n\n### Details\n")
        self.assertEqual(self.findings(body), [])

    def test_missing_heading_fails(self):
        self.assertEqual(self.findings(GOOD_BODY.replace("## Why\n", "")), ['the heading "Why" is missing'])

    def test_empty_body_fails(self):
        self.assertEqual(len(self.findings("")), len(HEADINGS))

    def test_extra_heading_fails(self):
        self.assertEqual(self.findings(GOOD_BODY + "\n\n## Notes\n"), ['the heading "Notes" is not in the template'])

    def test_wrong_order_or_repeated_heading_fails(self):
        swapped = GOOD_BODY.replace("## Result", "## TEMP").replace("## Why", "## Result").replace("## TEMP", "## Why")
        for body in (swapped, GOOD_BODY + "\n\n## Why\n"):
            with self.subTest(body=body):
                self.assertIn("not once each in the order", self.findings(body)[0])

    def test_html_comment_fails(self):
        for body in (GOOD_BODY.replace("## Why\n", "## Why\n\n<!-- State the problem. -->\n"),
                     GOOD_BODY + "\n\n<!--\nA comment on 2 lines.\n-->\n"):
            with self.subTest(body=body):
                self.assertEqual(self.findings(body),
                                 ["the description has an HTML comment. Delete the comments of the template"])

    def test_html_comment_in_code_does_not_count(self):
        body = GOOD_BODY.replace("## Why\n", "## Why\n\nThe `<!--` marker starts a comment.\n\n```html\n<!-- x -->\n```\n")
        self.assertEqual(self.findings(body), [])


class Rules(unittest.TestCase):
    def test_types_come_from_the_convention(self):
        self.assertEqual(check_pr_metadata.load_types(), {
            "feat", "fix", "docs", "refactor", "test", "perf", "build", "ci", "style", "chore", "revert"})

    def test_types_without_a_table_fail(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as file:
            file.write("# Commit message conventions\n\n| `feat` | Add functionality |\n")
        self.addCleanup(os.remove, file.name)
        with self.assertRaises(ValueError):
            check_pr_metadata.load_types(file.name)

    def test_headings_come_from_the_convention(self):
        self.assertEqual(check_pr_metadata.load_headings(), HEADINGS)

    def test_pr_template_file_matches_the_convention(self):
        with open(os.path.join(ROOT, ".github", "pull_request_template.md"), encoding="utf-8") as file:
            findings = check_pr_metadata.check_body(file.read(), check_pr_metadata.load_headings())
        self.assertEqual(findings, ["the description has an HTML comment. Delete the comments of the template"])

    def test_scopes_come_from_the_config(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "config.json")
            with open(path, "w") as file:
                json.dump({"commit": {"scopes": [{"name": "intent", "area": "", "paths": []}]}}, file)
            self.assertEqual(check_pr_metadata.load_scopes(path), {"intent"})
            self.assertEqual(check_pr_metadata.load_scopes(os.path.join(directory, "missing.json")), set())


class Script(unittest.TestCase):
    def run_script(self, title, body=GOOD_BODY):
        env = {key: value for key, value in os.environ.items() if key not in ("PR_TITLE", "PR_BODY")}
        if title is not None:
            env["PR_TITLE"] = title
        if body is not None:
            env["PR_BODY"] = body
        return subprocess.run([sys.executable, SCRIPT], cwd=ROOT, env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    def test_good_pull_request_exits_0(self):
        self.assertEqual(self.run_script("feat(plugin): add the PR metadata check").returncode, 0)

    def test_bad_title_exits_1_with_findings(self):
        result = self.run_script("Feature(ci): Add the PR metadata check.")
        self.assertEqual(result.returncode, 1)
        self.assertIn("is not in the Types table", result.stderr)
        self.assertIn('the scope "ci" is not in commit.scopes', result.stderr)
        self.assertIn("lowercase letter", result.stderr)

    def test_bad_description_exits_1_with_findings(self):
        result = self.run_script("feat(plugin): add the PR metadata check", "## Summary\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn('PR description: the heading "Result" is missing', result.stderr)
        self.assertIn('PR description: the heading "Summary" is not in the template', result.stderr)

    def test_template_comments_exit_1(self):
        with open(os.path.join(ROOT, ".github", "pull_request_template.md"), encoding="utf-8") as file:
            result = self.run_script("feat(plugin): add the PR metadata check", file.read())
        self.assertEqual(result.returncode, 1)
        self.assertIn("PR description: the description has an HTML comment", result.stderr)

    def test_missing_title_or_body_exits_2(self):
        self.assertEqual(self.run_script(None).returncode, 2)
        self.assertEqual(self.run_script("feat: add a check", None).returncode, 2)

    def test_body_comes_only_from_pr_body(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json") as event:
            json.dump({"pull_request": {"body": GOOD_BODY}}, event)
            event.flush()
            os.environ["GITHUB_EVENT_PATH"] = event.name
            try:
                result = self.run_script("feat: add a check", None)
            finally:
                del os.environ["GITHUB_EVENT_PATH"]
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
