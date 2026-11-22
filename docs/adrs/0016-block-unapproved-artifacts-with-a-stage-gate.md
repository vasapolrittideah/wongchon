# ADR-0016: Block unapproved stage artifacts with a Stage gate CI job

Status: `Accepted`

Spec: [`docs/specs/design-specs-and-adrs.md`](../specs/design-specs-and-adrs.md)

## Context

An intent, a spec, or a plan must not merge before its owner approves it. The agent uses the GitHub token of the maintainer, so a commit does not show who approved. The ready rule of the pull request conventions requires passing CI. [#14](https://github.com/vasapolrittideah/wongchon/pull/14) first recorded this decision, and the Stage gate part of [`docs/specs/design-specs-and-adrs.md`](../specs/design-specs-and-adrs.md) states how the job works.

## Decision

A CI job named `Stage gate` fails while an intent, a spec, or a plan that the PR changes has a status other than `Approved`. The agent changes the status after the owner approves the artifact. The ready rule of the pull request conventions excludes only this job.

## Rejected options

| Option | Reason |
| --- | --- |
| A pending commit status | It needs the `statuses: write` permission and calls to the GitHub API. |
| No status line | The intent of version 1 chose a status. |

## Consequences

- The PR of a stage artifact shows a failed check until the owner approves it.
- The status of an artifact states only its approval, not the progress of the change.

## Confirmation

The `Stage gate` CI job is the check. The `design-specs-and-adrs` change adds it.
