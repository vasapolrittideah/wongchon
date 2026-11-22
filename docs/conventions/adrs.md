# Architecture decision record conventions

This convention defines the file, the format, the status, and the life cycle of 1 architecture decision record (ADR) in `docs/adrs/`. An ADR records 1 decision of a project that rejects options, the reasons for it, and the check that keeps it true.

The design stage writes the ADRs of a change together with its spec, as the [Spec](specs.md) conventions state. The [Decision records](../../ROADMAP.md#decisions) decision of the roadmap states why the project uses ADRs.

## Template

An ADR has a [Title](#title), a [Status line](#status-line), a [Spec line](#spec-line), [Context](#context), [Decision](#decision), [Rejected options](#rejected-options), [Consequences](#consequences), and [Confirmation](#confirmation).

```markdown
# ADR-<number>: <decision>

Status: <status value>

Spec: <link to the spec of the change>

## Context

<facts and forces that the decision answers>

## Decision

<chosen option and what it requires>

## Rejected options

| Option | Reason |
| --- | --- |
| <option that the decision rejects> | <reason for the rejection> |

## Consequences

- <effect of the decision>

## Confirmation

<check that keeps the decision true>
```

### Title

- Write the title as `# ADR-<number>: <decision>`, with the number of the file name.
- Write the decision as 1 sentence in the present tense that names the chosen option, such as "Store ADRs in docs/adrs".

### Status line

- Write 1 value from the [Status values](#status-values) table. Put `Accepted` in backticks. In a superseded ADR, write `Superseded by` and a link to the new ADR, such as `Superseded by [ADR-0007](0007-store-adrs-in-docs-adrs.md)`.
- Change the value only as the [Changes](#changes) rules state.

### Spec line

- Link the spec of the change that took the decision, with the relative path `../specs/<change name>.md`, and use the path from the repository root in backticks as the link text.
- If the decision has no spec, follow [Decisions from before the design stage](#decisions-from-before-the-design-stage).

### Context

- Write 1 to 3 paragraphs.
- State the facts and the forces that the decision must answer, such as a limit, a rule, a risk, or a need of a user.
- If the spec of the change already states a fact, link the spec instead of repeating it.
- If the ADR supersedes another ADR, link the old ADR, and state what changed since that decision.

### Decision

- State the chosen option in the present tense, such as "The project stores ADRs in `docs/adrs/`".
- State what the decision requires from the project, such as a folder, a format, or a rule for the code.
- If the ADR supersedes another ADR, also state each part of the old decision that stays true, so that this ADR holds the whole current decision.

### Rejected options

- Write 1 row for each option that the decision rejects, and at least 1 row.
- In the Reason column, state why the decision rejects the option in 1 or 2 sentences.

### Consequences

- Write 1 bullet for each effect of the decision, such as a task that becomes easier or harder, a cost, or a later decision that it needs.
- Write each effect as a fact, not as a hope, such as "Each new ADR needs a check" instead of "This keeps ADRs useful".

### Confirmation

- Name the deterministic check that keeps the decision true, such as a test, a linter rule, a hook, or a CI job.
- If no check is possible yet, name the follow-up task that adds it, and state who checks the decision until then.
- Do not name a review by a person as the only check of a decision that a tool can check.

## Rules

### Naming and location

- Save each ADR as `docs/adrs/<number>-<decision>.md`.
- Write the number with 4 digits, such as `0007`. Give each new ADR the next number after the highest number in `docs/adrs/`.
- Write the decision part of the file name as a short form of the title, in lowercase words and numbers separated by single hyphens, such as `store-adrs-in-docs-adrs`.
- Do not reuse a number, and do not skip a number.
- Do not rename an ADR after it merges.

### Format and content

- Follow the [English prose](english-prose.md) and [Markdown](markdown.md) conventions.
- Write 1 decision in each ADR. If a spec takes 2 decisions, write 2 ADRs.
- Write in the ADR the reasons for the decision and the options that it rejects. The spec of the change states how the decision applies to the change.

### Workflow

- Write 1 ADR for each decision of a spec that rejects options.
- Open each ADR in the same pull request (PR) as the spec of its change.
- List each ADR in the Decisions section of the spec of its change.

### Status and approval

- Open the PR of an ADR with the status `Accepted`. The owner accepts the ADR when they merge the PR.
- Do not merge an ADR before the owner approves the spec of its change.

### Changes

- To change a decision, write a new ADR that supersedes the old ADR. In the same PR, change the status line of the old ADR to `Superseded by` with a link to the new ADR.
- Supersede the whole old ADR. If a part of the old decision stays true, state it in the Decision of the new ADR.
- Apply a change of this convention only to new ADRs and to ADRs that a later PR changes.
- Do not edit an accepted ADR, except its status line when a new ADR supersedes it.
- Do not supersede a part of an ADR, and do not add a scoped exception to an ADR.
- Do not delete an ADR. A superseded ADR stays as the record of the old decision.

## Decisions from before the design stage

A project can have decisions that it took before it used the design stage, such as the decisions in a roadmap. When the project moves such a decision into an ADR, the decision has no spec.

- Write the Spec line as `Spec: None`.
- In Context, link the PR or the document that first recorded the decision.
- Open these ADRs in their own PR, without a spec.

## Reference

### Status values

| Status | Meaning |
| --- | --- |
| `Accepted` | The decision is in force. |
| `Superseded by` a link to a new ADR | The new ADR replaces the whole decision. |

## Examples

### File names

These file names follow the convention:

| Title | File name |
| --- | --- |
| `# ADR-0007: Store ADRs in docs/adrs` | `docs/adrs/0007-store-adrs-in-docs-adrs.md` |
| `# ADR-0012: Use Python with the standard library for hooks` | `docs/adrs/0012-use-python-for-hooks.md` |

### Status lines

This status line follows the convention. The old ADR names the ADR that replaces it:

```markdown
Status: Superseded by [ADR-0012](0012-use-python-for-hooks.md)
```

This status line does not follow the convention. It supersedes a part of the ADR, which the [Changes](#changes) rules forbid:

```markdown
Status: Accepted, except the hook language, which ADR-0012 supersedes
```
