#!/usr/bin/env python3
import argparse
import datetime
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote

ROLE_FOLDER = "reviewers"
PR_TEXT_ROLE = "writing-reviewer"
ROLE_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ROLE_FILE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
REQUIRED_FIELDS = ("name", "description", "model", "effort", "paths")
SEVERITIES = ("Important", "Nit", "Pre-existing")
FINDING_FIELDS = ("severity", "file", "line", "rule", "problem", "fix")
MAX_ROUNDS = 3
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
FRAMEWORK_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW_TIMEOUT_SECONDS = 1800

SCHEMA = {
    "type": "object",
    "required": ["summary", "findings"],
    "properties": {
        "summary": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": list(FINDING_FIELDS),
                "properties": {
                    "severity": {"type": "string", "enum": list(SEVERITIES)},
                    "file": {"type": "string"},
                    "line": {"type": "integer"},
                    "rule": {"type": "string"},
                    "problem": {"type": "string"},
                    "fix": {"type": "string"},
                },
            },
        },
    },
}


class ReviewError(Exception):
    pass


def git(*args, env=None):
    result = subprocess.run(["git"] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            encoding="utf-8", errors="replace", env=env)
    if result.returncode != 0:
        raise ReviewError("git {0} failed: {1}".format(" ".join(args), result.stderr.strip()))
    return result.stdout


def default_ref():
    try:
        return git("symbolic-ref", "--short", "refs/remotes/origin/HEAD").strip()
    except ReviewError:
        try:
            git("rev-parse", "--verify", "--quiet", "refs/remotes/origin/main")
        except ReviewError:
            raise ReviewError("the script reads the role files from the default branch on origin, but neither "
                              "origin/HEAD nor origin/main exists. Run `git fetch origin` and "
                              "`git remote set-head origin --auto`.")
        return "origin/main"


def common_dir():
    return os.path.abspath(git("rev-parse", "--path-format=absolute", "--git-common-dir").strip())


def reviews_dir(role):
    return os.path.join(common_dir(), "wongchon", "reviews", role)


def stamp_path(role, key):
    return os.path.join(reviews_dir(role), key)


def text_key(text):
    return "text-" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def rounds_path(role, branch):
    return os.path.join(reviews_dir(role), "rounds", quote(branch, safe=""))


def current_branch():
    try:
        return git("symbolic-ref", "--short", "HEAD").strip()
    except ReviewError:
        raise ReviewError("HEAD is not on a branch. Check out the branch of the change before the review.")


def project_root():
    return git("rev-parse", "--show-toplevel").strip()


def glob_regex(pattern):
    parts = []
    index = 0
    while index < len(pattern):
        if pattern.startswith("**/", index):
            parts.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("**", index):
            parts.append(".*")
            index += 2
        elif pattern[index] == "*":
            parts.append("[^/]*")
            index += 1
        elif pattern[index] == "?":
            parts.append("[^/]")
            index += 1
        else:
            parts.append(re.escape(pattern[index]))
            index += 1
    return re.compile("".join(parts) + r"\Z")


def matches(path, patterns):
    matched = False
    for pattern in patterns:
        negated = pattern.startswith("!")
        if glob_regex(pattern[1:] if negated else pattern).match(path):
            matched = not negated
    return matched


