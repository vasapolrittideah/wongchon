# ADR-0023: Choose the review roles of a commit from fixed path rules

Status: `Accepted`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Context

Each role checks 1 kind of file: code, prose, or stage artifacts. A role that reads files outside its kind uses tokens and writes findings that are not its work. The [Roadmap](../../ROADMAP.md) states that the framework fixes the rules, and that a project cannot change a convention or a stage.

## Decision

The front matter of each role file lists its paths. A commit needs the stamp of each role whose paths match a staged file. The writing reviewer covers each `.md` file and the text of a PR. The artifact reviewer covers `docs/intents/**`, `docs/specs/**`, `docs/adrs/**`, `CONSTRAINTS.md`, and `GLOSSARY.md`. The code reviewer covers each other file. A project cannot change these paths.

## Rejected options

| Option | Reason |
| --- | --- |
| All 3 roles for each commit | It uses more tokens, and a role writes findings outside its work. |
| Paths of each role in `.wongchon/config.json` | A project could then change a rule of the framework. |

## Consequences

- A stage artifact needs both the artifact reviewer and the writing reviewer.
- A project with Markdown outside these paths, such as a README, gets only the writing reviewer for it.

## Confirmation

The unit tests of `hooks/review_guard.py` check the required roles for each kind of path.
