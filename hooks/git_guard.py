#!/usr/bin/env python3
import fnmatch
import json
import os
import re
import shlex
import subprocess
import sys

PROTECTED_BRANCH = "main"

OPERATORS = "();<>|&`\n"
WRAPPERS = {"env", "command", "builtin", "exec", "nohup", "time", "nice", "timeout", "sudo", "xargs",
            "!", "{", "if", "then", "else", "elif", "do", "while", "until"}
SHELLS = {"sh", "bash", "zsh", "dash", "ksh"}
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")

GIT_VALUE_OPTIONS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env", "--super-prefix"}
COMMIT_LONG_VALUES = {"--message", "--file", "--author", "--date", "--reuse-message", "--reedit-message",
                      "--template", "--fixup", "--squash", "--trailer", "--cleanup", "--pathspec-from-file"}
PUSH_LONG_VALUES = {"--repo", "--push-option", "--receive-pack", "--exec"}
PUSH_FORCE_OPTIONS = ("--force", "--force-with-lease", "--force-if-includes", "--mirror")
PUSH_ALL_OPTIONS = ("--all", "--branches", "--prune")
API_LONG_VALUES = {"--method", "--header", "--field", "--raw-field", "--input", "--jq", "--template",
                   "--hostname", "--preview", "--cache"}
REPO_WRITES = {"edit", "rename", "archive", "unarchive", "delete"}
RULESET_READS = {"list", "ls", "view", "check"}
REPO_WRITE_PATHS = {"issues", "pulls", "labels", "milestones"}
GRAPHQL_MERGES = re.compile(r"\b(mergePullRequest|mergeBranch|enablePullRequestAutoMerge|enqueuePullRequest)\b")
GRAPHQL_SETTINGS = re.compile(
    r"\b((create|update|delete)(RepositoryRuleset|BranchProtectionRule)"
    r"|updateRepository|archiveRepository|(create|update|delete)Ref|updateRefs|createCommitOnBranch)\b"
)

MERGE = ("Only the maintainer merges pull requests. Do not merge a pull request, enable auto-merge, "
         "or add a pull request to a merge queue.")
SETTINGS = ("Only the maintainer changes branch protection, rulesets, refs, and repository settings. "
            "Ask the maintainer to make the change.")
API_WRITE = ("A `gh api` call can write only to the issues, pull requests, labels, and milestones of a "
             "repository. " + SETTINGS)
FORCE = "Do not force-push. If a pushed commit needs a fix, add a new commit."
NO_VERIFY = "Do not skip the Git hooks with --no-verify, or with -n on git commit. Fix the problem that the hook reports."
MAIN_PUSH = "Do not push to or delete {0}. Push your own branch, and open a pull request."
MAIN_COMMIT = "Do not commit on {0}. Create a branch from {0}, and commit there."
PUSH_ALL = "Name the branch to push. --all, --branches, and --prune can push to or delete {0}."


def strip_heredocs(text):
    rows, ends = [], []
    for row in text.split("\n"):
        if ends:
            if row.lstrip("\t") == ends[0]:
                ends.pop(0)
            continue
        rows.append(row)
        ends = [m.group(2) for m in HEREDOC.finditer(row) if row[m.start() - 1:m.start()] != "<"]
    return "\n".join(rows)


def split_commands(text):
    lexer = shlex.shlex(strip_heredocs(text), posix=True, punctuation_chars=OPERATORS)
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    commands, words = [], []
    for token in list(lexer) + [";"]:
        if set(token) <= set(OPERATORS):
            if words:
                commands.append(words)
            words = []
            continue
        words.append(token)
        for marker in ("$(", "`"):
            if marker in token:
                commands += split_commands(token.split(marker, 1)[1])
    for words in list(commands):
        name = os.path.basename(words[0])
        if name == "eval":
            commands += split_commands(" ".join(words[1:]))
        elif name in SHELLS:
            for i, word in enumerate(words[1:-1], 1):
                if word.startswith("-") and "c" in word[1:]:
                    commands += split_commands(words[i + 1])
    return commands


def parse(args, short_values="", long_values=(), short_optional=""):
    options, positionals, i = [], [], 0
    while i < len(args):
        arg = args[i]
        if arg == "--":
            positionals += args[i + 1:]
            break
        if arg.startswith("--"):
            name, equals, value = arg.partition("=")
            if not equals and name in long_values and i + 1 < len(args):
                i += 1
                value = args[i]
            options.append((name, value))
        elif arg.startswith("-") and len(arg) > 1:
            for j, letter in enumerate(arg[1:], 2):
                if letter in short_values:
                    value = arg[j:]
                    if not value and i + 1 < len(args):
                        i += 1
                        value = args[i]
                    options.append(("-" + letter, value))
                    break
                options.append(("-" + letter, ""))
                if letter in short_optional:
                    break
        else:
            positionals.append(arg)
        i += 1
    return options, positionals


def is_option(name, full):
    return len(name) > 2 and full.startswith(name)


def run_git(args, cwd):
    try:
        result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def check_commit(args, current_branch):
    options, _ = parse(args, "mFCct", COMMIT_LONG_VALUES, short_optional="Su")
    if any(name == "-n" or is_option(name, "--no-verify") for name, _ in options):
        return NO_VERIFY
    if current_branch() == PROTECTED_BRANCH:
        return MAIN_COMMIT.format(PROTECTED_BRANCH)
    return None


