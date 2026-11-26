# ADR-0038: Give a milestone only to a change with a spec

Status: `Accepted`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Context

[ADR-0030](0030-track-tasks-as-github-issues-in-a-milestone.md) gives each change 1 milestone. A milestone shows the progress of a change across its tasks. A small change has 1 task, as [ADR-0014](0014-start-small-changes-at-the-build-stage.md) states. Its milestone shows only the state of its 1 Issue, and each small change adds 1 more milestone.

## Decision

A plan links 1 GitHub Issue for each task, in the order of the build, and the Issues hold the details of the tasks. The `Blocked by` links of GitHub hold the order of the tasks.

Each change with a spec has 1 milestone with the name of the change. The Issue of a small change has no milestone.

Each Issue joins the GitHub Project that `github.project` in `.wongchon/config.json` names. Without that key, the skills skip the Project.

The plan has only the statuses `Draft` and `Approved`. Other trackers come after version 1, and only the GitHub Issue convention and the steps of the `plan` and `build` skills name GitHub.

## Rejected options

| Option | Reason |
| --- | --- |
| A milestone for each small change | It shows only the state of 1 Issue, and the milestones grow with each small change. |
| A small change without an Issue | The plan then links no task, and GitHub does not close a task when its PR merges. |
| A plan that holds each task in full, with a dependency graph, as flowspace-api does | The plan and the Issues then hold the same details, and they drift apart during the build. |
| A task list in a JSON file in the repository | GitHub then does not close a task when its PR merges, and the maintainer reads the tasks in 2 places. |
| Support for Jira, Monday.com, ClickUp, or GitLab in version 1 | Version 1 has only the maintainer as its user, and the maintainer uses GitHub. |
| A `Complete` status of a plan | The milestone and its closed Issues already show the progress of the change. |

## Consequences

- The check of the order of the Issues has no milestone to read for a small change, and its 1 task cannot share a file with another task.
- The Issue of a small change has no milestone while its PR is open, so the triage of follow-up tasks can list it. The owner can decide to wait on that Issue.
- The `plan` and `build` skills need the `gh` command and a login to GitHub.
- A tracker other than GitHub needs a new convention for its tasks, and new steps in the `plan` and `build` skills.

## Confirmation

The `Stage gate` CI job fails on a plan with the Spec line `None` that links a milestone, and the unit tests of `scripts/check_stage_gate.py` check it. The job also runs `scripts/check_plan_issues.py` on the milestone of each other approved plan.
