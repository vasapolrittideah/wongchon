# Plan: build plans and tasks

Author: Vasapol Rittideah

Status: `Draft`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Tasks

Tasks are tracked in the [wongchon](https://github.com/users/vasapolrittideah/projects/5) GitHub Project under the [build-plans-and-tasks](https://github.com/vasapolrittideah/wongchon/milestone/2) milestone. Each task is 1 PR, in this order, except task 7, which creates Issues and has no PR. Each Issue states its result, requirements, files, proof, owner action, and the Issues that block it.

1. [#56 Show a review role the changes since its last round](https://github.com/vasapolrittideah/wongchon/issues/56)
2. [#57 Accept redirections after `git commit` in the review guard](https://github.com/vasapolrittideah/wongchon/issues/57)
3. [#58 Add the plan and GitHub Issue conventions](https://github.com/vasapolrittideah/wongchon/issues/58)
4. [#59 Add the check of the Issues of a plan](https://github.com/vasapolrittideah/wongchon/issues/59)
5. [#60 Check plans and small changes in the stage gate](https://github.com/vasapolrittideah/wongchon/issues/60)
6. [#61 Make each follow-up task an Issue](https://github.com/vasapolrittideah/wongchon/issues/61)
7. [#62 Turn the follow-up tasks of merged PRs into Issues](https://github.com/vasapolrittideah/wongchon/issues/62)
8. [#63 Check that each subagent has only read-only tools](https://github.com/vasapolrittideah/wongchon/issues/63)
9. [#64 Copy the planning, incremental, and test-driven skills](https://github.com/vasapolrittideah/wongchon/issues/64)
10. [#65 Add the plan and build skills](https://github.com/vasapolrittideah/wongchon/issues/65)
11. [#66 Record the end of `build-plans-and-tasks` in the roadmap](https://github.com/vasapolrittideah/wongchon/issues/66)

## Checkpoints

- After task 2: A later review round gets the diff since the last round, and a commit with `2>&1` passes the review guard.
- After task 6: A PR with a follow-up task without an Issue fails the `PR metadata` job.
- After task 10: Each requirement of the spec has its proof, with 2 exceptions. The change `plugin-skeleton-and-setup` proves requirement 15, and the maintainer checks requirement 16 in task 11.

## Risks

| Risk | Mitigation |
| --- | --- |
| The review script reads the role files from the default branch, so the rule of later rounds starts only after task 1 merges. | Task 1 merges first. |
| The token of a `pull_request_target` job may not read the `Blocked by` links of Issues. | Task 5 proves it on the next plan PR, and the job fails when it cannot read the Issues. |
| No local copy of agent-skills 0.6.17 exists. | Task 9 reads the skills from GitHub at the commit that `skills/THIRD_PARTY.md` states. |
| Task 7 creates many Issues at once. | The maintainer approves 1 table first, and each closed row records its reason. |

## Open questions

Requirement 15 is proved only in the change `plugin-skeleton-and-setup`. The maintainer checks it at the end of that change.
