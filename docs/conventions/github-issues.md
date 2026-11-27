# GitHub Issue conventions

This convention defines the title, the body, the milestone, the Project item, and the `Blocked by` links of each GitHub Issue of a project. An Issue is either a task of a plan or a follow-up task of a pull request (PR).

The Plan tasks and Follow-up tasks decisions of the [roadmap](../../ROADMAP.md#decisions) state why tasks and follow-up tasks are Issues, and the [Plan](plans.md) conventions define the plan that links the Issues of a change.

## Template

An Issue has a [Title](#title), a [Source line](#source-line), a [Result](#result), [Requirements](#requirements), [Files](#files), [Proof](#proof), an [Owner action](#owner-action), [Why](#why), and an [Attribution line](#attribution-line).

```markdown
<Issue title>

<line with the link to the plan or the PR>

## Result

<lasting effect of the task on main>

## Requirements

<requirements of the spec that the task proves, if any>

## Files

- `<path of a file that the task changes or creates>`

## Proof

- [ ] <check that proves the result>

## Owner action

<step that only the owner can take, if any>

## Why

<reason for the follow-up task, if any>

<attribution line, if any>
```

### Title

- Write at most 72 characters.
- Name the change that the task makes and the thing that it changes, such as `Add the check of plan Issues`, so that a reader understands the Issue without its body.
- Start with a verb in the imperative mood, and do not end with a period.
- Put code, file names, and change names in backticks, as the Markdown conventions state.

### Source line

- In a task Issue, write `Plan:` and a link to the plan on `main`, with the path of the plan in backticks as the link text.
- In a follow-up Issue, write `Source:` and the link of the PR that left the work.

### Result

- Write 1 to 3 sentences that state the lasting effect of the task on `main`, as the [Result](pull-requests.md#result) rules of the pull request conventions state for a PR.

### Requirements

- Write 1 sentence that names the IDs of the requirements of the spec and links the spec, such as "R3 and R4 of the spec." For a spec whose requirements have no IDs, name their numbers, such as "Requirements 3 and 4 of the spec."
- If the task builds a part of the Design with no requirement of its own, name the part.
- For a small change, write `None`.

### Files

- Write 1 bullet for each file that the task changes or creates, with its path in backticks.
- Write ` (new)` after the path of a file that the task creates. For a folder of new files, write the path of the folder with `/`, such as `` `skills/plan/` (new) ``.
- If the task changes no file, such as a task that only creates Issues, write `None`.

### Proof

- Write 1 checkbox for each check that proves the result, such as a test command or a manual check.
- If the task has a PR, end with `- [ ] Review the CI results on the PR.`.

### Owner action

- If the task needs a step that only the owner can take, such as a setting of the repository or an approval in the chat, state the step and when to take it.
- Omit the section if the task needs no step of the owner.

### Why

- In a follow-up Issue, state the problem and why it waits for later, in 1 or 2 sentences.

### Attribution line

- If the agent harness gives an attribution line for PR descriptions, put it at the end of the body.

## Rules

### Format and content

- Follow the [English prose](english-prose.md) and [Markdown](markdown.md) conventions.
- Use the sections from Result to Owner action in a task Issue, and only the sections Result and Why in a follow-up Issue.
- Write each Issue so that an agent with no memory of the session can do the task from the Issue, the spec, and the plan.

### Workflow

- Create the task Issues of a plan after the owner agrees with the tasks, and before the plan becomes `Approved`, as the plan conventions state.
- Create a follow-up Issue for each piece of work that a PR leaves for later and that no plan holds, without a question to the owner first. Do not create an Issue for a step of the next stage, such as the spec after an intent.
- At the start of each change, list the open Issues without a milestone that have the area label of the scope of the change. The owner decides each one: join the change, wait, or close it. The open Issue of a small change can be in the list while its PR is open, and the owner can decide to wait on it.
- When a follow-up Issue joins a change, give it the milestone of the change, and add the sections of a task Issue to its body.

### Links and tracking

- Apply the labels that the PR of the task will have, as the [GitHub label](github-labels.md) conventions state.
- Give each task Issue of a change with a spec the milestone of its change. Name the milestone after the change, and write `Plan: <link to the plan on main>` as its description.
- Give the task Issue of a small change no milestone, because a milestone of 1 Issue shows only the state of that Issue.
- Give a follow-up Issue no milestone.
- If 2 Issues of a milestone change or create the same file, add a `Blocked by` link from the later Issue to the earlier one, with `gh issue edit <number> --add-blocked-by <number>`. Do not write the order of Issues in their bodies.
- If `github.project` in `.wongchon/config.json` names a Project, add each Issue to it with the status `Todo`. Set the status `In Progress` when the build of the Issue starts. If the Project does not move the Issue to `Done` when it closes, set the status `Done`.

### Status and approval

- Close a task Issue with `Closes #<number>` in its PR. Close a task Issue without a PR with `gh issue close <number>` after each checkbox of Proof holds.
- Close a follow-up Issue that the owner chose to close with `gh issue close <number> --reason "not planned" --comment "<reason>"`.
- Close the milestone of a change after its last Issue closes.

### Changes

- When a task changes during the build, edit its Issue, as the [Changes](plans.md#changes) rules of the plan conventions state.
- Apply a change of this convention only to new Issues and to Issues that a later PR or task changes. Do not edit closed Issues to follow it.

## Examples

The task Issue [#59](https://github.com/vasapolrittideah/wongchon/issues/59) follows the convention, with a `Plan:` line, Files, Proof, and a `Blocked by` link.

The follow-up Issue [#68](https://github.com/vasapolrittideah/wongchon/issues/68) follows the convention, with a `Source:` line, Result, and Why.

This title does not follow the convention. It has 80 characters and names neither the change nor the thing that it changes, which the [Title](#title) rules forbid.

```text
Follow-up work from the review of the previous PR about the parser and its tests
```
