# Spec conventions

This convention defines the file, the format, and the status of 1 spec in `docs/specs/`. A spec is the artifact of the design stage. It states how to build a change after its intent states what the change must achieve and why.

The design stage writes the spec of a change and its architecture decision records (ADRs) together. The [Stage artifacts](../../ROADMAP.md#decisions) decision of the roadmap states the folder of each kind of artifact. A spec describes 1 transition of the project, and `ARCHITECTURE.md` describes the project as it is after each transition.

## Template

A spec has a [Title](#title), an [Author line](#author-line), a [Status line](#status-line), an [Intent line](#intent-line), [Current state](#current-state), [Requirements](#requirements), [Design](#design), [Rules](#rules-section), [Boundaries](#boundaries), [Decisions](#decisions), [Concerns](#concerns), [Assumptions and open questions](#assumptions-and-open-questions), [Answers to the intent](#answers-to-the-intent), [Answers](#answers), and [References](#references).

```markdown
# Spec: <name of the change>

Author: <name of the owner of the change>

Status: <status value>

Intent: <link to the intent>

## Current state

<parts of the project that the change builds on or changes, as they are before the change>

## Requirements

1. Given <state>, when <action>, then <result>. Criterion: <success criterion ID>. Proof: <test level>.

## Design

### <name of a part>

<contract and behavior of the part, and how it fits the current state>

## Rules

| Rule | Check |
| --- | --- |
| <rule that the change adds to the project, if any> | <check that enforces the rule> |

## Boundaries

- Ask first: <change that needs the approval of the owner during the build, if any>
- Never: <part that the build must not change, if any>

## Decisions

| Decision | ADR |
| --- | --- |
| <decision of the change in 1 sentence, if any> | <link to the ADR> |

## Concerns

| Concern | Resolution |
| --- | --- |
| <conflict between rules or risk that the design found, if any> | <decision of the owner> |

## Assumptions and open questions

- <unproven fact or question for a later stage, if any>

## Answers to the intent

| Open question of the intent | Answer |
| --- | --- |
| <open question of the intent, if any> | <answer, or the stage that decides it> |

## Answers

| Question | Reply |
| --- | --- |
| <question to the owner> | <meaning of the reply> |

## References

| Source | What this spec takes from it | Parts read only in a summary |
| --- | --- | --- |
| <link to a source, if any> | <point that the spec uses> | <parts of the source that the writer did not read in full> |
```

### Title

- Write the title as `# Spec: <name of the change>`.
- Use the name of the change from the title of its intent.

### Author line

- Write the name of the person who owns the change. Use the name from the Author line of the intent.
- Do not write the name of an agent.

### Status line

- Write 1 value from the [Status values](#status-values) table, in backticks.
- Change the value only as the [Status and approval](#status-and-approval) rules state.

### Intent line

- Link the intent with the relative path `../intents/<change name>.md`, and use the path from the repository root in backticks as the link text, such as `docs/intents/account-email-change.md`.

### Current state

- Write 1 or 2 paragraphs.
- Link each project document, ADR, and part of `ARCHITECTURE.md` that the change builds on or changes.
- In a project with no code yet, write `None`.
- Do not repeat the problem, the outcome, the success criteria, or the scope of the intent. Link the intent instead.

### Requirements

- Write each requirement as 1 numbered item in the form Given, when, then, so that a test can prove it.
- After the result, name the ID of the success criterion of the intent that the requirement serves, such as `S1`. Give each success criterion at least 1 requirement.
- After the criterion, name the level of the test that proves the requirement, such as unit, integration, end-to-end, or a manual check. The plan of the build stage names each test.
- Write a requirement for each behavior that must not change, such as an existing login that keeps working.
- Do not copy the text of a success criterion. Name its ID.

### Design

- Write 1 `###` subsection for each part of the change, such as a module, an interface, a check, a document, or a skill. Name each subsection with a short noun phrase.
- State the contract of each part: its inputs, outputs, data, and errors, or the format of the file that it adds or changes.
- If the change has a user interface, link its mock in the subsection of that part.
- If a decision of a part rejects options, link its ADR in the subsection. Do not repeat the rejected options.
- Do not list the files to change, the order of the work, or the names of tests. The plan of the build stage states them.

### Rules section

- Write 1 row for each rule that the change adds to the project, such as a rule for the parts of the project or for an artifact. The build stage moves each rule into `ARCHITECTURE.md` after the change.
- In the Check column, name a deterministic check, such as a test, a linter rule, a hook, or a CI job. If no check is possible yet, name the follow-up task that adds it, and state who checks the rule until then.
- If the change adds or changes a rule of `CONSTRAINTS.md`, edit that file in the same PR instead of this table.
- Do not name a review by a person as the only check of a rule that a tool can check.

### Boundaries

- Write only the limits that the design decides for the build of this change.
- Use `Ask first` for a change that the build can make only after the owner approves it, and `Never` for a part that the build must not change.
- Do not repeat a constraint of the intent or a rule of `AGENTS.md` or `CONSTRAINTS.md`. The build already follows them.

### Decisions

- If the change has ADRs, add this section, and write 1 row for each ADR of the change in the order of the ADR numbers.
- Write the decision as 1 sentence that states the chosen option.
- Do not list a decision that has no ADR.

### Concerns

- Write 1 row for each conflict between the rules that the design must follow, and for each risk that the owner must accept, such as a cost or a security risk.
- In the Resolution column, state what the owner decided, and the owner of the rule when another person owns it.
- Resolve each concern before the status changes to `Approved`.

### Assumptions and open questions

- Write 1 bullet for each fact that the design depends on and that nobody proved yet, such as the behavior of a tool, and for each question that a later stage decides.
- Name the stage, the change, or the person that proves or decides each item.
- Do not leave a question that changes a requirement, a part, or a decision. Answer it before the status changes to `Approved`.

### Answers to the intent

- If the intent has an Open questions section, add this section, and write 1 row for each open question of the intent, in the order of the intent.
- Answer each question, or name the later stage that decides it.

### Answers

- Write 1 row for each question that the writer asked the owner during the design stage, in the order of the questions.
- In the Reply column, write in English the meaning of the reply of the owner, as a summary and not a copy of the words. If the owner only confirms a recommendation, write the confirmed recommendation.
- If a later answer changes an earlier answer, update the earlier row to the final answer.

### References

- If the spec uses an outside source, such as an article, a study, or documentation, add this section.
- Write 1 row for each source, and link the source in the Source column.
- In the third column, write the parts of the source that the writer read only in a summary. If the writer read the whole source, write `None`.
- Do not list a source that the spec does not use.

## Rules

### Naming and location

- Save each spec as `docs/specs/<change name>.md`, with the change name of its intent, as the [Naming and location](intents.md#naming-and-location) rules of the intent conventions state.

### Format and content

- Follow the [English prose](english-prose.md) and [Markdown](markdown.md) conventions.
- Keep each spec at most 200 lines, blank lines included, so that the owner can review it in 1 sitting.
- Write how to build the change. The intent states what the change must achieve and why, the ADRs state the reasons for the decisions, and the plan states the files, the tasks, and the tests.

### Workflow

- Write 1 spec for each change that has an intent. A change without an intent has no spec, and it starts at the build stage.
- Start the spec after the intent of the change merges with the status `Approved`.
- Before you write the spec, ask the owner about each undecided choice, 1 topic at a time, with the options and your recommendation.
- If the requirements form groups that can ship and be tested apart, stop and propose to the owner to split the change into 1 change for each group, each with its own intent.
- Open the spec and each ADR of the change in 1 PR. If the change adds or changes a rule of `CONSTRAINTS.md` or a term of `GLOSSARY.md`, update the file in the same PR.

### Status and approval

- Write the status `Draft` when you create the spec.
- Change the status to `Approved` only after the owner approves the spec in the chat or in a review of the PR. Commit the change on the branch of the PR.
- Do not merge a spec whose status is not `Approved`. The owner approves the gate of the design stage when they merge the PR.

### Changes

- To change an approved spec, edit the file in a new PR, and change its status to `Draft` in that PR. Then follow the Status and approval rules again.
- Apply a change of this convention only to new specs and to specs that a later PR changes.
- Do not change a spec in the PR of a plan or of code.
- Do not change a spec after the last PR of its change merges. To change the design later, start a new change, and write a new ADR for each changed decision.

## Reference

### Status values

| Status | Meaning |
| --- | --- |
| `Draft` | The owner did not approve the spec yet. |
| `Approved` | The owner approved the spec, and the build stage of the change can start. |

## Examples

### Requirements

These requirements follow the convention. Each one names a success criterion of the intent and a test level, and the last one keeps an existing behavior:

```markdown
## Requirements

1. Given an account with a confirmed email address, when the user enters a new address, then the service sends a 6-digit code to the new address. Criterion: S1. Proof: integration test.
2. Given a code that the service sent, when the user enters it within 15 minutes, then the new address replaces the old address. Criterion: S1. Proof: integration test.
3. Given a pending change of address, when the user signs in with the old address, then the sign-in succeeds. Criterion: S2. Proof: end-to-end test.
```

This requirement does not follow the convention. It copies the text of a success criterion and names no test level, which the [Requirements](#requirements) rules forbid.

```markdown
1. A user who changes their email address receives a confirmation code at the new address.
```

### Boundaries

This Boundaries section does not follow the convention. The intent of the change already has the constraint "No new personal data in the session", and the first bullet repeats it, which the [Boundaries](#boundaries) rules forbid.

```markdown
## Boundaries

- Never: Store new personal data in the session.
- Ask first: Add a column to the accounts table.
```
