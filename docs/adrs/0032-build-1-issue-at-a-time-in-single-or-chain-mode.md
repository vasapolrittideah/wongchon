# ADR-0032: Build 1 Issue at a time in single or chain mode

Status: `Accepted`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Context

flowspace-api has 4 build modes: single, chain, fanout, and swarm. Fanout and swarm build several Issues at the same time in separate worktrees. The review time of the maintainer is the main limit of version 1, and each PR that is open at the same time needs its own review.

## Decision

The `build` skill has 2 modes. Single mode builds the first Issue in the order of the plan that is open and whose blockers are closed, up to a ready PR, and stops. Chain mode repeats single mode after the owner merges each PR, until the milestone has no open Issue. Neither mode opens a PR on top of a PR that did not merge.

## Rejected options

| Option | Reason |
| --- | --- |
| Fanout and swarm modes in version 1 | Several open PRs at the same time add review time, which is the main limit of version 1. |
| A chain of stacked PRs | A fix in an early PR then changes each later PR, and the maintainer reviews the same code again. |

## Consequences

- A change of several Issues takes at least 1 merge of the maintainer for each Issue.
- Parallel modes can come after version 1, with the check of the order of the Issues that this change adds.

## Confirmation

No check exists yet. [#53](https://github.com/vasapolrittideah/wongchon/issues/53) adds a check that fails when a PR for an Issue of a milestone opens while another PR of the same milestone is open. Until then, the maintainer checks it in the review of each PR.
