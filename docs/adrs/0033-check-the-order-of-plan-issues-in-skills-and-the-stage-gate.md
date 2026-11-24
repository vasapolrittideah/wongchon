# ADR-0033: Check the order of the Issues of a plan in the skills and the stage gate

Status: `Accepted`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Context

Tasks that share files must run one after another, as the playbook states. In the plan of `plugin-review-gate`, 2 tasks changed 1 file with no `Blocked by` link, and the agent added the link by hand during the build. flowspace-api states this rule only in prose. A check in a skill depends on the report of the agent, and Issues change outside a PR.

## Decision

`scripts/check_plan_issues.py <milestone>` reads each Issue of the milestone and its `Blocked by` links. It fails when 2 Issues share a path of their Files sections and no chain of `Blocked by` links orders them. The `plan` skill runs it before a plan becomes `Approved`, the `build` skill runs it before each Issue, and the `Stage gate` CI job runs it for each changed plan that is `Approved`. The job gets the permission `issues: read`.

## Rejected options

| Option | Reason |
| --- | --- |
| The check in the skills only | The result then depends on the report of the agent. |
| The rule in prose only, as flowspace-api has it | Nothing enforces it, as the plan of `plugin-review-gate` shows. |
| A dependency graph in the plan | It repeats the `Blocked by` links of the Issues, and the 2 drift apart. |

## Consequences

- The `Stage gate` job reads Issues with the token of the workflow.
- An edit of an Issue after its plan merged does not run the job again, so the `build` skill runs the check before each Issue.

## Confirmation

The unit tests of `scripts/check_plan_issues.py` check each failure with fake Issue data, and the `Stage gate` CI job runs the script.
