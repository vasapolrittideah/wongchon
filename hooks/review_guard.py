#!/usr/bin/env python3
import json
import os
import re
import shlex
import sys

HOOKS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HOOKS)
sys.path.insert(0, os.path.join(os.path.dirname(HOOKS), "scripts"))
import git_guard  # noqa: E402
import review  # noqa: E402

COMMIT_SHORT_VALUES = "mFCct"
COMMIT_STAGING_OPTIONS = ("--all", "--include", "--only", "--interactive", "--patch", "--pathspec-from-file")
PR_SHORT_VALUES = "tbFBHRalmprT"
PR_TEXT_OPTIONS = {"-t", "--title", "-b", "--body", "-F", "--body-file", "-f", "--fill", "--fill-first",
                   "--fill-verbose", "-T", "--template", "-w", "--web", "-e", "--editor"}
PR_UNREADABLE = {"-b", "--body", "-f", "--fill", "--fill-first", "--fill-verbose", "-T", "--template", "-w", "--web",
                 "-e", "--editor"}
GIT_VARIABLE = re.compile(r"^GIT_[A-Z_]*=")
REDIRECTION = re.compile(r"\d*(>>|>&|>)")
FD_TARGET = re.compile(r"\d+|-")
FILE_TARGET = re.compile(r"[ \t]*[^\s;&|()<>`'\"$\\]+")
PR_LONG_VALUES = {"--title", "--body", "--body-file", "--base", "--head", "--repo", "--label", "--assignee",
                  "--milestone", "--project", "--reviewer", "--template", "--add-label", "--remove-label",
                  "--add-assignee", "--remove-assignee", "--add-project", "--remove-project",
                  "--add-reviewer", "--remove-reviewer", "--recover"}

ALONE = "Run `{0}` as the only command of the shell command, so that the review covers what it sends."
STAGING = ("Stage the files with `git add` first, and then run `git commit` without -a, -i, -o, -p, "
           "--pathspec-from-file, or paths, so that the commit holds the staged tree that the roles reviewed.")
GIT_OPTIONS = ("Run `git commit` without -c, --git-dir, --work-tree, --namespace, or a GIT_ variable such as "
               "GIT_INDEX_FILE, so that this hook reads the same tree.")
MISSING = ("The staged tree {0} has no approval stamp of {1}. Run `python3 scripts/review.py <role>` for each "
           "missing role, fix the Important findings, and commit after each role approves.")
PR_TEXT = ("Pass the title with --title and the description with 1 --body-file, and not --body, --fill, "
           "--template, --web, or --editor, so that this hook can check the review of the PR text.")
PR_MISSING = ("The PR text has no approval stamp of {0}. Write the title on the first line of a file and the "
              "description after it, and run `python3 scripts/review.py {0} --pr-text <file>`. After it approves, "
              "pass the first line as --title and a file with only the description as --body-file.")


def strip_redirections(text):
    rows, ends, quote = [], [], None
    for row in text.split("\n"):
        if ends:
            if row.lstrip("\t") == ends[0]:
                ends.pop(0)
            rows.append(row)
            continue
        row, quote = strip_row(row, quote)
        rows.append(row)
        if not quote:
            ends = [m.group(2) for m in git_guard.HEREDOC.finditer(row) if row[m.start() - 1:m.start()] != "<"]
    return "\n".join(rows)


def strip_row(line, quote=None):
    out, i = [], 0
    while i < len(line):
        char = line[i]
        if quote:
            if char == "\\" and quote == '"':
                out.append(line[i:i + 2])
                i += 2
                continue
            if char == quote:
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "\\":
            out.append(line[i:i + 2])
            i += 2
            continue
        elif i == 0 or line[i - 1].isspace():
            match = REDIRECTION.match(line, i)
            target = match and (FD_TARGET if match.group(1) == ">&" else FILE_TARGET).match(line, match.end())
            if target:
                out.append(" ")
                i = target.end()
                continue
        out.append(char)
        i += 1
    return "".join(out), quote


def command_words(line):
    lexer = shlex.shlex(git_guard.strip_heredocs(line), posix=True, punctuation_chars=";&|`\n()")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    commands, words = [], []
    for token in list(lexer) + [";"]:
        if set(token) <= set(";&|`\n()"):
            if words:
                commands.append(words)
            words = []
        else:
            words.append(token)
            if "$(" in token or "`" in token:
                commands.append([token])
    return commands


def alone(line):
    commands = [words for words in command_words(line) if os.path.basename(words[0]) != "cd"]
    nested = any(os.path.basename(word) in git_guard.SHELLS or word == "eval" for words in commands for word in words)
    return len(commands) <= 1 and not nested


