<!-- Follow docs/conventions/pull-requests.md. Use a paragraph for 1 connected point and bullets for 2 or more independent points, except in Result and What changed. Delete these comments. -->

## Result

<!-- Write 1 paragraph of 1 to 3 sentences that states the lasting effect of the PR on `main`, for a later reader of `main`. The squash commit has only the PR title, so this paragraph is the lasting record. -->

## What changed

<!-- List each change that a reviewer must know, with bullets and tables only, also for 1 change. Use a table with the columns `Value`, `Before`, and `After` for each existing value that the PR changes. List added or removed values in bullets. For a revert, start with `Reverts <full SHA>.` -->

## Why

<!-- State the problem and the reason for the chosen change. Link artifacts in Related artifacts, not here. -->

## Breaking changes

<!-- If the title has `!` or another change is incompatible, state what breaks and what users must change. -->

n/a

## Verification

<!-- Write 1 bullet for each check that you ran: `- <check>: <result>.` Write a command in backticks, or describe a manual check in words. Write the result as `passed`, `failed`, or `did not run`, and add a count or short summary from the output in parentheses, such as `passed (32/32 tests)`. Give the cause of a failure or the reason a check did not run. Order the bullets: checks from `AGENTS.md`, Issue verification commands, other checks, then unresolved CI failures. -->

## Risks or limitations

<!-- Write revert safety when a revert is not safe, the parts that a failure affects when the PR changes a shared path, security risks, and remaining limits. Write check results in Verification. -->

n/a

## Follow-up tasks

<!-- Write 1 bullet for each piece of later work: `- #<Issue number>: <remaining work>.` for work with an open Issue, or `- <remaining work>.` for work without one. -->

n/a

## Related artifacts

<!-- Write 1 bullet for each intent, specification, plan, or other lifecycle artifact that the PR implements, changes, or depends on, with its path in backticks as the link text. Order the bullets by stage. -->

n/a

## Related issues

<!-- Write 1 line for each Issue: `Closes #<Issue number>.` if this PR completes it, or `Refs #<Issue number>.` if it stays open. -->

n/a
