---
name: spec-driven-development
description: Writes the spec of a change in docs/specs/, in the format of the spec convention, after the intent of the change is approved. Use in the design stage when a change has an approved intent and no spec yet, when the requirements of a change span several independently testable capabilities and the change needs splitting, or when the design of a change must change.
---

# Spec-Driven Development

## Overview

Write a structured specification before writing any code. The spec is the shared source of truth between you and the human engineer — it defines how we'll build the change and how we'll know it's done. Code without a spec is guessing.

In this project, the intent of a change states what the change must achieve and why, and the spec states how to build it. The [spec convention](../../docs/conventions/specs.md) defines the file, the sections, and the status of a spec. Its ADRs record the decisions, as the [ADR convention](../../docs/conventions/adrs.md) states.

## When to Use

- A change has an approved intent in `docs/intents/` and no spec yet
- The change touches multiple files or modules
- You're about to make an architectural decision
- The requirements of the change span several independently testable capabilities
- The approved spec of a change must change before the last pull request of the change merges

**When NOT to use:** A change without an intent. It has no spec, and it starts at the build stage.

## The Gated Workflow

A change moves through the stages of the project. Each stage ends with a pull request, and the owner approves its gate when they merge it. Do not advance to the next stage until the current one is approved.

```
INTENT ──→ DESIGN ──→ BUILD ──→ VERIFY
   │          │         │         │
   ▼          ▼         ▼         ▼
 Owner      Owner     Owner     Owner
 merges     merges    merges    merges
```

This skill does the design stage: the spec and its ADRs. Before you start, read the approved intent of the change and the project documents that the spec convention names, such as `ARCHITECTURE.md`, `CONSTRAINTS.md`, and `GLOSSARY.md`.

### Phase 0: Scope Check

Most intents describe one capability. If this one does, skip this phase and go straight to Specify — Phase 0 exists for the exception, not the rule.

**Detection.** Split the change before specifying when its requirements bundle several independently testable capabilities:

- The requirements name distinct capabilities with their own consumers or data (e.g. identity, billing, notifications, reporting)
- The requirements cluster into groups that could ship and be verified separately
- One capability could be cut or replaced without rewriting the others' requirements

**Propose a capability map before writing any spec.** Small and reviewable — a module table plus a build order, not a project plan:

```markdown
# Capability Map: [Initiative Name]

| Change | Responsibility | Depends on |
|---|---|---|
| identity-accounts | Accounts, sessions, SSO | — |
| billing-invoices | Plans, invoices, payments | identity-accounts |
| notifications-fan-out | Email and webhook fan-out | identity-accounts |
| reporting-usage | Usage dashboards | billing-invoices, notifications-fan-out |

Build order: identity-accounts → billing-invoices, notifications-fan-out → reporting-usage
```

