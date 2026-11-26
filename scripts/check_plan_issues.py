#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys

MAX_TITLE = 72
MAX_ISSUES = 1000
FILE = re.compile(r"^- `([^`]+)`(?: \(new\))?$")


class IssueError(Exception):
    pass


def gh(*args):
    try:
        result = subprocess.run(["gh"] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True)
    except OSError as error:
        raise IssueError("cannot run gh: {0}".format(error))
    if result.returncode != 0:
        raise IssueError("gh {0} failed: {1}".format(" ".join(args), result.stderr.strip()))
    try:
        return json.loads(result.stdout)
    except ValueError:
        raise IssueError("gh {0} did not return JSON".format(" ".join(args)))


def load(milestone):
    issues = gh("issue", "list", "--milestone", milestone, "--state", "all", "--limit", str(MAX_ISSUES),
                "--json", "number,title,body")
    if not issues:
        raise IssueError('the milestone "{0}" has no Issues, or it does not exist'.format(milestone))
    if len(issues) >= MAX_ISSUES:
        raise IssueError('the milestone "{0}" has {1} Issues or more'.format(milestone, MAX_ISSUES))
    for issue in issues:
        path = "repos/{{owner}}/{{repo}}/issues/{0}/dependencies/blocked_by?per_page=100".format(issue["number"])
        blockers = gh("api", path)
        issue["blocked_by"] = [blocker["number"] for blocker in blockers]
    return issues


def files(body):
    paths, in_files = [], False
    for line in (body or "").splitlines():
        if line.startswith("## "):
            in_files = line.strip() == "## Files"
        elif in_files:
            match = FILE.match(line.strip())
            if match:
                paths.append(match.group(1))
    return paths


def overlap(first, second):
    return (first == second or (first.endswith("/") and second.startswith(first))
            or (second.endswith("/") and first.startswith(second)))


def blocked(issues, later, earlier):
    blockers = {issue["number"]: issue["blocked_by"] for issue in issues}
    seen, todo = set(), list(blockers.get(later, []))
    while todo:
        number = todo.pop()
        if number == earlier:
            return True
        if number not in seen:
            seen.add(number)
            todo += blockers.get(number, [])
    return False


def check(issues):
    findings = []
    for issue in issues:
        if len(issue["title"]) > MAX_TITLE:
            findings.append("#{0} has a title of {1} characters, more than {2}".format(
                issue["number"], len(issue["title"]), MAX_TITLE))
    issues = sorted(issues, key=lambda issue: issue["number"])
    for i, first in enumerate(issues):
        for second in issues[i + 1:]:
            shared = sorted({a for a in files(first["body"]) for b in files(second["body"]) if overlap(a, b)})
            if shared and not blocked(issues, first["number"], second["number"]) \
                    and not blocked(issues, second["number"], first["number"]):
                findings.append("#{0} and #{1} both change {2}, and no chain of Blocked by links orders them".format(
                    first["number"], second["number"], ", ".join(shared)))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check the order and the titles of the Issues of a milestone.")
    parser.add_argument("milestone", help="the title of the milestone, which is the name of the change")
    args = parser.parse_args(argv)
    try:
        issues = load(args.milestone)
    except IssueError as error:
        print("Cannot read the Issues of the milestone: {0}.".format(error), file=sys.stderr)
        sys.exit(2)
    findings = check(issues)
    if findings:
        print('The Issues of the milestone "{0}" fail. See docs/conventions/github-issues.md:'.format(args.milestone),
              file=sys.stderr)
        for finding in findings:
            print("- " + finding, file=sys.stderr)
        sys.exit(1)
    print('The {0} Issues of the milestone "{1}" pass.'.format(len(issues), args.milestone))


if __name__ == "__main__":
    main()
