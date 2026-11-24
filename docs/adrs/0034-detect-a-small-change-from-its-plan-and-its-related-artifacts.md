# ADR-0034: Detect a small change from its plan and its related artifacts

Status: `Accepted`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Context

[ADR-0014](0014-start-small-changes-at-the-build-stage.md) lets a change of 1 PR start at the build stage, if it changes no ADR, `ARCHITECTURE.md`, or `CONSTRAINTS.md`, and it waits for 2 CI checks. A check must know which PR belongs to a change without an intent. A PR without a plan can also change these files.

## Decision

A plan with the Spec line `None` is the plan of a small change, and the change has its plan and its code in 1 PR. The `Stage gate` job fails when such a plan has more than 1 task. It also fails when a PR changes `docs/adrs/**`, `ARCHITECTURE.md`, or `CONSTRAINTS.md` and its Related artifacts section links no spec. The job reads the body of the PR from the event.

## Rejected options

| Option | Reason |
| --- | --- |
| The plan alone | A PR without a plan can then change an ADR. |
| A label for small changes | The agent sets the labels, and a label states nothing about the files. |
| The Spec line of each ADR | `ARCHITECTURE.md` and `CONSTRAINTS.md` have no Spec line. |

## Consequences

- Each PR that changes an ADR, `ARCHITECTURE.md`, or `CONSTRAINTS.md` links a spec, also in the build stage.
- The `Stage gate` script reads the PR body as well as the files.

## Confirmation

The unit tests of `scripts/check_stage_gate.py` check both rules, and the `Stage gate` CI job runs the script.
