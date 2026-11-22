# ADR-0004: Name the stages intent, design, build, verify, deploy, and maintain

Status: `Accepted`

Spec: None

## Context

The playbook names its stages Plan, Design, Build, Test, Deploy, and Maintain. `plan` is also the name of a skill, and verification covers more than tests. [#3](https://github.com/vasapolrittideah/wongchon/pull/3) first recorded this decision in the roadmap.

## Decision

The 6 stages are `intent`, `design`, `build`, `verify`, `deploy`, and `maintain`. The approval of the plan is the gate of the build stage.

## Rejected options

| Option | Reason |
| --- | --- |
| The names Plan and Test of the playbook | `plan` is also the name of a skill, and verification covers more than tests. |
| A split into 7 stages | A separate plan stage takes the plan gate away from the build stage. |

## Consequences

- The commit scopes, the labels, and the skills of the framework use these stage names.
- The build stage has 2 skills, `plan` and `build`, because the plan and its approval belong to the stage.

## Confirmation

`scripts/check_pr_metadata.py` accepts only the scopes in the `commit.scopes` list of `.wongchon/config.json`, which holds the stage names. No check covers the names in prose yet.
