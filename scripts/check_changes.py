#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys

CHECK_PATHS = (".github/workflows/", "scripts/", "hooks/", "reviewers/")
CHECK_FILES = (".claude/settings.json",)
WORKFLOWS = ".github/workflows/"
PROTECTED_WORKFLOW = ".github/workflows/protected-checks.yml"
PROTECTED_JOBS = ("PR metadata", "Stage gate", "Check changes")
PROTECTED_EVENT = "pull_request_target"


def git(*args):
    return subprocess.run(["git"] + list(args), check=True, stdout=subprocess.PIPE,
                          universal_newlines=True).stdout


def escape_data(value):
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def escape_property(value):
    return escape_data(value).replace(":", "%3A").replace(",", "%2C")


def changed_files(base, head):
    output = git("diff", "-z", "--name-only", "--no-renames", base + "..." + head)
    return [path for path in output.split("\0") if path]


def check_files(paths):
    return [path for path in paths if path.startswith(CHECK_PATHS) or path in CHECK_FILES]


def workflow_files(head):
    output = git("ls-tree", "-r", "-z", "--name-only", head, "--", WORKFLOWS)
    return [path for path in output.split("\0") if path.endswith((".yml", ".yaml"))]


def protected_names(text):
    names = []
    for line in text.splitlines():
        match = re.match(r"^\s+(?:- )?name:\s*(.*?)\s*$", line)
        if match:
            raw = match.group(1)
            if not raw.startswith(("'", '"')):
                raw = re.sub(r"\s+#.*$", "", raw)
            value = " ".join(raw.strip("\"'").split())
            if value in PROTECTED_JOBS and value not in names:
                names.append(value)
    return names


def protected_events(text):
    lines = text.splitlines()
    starts = [index for index, line in enumerate(lines) if re.match(r"^[\"']?on[\"']?\s*:", line)]
    if len(starts) != 1 or lines[starts[0]].split(":", 1)[1].strip():
        return None
    events = []
    for line in lines[starts[0] + 1:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            break
        if line.startswith("   "):
            continue
        match = re.match(r"^  [\"']?([A-Za-z_]+)[\"']?\s*:", line)
        if not match:
            return None
        events.append(match.group(1))
    return events


def findings(head):
    problems = []
    for path in workflow_files(head):
        text = git("show", "{0}:{1}".format(head, path))
        if path == PROTECTED_WORKFLOW:
            if protected_events(text) != [PROTECTED_EVENT]:
                problems.append("{0} must run only on {1}, in the block form `on:` and `  {1}:`".format(
                    path, PROTECTED_EVENT))
            continue
        for name in protected_names(text):
            problems.append("{0} uses the protected job name {1!r}".format(path, name))
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="Show changed check files, and fail on protected job names.")
    parser.add_argument("base", nargs="?", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args(argv)
    try:
        changed = check_files(changed_files(args.base, args.head))
        problems = findings(args.head)
    except subprocess.CalledProcessError:
        print("Cannot read the changes from {0} to {1}. Fetch both refs.".format(args.base, args.head),
              file=sys.stderr)
        return 2
    for path in changed:
        print("::warning file={0},title=Check file changed::This PR changes {1}, which a check or a hook runs. "
              "The protected checks run the version of main until this PR merges.".format(escape_property(path),
                                                                                   escape_data(path)))
    for problem in problems:
        print("::error title=Protected check::" + escape_data(problem))
    if problems:
        print("Check changes fails: a workflow of this PR can report the result of a protected check.",
              file=sys.stderr)
        return 1
    print("Check changes passes: {0} changed check files, and no workflow uses a protected job name.".format(
        len(changed)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
