# ADR-0030: Track the tasks of a plan as GitHub Issues in a milestone

Status: `Accepted`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Context

The build stage needs a plan that the owner approves and a place that tracks each task until it merges. The playbook names 1 system as the source of truth for tasks. The plan of `plugin-review-gate` linked 8 Issues in 1 milestone and in a GitHub Project, and the maintainer chose to keep that format. Other users can use other trackers, such as Jira, Monday.com, ClickUp, or GitLab, but version 1 has only the maintainer as its user.

## Decision

A plan links 1 GitHub Issue for each task, in the order of the build, and the Issues hold the details of the tasks. Each change has 1 milestone with the name of the change. The `Blocked by` links of GitHub hold the order of the tasks. Each Issue joins the GitHub Project that `github.project` in `.wongchon/config.json` names. Without that key, the skills skip the Project. The plan has only the statuses `Draft` and `Approved`. Other trackers come after version 1, and only the GitHub Issue convention and the steps of the `plan` and `build` skills name GitHub.

## Rejected options

| Option | Reason |
| --- | --- |
| A plan that holds each task in full, with a dependency graph, as flowspace-api does | The plan and the Issues then hold the same details, and they drift apart during the build. |
| A task list in a JSON file in the repository | GitHub then does not close a task when its PR merges, and the maintainer reads the tasks in 2 places. |
| Support for Jira, Monday.com, ClickUp, or GitLab in version 1 | Version 1 has only the maintainer as its user, and the maintainer uses GitHub. |
| A `Complete` status of a plan | The milestone and its closed Issues already show the progress of the change. |

## Consequences

- The `plan` and `build` skills need the `gh` command and a login to GitHub.
- A tracker other than GitHub needs a new convention for its tasks, and new steps in the `plan` and `build` skills.
- The checks of the build stage read Issues, so they need the permission to read Issues.

## Confirmation

`scripts/check_plan_issues.py` reads the Issues of the milestone of each approved plan, and the `Stage gate` CI job runs it.
