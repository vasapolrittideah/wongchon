# Constraint conventions

This convention defines the format of `CONSTRAINTS.md` at the root of a project, and how its rules and exceptions change. `CONSTRAINTS.md` states the quality bar of the project, and each rule in it names the check that enforces it.

The [Project documents](../../ROADMAP.md#decisions) decision of the roadmap states why a project has this file. The design stage writes it in the first change of the project, as the [Spec](specs.md) conventions state.

## Template

`CONSTRAINTS.md` has a [Title](#title), an [Introduction](#introduction), a [Floor](#floor), [Constraints](#constraints), [Measured, not yet enforced](#measured-not-yet-enforced), and [Exceptions](#exceptions).

```markdown
# Constraints

This file states the quality bar of the project. Each rule names the check that enforces it.

## Floor

| ID | Rule | Check |
| --- | --- | --- |
| F1 | <rule from the Floor rules table> | <command that checks the rule> |

## Constraints

| ID | Dimension | Rule | Check | Runs at | Reason |
| --- | --- | --- | --- | --- | --- |
| C1 | <quality that the rule measures> | <rule with a number> | <command that checks the rule> | <when the check runs> | <reason for the number> |

## Measured, not yet enforced

| ID | Dimension | Measure | Command | Target |
| --- | --- | --- | --- | --- |
| M1 | <quality that the project measures, if any> | <what the command reports> | <command that measures it> | <number that the project aims for> |

## Exceptions

| ID | Rule | Path | Reason | Owner | Expires |
| --- | --- | --- | --- | --- | --- |
| E1 | <ID of the rule, if any> | <path that the exception covers> | <reason for the exception> | <person who repairs it> | <date> |
```

### Title

- Write the title as `# Constraints`.

### Introduction

- Copy the introduction of the template without changes.

### Floor

- Write 1 row for each rule of the [Floor rules](#floor-rules) table, with its ID and its text, in the order of the table.
- In the Check column, name the command that checks the rule. If no command checks the rule yet, write `None yet`, and name the follow-up task that adds the check in the PR description.
- Add a rule of the project after the rules of the table, with the next `F` number.
- Do not remove or change a rule of the Floor rules table.

### Constraints

- Write 1 row for each rule that the project enforces with a number, such as zero test failures or a minimum coverage.
- Write the ID as `C` and the next number, such as `C1`.
- In the Rule column, state the number, such as "Zero findings" or "Added lines at least 80% covered".
- In the Check column, name the command that checks the rule. Use the commands of `.wongchon/config.json` where they apply.
- In the Runs at column, write 1 or more values from the [Runs at values](#runs-at-values) table, separated by commas.
- In the Reason column, state why the project chose the number, such as a measured baseline.

### Measured, not yet enforced

- If the project measures a quality but no rule blocks a change yet, add this section, and write 1 row for each measure.
- Write the ID as `M` and the next number, such as `M1`.
- When a check of the measure can block a change, move the measure to Constraints in a new row, and remove its row from this section.

### Exceptions

- If a rule has an exception, add this section, and write 1 row for each exception.
- Write the ID as `E` and the next number, such as `E1`.
- In the Rule column, write the ID of the rule that the exception relaxes.
- In the Path column, write each file or folder that the exception covers.
- In the Reason column, state why the change must break the rule, and what repairs it.
- In the Owner column, write the name of the person who repairs it.
- In the Expires column, write a date in the form `YYYY-MM-DD`, at most 90 days after the date of the PR that adds the row.

## Rules

### Naming and location

- Save the file as `CONSTRAINTS.md` at the root of the project.

### Format and content

- Follow the [English prose](english-prose.md) and [Markdown](markdown.md) conventions.
- Give each rule a check that blocks a change locally or in CI. A rule without a check is a measure, so put it in Measured, not yet enforced.
- Do not reuse an ID, also after its row is removed.

### Workflow

- Write the file in the design stage of the first change of the project, with the `constraint-driven-development` skill, after the project has the commands of its stack.
- Before a row merges, run its check on the branch, and make sure that it passes.
- If a spec adds or changes a rule, update the file in the PR of the spec.

### Changes

- To tighten a rule, change its row in a PR of the design stage.
- To break a rule for a change, add a row to Exceptions in the same PR, and state the reason in the PR description.
- To extend an exception, change its date in a new PR, at most 90 days after the date of that PR, and state why the repair is late.
- When the repair of an exception merges, remove the row of the exception in the same PR.
- Apply a change of this convention to the file in the next PR that changes the file.
- Do not weaken a rule, such as a lower number or a removed row, except through an exception.
- Do not keep an exception after its date. The PR that finds an expired exception repairs the cause, removes the row, or extends it.

## Reference

### Floor rules

| ID | Rule |
| --- | --- |
| F1 | Each linter directive that turns off a check names each rule that it turns off, and the PR description states the reason. |
| F2 | The code has no unimplemented stub, no empty error handler, and no marker for later work, such as `TODO` or `FIXME`. |
| F3 | No change skips or deletes a test or removes an assertion, unless Exceptions has a row for it. |
| F4 | No file has a secret, such as a password, a private key, or an access token. |
| F5 | No change weakens this file, unless Exceptions has a row for it. A change can tighten a rule. |

### Runs at values

| Value | When the check runs |
| --- | --- |
| `edit` | After each edit of a file, through a hook |
| `task end` | Before each commit of a task |
| `CI` | On each PR |

## Examples

### Constraints

These rows follow the convention. Each rule has a number, a command, and a reason:

```markdown
| ID | Dimension | Rule | Check | Runs at | Reason |
| --- | --- | --- | --- | --- | --- |
| C1 | Tests | Zero test failures | `npm test` | task end, CI | A failing test means the change is not ready. |
| C2 | Changed-line coverage | Added lines at least 80% covered | `npm run coverage:diff` | CI | 80% forces regression tests and allows small untested configuration changes. |
```

This row does not follow the convention. Its rule has no number and its Check column names no command, which the [Constraints](#constraints) rules forbid:

```markdown
| C3 | Performance | Pages load fast | Manual review | CI | Users want fast pages. |
```

### Exceptions

This row follows the convention. It names the rule, the path, the repair, the owner, and a date within 90 days:

```markdown
| E1 | F3 | `tests/test_export.py` | The export test calls a service that shuts down. A new test with a local fake service replaces it. | Kim Lee | 2027-02-15 |
```
