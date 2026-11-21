#!/usr/bin/env python3
import json
import os
import re
import sys

CONVENTIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "docs", "conventions")
COMMIT_CONVENTION = os.path.join(CONVENTIONS, "commit-messages.md")
PR_CONVENTION = os.path.join(CONVENTIONS, "pull-requests.md")
CONFIG = os.path.join(".wongchon", "config.json")
MAX_LENGTH = 72
SUBJECT = re.compile(r"^(?P<type>[^\s():!]+)(?:\((?P<scope>[^()]*)\))?(?P<breaking>!)?: (?P<description>\S.*)$")
TYPE_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|")
MARKUP = re.compile(r"`|\]\(|://")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")


def load_types(path=COMMIT_CONVENTION):
    types = set()
    in_table = False
    with open(path, encoding="utf-8") as file:
        for line in file:
            if line.startswith("#"):
                in_table = line.strip() == "### Types"
            elif in_table:
                match = TYPE_ROW.match(line)
                if match:
                    types.add(match.group(1))
    if not types:
        raise ValueError("cannot read the Types table of {0}".format(path))
    return types


def load_scopes(path=CONFIG):
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as file:
        config = json.load(file)
    return {scope["name"] for scope in config.get("commit", {}).get("scopes", [])}


def load_headings(path=PR_CONVENTION):
    headings = []
    with open(path, encoding="utf-8") as file:
        lines = file.read().splitlines()
    start = lines.index("## Template")
    in_block = False
    for line in lines[start + 1:]:
        if FENCE.match(line):
            if in_block:
                break
            in_block = True
        elif in_block and line.startswith("## "):
            headings.append(line[3:].strip())
    if not headings:
        raise ValueError("cannot read the headings of the Template section of {0}".format(path))
    return headings


def prose_lines(body):
    lines = []
    in_block = False
    for line in body.splitlines():
        if FENCE.match(line):
            in_block = not in_block
        elif not in_block:
            lines.append(INLINE_CODE.sub("", line))
    return lines


def check_title(title, types, scopes):
    match = SUBJECT.match(title)
    if not match:
        return ['"{0}" does not have the form <type>(<scope>)!: <description>, '
                "with an optional scope and !".format(title)]
    findings = []
    if match.group("type") not in types:
        findings.append('the type "{0}" is not in the Types table. Use one of: {1}'.format(
            match.group("type"), ", ".join(sorted(types))))
    scope = match.group("scope")
    if scope is not None and scope not in scopes:
        findings.append('the scope "{0}" is not in commit.scopes of {1}. Use one scope name of: {2}, '
                        "or omit the scope".format(scope, CONFIG, ", ".join(sorted(scopes)) or "none"))
    description = match.group("description")
    if not description[0].islower():
        findings.append("the description does not start with a lowercase letter")
    if description.endswith("."):
        findings.append("the description ends with a period")
    if MARKUP.search(description):
        findings.append("the description has a backtick, a Markdown link, or a URL. Write plain text")
    if len(title) > MAX_LENGTH:
        findings.append("the title has {0} characters, more than {1}".format(len(title), MAX_LENGTH))
    return findings


def check_body(body, expected):
    lines = prose_lines(body)
    actual = [line[3:].strip() for line in lines if line.startswith("## ")]
    findings = []
    if actual != expected:
        findings = ['the heading "{0}" is missing'.format(heading) for heading in expected if heading not in actual]
        findings += ['the heading "{0}" is not in the template'.format(heading)
                     for heading in actual if heading not in expected]
        if not findings:
            findings.append("the headings are not once each in the order of the template: " + ", ".join(expected))
    if any("<!--" in line for line in lines):
        findings.append("the description has an HTML comment. Delete the comments of the template")
    return findings


def main():
    title = os.environ.get("PR_TITLE")
    body = os.environ.get("PR_BODY")
    if not title or body is None:
        print("Set PR_TITLE to the pull request title and PR_BODY to its description.", file=sys.stderr)
        sys.exit(2)
    findings = ["PR title: " + finding for finding in check_title(title, load_types(), load_scopes())]
    findings += ["PR description: " + finding for finding in check_body(body, load_headings())]
    if findings:
        print("The pull request does not follow docs/conventions/commit-messages.md and "
              "docs/conventions/pull-requests.md:", file=sys.stderr)
        for finding in findings:
            print("- " + finding, file=sys.stderr)
        sys.exit(1)
    print("The PR title and the description follow the conventions.")


if __name__ == "__main__":
    main()
