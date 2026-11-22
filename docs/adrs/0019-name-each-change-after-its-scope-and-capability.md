# ADR-0019: Name each change after its scope and capability

Status: `Accepted`

Spec: None

## Context

The files of 1 change share 1 name across the folders of the artifacts. flowspace-api starts each module ID with its service, and in a project of any stack the commit scope plays that role. [#15](https://github.com/vasapolrittideah/wongchon/pull/15) first recorded this decision, and the [Intent](../conventions/intents.md#naming-and-location) conventions state the rule.

## Decision

Each change has the name `<scope>-<capability>`: the commit scope of its main change, and then what the change delivers, such as `design-specs-and-adrs`.

## Rejected options

| Option | Reason |
| --- | --- |
| The name of the project and a version as a prefix, such as `wongchon-v1-design-stage` | Each change belongs to the project, and a change can finish in a later version. |
| A general word as the capability, such as `build-stage` | It does not name what the change delivers. |

## Consequences

- The scope part of a change name matches an area label of its PRs.
- A change that no single scope covers has a name with no scope part.

## Confirmation

No check exists yet. A follow-up task adds a check that the scope part of each change name is a scope in `commit.scopes`.
