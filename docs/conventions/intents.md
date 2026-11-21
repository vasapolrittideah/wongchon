# Intent conventions

This convention defines the file, the format, and the status of 1 intent in `docs/intents/`. An intent states what a change must achieve and why, before the design of the change starts.

## Template

An intent has a [Title](#title), an [Author line](#author-line), a [Status line](#status-line), [Problem](#problem), [Outcome](#outcome), [Success criteria](#success-criteria), [Affected users and systems](#affected-users-and-systems), [Constraints](#constraints), [Out of scope](#out-of-scope), [Open questions](#open-questions), [Answers](#answers), and [References](#references).

```markdown
# Intent: <name of the change>

Author: <name of the owner of the intent>

Status: <status value>

## Problem

<problem that the change solves and the reason to solve it now>

## Outcome

<results that the change gives to its users>

## Success criteria

- <observable result>

## Affected users and systems

- <user or system that the change affects>

## Constraints

- <limit that exists before the design>

## Out of scope

- <item that the change excludes>

## Open questions

- <question for a later stage, if any>

## Answers

| Question | Reply |
| --- | --- |
| <question of the interview> | <meaning of the reply> |

## References

| Source | What this intent takes from it | Parts read only in a summary |
| --- | --- | --- |
| <link to a source, if any> | <point that the intent uses> | <parts of the source that the writer did not read in full> |
```

### Title

- Write the title as `# Intent: <name of the change>`.
- Write the name of the change as a short noun phrase, such as "wongchon version 1" or "email change".

### Author line

- Write the name of the person who owns the intent. The owner answers the interview and approves the intent.
- Do not write the name of an agent.

### Status line

- Write 1 value from the [Status values](#status-values) table, in backticks.
- Change the value only as the [Status and approval](#status-and-approval) rules state.

### Problem

- Write 1 or 2 paragraphs.
- State who has the problem, what goes wrong for them, and why the change starts now.

### Outcome

- State each result that the change gives to its users or to other systems.
- Describe each result as behavior that a user or a system sees, not as the code that produces it.

### Success criteria

- Write each criterion as a result that a person or a check can observe, such as "The maintainer installs the plugin in a project that uses another stack". The verify stage collects its evidence against these criteria.
- If a criterion is about an amount, such as speed or size, give the number.
- Do not write a criterion that nobody can observe, such as "easy to use" or "fast".

### Affected users and systems

- Write 1 bullet for each kind of user and each system that the change affects, and state how the change affects it.

### Constraints

- Write each limit that the design must respect and that exists before the design, such as a required platform, a deadline, a budget, or a law.
- Put the main limit first.
- If a project document already states a limit, link the document instead of repeating the limit.

### Out of scope

- Write 1 bullet for each item that a reader can expect in the change but that the change excludes. If the item comes later, state when.
- Write at least 1 bullet.

### Open questions

- If the intent leaves a question for a later stage, add this section.
- Name the stage that decides each question. If 1 stage decides all questions, name the stage once in a paragraph before the list.
- Do not leave a question that changes the problem, the outcome, the success criteria, or the scope. Answer it before the status changes to `Approved`.

### Answers

- Write 1 row for each question of the interview, in the order of the interview.
- In the Reply column, write in English the meaning of the reply of the owner, as a summary and not a copy of the words. If the owner only confirms a guess, write the confirmed guess.
- Write each reply so that a reader understands it without the chat.

### References

- If the intent uses an outside source, such as an article, a study, or documentation, add this section.
- Write 1 row for each source, and link the source in the Source column.
- In the third column, write the parts of the source that the writer read only in a summary. If the writer read the whole source, write `None`.
- Do not list a source that the intent does not use.

## Rules

### Naming and location

- Save each intent as `docs/intents/<change name>.md`. Write the change name as lowercase words and numbers separated by single hyphens, such as `wongchon-v1` or `email-change`.

### Format and content

- Follow the [English prose](english-prose.md) and [Markdown](markdown.md) conventions.
- Write what the change must achieve and why. The design of the change states how to build it.
- Do not name a file, a class, a function, a library, or a data structure, unless a limit that exists before the design requires it. Put such a limit in [Constraints](#constraints).

### Workflow

- Write 1 intent for each change that needs more than 1 pull request (PR). A change that fits in 1 PR has no intent, and it starts at the build stage.
- Write the intent from an interview with its owner.
- Open the intent in its own PR, before the design of the change starts.

### Status and approval

- Write the status `Draft` when you create the intent.
- Change the status to `Approved` only after the owner approves the intent in the chat or in a review of the PR. Commit the change on the branch of the PR.
- Do not merge an intent whose status is not `Approved`. The owner approves the gate of the intent stage when they merge the PR.

### Changes

- To change an approved intent, edit the file in a new PR, and change its status to `Draft` in that PR. Then follow the Status and approval rules again.
- Apply a change of this convention only to new intents and to intents that a later PR changes.

## Reference

### Status values

| Status | Meaning |
| --- | --- |
| `Draft` | The owner did not approve the intent yet. |
| `Approved` | The owner approved the intent, and the design of the change can start. |

## Examples

### Success criteria

These criteria follow the convention, because a person or a check can observe each one:

```markdown
- A user who changes their email address receives a confirmation code at the new address.
- The old address keeps working until the user enters the code.
- 95% of confirmation emails arrive within 60 seconds.
```

These criteria do not follow the convention. The first criterion breaks the Success criteria rules, because nobody can observe "seamless". The second criterion names a library, and breaks the Format and content rules.

```markdown
- Email changes are seamless.
- The service sends the code with the Nodemailer library.
```

### Answers

This table writes the meaning of a reply in which the owner only confirmed the guess of the agent:

```markdown
| Question | Reply |
| --- | --- |
| Can a small change skip stages? | Yes, if it fits in 1 PR. It starts at the build stage. |
```
