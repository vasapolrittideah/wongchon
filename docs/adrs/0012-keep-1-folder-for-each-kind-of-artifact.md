# ADR-0012: Keep 1 folder for each kind of stage artifact

Status: `Accepted`

Spec: None

## Context

Each stage commits its artifacts, and the next stage must find them. The playbook keeps `spec.md` next to `intent.md` in 1 home for each change, and the playbook, flowspace-api, and the `spec-driven-development` skill call the artifact of the design stage a spec. [#14](https://github.com/vasapolrittideah/wongchon/pull/14) first recorded this decision, and [#18](https://github.com/vasapolrittideah/wongchon/pull/18) renamed the design artifact to spec and the ADR folder to `docs/adrs/`.

## Decision

Each kind of artifact has its own folder: `docs/intents/`, `docs/specs/`, `docs/plans/`, `docs/evidence/`, and `docs/adrs/`. All files of 1 change have the same change name. The artifact of the design stage is the spec, which states how to build the change.

## Rejected options

| Option | Reason |
| --- | --- |
| 1 folder for each change that holds all its files, such as `docs/changes/<change>/` | The maintainer chose 1 folder for each kind of artifact. |
| The name design for the artifact of the design stage, in `docs/designs/` | The playbook, flowspace-api, and the `spec-driven-development` skill call this artifact a spec. |
| `docs/adr/`, which flowspace-api and adr-tools use | The other folders of artifacts have plural names. |

## Consequences

- A reader finds the files of 1 change by its change name in each folder.
- Each convention of a stage artifact names its folder.

## Confirmation

No check exists yet. The `Stage gate` CI job of the `design-specs-and-adrs` change reads the artifacts in these folders. Until then, the maintainer checks the paths in the review of each PR.