def parse_front_matter(text):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ReviewError("the role file has no front matter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise ReviewError("the front matter of the role file has no end line")
    fields = {}
    key = None
    for line in lines[1:end]:
        item = re.match(r"^\s+- (.*)$", line)
        if item and key:
            values = fields.setdefault(key, [])
            if not isinstance(values, list):
                raise ReviewError("the field {0} has a value and also list items".format(key))
            values.append(item.group(1).strip().strip('"'))
            continue
        pair = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if not pair:
            raise ReviewError("cannot read the front matter line: " + line)
        key, value = pair.group(1), pair.group(2).strip()
        if value:
            fields[key] = value.strip('"')
    missing = [field for field in REQUIRED_FIELDS if not fields.get(field)]
    if missing:
        raise ReviewError("the role file lacks the fields: " + ", ".join(missing))
    if not isinstance(fields["paths"], list):
        raise ReviewError("the paths field of the role file is not a list")
    return fields, "\n".join(lines[end + 1:]).strip() + "\n"


def load_role(role, ref=None):
    if not ROLE_NAME.match(role):
        raise ReviewError("{0} is not a role name".format(role))
    ref = ref or default_ref()
    text = git("show", "{0}:{1}/{2}.md".format(ref, ROLE_FOLDER, role))
    fields, body = parse_front_matter(text)
    if fields["name"] != role:
        raise ReviewError("the role file of {0} has the name {1}".format(role, fields["name"]))
    return fields, body


def list_roles(ref=None):
    ref = ref or default_ref()
    names = git("ls-tree", "--name-only", "{0}:{1}".format(ref, ROLE_FOLDER)).split()
    return sorted(name[:-3] for name in names if ROLE_FILE.match(name))


def required_roles(paths, ref=None):
    ref = ref or default_ref()
    roles = []
    for role in list_roles(ref):
        fields, _ = load_role(role, ref)
        if any(matches(path, fields["paths"]) for path in paths):
            roles.append(role)
    return roles


def head_tree():
    try:
        return git("rev-parse", "HEAD^{tree}").strip()
    except ReviewError:
        return EMPTY_TREE


def staged_tree():
    index = os.path.abspath(git("rev-parse", "--path-format=absolute", "--git-path", "index").strip())
    with tempfile.TemporaryDirectory() as folder:
        copy = os.path.join(folder, "index")
        if os.path.exists(index):
            shutil.copyfile(index, copy)
        env = dict(os.environ, GIT_INDEX_FILE=copy)
        return git("write-tree", env=env).strip()


def changed_paths(tree):
    output = git("diff", "-z", "--name-only", "--no-renames", head_tree(), tree)
    return [path for path in output.split("\0") if path]


def read_round(role, branch):
    try:
        with open(rounds_path(role, branch), encoding="utf-8") as file:
            return int(file.read().strip() or "0")
    except FileNotFoundError:
        return 0
    except ValueError:
        raise ReviewError("the count of rounds of {0} on {1} is not a number".format(role, branch))


def write_round(role, branch, count):
    path = rounds_path(role, branch)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(str(count) + "\n")


def reset_rounds(role, branch):
    try:
        os.remove(rounds_path(role, branch))
    except FileNotFoundError:
        pass


def review_command():
    return shlex.split(os.environ.get("WONGCHON_REVIEW_COMMAND", "claude"))


def run_reviewer(fields, body, request):
    command = review_command() + [
        "-p", "--safe-mode", "--tools", "Read,Grep,Glob", "--permission-mode", "dontAsk",
        "--no-session-persistence", "--output-format", "json", "--json-schema", json.dumps(SCHEMA),
        "--model", fields["model"], "--effort", fields["effort"], "--append-system-prompt", body,
        "--add-dir", FRAMEWORK_ROOT]
    try:
        result = subprocess.run(command, input=request, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                encoding="utf-8", errors="replace", timeout=REVIEW_TIMEOUT_SECONDS,
                                cwd=project_root())
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ReviewError("the reviewer did not run: {0}".format(error))
    if result.returncode != 0:
        raise ReviewError("the reviewer exited with {0}: {1}".format(result.returncode, result.stderr.strip()))
    return parse_output(result.stdout)


def parse_output(stdout):
    try:
        output = json.loads(stdout)
    except ValueError:
        raise ReviewError("the output of the reviewer is not JSON")
    if not isinstance(output, dict) or output.get("is_error"):
        raise ReviewError("the reviewer returned an error: {0}".format(str(output)[:500]))
    report = output.get("structured_output")
    if not isinstance(report, dict) or not isinstance(report.get("summary"), str):
        raise ReviewError("the reviewer returned no structured output")
    findings = report.get("findings")
    if not isinstance(findings, list):
        raise ReviewError("the structured output has no list of findings")
    for finding in findings:
        if not isinstance(finding, dict) or any(field not in finding for field in FINDING_FIELDS):
            raise ReviewError("a finding lacks a field of the schema: {0}".format(finding))
        if finding["severity"] not in SEVERITIES:
            raise ReviewError("a finding has an unknown severity: {0}".format(finding["severity"]))
    return report


def approves(report):
    return not any(finding["severity"] == "Important" and str(finding["rule"]).strip()
                   for finding in report["findings"])


def build_request(mode, content, reply):
    parts = [
        "Framework folder: " + FRAMEWORK_ROOT,
        "Project root: " + project_root(),
        "Mode: " + mode,
        "",
        content,
    ]
    if reply:
        parts += ["", "Findings of the last round and the replies of the author:", "", reply]
    return "\n".join(parts) + "\n"


def write_stamp(role, key, fields, report):
    path = stamp_path(role, key)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    stamp = {
        "role": role,
        "key": key,
        "model": fields["model"],
        "effort": fields["effort"],
        "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "summary": report["summary"],
        "findings": report["findings"],
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(stamp, file, indent=2)
        file.write("\n")
    return path


def read_stamp(role, key):
    try:
        with open(stamp_path(role, key), encoding="utf-8") as file:
            stamp = json.load(file)
    except (OSError, ValueError) as error:
        raise ReviewError("cannot read the stamp of {0} for {1}: {2}".format(role, key, error))
    if not isinstance(stamp, dict) or stamp.get("role") != role or stamp.get("key") != key:
        raise ReviewError("the stamp of {0} for {1} does not name that role and key".format(role, key))
    return stamp


def print_report(role, report, approved):
    for finding in report["findings"]:
        print("- {severity} {file}:{line} [{rule}] {problem} Fix: {fix}".format(**finding))
    print("summary: " + report["summary"])
    print("verdict: {0} ({1})".format("APPROVE" if approved else "REQUEST_CHANGES", role))


def review(role, pr_text=None, reply=None):
    if pr_text is not None and role != PR_TEXT_ROLE:
        raise ReviewError("only {0} reviews the text of a PR".format(PR_TEXT_ROLE))
    fields, body = load_role(role)
    branch = current_branch()
    done = read_round(role, branch)
    if done >= MAX_ROUNDS:
        raise ReviewError(
            "{0} did not approve this branch in {1} rounds. Stop and ask the maintainer. Only the maintainer "
            "runs `python3 scripts/review.py {0} --reset-rounds` after they decide.".format(role, MAX_ROUNDS))
    if pr_text is not None:
        key = text_key(pr_text)
        request = build_request("PR text", pr_text, reply)
    else:
        tree = staged_tree()
        changed = changed_paths(tree)
        paths = [path for path in changed if matches(path, fields["paths"])]
        if not paths:
            raise ReviewError("the staged change has no file that {0} reviews".format(role))
        key = tree
        pathspecs = [] if paths == changed else ["--"] + [":(top,literal)" + path for path in paths]
        diff = git("diff", "--no-renames", "--no-ext-diff", "--no-textconv", "--no-color", "--src-prefix=a/",
                   "--dst-prefix=b/", head_tree(), tree, *pathspecs)
        if not diff.strip():
            raise ReviewError("the diff of the files of {0} is empty".format(role))
        request = build_request("staged change", diff, reply)
    report = run_reviewer(fields, body, request)
    approved = approves(report)
    if approved:
        write_stamp(role, key, fields, report)
        reset_rounds(role, branch)
    else:
        write_round(role, branch, done + 1)
    print_report(role, report, approved)
    print("round: {0} of {1}".format(done + 1, MAX_ROUNDS))
    return approved


def main(argv=None):
    parser = argparse.ArgumentParser(description="Review the staged change or the text of a PR with 1 review role.")
    parser.add_argument("role")
    parser.add_argument("--pr-text", help="file with the PR title on the first line and the description after it")
    parser.add_argument("--reply", help="file with the findings of the last round and the replies of the author")
    parser.add_argument("--reset-rounds", action="store_true", help="for the maintainer only")
    args = parser.parse_args(argv)
    try:
        if args.reset_rounds:
            load_role(args.role)
            reset_rounds(args.role, current_branch())
            print("The count of rounds of {0} on this branch is reset.".format(args.role))
            return 0
        pr_text = reply = None
        if args.pr_text:
            with open(args.pr_text, encoding="utf-8") as file:
                pr_text = file.read()
        if args.reply:
            with open(args.reply, encoding="utf-8") as file:
                reply = file.read()
        return 0 if review(args.role, pr_text, reply) else 1
    except (ReviewError, OSError, UnicodeError) as error:
        print("review: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
