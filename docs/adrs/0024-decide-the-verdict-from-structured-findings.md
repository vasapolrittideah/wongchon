# ADR-0024: Decide the verdict in the review script from structured findings

Status: `Accepted`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Context

A verdict in free text needs a parser that a reviewer can break with other words or a second verdict line. The code review article of the Claude Code team tags each finding as Important, Nit, or Pre-existing, and confirms each finding in a second pass before a person sees it. A second pass costs about as much as the first review.

## Decision

Each role returns structured output that a JSON schema defines. Each finding has a severity of `Important`, `Nit`, or `Pre-existing`, a file, a line, a rule, a problem, and a fix. The script approves a change only when no finding is `Important`. A finding without a rule does not block. Missing or invalid output is not an approval. The change has no second pass.

## Rejected options

| Option | Reason |
| --- | --- |
| A second pass that confirms each finding | It about doubles the cost and the time of each review. The verify phase measures the noise with evals first. |
| A `Verdict:` line in free text | The parse is not deterministic. |
| The verdict of the reviewer | A reviewer can approve a change and still list a blocking finding. |

## Consequences

- `Pre-existing` findings do not block the author of the change.
- A role must cite a rule for each finding that blocks.

## Confirmation

The unit tests of the review script check the verdict for each severity and for missing or invalid output.
