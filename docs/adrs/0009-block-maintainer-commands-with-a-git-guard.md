# ADR-0009: Block the commands of the maintainer with a Git guard hook

Status: `Accepted`

Spec: None

## Context

The agent uses the GitHub token of the maintainer, so GitHub cannot tell the agent from the maintainer. The maintainer is the only person who merges a PR or changes the settings of the repository. [#3](https://github.com/vasapolrittideah/wongchon/pull/3) first recorded this decision in the roadmap.

## Decision

The `hooks/git_guard.py` hook blocks the commands that only the maintainer runs, such as a merge, a push to `main`, a force-push, and `--no-verify`. Deny rules in `.claude/settings.json` also block some of these commands, such as `gh pr merge` and `git push --force`. A separate identity for the agent comes after version 1.

## Rejected options

| Option | Reason |
| --- | --- |
| A separate identity for the agent now | It is too much setup for 1 maintainer. |

## Consequences

- The hook finds mistakes, but it does not stop a deliberate bypass, such as a command in a script file.
- GitHub still cannot tell the actions of the agent from the actions of the maintainer.

## Confirmation

`hooks/test_git_guard.py` tests the hook, and the CI workflow runs the tests on each PR. Claude Code runs the hook before each shell command, as `.claude/settings.json` states.
