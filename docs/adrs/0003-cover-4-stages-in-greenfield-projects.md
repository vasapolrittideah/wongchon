# ADR-0003: Cover 4 stages in greenfield projects in version 1

Status: `Accepted`

Spec: None

## Context

The deploy and maintain stages depend most on the stack and the cloud provider of a project. The first project that uses version 1 is greenfield, which is a new project without code. [#3](https://github.com/vasapolrittideah/wongchon/pull/3) first recorded this decision in the roadmap, and [#5](https://github.com/vasapolrittideah/wongchon/pull/5) moved brownfield projects out of version 1.

## Decision

Version 1 covers the intent, design, build, and verify stages in greenfield projects. The deploy and maintain stages and brownfield projects, which are existing projects with code and documents, come after version 1. The design of each change must not assume that a project has no code or no documents.

## Rejected options

| Option | Reason |
| --- | --- |
| All 6 stages | The deploy and maintain stages depend most on the stack and the cloud provider of a project. |
| Brownfield projects in version 1 | The first project that uses version 1 is greenfield. |

## Consequences

- The roadmap lists the deploy and maintain stages and brownfield support in the work after version 1.
- Each spec must work in a project that already has code and documents, so that brownfield support needs no redesign.

## Confirmation

No tool can check the scope of a change. The maintainer checks the scope of each intent and spec at the gate of its stage.
