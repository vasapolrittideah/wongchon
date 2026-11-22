---
name: documentation-and-adrs
description: Records architecture decisions as ADRs in docs/adrs/, in the format of the ADR convention. Use in the design stage when the spec of a change takes a decision that rejects options, when you need to record the reasoning behind a design choice, or when a decision changes and a new ADR must supersede the old one.
---

# Documentation and ADRs

## Overview

Document decisions, not just code. The most valuable documentation captures the *why* — the context, constraints, and trade-offs that led to a decision. Code shows *what* was built; documentation explains *why it was built this way* and *what alternatives were considered*. This context is essential for future humans and agents working in the codebase.

In this project, the design stage writes the ADRs of a change together with its spec. The [ADR convention](../../docs/conventions/adrs.md) defines the file, the sections, the status, and the life cycle of each ADR. The [Code comments](../../docs/conventions/code-comments.md) convention states where other information goes.

## When to Use

- Making a significant architectural decision
- Choosing between competing approaches
- Writing the spec of a change that takes a decision with rejected options
- Changing a decision that an accepted ADR records

**When NOT to use:** Don't write an ADR for a decision that rejects no option. Don't write docs for throwaway prototypes.

## Architecture Decision Records (ADRs)

ADRs capture the reasoning behind significant technical decisions. They're the highest-value documentation you can write.

### When to Write an ADR

Write 1 ADR for each decision of a spec that rejects options, as the [Workflow](../../docs/conventions/adrs.md#workflow) rules of the ADR convention state. Examples:

- Choosing a framework, library, or major dependency
- Designing a data model or database schema
- Selecting an authentication strategy
- Deciding on an API architecture (REST vs. GraphQL vs. tRPC)
- Choosing between build tools, hosting platforms, or infrastructure
- Any decision that would be expensive to reverse

### Follow the ADR convention

Write each ADR with the template and the rules of the [ADR convention](../../docs/conventions/adrs.md). It defines the location `docs/adrs/<number>-<decision>.md`, the 4-digit numbers, the sections, and the status values. Before you write an ADR, read the existing ADRs in `docs/adrs/`, and continue their sequence.

- Write 1 decision in each ADR.
- List the options that the decision rejects in the Rejected options table, with the reason for each rejection.
- Name the deterministic check that keeps the decision true in Confirmation.
- Open each ADR in the same pull request as the spec of its change, and list it in the Decisions section of the spec.

If the project already has decision records in another format or folder, surface the conflict to the owner rather than silently introducing a second scheme.

### ADR Lifecycle

```
ACCEPTED → SUPERSEDED
```

- An ADR opens with the status `Accepted`. The owner accepts it when they merge the pull request.
- **Don't delete old ADRs.** They capture historical context.
- **Don't edit an accepted ADR**, except its status line when a new ADR supersedes it.
- When a decision changes, write a new ADR that supersedes the whole old one, and change the status line of the old ADR to `Superseded by` with a link to the new ADR.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The code is self-documenting" | Code shows what. It doesn't show why, what alternatives were rejected, or what constraints apply. |
| "Nobody reads docs" | Agents do. Future engineers do. Your 3-months-later self does. |
| "ADRs are overhead" | A 10-minute ADR prevents a 2-hour debate about the same decision six months later. |
| "I'll just fix the old ADR" | An accepted ADR is the record of the old decision. A new ADR that supersedes it keeps both the old reasons and the new ones. |

## Red Flags

- Architectural decisions with no written rationale
- No ADRs in a project with significant architectural choices
- An ADR with no rejected option, or with no check in Confirmation
- An accepted ADR edited in a later pull request, other than its status line
- An ADR that covers 2 decisions

## Verification

After documenting:

- [ ] Each decision of the spec that rejects options has 1 ADR
- [ ] Each ADR follows the template and the rules of the [ADR convention](../../docs/conventions/adrs.md)
- [ ] Each ADR is listed in the Decisions section of the spec
- [ ] Each superseded ADR has the status `Superseded by` with a link to the new ADR