- **Stable change names.** Each row is 1 change, named `<scope>-<capability>` as the [intent convention](../../docs/conventions/intents.md#naming-and-location) states. Choose each name once, and never rename it.
- **Dependency direction, no cycles.** Arrows point one way. If two changes each need the other, they are one change.
- **Interfaces live at the boundary.** The map records that `billing-invoices` depends on `identity-accounts`; the contract between them belongs in the spec of the provider change (see `api-and-interface-design` for designing it).

**The map is gated like every stage.** The owner reviews the boundaries, the dependency direction, and the build order before any spec is written. Getting the map wrong is expensive; reviewing ten lines is not.

**Then give each row its own intent.** After the owner approves the map, each change goes through the intent stage, and then gets its own spec, in the build order.

### Phase 1: Specify

Start from the approved intent. Ask the owner about each undecided choice, 1 topic at a time, with the options and your recommendation, as the [Workflow](../../docs/conventions/specs.md#workflow) rules of the spec convention state.

**Surface assumptions immediately.** Before writing any spec content, list what you're assuming:

```
ASSUMPTIONS I'M MAKING:
1. This is a web application (not native mobile)
2. Authentication uses session-based cookies (not JWT)
3. The database is PostgreSQL (based on existing Prisma schema)
4. We're targeting modern browsers only (no IE11)
→ Correct me now or I'll proceed with these.
```

Don't silently fill in ambiguous requirements. The spec's entire purpose is to surface misunderstandings *before* code gets written — assumptions are the most dangerous form of misunderstanding. Write each assumption that nobody proved yet in the Assumptions and open questions section of the spec.

**Write the spec with the template of the spec convention.** Save it as `docs/specs/<change name>.md`, with the status `Draft`. The sections of the upstream template of this skill have other places in this project:

- **Objective, success criteria, and out of scope** — The intent states them. The spec links the intent and names the ID of each success criterion.
- **Commands, project structure, code style, and testing strategy** — They apply to the whole project, so `AGENTS.md`, `ARCHITECTURE.md`, and `CONSTRAINTS.md` state them. If the change changes one of them, the spec states the change.
- **Boundaries** — The spec has `Ask first` and `Never` items for the build of this change only. The rules that always apply are in `AGENTS.md` and `CONSTRAINTS.md`.

**Turn each success criterion into requirements.** Write each requirement as 1 row of the Requirements table, with an ID such as `R1`. Use the form Given, when, then, so that a test can prove it:

```
SUCCESS CRITERION S1: "Users see their dashboard without a wait"

REQUIREMENTS:
| ID | Requirement | Criterion | Proof |
| --- | --- | --- | --- |
| R1 | Given a signed-in user on a 4G connection, when they open the dashboard, then its LCP is below 2.5s. | S1 | End-to-end test |
| R2 | Given the dashboard data, when the page loads, then the initial data load completes in < 500ms. | S1 | Integration test |
→ Are these the right targets?
```

This lets you loop, retry, and problem-solve toward a clear goal rather than guessing what "without a wait" means. If a success criterion is too vague to turn into requirements, stop, and ask the owner whether the intent must change.

**Stop after writing the spec (CRITICAL).** Once the spec is saved:

1. Make sure that the spec follows the spec convention, and fix each problem.
2. Open the spec and its ADRs in 1 draft pull request, as the spec convention states.
3. Summarize it and list any open questions.
4. Ask the owner to approve it or request changes.
5. **STOP YOUR TURN IMMEDIATELY.** Do NOT write the plan or code in this turn. Change the status to `Approved` only after the owner approves the spec in a later turn.

### After the spec

The build stage starts after the owner merges the spec. It writes the plan of the change, which states the files, the order of the work, and the tests, and then implements it. Do not put those in the spec.

## Keeping the Spec True

A spec describes 1 transition of the project, and `ARCHITECTURE.md` describes the project as it is after each transition:

- **Change it before the change ships** — To change an approved spec, edit it in a new pull request, and change its status to `Draft` in that pull request. Then get the approval of the owner again.
- **Don't change it in a plan or code pull request** — If the build finds that the design must change, stop, and change the spec first.
- **Don't change it after the change ships** — After the last pull request of the change merges, start a new change, and write a new ADR for each changed decision.
- **Reference the spec in PRs** — Link back to the spec that each PR implements.

## Changes to Shipped Behavior

A spec describes one change. New ideas and later changes don't expand it — they queue behind it.

- **Park new ideas.** When an idea arrives during the design or the build, tell the owner, and keep going. It becomes a new change with its own intent, not a new requirement of this spec.
- **Each follow-up change gets its own spec.** It covers only what changes. Its Current state section links the parts of the project that it builds on, and its requirements name each behavior that must not change.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is simple, I don't need a spec" | A simple change without an intent starts at the build stage. A change with an intent still needs its requirements written down. |
| "I'll write the spec after I code it" | That's documentation, not specification. The spec's value is in forcing clarity *before* code. |
| "The spec will slow us down" | A 15-minute spec prevents hours of rework. Waterfall in 15 minutes beats debugging in 15 hours. |
| "The user knows what they want" | Even clear requests have implicit assumptions. The spec surfaces those assumptions. |
| "This idea is good, I'll fold it into the current spec" | Scope growth during the build is how a change slips. Tell the owner, and make it a new change. |
| "The feature already has a spec, I'll just edit it for the change" | A shipped spec records a past transition. A new change with its own spec keeps the change reviewable on its own. |
| "It's one big feature; splitting it is overhead" | If the requirements cluster into independently testable groups, a monolithic spec forces every downstream task to reason over the whole contract. A ten-line capability map is the cheap alternative. |
| "I'll decompose during planning" | Planning slices tasks within a spec. By then the oversized artifact already exists — change boundaries and dependency direction must be decided before the spec is written, not after. |

## Red Flags

- Starting to write code without an approved spec for a change that has an intent
- Asking "should I just start building?" before clarifying what "done" means
- Implementing features not mentioned in any spec or plan
- Making architectural decisions without an ADR
- Copying the problem, the outcome, or the success criteria of the intent into the spec
- New requirements written straight into an approved spec during the build
- Changing a shipped spec instead of starting a new change
- Writing the spec and starting the plan or code in the same turn
- One spec whose requirements span several independently testable capabilities
- Change boundaries or build order decided implicitly during implementation because no capability map was approved up front

## Verification

Before the build stage starts, confirm:

- [ ] The spec follows the template and the rules of the [spec convention](../../docs/conventions/specs.md), and has at most 200 lines
- [ ] Each success criterion of the intent has at least 1 requirement, and each requirement has an ID and names a test level
- [ ] Each decision that rejects options has an ADR in the same pull request
- [ ] The owner has reviewed and approved the spec
- [ ] The turn ended after saving the spec; approval came in a later turn
- [ ] Ideas cut from this change were given to the owner, not silently dropped or silently included
- [ ] If the intent bundles several independently testable capabilities, a capability map (change names, dependency direction, build order) was approved before any spec was written
