# ADR-0028: Block a commit or a PR without its stamps in a separate hook

Status: `Accepted`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Context

`hooks/git_guard.py` blocks the commands that only the maintainer runs, as [ADR-0009](0009-block-maintainer-commands-with-a-git-guard.md) states. The review gate blocks a command for another reason: a missing stamp. Both hooks need the same parser of shell commands.

## Decision

`hooks/review_guard.py` is a separate `PreToolUse` hook for `Bash`. It uses the parser of `hooks/git_guard.py` and the path rules and stamp names of `scripts/review.py`. It checks `git commit`, `gh pr create`, and `gh pr edit`, and it blocks when it cannot decide.

## Rejected options

| Option | Reason |
| --- | --- |
| The checks of stamps in `hooks/git_guard.py` | 1 hook then holds 2 kinds of rules, and its tests and its move into the plugin get larger. |

## Consequences

- `.claude/settings.json` registers 2 hooks for `Bash`.
- A change of the parser affects both hooks.

## Confirmation

`hooks/test_review_guard.py` tests the hook, and the CI workflow runs the tests on each PR.
