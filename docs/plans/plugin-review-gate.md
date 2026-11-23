# Plan: plugin review gate

Author: Vasapol Rittideah

Status: `Draft`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Tasks

Tasks are tracked in the [wongchon](https://github.com/users/vasapolrittideah/projects/5) GitHub Project under the [plugin-review-gate](https://github.com/vasapolrittideah/wongchon/milestone/1) milestone. Each task is 1 PR, in this order, and each Issue states its result, requirements, files, proof, owner action, and the Issues that block it.

1. [#32 Add the code, writing, and artifact review roles](https://github.com/vasapolrittideah/wongchon/issues/32)
2. [#33 Add the review script that runs a role and stamps its approval](https://github.com/vasapolrittideah/wongchon/issues/33)
3. [#34 Block commits and PRs without stamps](https://github.com/vasapolrittideah/wongchon/issues/34)
4. [#35 Run the checks of PR data from main](https://github.com/vasapolrittideah/wongchon/issues/35)
5. [#36 Remove the old jobs of PR data from CI](https://github.com/vasapolrittideah/wongchon/issues/36)
6. [#37 Add the research and self-review subagents](https://github.com/vasapolrittideah/wongchon/issues/37)
7. [#38 Copy context-engineering and name the researcher in the stage skills](https://github.com/vasapolrittideah/wongchon/issues/38)
8. [#39 Mark phase 4 as done](https://github.com/vasapolrittideah/wongchon/issues/39)

## Checkpoints

- After task 3: A commit of the agent without a stamp is blocked, and the PR of task 3 states the result and the rounds of each role in Verification.
- After task 5: A test PR that edits a protected check gets the result of the check of `main`, and `Check changes` is a required check.
- After task 7: Each requirement of the spec has its proof, except requirement 13, which the change `build-plans-and-tasks` proves.

## Risks

| Risk | Mitigation |
| --- | --- |
| The script reads the role files from the default branch, so the gate cannot review before task 1 merges. | Task 1 merges first, and the maintainer reviews tasks 1 and 2 without the gate. |
| Without the Actions event policy, the protected jobs do not run, and their required checks stay pending. | The owner action of task 4 comes before its PR opens. |
| CI has no login of Claude Code, so it cannot run the integration test of requirement 7. | The test skips when the reviewer command is missing, and the PR of task 2 states the local result. |
| Each review uses the limit of the subscription of the maintainer. | The paths of each role keep a review to its own files, and the writing reviewer uses `sonnet`. |

## Open questions

- Requirement 13 is proved only in the change `build-plans-and-tasks`, after task 8 marks phase 4 as done. The maintainer checks it at the end of that change.