def check_push(args, current_branch, push_destination):
    options, positionals = parse(args, "o", PUSH_LONG_VALUES)
    for name, _ in options:
        if name == "-f" or any(is_option(name, full) for full in PUSH_FORCE_OPTIONS):
            return FORCE
        if is_option(name, "--no-verify"):
            return NO_VERIFY
        if any(is_option(name, full) for full in PUSH_ALL_OPTIONS):
            return PUSH_ALL.format(PROTECTED_BRANCH)
    refspecs = positionals[1:]
    if not refspecs:
        destination = push_destination() or ""
        if current_branch() == PROTECTED_BRANCH or destination.split("/", 1)[-1] == PROTECTED_BRANCH:
            return MAIN_PUSH.format(PROTECTED_BRANCH)
    for refspec in refspecs:
        if refspec.startswith("+"):
            return FORCE
        source, colon, destination = refspec.partition(":")
        if not colon:
            destination = source
        if destination in ("HEAD", "@"):
            destination = current_branch() or ""
        if destination.startswith("refs/heads/"):
            destination = destination[len("refs/heads/"):]
        if fnmatch.fnmatchcase(PROTECTED_BRANCH, destination):
            return MAIN_PUSH.format(PROTECTED_BRANCH)
    return None


def check_git(args, cwd, git):
    prefix, i = [], 0
    while i < len(args) and args[i].startswith("-"):
        size = 2 if args[i] in GIT_VALUE_OPTIONS else 1
        prefix += args[i:i + size]
        i += size
    if i >= len(args):
        return None
    subcommand, rest = args[i], args[i + 1:]

    def current_branch():
        return git(prefix + ["symbolic-ref", "--short", "-q", "HEAD"], cwd)

    def push_destination():
        return git(prefix + ["rev-parse", "--abbrev-ref", "@{push}"], cwd)

    if subcommand == "commit":
        return check_commit(rest, current_branch)
    if subcommand == "push":
        return check_push(rest, current_branch, push_destination)
    return None


def check_api(args, cwd, line):
    options, positionals = parse(args, "XHfFqtp", API_LONG_VALUES)
    endpoint = positionals[0] if positionals else ""
    path = re.sub(r"^https?://[^/]+/(api/v3/)?", "", endpoint).lstrip("/")
    parts = re.split(r"[?#]", path)[0].rstrip("/").split("/")
    method = "GET"
    for name, value in options:
        if name in ("-f", "-F", "--field", "--raw-field", "--input"):
            method = "POST"
    for name, value in options:
        if name in ("-X", "--method"):
            method = value.upper()
    files = [value for name, value in options if name == "--input"]
    files += [value.split("=@", 1)[1] for name, value in options if name in ("-F", "--field") and "=@" in value]

    if parts == ["graphql"]:
        texts = [line]
        for file in files:
            if file == "-":
                return "Pass the GraphQL query with -f query=... or in a file, so that this hook can read it."
            try:
                with open(os.path.join(cwd, file), encoding="utf-8") as handle:
                    texts.append(handle.read())
            except OSError:
                return "This hook cannot read the GraphQL query file {0}.".format(file)
        for pattern, reason in ((GRAPHQL_MERGES, MERGE), (GRAPHQL_SETTINGS, SETTINGS)):
            match = pattern.search("\n".join(texts))
            if match:
                return "Do not run the GraphQL mutation {0}. {1}".format(match.group(0), reason)
        return None

    writes = method not in ("GET", "HEAD")
    if parts[0] == "repos" and len(parts) >= 3:
        rest = parts[3:]
        if rest[:1] == ["merges"] or (rest[:1] == ["pulls"] and rest[2:3] == ["merge"]):
            return MERGE
        if writes and (not rest or rest[0] not in REPO_WRITE_PATHS):
            return API_WRITE
    elif writes and parts[0] in ("orgs", "enterprises"):
        return SETTINGS
    return None


def check_gh(args, cwd, line):
    _, words = parse(args, "R", {"--repo"})
    if words[:2] == ["pr", "merge"]:
        return MERGE
    if words[:1] == ["repo"] and words[1:2] and words[1] in REPO_WRITES:
        return SETTINGS
    if words[:1] in (["ruleset"], ["rs"]) and words[1:2] and words[1] not in RULESET_READS:
        return SETTINGS
    if words[:1] == ["api"]:
        return check_api(args[args.index("api") + 1:], cwd, line)
    return None


def decide(line, cwd, git=run_git):
    for words in split_commands(line):
        while words and ASSIGNMENT.match(words[0]):
            words = words[1:]
        if words and os.path.basename(words[0]) in WRAPPERS:
            names = [os.path.basename(word) for word in words]
            words = next((words[i:] for i, name in enumerate(names) if name in ("git", "gh")), [])
        if not words:
            continue
        name = os.path.basename(words[0])
        if name == "cd":
            cwd = os.path.join(cwd, os.path.expanduser(words[1] if len(words) > 1 else "~"))
        elif name == "git":
            reason = check_git(words[1:], cwd, git)
            if reason:
                return reason
        elif name == "gh":
            reason = check_gh(words[1:], cwd, line)
            if reason:
                return reason
    return None


def main():
    try:
        data = json.load(sys.stdin)
        command = (data.get("tool_input") or {}).get("command") or ""
        reason = decide(command, data.get("cwd") or os.getcwd())
    except Exception as error:
        reason = "This hook cannot check the command ({0}). Simplify the command.".format(error)
    if reason:
        print("git-guard blocked this command. " + reason, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
