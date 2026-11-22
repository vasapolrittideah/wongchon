# ADR-0018: Name each stage skill after its stage

Status: `Accepted`

Spec: None

## Context

Claude Code namespaces the skills of a plugin, such as `/wongchon:verify`, and it has a built-in `/verify` skill that builds and runs an app. The skill of the design stage writes both the spec and the ADRs of a change. [#14](https://github.com/vasapolrittideah/wongchon/pull/14) first recorded this decision, and [#18](https://github.com/vasapolrittideah/wongchon/pull/18) added the rejected name `spec`.

## Decision

Each stage skill has the name of its stage, such as `/wongchon:verify`. The skill of the verify stage can use the built-in `/verify` skill to run the app.

## Rejected options

| Option | Reason |
| --- | --- |
| `spec` for the skill of the design stage | The skill writes both the spec and the ADRs of a change. |
| `prove` for the verify skill | The skill name then differs from the stage name. |

## Consequences

- A user types the namespace to call a stage skill when a built-in skill has the same name.
- The build stage has 2 skills, `plan` and `build`.

## Confirmation

No check exists yet. A follow-up task adds a check that the folder of each stage skill has the name of a stage, `plan`, or `build`.
