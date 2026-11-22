# ADR-0002: Support only Claude Code in version 1

Status: `Accepted`

Spec: None

## Context

Each agent needs its own review runner and hook. Codex skips the hooks of a project until the user trusts them, so the hooks of the framework do not protect a Codex session at first. [#3](https://github.com/vasapolrittideah/wongchon/pull/3) first recorded this decision in the roadmap.

## Decision

Version 1 supports only Claude Code. `AGENTS.md` stays free of rules that only 1 agent can follow, so that other agents can follow it after version 1.

## Rejected options

| Option | Reason |
| --- | --- |
| Claude Code and Codex from the start | Each agent needs its own review runner and hook, and Codex skips project hooks until the user trusts them. |

## Consequences

- The hooks, skills, and review runner of version 1 use only the features of Claude Code.
- Support for other agents, such as Codex, comes after version 1, as the roadmap states.

## Confirmation

No check exists yet. A follow-up task adds a check that `AGENTS.md` names no agent-specific tool or path. Until then, the maintainer checks it in the review of each PR that changes `AGENTS.md`.
