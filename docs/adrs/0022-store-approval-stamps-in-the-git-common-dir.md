# ADR-0022: Store approval stamps in the Git common directory

Status: `Accepted`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Context

A stamp must state that a role approved 1 exact version of a change, before the commit or the PR exists. The change only catches mistakes, as its intent states, so a stamp does not need to resist a deliberate forgery. Several worktrees of 1 repository share 1 Git common directory.

## Decision

The review script writes each stamp as a JSON file in `<git common dir>/wongchon/reviews/<role>/`. The name of the file is the hash of the staged tree, or `text-` and the SHA-256 hash of the PR text. The file holds the role, the model, the effort, the time, and the findings.

## Rejected options

| Option | Reason |
| --- | --- |
| A stamp in a tracked file or a trailer of the commit message | The stamp changes the tree or the message that it approves. |
| Git notes | A note needs a commit, but the review comes before the commit. |

## Consequences

- Stamps are not part of the history, so the PR description states the result and the rounds of each role.
- Each worktree of the repository sees the same stamps.
- The agent can write a stamp by hand, and the gate does not stop this.

## Confirmation

The unit tests of the review script and of `hooks/review_guard.py` check the path, the name, and the content of each stamp.
