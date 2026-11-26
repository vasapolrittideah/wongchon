#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys

FOLDERS = ("docs/intents/", "docs/specs/", "docs/plans/")
SPEC_FOLDER = "docs/specs/"
PLAN_FOLDER = "docs/plans/"
DESIGN_PATHS = ("docs/adrs/",)
DESIGN_FILES = ("ARCHITECTURE.md", "CONSTRAINTS.md")
STATUS = re.compile(r"^Status: `([^`]+)`$")
SPEC_LINE = re.compile(r"^Spec: (.+)$")
TASK = re.compile(r"^\d+\. ")
MILESTONE_LINK = re.compile(r"/milestone/\d+")
SPEC_LINK = re.compile(r"^- \[`docs/specs/[^`\s]+\.md`\]\(\S+\)$")
APPROVED = "Approved"
MAX_SPEC_LINES = 200
CHECK_PLAN_ISSUES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_plan_issues.py")
CONVENTIONS = "docs/conventions/intents.md, docs/conventions/specs.md, and docs/conventions/plans.md"


def changed_files(base, head="HEAD", deleted=False):
    command = ["git", "diff", "-z", "--name-only", "--no-renames", base + "..." + head]
    if not deleted:
        command.insert(4, "--diff-filter=d")
    output = subprocess.run(command, check=True, stdout=subprocess.PIPE, universal_newlines=True).stdout
    return [path for path in output.split("\0") if path]


def changed_artifacts(paths):
    return [path for path in paths if path.startswith(FOLDERS) and path.endswith(".md")]


def section(lines, heading):
    rows, inside = [], False
    for line in lines:
        if line.startswith("## "):
            inside = line.strip() == heading
        elif inside:
            rows.append(line)
    return rows


def check_plan(path, lines, run_check):
    specs = [match.group(1) for match in map(SPEC_LINE.match, lines) if match]
    if not specs:
        return ["has no Spec line"]
    tasks = [line for line in section(lines, "## Tasks") if TASK.match(line)]
    if specs[0] == "None":
        findings = []
        if len(tasks) != 1:
            findings.append("is the plan of a small change with {0} tasks. A small change has 1 task".format(
                len(tasks)))
        if any(MILESTONE_LINK.search(line) for line in lines):
            findings.append("is the plan of a small change and links a milestone. A small change has no milestone")
        return findings
    milestone = os.path.splitext(os.path.basename(path))[0]
    return run_check(milestone)


def check_artifact(path, text, run_check=None):
    lines = text.splitlines()
    statuses = [match.group(1) for match in map(STATUS.match, lines) if match]
    findings = []
    if not statuses:
        findings.append("has no Status line in the form Status: `<value>`")
    elif statuses[0] != APPROVED:
        findings.append('has the status "{0}". After the owner approves it, change the status to `{1}`'.format(
            statuses[0], APPROVED))
    if path.startswith(SPEC_FOLDER) and len(lines) > MAX_SPEC_LINES:
        findings.append("has {0} lines, more than {1}".format(len(lines), MAX_SPEC_LINES))
    if path.startswith(PLAN_FOLDER) and not findings:
        findings += check_plan(path, lines, run_check or run_plan_issues)
    return findings


def run_plan_issues(milestone):
    result = subprocess.run([sys.executable, CHECK_PLAN_ISSUES, milestone], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode == 0:
        return []
    return ['fails the check of the Issues of the milestone "{0}": {1}'.format(
        milestone, " ".join(result.stderr.split()))]


def check_design_links(paths, body):
    design = [path for path in paths if path.startswith(DESIGN_PATHS) or path in DESIGN_FILES]
    if not design or any(SPEC_LINK.match(line.strip()) for line in section(body.splitlines(), "## Related artifacts")):
        return []
    return ["the PR changes {0}, and its Related artifacts section links no spec. Only a change with a spec "
            "changes an ADR, ARCHITECTURE.md, or CONSTRAINTS.md".format(", ".join(design))]


def read_artifact(path, head):
    if head is None:
        with open(path, encoding="utf-8") as file:
            return file.read()
    return subprocess.run(["git", "show", "{0}:{1}".format(head, path)], check=True, stdout=subprocess.PIPE,
                          universal_newlines=True).stdout


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check the stage artifacts and the small changes of a PR.")
    parser.add_argument("base", nargs="?", default="origin/main")
    parser.add_argument("--head", help="read the changed artifacts from this commit instead of the working tree")
    args = parser.parse_args(argv)
    base = args.base
    try:
        paths = changed_files(base, args.head or "HEAD")
        all_paths = changed_files(base, args.head or "HEAD", deleted=True)
    except subprocess.CalledProcessError:
        print("Cannot list the files that changed since {0}. Fetch {0}, or pass another base ref.".format(base),
              file=sys.stderr)
        sys.exit(2)
    artifacts = changed_artifacts(paths)
    findings = []
    for path in artifacts:
        try:
            text = read_artifact(path, args.head)
        except subprocess.CalledProcessError:
            print("Cannot read {0} from {1}.".format(path, args.head), file=sys.stderr)
            sys.exit(2)
        findings += ["{0} {1}".format(path, finding) for finding in check_artifact(path, text)]
    body = os.environ.get("PR_BODY")
    if body is not None:
        findings += check_design_links(all_paths, body)
    if findings:
        print("The stage gate fails. See {0}:".format(CONVENTIONS), file=sys.stderr)
        for finding in findings:
            print("- " + finding, file=sys.stderr)
        sys.exit(1)
    print("The stage gate passes for {0} changed intents, specs, and plans.".format(len(artifacts)))


if __name__ == "__main__":
    main()
