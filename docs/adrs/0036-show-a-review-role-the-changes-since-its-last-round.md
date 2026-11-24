# ADR-0036: Show a review role the changes since its last round

Status: `Accepted`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Context

[ADR-0025](0025-count-review-rounds-in-the-review-script.md) gives each later round the findings and replies of the last round. In the intent stage of this change, roles found new problems in text that did not change since their last round, so they used their 3 rounds, and the maintainer reset the count. The Claude Code team reviews only the changed lines after the first round, as its article on code review states. A script cannot map a finding of unchanged text to a line reliably, because the fixes move the lines.

## Decision

When a review ends without an approval, the review script saves its tree or its PR text. The next round gets the diff from that tree or text to the current one, and the findings and replies of the last round. From the second round, a role reports a new problem in text outside that diff as `Nit`, except a bug in code that loses data, opens a security hole, or crashes the program. The agent fixes each `Nit` of a later round or creates a follow-up Issue for it. The limit stays at 3 rounds, and the rest of ADR-0025 stays true.

## Rejected options

| Option | Reason |
| --- | --- |
| A limit of 5 rounds | It hides the cause of the failed rounds and uses more of the subscription. |
| A verdict in the script that drops `Important` findings outside the diff | The lines of an unfixed finding move after a fix, so the script can drop a finding that must block. |

## Consequences

- A later round can miss a problem in prose or format that the first round did not report.
- The script stores 1 more file for each role and branch, and deletes it with the count.

## Confirmation

The unit tests of the review script check that a later round gets the diff since the last round. No tool can check the severity that a role gives, so the maintainer checks the rounds of this change until the verify phase adds evals of the reviewers.
