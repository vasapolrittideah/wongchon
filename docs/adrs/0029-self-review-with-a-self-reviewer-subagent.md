# ADR-0029: Run the self-review with a self-reviewer subagent

Status: `Accepted`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Context

The [Roadmap](../../ROADMAP.md) gives self-review to a read-only subagent, and a self-review before the gate only gives advice. The code review article of the Claude Code team runs a subagent with fresh context on the diff before a PR. The `doubt-driven-development` skill of agent-skills describes such a fresh-context review. The built-in `Explore` subagent of Claude Code is read-only, but it finds code and does not review it.

## Decision

The `doubt-driven-development` skill runs the self-review with a `self-reviewer` subagent in `agents/`. The subagent has only the tools `Read`, `Grep`, and `Glob`, and it uses a role file of `reviewers/` as its checklist. Its result is advice. It writes no stamp and does not replace the gate.

## Rejected options

| Option | Reason |
| --- | --- |
| The built-in `Explore` subagent | It finds code and does not review it. |
| No self-review | The gate then finds each problem, and each round of the gate uses a round of the limit of 3. |

## Consequences

- The main agent writes the prompt of the self-review, so the self-review can miss what the gate finds.
- The `plugin-skeleton-and-setup` change moves `agents/` into the plugin.

## Confirmation

The front matter of `agents/self-reviewer.md` lists its tools. A follow-up task adds a check that each subagent in `agents/` has no tool that writes. Until then, the maintainer checks it in the review of each PR.
