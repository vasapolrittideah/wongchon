# Glossary entry conventions

This convention defines the format of `GLOSSARY.md` at the root of a project, and the term and the meaning of each entry in it. An entry defines a term that has a narrower or different meaning in the project than in general English.

The [Project documents](../../ROADMAP.md#decisions) decision of the roadmap states why a project has this file and when it starts. The design stage adds and changes its entries, as the [Spec](specs.md) conventions state.

## Template

`GLOSSARY.md` has a [Title](#title), an [Introduction](#introduction), and 1 table with a [Term](#term) and a [Meaning](#meaning) in each row.

```markdown
# Glossary

This file defines each term that has a narrower or different meaning in the project than in general English.

| Term | Meaning |
| --- | --- |
| <term> | <meaning in the project> |
```

### Title

- Write the title as `# Glossary`.

### Introduction

- Copy the introduction of the template without changes.

### Term

- Write the term as the text of the project uses it, in lowercase, except for names and abbreviations, such as "task", "PR", or "GitHub text".
- Write a noun or a noun phrase in the singular form. If the term names a set, such as "service paths", write the plural form.
- If the term describes a quality, such as "ready", write the adjective, and start the meaning with the noun that it describes, such as "Of a PR:".

### Meaning

- Write 1 or more sentences that state what the term means in the project.
- If a document owns the decision behind the term, such as an ADR, link to it.
- Do not write rules in the meaning. Put each rule in the convention or the document that owns it.

## Rules

### Naming and location

- Save the file as `GLOSSARY.md` at the root of the project.
- Create the file in the PR that adds the first term of the project.

### Format and content

- Follow the [English prose](english-prose.md) and [Markdown](markdown.md) conventions.
- Order the rows by term in alphabetical order, without regard to case.
- Write 1 row for each term. If the project uses 1 term with 2 meanings, rename the term of 1 meaning in the text of the project.
- Define only a term that has a narrower or different meaning in the project than in general English.
- Do not define a term of the glossary again in another file, such as a convention, a spec, or an ADR. Link the glossary instead.

### Workflow

- If a change uses a new term, or changes the meaning of a term, add or update its row in the same PR.

### Changes

- If a term is no longer used, remove its row in the PR that removes its last use.
- Apply a change of this convention only to new rows and to rows that a later PR changes.

## Examples

This row defines a term with a meaning in the project:

```markdown
| task | 1 piece of work that 1 PR completes. |
```

This row describes a quality of a PR:

```markdown
| ready | Of a PR: the checks of the pull request conventions and CI pass, and the title, the description, and the labels match the final work. |
```

These rows do not follow the convention. They define 1 term with 2 meanings, which the [Format and content](#format-and-content) rules forbid:

```markdown
| index | The table of records in the ADR folder. |
| index | The list of specs and their status. |
```
