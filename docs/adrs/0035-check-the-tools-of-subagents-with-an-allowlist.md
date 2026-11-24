# ADR-0035: Check the tools of subagents with an allowlist

Status: `Accepted`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Context

[ADR-0029](0029-self-review-with-a-self-reviewer-subagent.md) gives the subagents in `agents/` only tools that read, and waits for a check. A subagent without a `tools` field gets each tool of Claude Code. A unit test runs the code of the PR, so a PR can change it, and the `Check changes` job runs from `main`.

## Decision

The `Check changes` job reads each file of `agents/` at the head of the PR. It fails when the `tools` field is missing or names a tool outside `Read`, `Grep`, `Glob`, `WebFetch`, and `WebSearch`. It also warns about each changed file of `agents/`.

## Rejected options

| Option | Reason |
| --- | --- |
| A unit test in `scripts/` | It runs from the branch of the PR, so a PR can change it. |
| A list of the tools that write | A new tool of Claude Code that writes then passes the check. |

## Consequences

- A subagent that needs a new read-only tool needs a change of the allowlist on `main` first.
- The change `plugin-skeleton-and-setup` moves `agents/` into the plugin, and the check must follow the new path.

## Confirmation

The unit tests of `scripts/check_changes.py` check the allowlist, and the `Check changes` CI job runs the script.
