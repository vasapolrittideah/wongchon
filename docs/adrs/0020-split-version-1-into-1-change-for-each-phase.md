# ADR-0020: Split version 1 into 1 change for each phase

Status: `Accepted`

Spec: None

## Context

The review time of the maintainer is the main limit of version 1. 1 intent and 1 spec for all of version 1 grow long for each gate, and the plans of phases 4 and 5 then share 1 file. [#16](https://github.com/vasapolrittideah/wongchon/pull/16) first recorded this decision.

## Decision

From phase 3, each phase of the roadmap is 1 change or more, and each change has its own intent, spec, plan, and evidence. The Change column of the Phases table names each change. Phases 0 to 2 came before this rule and have no change name. The Version 1 section of the roadmap states the success criteria of the whole version.

## Rejected options

| Option | Reason |
| --- | --- |
| 1 change for all of version 1, with 1 intent and 1 spec | Its artifacts grow long for each gate, and the plans of phases 4 and 5 then share 1 file. |
| Intents written after the work for phases 0 to 2 | Their reasons then exist in 2 places. |

## Consequences

- Each phase starts with an interview for its own intent.
- The success criteria of version 1 live in the roadmap and not in an intent.

## Confirmation

No tool can check how the work splits into changes. The maintainer checks it at the gate of each intent.
