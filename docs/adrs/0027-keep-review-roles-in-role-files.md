# ADR-0027: Keep each review role in a role file in reviewers

Status: `Accepted`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Context

The review script reads the prompt of each role from a file, as [ADR-0010](0010-run-review-roles-in-a-review-script.md) states. Claude Code loads each file in an `agents/` folder as a subagent that the main agent can start. The quality of a review depends on the model, and the subscription login has a limit of use.

## Decision

Each review role is 1 Markdown file in `reviewers/`, with `name`, `description`, `model`, `effort`, and `paths` in its front matter. The code reviewer and the artifact reviewer use `opus` with `medium` effort, and the writing reviewer uses `sonnet` with `high` effort.

## Rejected options

| Option | Reason |
| --- | --- |
| Role files in `agents/` | Claude Code loads them as subagents, so the main agent could run a role itself instead of the gate. |
| `opus` for each role | It uses the limit of the subscription faster, and the writing reviewer applies explicit rules. |
| No model in the role file | The default model of the CLI changes between versions, so the result of a review changes. |

## Consequences

- The `plugin-skeleton-and-setup` change moves `reviewers/` into the plugin.
- A change of the model of a role is a change of its role file.

## Confirmation

The unit tests of the review script fail when a role file lacks a field of its front matter.
