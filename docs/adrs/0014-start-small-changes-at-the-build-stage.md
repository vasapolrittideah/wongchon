# ADR-0014: Start a change of 1 PR at the build stage

Status: `Accepted`

Spec: None

## Context

A change that fits in 1 PR does not need an intent and a spec, but nothing must let a design decision skip the design stage. A limit on the size of a diff depends on the stack. [#14](https://github.com/vasapolrittideah/wongchon/pull/14) first recorded this decision.

## Decision

A change without an intent has a plan with 1 task, which is 1 PR, and that PR does not change `docs/adrs/`, `ARCHITECTURE.md`, or `CONSTRAINTS.md`. CI checks both rules. The owner can take any change through all stages.

## Rejected options

| Option | Reason |
| --- | --- |
| A limit on the size of the diff | No source supports a number, and the number depends on the stack. |
| A limit of 1 PR alone | A change to these files is a design decision. |

## Consequences

- A small change has a plan and evidence, but no intent and no spec.
- A change of an ADR, `ARCHITECTURE.md`, or `CONSTRAINTS.md` always goes through the design stage.

## Confirmation

No check exists yet. The `build-plans-and-tasks` change adds both CI checks, because they read plans.
