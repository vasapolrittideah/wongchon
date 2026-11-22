#!/usr/bin/env python3
import re
import subprocess
import sys

FOLDERS = ("docs/intents/", "docs/specs/")
SPEC_FOLDER = "docs/specs/"
STATUS = re.compile(r"^Status: `([^`]+)`$")
APPROVED = "Approved"
MAX_SPEC_LINES = 200


def changed_artifacts(base):
    output = subprocess.run(
        ["git", "diff", "-z", "--name-only", "--diff-filter=d", base + "...HEAD"],
        check=True, stdout=subprocess.PIPE, universal_newlines=True).stdout
    return [path for path in output.split("\0") if path.startswith(FOLDERS) and path.endswith(".md")]


def check_artifact(path, text):
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
    return findings


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    try:
        paths = changed_artifacts(base)
    except subprocess.CalledProcessError:
        print("Cannot list the files that changed since {0}. Fetch {0}, or pass another base ref.".format(base),
              file=sys.stderr)
        sys.exit(2)
    findings = []
    for path in paths:
        with open(path, encoding="utf-8") as file:
            findings += ["{0} {1}".format(path, finding) for finding in check_artifact(path, file.read())]
    if findings:
        print("The stage gate fails. See docs/conventions/intents.md and docs/conventions/specs.md:",
              file=sys.stderr)
        for finding in findings:
            print("- " + finding, file=sys.stderr)
        sys.exit(1)
    print("The stage gate passes for {0} changed intents and specs.".format(len(paths)))


if __name__ == "__main__":
    main()
