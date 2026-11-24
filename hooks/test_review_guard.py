import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_guard  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "review_guard.py")

ROLES = {
    "code-reviewer": '  - "**"\n  - "!**/*.md"\n',
    "writing-reviewer": '  - "**/*.md"\n',
    "artifact-reviewer": '  - "docs/specs/**"\n',
}


def role(name, paths):
    return ("---\nname: {0}\ndescription: Reviews.\nmodel: opus\neffort: medium\npaths:\n{1}---\n\n# Role\n"
            .format(name, paths))


def run(args, cwd):
    return subprocess.run(["git"] + args, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True).stdout.strip()


class Guard(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        self.folder = tempfile.mkdtemp()
        self.repo = os.path.realpath(os.path.join(self.folder, "repo"))
        os.makedirs(os.path.join(self.repo, "reviewers"))
        run(["init", "-q", "-b", "feat/x"], self.repo)
        run(["config", "user.email", "test@example.com"], self.repo)
        run(["config", "user.name", "Test"], self.repo)
        for name, paths in ROLES.items():
            self.write("reviewers/{0}.md".format(name), role(name, paths))
        run(["add", "."], self.repo)
        run(["commit", "-q", "-m", "roles"], self.repo)
        run(["update-ref", "refs/remotes/origin/main", "HEAD"], self.repo)
        run(["symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main"], self.repo)

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.folder)

    def write(self, path, text):
        path = os.path.join(self.repo, path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)

    def stage(self, path, text="x\n"):
        self.write(path, text)
        run(["add", path], self.repo)

    def stamp(self, role_name, key=None):
        key = key or run(["write-tree"], self.repo)
        folder = os.path.join(self.repo, ".git", "wongchon", "reviews", role_name)
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, key), "w", encoding="utf-8") as file:
            json.dump({"role": role_name, "key": key}, file)

    def decide(self, line, cwd=None):
        return review_guard.decide(line, cwd or self.repo)

    def test_commit_without_the_stamp_of_a_role_is_blocked(self):
        self.stage("a.py")
        reason = self.decide("git commit -m 'feat: add a'")
        self.assertIn("no approval stamp of code-reviewer", reason)
        self.assertIn("python3 scripts/review.py", reason)

    def test_commit_with_each_stamp_is_allowed(self):
        self.stage("a.py")
        self.stage("docs/specs/a.md")
        self.stamp("code-reviewer")
        self.stamp("writing-reviewer")
        self.assertIn("artifact-reviewer", self.decide("git commit -m x"))
        self.stamp("artifact-reviewer")
        self.assertIsNone(self.decide("git commit -m x"))
        self.assertIsNone(self.decide("git commit -F - <<'EOF'\nfeat: add a\n\nBody.\nEOF"))

    def test_stamp_of_another_tree_does_not_count(self):
        self.stage("a.py")
        self.stamp("code-reviewer")
        self.stage("a.py", "y\n")
        self.assertIn("code-reviewer", self.decide("git commit -m x"))

    def test_stamp_that_names_another_role_does_not_count(self):
        self.stage("a.py")
        tree = run(["write-tree"], self.repo)
        folder = os.path.join(self.repo, ".git", "wongchon", "reviews", "code-reviewer")
        os.makedirs(folder)
        with open(os.path.join(folder, tree), "w", encoding="utf-8") as file:
            json.dump({"role": "writing-reviewer", "key": tree}, file)
        self.assertIn("code-reviewer", self.decide("git commit -m x"))

    def test_commit_of_the_same_tree_is_allowed(self):
        self.assertIsNone(self.decide("git commit --amend -m 'feat: better message'"))

    def test_commit_that_stages_files_itself_is_blocked(self):
        self.stage("a.py")
        self.stamp("code-reviewer")
        for line in ["git commit -a -m x", "git commit -am x", "git commit -m x a.py", "git commit --all -m x",
                     "git commit -i a.py -m x", "git commit --only -m x a.py", "git commit -p", "git commit -- a.py",
                     "git commit --pathspec-from-file=list -m x"]:
            with self.subTest(line=line):
                self.assertEqual(self.decide(line), review_guard.STAGING)

    def test_commit_with_another_command_is_blocked(self):
        self.stage("a.py")
        self.stamp("code-reviewer")
        for line in ["git add b.py && git commit -m x", "git commit -m x; echo done", "echo $(git commit -m x)",
                     'bash -c "git add b.py && git commit -m x"', "eval 'git add b.py; git commit -m x'",
                     'sh -c "git commit -m x"']:
            with self.subTest(line=line):
                self.assertIn("only command", self.decide(line))

    def test_commit_follows_cd_and_git_c(self):
        self.stage("a.py")
        self.assertIn("code-reviewer", self.decide("cd {0} && git commit -m x".format(self.repo), "/"))
        self.assertIn("code-reviewer", self.decide("git -C {0} commit -m x".format(self.repo), "/"))
        self.assertIn("code-reviewer", self.decide("cd sub && git commit -m x".replace("sub", "."), self.repo))

    def test_commit_with_options_that_change_the_tree_is_blocked(self):
        for line in ["git --git-dir=/tmp/other commit -m x", "git --work-tree /tmp commit -m x",
                     "git -c core.hooksPath=/dev/null commit -m x", "GIT_INDEX_FILE=/tmp/i git commit -m x",
                     "env GIT_INDEX_FILE=/tmp/i git commit -m x", "GIT_DIR=/tmp/g GIT_WORK_TREE=/tmp git commit -m x",
                     "env GIT_INDEX_FILE=/tmp/i /usr/bin/git commit -m x"]:
            with self.subTest(line=line):
                self.assertEqual(self.decide(line), review_guard.GIT_OPTIONS)

    def test_commit_outside_a_repository_is_blocked(self):
        with self.assertRaises(Exception):
            self.decide("git commit -m x", self.folder)

    def test_commit_without_origin_is_blocked(self):
        self.stage("a.py")
        run(["symbolic-ref", "--delete", "refs/remotes/origin/HEAD"], self.repo)
        run(["update-ref", "-d", "refs/remotes/origin/main"], self.repo)
        with self.assertRaises(Exception):
            self.decide("git commit -m x")

    def test_commit_with_a_redirect_or_a_heredoc_is_alone(self):
        self.stage("a.py")
        self.stamp("code-reviewer")
        for line in ["git commit -m x > /tmp/log", "git commit -F - <<'EOF'\nfeat: add a\nEOF",
                     "git commit -F msg 2>&1", "git commit -m x >> log.txt", "git commit -m x 2> err.txt",
                     "git commit -m x >log 2>&1", "git commit -m 'a > b' 2>&1", "git commit -m x 2>&-",
                     ">log git commit -m x", "2>/dev/null git commit -m x",
                     "git commit -F - <<'EOF' 2>&1\nfeat: don't stop\nEOF", 'git commit -m "feat: x\n\nBody." 2>&1']:
            with self.subTest(line=line):
                self.assertIsNone(self.decide(line))

    def test_commit_with_a_redirection_and_another_command_is_blocked(self):
        self.stage("a.py")
        self.stamp("code-reviewer")
        for line in ["git commit -m x 2>&1 | tail", "git commit -m x 2>&1; echo done", "git commit -m x > log && ls",
                     "git commit -m x 2> err || ls", "git commit -m x > $(echo log)", "git commit -m x >`echo log`"]:
            with self.subTest(line=line):
                self.assertIn("only command", self.decide(line))

    def test_commit_after_a_heredoc_still_needs_its_stamp(self):
        self.stage("a.py")
        for line in ["cat <<EOF\nx\nEOF\ngit commit -m x", "git commit -F - <<'EOF'\nmsg\nEOF\ngit commit -m y",
                     "cat <<EOF 2>&1\ndon't\nEOF\ngit commit -m x 2>&1"]:
            with self.subTest(line=line):
                self.assertIsNotNone(self.decide(line))

    def test_row_that_ends_inside_a_quote_starts_no_heredoc(self):
        self.assertEqual(review_guard.strip_redirections('git commit -m "a <<EOF\nb" 2>&1'),
                         'git commit -m "a <<EOF\nb"  ')

    def test_backslash_in_single_quotes_is_literal(self):
        self.assertEqual(review_guard.strip_redirections("echo 'a\\' 2>&1"), "echo 'a\\'  ")

    def test_quoted_heredoc_marker_stays_blocked(self):
        with self.assertRaises(ValueError):
            self.decide('git commit -m "a <<EOF\nb" 2>&1')

    def test_here_string_is_not_a_heredoc(self):
        self.assertEqual(review_guard.strip_redirections("cat <<<EOF 2>&1\ngit commit -m x 2>&1"),
                         "cat <<<EOF  \ngit commit -m x  ")

    def test_heredoc_body_keeps_its_redirections(self):
        line = "cat <<EOF\na 2>&1 b\nEOF\n"
        self.assertEqual(review_guard.strip_redirections(line), line)

    def test_redirection_without_a_target_or_in_a_word_stays(self):
        for line, kept in [("git commit -m x 2>", "2>"), ("git commit -m a2>b", "a2>b"), ('echo "2>&1"', '"2>&1"'),
                           ("git commit -m x 2>&y", "2>&y"), ('git commit -m "a \\" 2>&1"', '2>&1'),
                           ("echo \\>x", "\\>x")]:
            with self.subTest(line=line):
                self.assertIn(kept, review_guard.strip_redirections(line))

    def test_other_git_commands_are_allowed(self):
        self.stage("a.py")
        for line in ["git status", "git add a.py", "git push -u origin feat/x", "git log --oneline -1"]:
            with self.subTest(line=line):
                self.assertIsNone(self.decide(line))

    def pr_file(self, text="## Result\n\nText.\n"):
        path = os.path.join(self.folder, "body.md")
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        return path

    def test_pr_without_the_stamp_of_its_text_is_blocked(self):
        body = self.pr_file()
        reason = self.decide("gh pr create --draft --title 'feat: add a' --body-file {0}".format(body))
        self.assertIn("no approval stamp of writing-reviewer", reason)

    def test_pr_with_the_stamp_of_its_text_is_allowed(self):
        body = self.pr_file()
        self.stamp("writing-reviewer", review_guard.review.text_key("feat: add a\n## Result\n\nText.\n"))
        for line in ["gh pr create --draft --base main --title 'feat: add a' --body-file {0} --label type:feat",
                     "gh pr create -t 'feat: add a' -F {0}",
                     "gh pr create -d -t 'feat: add a' -F {0}",
                     "gh pr new --title 'feat: add a' --body-file {0}",
                     "gh pr edit 41 --title 'feat: add a' --body-file {0}"]:
            with self.subTest(line=line):
                self.assertIsNone(self.decide(line.format(body)))

    def test_pr_text_that_the_hook_cannot_read_is_blocked(self):
        body = self.pr_file()
        for line in ["gh pr create --title t --body text", "gh pr create --fill", "gh pr create --web",
                     "gh pr create --title t", "gh pr create --title t --body-file -",
                     "gh pr edit 41 --body-file {0}", "gh pr edit 41 --title t",
                     "gh pr create --title t --body-file {0} --body-file {0}",
                     "gh pr create -t t -F {0} -d -F other.md", "gh pr create -e -t t -F {0}",
                     "gh pr new --title t --body text", "gh pr edit 41 --editor"]:
            with self.subTest(line=line):
                self.assertEqual(self.decide(line.format(body)), review_guard.PR_TEXT)

    def test_pr_with_another_command_is_blocked(self):
        body = self.pr_file()
        self.assertIn("only command", self.decide("git push && gh pr create --title t --body-file " + body))

    def test_pr_edit_without_text_and_other_gh_commands_are_allowed(self):
        for line in ["gh pr edit 41 --add-label type:feat", "gh pr ready 41", "gh pr view 41", "gh issue list"]:
            with self.subTest(line=line):
                self.assertIsNone(self.decide(line))

    def test_main_blocks_an_unreadable_input_and_a_missing_stamp(self):
        self.stage("a.py")
        for data in ["not json", json.dumps({"tool_input": {"command": "git commit -m x"}, "cwd": self.repo})]:
            with self.subTest(data=data):
                result = subprocess.run([sys.executable, SCRIPT], input=data, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, universal_newlines=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn("review-guard blocked this command.", result.stderr)

    def test_main_allows_a_command_without_a_review(self):
        data = json.dumps({"tool_input": {"command": "git status"}, "cwd": self.repo})
        result = subprocess.run([sys.executable, SCRIPT], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
