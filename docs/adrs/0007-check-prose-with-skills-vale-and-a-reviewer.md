# ADR-0007: Check prose with skills, Vale, and a writing reviewer

Status: `Accepted`

Spec: None

## Context

The prose of the project must follow its conventions. A linter can check words and form but cannot judge meaning, and a skill alone has nothing that enforces it. [#3](https://github.com/vasapolrittideah/wongchon/pull/3) first recorded this decision in the roadmap.

## Decision

The project writes prose with the `simple-english` and `humanizer` skills, checks it with Vale and rules from the conventions of this project, and checks its meaning with a writing reviewer. The writing reviewer comes in the agent workflow phase, and Vale comes in the build phase.

## Rejected options

| Option | Reason |
| --- | --- |
| Vale alone | It cannot judge meaning. |
| The skills alone | Nothing enforces them. |
| The stock Vale styles | They conflict with the conventions of this project. |
| textlint, write-good, and alex | They need Node. |

## Consequences

- The project writes its own Vale rules from its conventions.
- The writing reviewer checks the meaning that Vale cannot check.

## Confirmation

No check exists yet. The `plugin-review-gate` change adds the writing reviewer, and the build phase adds Vale to CI. Until then, the maintainer checks the prose in the review of each PR.
