import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import git_guard  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "git_guard.py")


def fake_git(branch="feat/x", push_destination=None, calls=None):
    def run(args, cwd):
        if calls is not None:
            calls.append((args, cwd))
        if "symbolic-ref" in args:
            return branch
        if "@{push}" in args:
            return push_destination
        return None
    return run


class BlockedCommands(unittest.TestCase):
    def assert_blocked(self, commands, expected, git=None):
        for command in commands:
            with self.subTest(command=command):
                reason = git_guard.decide(command, "/repo", git or fake_git())
                self.assertIsNotNone(reason, "allowed: " + command)
                self.assertIn(expected, reason)

    def test_merge_pull_request(self):
        self.assert_blocked([
            "gh pr merge 12",
            "gh pr merge 12 --squash --auto",
            "gh pr merge --auto",
            "gh -R owner/repo pr merge 12",
            "gh pr --repo owner/repo merge 12",
            "gh api -X PUT repos/owner/repo/pulls/12/merge",
            "gh api -XPUT repos/{owner}/{repo}/pulls/12/merge",
            "gh api --method=PUT /repos/owner/repo/pulls/12/merge?x=1",
            "gh api https://api.github.com/repos/owner/repo/pulls/12/merge",
            "gh api repos/owner/repo/merges -f base=main -f head=feat/x",
            "gh api repos/owner/repo/pulls/12/merge",
            "gh api graphql -f query='mutation { mergePullRequest(input: {pullRequestId: \"x\"}) { clientMutationId } }'",
            "gh api graphql -f query='mutation { enablePullRequestAutoMerge(input: {}) { clientMutationId } }'",
            "gh api graphql -f query='mutation { enqueuePullRequest(input: {}) { clientMutationId } }'",
            "gh api graphql -f query='mutation { mergeBranch(input: {}) { clientMutationId } }'",
        ], "merges pull requests")

    def test_change_protection_or_settings(self):
        self.assert_blocked([
            "gh repo edit --enable-auto-merge",
            "gh repo edit owner/repo --default-branch dev",
            "gh repo rename new-name",
            "gh repo archive",
            "gh repo delete owner/repo --yes",
            "gh ruleset create",
            "gh api -X PATCH repos/owner/repo -f allow_auto_merge=true",
            "gh api repos/owner/repo -F delete_branch_on_merge=true",
            "gh api -X DELETE repos/owner/repo/rulesets/1",
            "gh api repos/owner/repo/rulesets --input ruleset.json",
            "gh api -X PUT repos/owner/repo/branches/main/protection --input p.json",
            "gh api -X DELETE repos/owner/repo/branches/main/protection",
            "gh api -X PATCH repos/owner/repo/git/refs/heads/main -f sha=abc -F force=true",
            "gh api -X PUT repos/owner/repo/contents/README.md -f message=x -f content=eA==",
            "gh api -X POST orgs/owner/rulesets --input r.json",
            "gh api graphql -f query='mutation { updateRepositoryRuleset(input: {}) { clientMutationId } }'",
            "gh api graphql -f query='mutation { deleteBranchProtectionRule(input: {}) { clientMutationId } }'",
            "gh api graphql -f query='mutation { updateRepository(input: {}) { clientMutationId } }'",
            "gh api graphql -f query='mutation { updateRefs(input: {}) { clientMutationId } }'",
        ], "Only the maintainer changes")

    def test_push_to_main(self):
        self.assert_blocked([
            "git push origin main",
            "git push origin HEAD:main",
            "git push origin feat/x:main",
            "git push origin HEAD:refs/heads/main",
            "git push origin refs/heads/main",
            "git push origin :main",
            "git push origin --delete main",
            "git push -d origin main",
            "git push -u origin main",
            "git push origin 'refs/heads/*:refs/heads/*'",
        ], "Do not push to or delete main")

    def test_push_while_on_main(self):
        on_main = fake_git(branch="main")
        self.assert_blocked(["git push", "git push origin", "git push -u origin HEAD", "git push origin @"],
                            "Do not push to or delete main", on_main)

    def test_push_to_an_upstream_of_main(self):
        self.assert_blocked(["git push"], "Do not push to or delete main",
                            fake_git(branch="feat/x", push_destination="origin/main"))

    def test_commit_on_main(self):
        self.assert_blocked(["git commit -m x", "git commit --amend --no-edit", "git -C ../other commit -m x"],
                            "Do not commit on main", fake_git(branch="main"))

    def test_force_push(self):
        self.assert_blocked([
            "git push -f",
            "git push -f origin feat/x",
            "git push -uf origin feat/x",
            "git push --force origin feat/x",
            "git push --force-with-lease origin feat/x",
            "git push --force-with-lease=feat/x:abc123 origin feat/x",
            "git push --force-if-includes origin feat/x",
            "git push --forc origin feat/x",
            "git push --mirror",
            "git push origin +feat/x",
            "git push origin +HEAD:feat/x",
        ], "Do not force-push")

    def test_push_all_branches(self):
        self.assert_blocked(["git push --all", "git push --branches origin", "git push --prune origin"],
                            "Name the branch to push")

    def test_no_verify(self):
        self.assert_blocked([
            "git commit --no-verify -m x",
            "git commit -n -m x",
            "git commit -nm x",
            "git commit -anm x",
            "git commit --no-veri -m x",
            "git push --no-verify origin feat/x",
        ], "Do not skip the Git hooks")

    def test_compound_and_wrapped_commands(self):
        self.assert_blocked([
            "git status && gh pr merge 12",
            "git status; gh pr merge 12",
            "git status || gh pr merge 12",
            "echo 12 | xargs gh pr merge",
            "(gh pr merge 12)",
            "{ gh pr merge 12; }",
            "echo $(gh pr merge 12)",
            "echo \"$(gh pr merge 12)\"",
            "echo `gh pr merge 12`",
            "bash -c 'gh pr merge 12'",
            "sh -lc \"gh pr merge 12\"",
            "eval 'gh pr merge 12'",
            "env GH_TOKEN=x gh pr merge 12",
            "env -i gh pr merge 12",
            "command gh pr merge 12",
            "GH_REPO=owner/repo gh pr merge 12",
            "/opt/homebrew/bin/gh pr merge 12",
            "timeout 30 gh pr merge 12",
            "if true; then gh pr merge 12; fi",
            "git status\ngh pr merge 12",
            "'gh' 'pr' 'merge' '12'",
            "g\\h pr merge 12",
        ], "merges pull requests")

    def test_git_options_before_the_subcommand(self):
        self.assert_blocked([
            "git -C ../repo push origin main",
            "git -c core.editor=vi push origin main",
            "git --no-pager push origin main",
        ], "Do not push to or delete main")

    def test_graphql_query_file(self):
        with tempfile.TemporaryDirectory() as folder:
            with open(os.path.join(folder, "merge.graphql"), "w") as handle:
                handle.write("mutation { mergePullRequest(input: {}) { clientMutationId } }")
            for command in ("gh api graphql -F query=@merge.graphql", "gh api graphql --input merge.graphql"):
                with self.subTest(command=command):
                    self.assertIn("merges pull requests", git_guard.decide(command, folder, fake_git()))
            for command in ("gh api graphql -F query=@missing.graphql", "gh api graphql --input -"):
                with self.subTest(command=command):
                    self.assertIsNotNone(git_guard.decide(command, folder, fake_git()))

    def test_unbalanced_quote_fails_closed(self):
        result = run_hook({"tool_input": {"command": "gh pr view 'x"}, "cwd": "."})
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot check the command", result.stderr)


