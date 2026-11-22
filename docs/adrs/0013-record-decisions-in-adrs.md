# ADR-0013: Record each decision that rejects options in an ADR

Status: `Accepted`

Spec: None

## Context

A decision with rejected options needs 1 home, so that its reasons do not exist in 2 places. The merge of a PR already approves its content. [#14](https://github.com/vasapolrittideah/wongchon/pull/14) first recorded this decision, and the [ADR](../conventions/adrs.md) conventions state its rules.

## Decision

The design stage writes 1 architecture decision record (ADR) in `docs/adrs/<number>-<decision>.md` for each decision that rejects options. The PR of an ADR opens with the status `Accepted`, and the merge accepts it. A new ADR supersedes the whole of an accepted ADR, which changes only its status line. The decisions of the roadmap that have rejected options move into ADRs.

## Rejected options

| Option | Reason |
| --- | --- |
| A `Proposed` status | The merge already approves the ADR. |
| Decisions that stay in the roadmap | Each decision then has 2 homes after the ADRs start. |

## Consequences

- The Decisions section of the roadmap only links the ADRs.
- A change of a decision needs a new ADR and a new change.

## Confirmation

No check exists yet. A follow-up task adds a CI check that an accepted ADR changes only in its status line, and that each new ADR takes the next number. Until then, the maintainer checks the ADRs in the review of each PR.
