# ADR-0031: Make each follow-up task an Issue without a milestone

Status: `Accepted`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Context

On November 23, 2026, 25 merged PRs had 54 follow-up tasks, and none had an Issue, so nobody tracked them. The pull request conventions told the agent to ask the maintainer before it created an Issue, and the maintainer chose to remove that question. The `intent` skill must find the open follow-up tasks of the area of a new change.

## Decision

Each follow-up task of a PR is a GitHub Issue, which the agent creates without asking the maintainer first. Each bullet of Follow-up tasks has the form `- #<number>: <remaining work>.`, and a PR without work for later writes `n/a`. A follow-up Issue has a `Source:` line with the link of its PR. It also has the area label of its work and no milestone. A step of the next stage is not a follow-up task. At the start of each change, the owner decides each open Issue without a milestone in the area of the change: join the change, wait, or close it with a reason.

## Rejected options

| Option | Reason |
| --- | --- |
| Follow-up tasks as bullets without an Issue | Nobody tracks them, as the 54 bullets show. |
| A question to the maintainer before each Issue | It costs review time for each follow-up task, and the triage at the start of each change already lets the owner close an Issue. |
| A `follow-up` label | The label conventions derive each label from a type or a scope, and an Issue without a milestone already marks a follow-up task. |
| An Issue for each step of the next stage | The skill of the next stage already does the step, so the Issue adds work that nobody tracks. |

## Consequences

- The agent creates more Issues, and the owner closes the ones that do not matter at the start of a change.
- The `intent` skill gets a step that lists the open follow-up Issues of the area of the change.
- The follow-up tasks of the PRs that merged before this change need a sweep into Issues.

## Confirmation

`scripts/check_pr_metadata.py` fails on a bullet of Follow-up tasks without an Issue number, and the `PR metadata` CI job runs it.