class AllowedCommands(unittest.TestCase):
    def test_ordinary_work(self):
        for command in [
            "git status",
            "git switch -c feat/x",
            "git commit -m 'feat: add x'",
            "git commit --file /tmp/message.txt",
            "git commit -m 'do not run gh pr merge or git push --force'",
            "git commit -m \"$(cat <<'EOF'\nfeat: add x\n\ngh pr merge 12 is blocked\ngit push --force too\nEOF\n)\"",
            "git commit -m -n",
            "git push",
            "git push -u origin feat/x",
            "git push origin HEAD",
            "git push origin HEAD:feat/x",
            "git push -n origin feat/x",
            "git push --dry-run origin feat/x",
            "git push --follow-tags origin feat/x",
            "git push origin --delete feat/old",
            "git push origin main:feat/x",
            "git fetch origin main",
            "git pull --ff-only origin main",
            "git log main..HEAD",
            "git diff --check origin/main...HEAD",
            "gh pr create --draft --title 'feat: x' --body-file /tmp/body.md",
            "gh pr edit 12 --add-label type:feat",
            "gh pr view 12 --json state",
            "gh pr ready 12",
            "gh pr checks 12",
            "gh repo view",
            "gh ruleset list",
            "gh ruleset view 1",
            "gh ruleset check main",
            "gh label create type:feat --color 0E8A16",
            "gh api repos/owner/repo",
            "gh api repos/owner/repo/rulesets",
            "gh api repos/owner/repo/branches/main/protection",
            "gh api -X GET repos/owner/repo/pulls -f state=open",
            "gh api repos/owner/repo/pulls/12",
            "gh api repos/owner/repo/issues/12/comments -f body='LGTM'",
            "gh api -X PATCH repos/owner/repo/pulls/12 -f title=x",
            "gh api repos/owner/repo/pulls/12/comments/3/replies -f body=done",
            "gh api graphql -f query='query { viewer { login } }'",
            "echo 'gh pr merge 12' > notes.txt",
            "cat <<'EOF' > body.md\ngh pr merge 12\ngit push --force\nEOF",
            "grep -rn 'git push --force' docs",
            "python3 -m unittest discover -s hooks",
        ]:
            with self.subTest(command=command):
                self.assertIsNone(git_guard.decide(command, "/repo", fake_git()))

    def test_git_options_reach_the_branch_query(self):
        calls = []
        git_guard.decide("cd sub && git -C nested commit -m x", "/repo", fake_git(calls=calls))
        self.assertEqual(calls, [(["-C", "nested", "symbolic-ref", "--short", "-q", "HEAD"], "/repo/sub")])

    def test_hook_allows_a_plain_command(self):
        result = run_hook({"tool_input": {"command": "ls"}, "cwd": "."})
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_hook_blocks_with_exit_code_2(self):
        result = run_hook({"tool_input": {"command": "gh pr merge 12"}, "cwd": "."})
        self.assertEqual(result.returncode, 2)
        self.assertIn("git-guard blocked this command", result.stderr)


class KnownLimits(unittest.TestCase):
    def test_only_main_is_protected(self):
        git = fake_git(branch="master")
        for command in ("git commit -m x", "git push", "git push origin master"):
            with self.subTest(command=command):
                self.assertIsNone(git_guard.decide(command, "/repo", git))

    def test_quoted_operator_ends_a_command(self):
        reason = git_guard.decide("echo '&&' git push --force origin feat/x", "/repo", fake_git())
        self.assertIn("Do not force-push", reason)

    def test_abbreviated_value_option_does_not_skip_its_value(self):
        self.assertIsNone(git_guard.decide("git commit --message -n", "/repo", fake_git()))
        self.assertIn("Do not skip the Git hooks", git_guard.decide("git commit --mess -n", "/repo", fake_git()))

    def test_cd_in_a_subshell_applies_to_later_commands(self):
        calls = []
        git_guard.decide("(cd sub) && git commit -m x", "/repo", fake_git(calls=calls))
        self.assertEqual(calls[0][1], "/repo/sub")


def run_hook(data):
    return subprocess.run([sys.executable, SCRIPT], input=json.dumps(data), capture_output=True, text=True)


if __name__ == "__main__":
    unittest.main()