def missing_roles(cwd):
    os.chdir(cwd)
    tree = review.staged_tree()
    if tree == review.head_tree():
        return tree, []
    roles = review.required_roles(review.changed_paths(tree))
    missing = []
    for role in roles:
        try:
            review.read_stamp(role, tree)
        except review.ReviewError:
            missing.append(role)
    return tree, missing


def check_commit(args, cwd):
    options, positionals = git_guard.parse(args, COMMIT_SHORT_VALUES, git_guard.COMMIT_LONG_VALUES,
                                           short_optional="Su")
    for name, _ in options:
        if name in ("-a", "-i", "-o", "-p") or any(git_guard.is_option(name, full) for full in COMMIT_STAGING_OPTIONS):
            return STAGING
    if positionals:
        return STAGING
    tree, missing = missing_roles(cwd)
    if missing:
        return MISSING.format(tree, ", ".join(missing))
    return None


def pr_text(options, cwd):
    titles = [value for name, value in options if name in ("-t", "--title")]
    bodies = [value for name, value in options if name in ("-F", "--body-file")]
    if any(name in PR_UNREADABLE for name, _ in options):
        return None
    if len(titles) != 1 or len(bodies) != 1 or bodies[0] == "-":
        return None
    with open(os.path.join(cwd, bodies[0]), encoding="utf-8") as file:
        return titles[0] + "\n" + file.read()


def check_pr(subcommand, args, cwd):
    options, _ = git_guard.parse(args, PR_SHORT_VALUES, PR_LONG_VALUES)
    names = {name for name, _ in options}
    if subcommand == "edit" and not names & PR_TEXT_OPTIONS:
        return None
    text = pr_text(options, cwd)
    if text is None:
        return PR_TEXT
    os.chdir(cwd)
    try:
        review.read_stamp(review.PR_TEXT_ROLE, review.text_key(text))
    except review.ReviewError:
        return PR_MISSING.format(review.PR_TEXT_ROLE)
    return None


def git_target(words, cwd):
    args, i = words[1:], 0
    while i < len(args) and args[i].startswith("-"):
        if args[i] == "-C" and i + 1 < len(args):
            cwd = os.path.join(cwd, os.path.expanduser(args[i + 1]))
            i += 2
        elif args[i] in git_guard.GIT_VALUE_OPTIONS or args[i].startswith(("--git-dir", "--work-tree", "--namespace")):
            return None, None, None
        else:
            i += 1
    if i >= len(args):
        return cwd, None, []
    return cwd, args[i], args[i + 1:]


def gh_pr(words):
    _, positionals = git_guard.parse(words[1:], "R", {"--repo"})
    if positionals[:1] == ["pr"] and positionals[1:2] and positionals[1] in ("create", "new", "edit"):
        index = words.index(positionals[1])
        return {"new": "create"}.get(positionals[1], positionals[1]), words[index + 1:]
    return None, None


def decide(line, cwd):
    line = strip_redirections(line)
    commands = []
    for words in git_guard.split_commands(line):
        names = [os.path.basename(word) for word in words]
        before_git = words[:names.index("git")] if "git" in names else []
        if "commit" in words and any(GIT_VARIABLE.match(word) for word in before_git):
            return GIT_OPTIONS
        while words and git_guard.ASSIGNMENT.match(words[0]):
            words = words[1:]
        if words and os.path.basename(words[0]) in git_guard.WRAPPERS:
            names = [os.path.basename(word) for word in words]
            words = next((words[i:] for i, name in enumerate(names) if name in ("git", "gh")), words)
        if words:
            commands.append(words)
    for words in commands:
        name = os.path.basename(words[0])
        if name == "cd":
            cwd = os.path.join(cwd, os.path.expanduser(words[1] if len(words) > 1 else "~"))
        elif name == "git":
            target, subcommand, rest = git_target(words, cwd)
            if target is None:
                if "commit" in words:
                    return GIT_OPTIONS
                continue
            if subcommand == "commit":
                if not alone(line):
                    return ALONE.format("git commit")
                reason = check_commit(rest, target)
                if reason:
                    return reason
        elif name == "gh":
            subcommand, rest = gh_pr(words)
            if subcommand:
                if not alone(line):
                    return ALONE.format("gh pr " + subcommand)
                reason = check_pr(subcommand, rest, cwd)
                if reason:
                    return reason
    return None


def main():
    try:
        data = json.load(sys.stdin)
        command = (data.get("tool_input") or {}).get("command") or ""
        reason = decide(command, data.get("cwd") or os.getcwd())
    except Exception as error:
        reason = "This hook cannot check the review of the command ({0}). The command stays blocked.".format(error)
    if reason:
        print("review-guard blocked this command. " + reason, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
