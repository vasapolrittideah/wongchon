# ADR-0025: Count review rounds in the review script

Status: `Accepted`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Context

[ADR-0010](0010-run-review-roles-in-a-review-script.md) limits each review to 3 rounds, and then the agent asks the maintainer. flowspace-api states this limit only in prose, and no script counts the rounds.

## Decision

The review script counts the reviews of each role on each branch that end without an approval, in `<git common dir>/wongchon/reviews/<role>/rounds/<branch>`. It refuses a fourth review and tells the agent to ask the maintainer. An approval deletes the count. Only the maintainer resets a count with `--reset-rounds`, and the Git guard blocks this option for the agent. Each round is a new process that gets the findings of the last round and the replies of the agent.

## Rejected options

| Option | Reason |
| --- | --- |
| `--resume` of the session of the last round | It needs saved sessions, and the prompt of each later round comes from the agent. |
| The limit in prose only | Nothing enforces it. |

## Consequences

- A reviewer does not remember earlier rounds beyond the findings and replies that the script gives it.
- A count stays until an approval or a reset, also after the branch merges.

## Confirmation

The unit tests of the review script check the count and the refusal, and the tests of `hooks/git_guard.py` check the block of `--reset-rounds`.
