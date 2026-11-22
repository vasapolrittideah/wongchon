# ADR-0010: Run each review role in a separate process with approval stamps

Status: `Accepted`

Spec: None

## Context

A review at the gate must not depend on the main agent, because the main agent can write the prompt of a subagent, skip it, and report its verdict. [#3](https://github.com/vasapolrittideah/wongchon/pull/3) first recorded this decision in the roadmap.

## Decision

A script runs each review role as a separate, read-only process. The script takes the prompt from the file of the role and the diff from the staged tree, so the main agent cannot change them. If the role approves, the script writes a stamp for the tree, and a hook blocks a commit or a PR that has no stamp. The main agent fixes the findings and sends the change back to the same reviewer, for at most 3 rounds. After the third round, the main agent stops and asks the maintainer.

## Rejected options

| Option | Reason |
| --- | --- |
| A subagent as the reviewer of the gate | The main agent writes its prompt, can skip it, and reports its verdict. |

## Consequences

- Each review role needs a file with its prompt.
- A change that the reviewer does not approve after 3 rounds goes to the maintainer.

## Confirmation

No check exists yet. The `plugin-review-gate` change adds the review script, the stamps, and the hook that blocks a commit or a PR without a stamp.
