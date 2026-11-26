# Plan conventions

This convention defines the file, the format, the status, and the changes of 1 plan in `docs/plans/`. A plan is the artifact of the build stage. It splits a change into tasks, and its approval is the gate of the build stage.

The [Plan tasks](../../ROADMAP.md#decisions) decision of the roadmap states why each task is a GitHub Issue, and the [GitHub Issue](github-issues.md) conventions define the Issues, the milestone, and the Project of a plan.

## Template

A plan has a [Title](#title), an [Author line](#author-line), a [Status line](#status-line), a [Spec line](#spec-line), [Tasks](#tasks), [Checkpoints](#checkpoints), [Risks](#risks), and [Open questions](#open-questions).

```markdown
# Plan: <name of the change>

Author: <name of the owner of the change>

Status: <status value>

Spec: <link to the spec, or None>

## Tasks

Tasks are tracked in the [<name of the Project>](<link to the Project>) GitHub Project under the [<change name>](<link to the milestone>) milestone. Each task is 1 PR, in this order. Each Issue states its result, requirements, files, proof, owner action, and the Issues that block it.

1. [#<Issue number> <Issue title>](<link to the Issue>)

## Checkpoints

- <task after which the checkpoint comes, and the result to observe, if any>

## Risks

| Risk | Mitigation |
| --- | --- |
| <risk of the build, if any> | <how the plan reduces the risk> |

## Open questions

- <question for a later task or change, if any>
```

### Title

- Write the title as `# Plan: <name of the change>`.
- Use the name of the change from the title of its intent. For a small change, write the name as a short noun phrase.

### Author line

- Write the name of the person who owns the change. Use the name from the Author line of the intent, if the change has one.
- Do not write the name of an agent.

### Status line

- Write 1 value from the [Status values](#status-values) table, in backticks.
- Change the value only as the [Status and approval](#status-and-approval) rules state.

### Spec line

- Link the spec with the relative path `../specs/<change name>.md`, and use the path from the repository root in backticks as the link text, such as `docs/specs/account-email-change.md`.
- For a small change, write `None`, as the [Small changes](#small-changes) section states.

### Tasks

- While the PR of the plan is a draft, write each task in full under a `### Task <number>: <Issue title>` heading. Give it the bullets Result, Requirements, Files, Proof, Owner action, and Depends on, with the content that the GitHub Issue conventions state for each section of the Issue.
- After the owner agrees with the tasks in the chat, create the Issues, and replace the tasks with the numbered links of the Template.
- Write 1 numbered item for each task, in the order of the build. Keep the order the same as the order of the `Blocked by` links of the Issues.
- Write each item as a link to its Issue, with the Issue number and the Issue title as the link text.
- If the Project has no number in `.wongchon/config.json`, write the tracking sentence without the Project.
- For a small change, write the tracking sentence without the milestone, because its Issue has none.
- If a task has no PR, such as a task that only creates Issues, state it in the tracking sentence.

### Checkpoints

- Write 1 bullet for each point of the build where a later task depends on a result that a person or a check must see first.
- Write each bullet as `After task <number>: <result>.`, with a result that a person or a check can observe.
- Omit the section if the plan has no checkpoint.

### Risks

- Write 1 row for each risk that can stop or delay the build, such as a check that needs a permission, a setting of the owner, or a missing source.
- In the Mitigation column, state the task, the order, or the check that reduces the risk.
- Omit the section if the plan has no risk.

### Open questions

- Write 1 bullet for each question that a later task or change decides, and name that task or change.
- Omit the section if the plan has no open question.
- Do not leave a question that changes a task of this plan. Answer it before the status changes to `Approved`.

## Rules

### Naming and location

- Save each plan as `docs/plans/<change name>.md`, with the change name of its intent, as the [Naming and location](intents.md#naming-and-location) rules of the intent conventions state.
- For a small change, choose the change name with the same rules.

### Format and content

- Follow the [English prose](english-prose.md) and [Markdown](markdown.md) conventions.
- Write in the plan only the order of the tasks, the checkpoints, the build risks, and the open questions. Each Issue holds the result, the requirements, the files, the proof, and the owner action of its task.
- Do not repeat the requirements or the design of the spec. Link the spec instead.

### Workflow

- Write 1 plan for each change. Start it after the spec of the change merges with the status `Approved`, or at the request of the owner for a small change.
- Make each task 1 PR. If 2 tasks change or create the same file, the later task depends on the earlier task.

### Links and tracking

- Give each task 1 Issue, as the GitHub Issue conventions state. Put the Issues of a change with a spec in the milestone of the change.

### Status and approval

- Write the status `Draft` when you create the plan.
- Change the status to `Approved` only after each Issue exists and the owner approves the plan in the chat or in a review of the PR. Commit the change on the branch of the PR.
- Do not merge a plan whose status is not `Approved`. The owner approves the gate of the build stage when they merge the PR.

### Changes

- If a task changes during the build, edit its Issue. Keep the plan unchanged when only the content of a task changes.
- To add, remove, or reorder a task during the build, ask the owner in the chat first. Then edit the plan, the Issues, and their `Blocked by` links in the PR of the task that found the change. The status stays `Approved`.
- Apply a change of this convention only to new plans and to plans that a later PR changes.
- Do not change a plan after the last task of its change is done. Start a new change instead.

## Small changes

A small change is a change of 1 PR without an intent and a spec, as the [Small change checks](../../ROADMAP.md#decisions) decision of the roadmap states. Its plan and its code are in the same PR.

- Write `None` in the Spec line.
- Write exactly 1 task, with 1 Issue and no milestone.
- Do not change `docs/adrs/`, `ARCHITECTURE.md`, or `CONSTRAINTS.md` in the PR. A change of these files needs an intent and a spec.

## Reference

### Status values

| Status | Meaning |
| --- | --- |
| `Draft` | The owner did not approve the plan yet. |
| `Approved` | The owner approved the plan, and the build of its tasks can start. |

## Examples

The plan of `build-plans-and-tasks` follows the convention: [`docs/plans/build-plans-and-tasks.md`](../plans/build-plans-and-tasks.md).

This Tasks list does not follow the convention. It writes the result of each task in the plan instead of a link to its Issue, which the [Format and content](#format-and-content) rules forbid after the Issues exist.

```markdown
## Tasks

1. Add the check of plan Issues: `scripts/check_plan_issues.py` fails on 2 Issues that share a file.
2. Check plans in the stage gate: the `Stage gate` job reads plans.
```
