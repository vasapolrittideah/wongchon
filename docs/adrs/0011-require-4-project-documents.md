# ADR-0011: Require AGENTS.md, CONSTRAINTS.md, ARCHITECTURE.md, and GLOSSARY.md

Status: `Accepted`

Spec: [`docs/specs/design-specs-and-adrs.md`](../specs/design-specs-and-adrs.md)

## Context

Agents get the context of a project from its project documents, but a document that repeats the code goes out of date. The framework fixes its paths, so each project keeps the same documents in the same place. [#4](https://github.com/vasapolrittideah/wongchon/pull/4) first recorded the decision about `ARCHITECTURE.md`, and [#14](https://github.com/vasapolrittideah/wongchon/pull/14) added the other documents. The Project documents part of [`docs/specs/design-specs-and-adrs.md`](../specs/design-specs-and-adrs.md) states the content and the check of `CONSTRAINTS.md` and `GLOSSARY.md`.

## Decision

`ARCHITECTURE.md` at the root states the parts of the project, how they connect, the reasons, and the rules. It does not list folders or versions, because the code holds them. In a greenfield project, the design stage plans the structure and the stack, and the reasons and rules move into `ARCHITECTURE.md` after the build. A brownfield project moves its existing architecture document to `ARCHITECTURE.md` and arranges its content for the framework. The framework also requires `AGENTS.md`, with `CLAUDE.md` as a symbolic link to it, and `CONSTRAINTS.md`, which the design stage of the first change writes. `GLOSSARY.md` exists only after a project has its first term of its domain.

## Rejected options

| Option | Reason |
| --- | --- |
| `docs/architecture.md` | The other project documents are at the root. |
| A path that a project sets in `.wongchon/config.json` | The framework fixes its paths. |
| Separate project structure and technology stack documents after the build | The code holds that information, and the documents go out of date. |
| `GLOSSARY.md` in each project | A project can start with no terms of its domain. |

## Consequences

- Each rule in `ARCHITECTURE.md` needs a deterministic check in the stack of the project.
- A greenfield project has no `ARCHITECTURE.md` until the build of its first change.

## Confirmation

No check exists yet. The `design-specs-and-adrs` change adds the conventions of `CONSTRAINTS.md` and `GLOSSARY.md`, and its spec lists a check of the commands in `CONSTRAINTS.md` as a follow-up task. Until then, the maintainer checks the documents in the review of each PR.
