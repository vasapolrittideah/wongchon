# Spec: design specs and ADRs

Author: Vasapol Rittideah

Status: `Approved`

Intent: [`docs/intents/design-specs-and-adrs.md`](../intents/design-specs-and-adrs.md)

## Context

The intent of this change asks for a design stage that works: an agent writes the spec of a change from its approved intent, records its decisions in architecture decision records (ADRs), and the owner approves the spec when they merge its pull request (PR). This spec states how this repository builds that stage in phase 3 of the [Roadmap](../../ROADMAP.md).

The Decisions section of the roadmap holds each decision of this spec with its rejected options. The decisions that only later changes build, such as the plugin layout, the setup command, and the rule for small changes, stay there for the specs of those changes.

## Spec artifact

The spec convention defines the spec, which is the artifact of the design stage. This spec is its first example.

- Save each spec as `docs/specs/<change name>.md`, with the change name of its intent, as the [Stage artifacts](../../ROADMAP.md#decisions) decision states.
- Give each spec an Author line, a Status line with the values `Draft` and `Approved`, and a link to its intent.
- Keep each spec at most 200 lines, as the success criteria of the intent state.
- Write in a spec how to build the change. Do not repeat the problem, the outcome, the success criteria, or the scope of the intent.

A spec starts from these parts. The PR of the spec convention asks the maintainer about each part before it fixes the sections:

- The context, which links the intent and the decisions that the spec depends on
- The parts of the change, how they connect, and the interfaces between them
- The check that enforces each rule of the change, or the follow-up task that adds the check
- The order of the work, which the plan of the build stage turns into tasks
- The open questions for later stages, the answers of the owner, and the references

## Decision records

The ADR convention defines the ADRs of a project, as the [Decision records](../../ROADMAP.md#decisions) decision states.

- Save each ADR as `docs/adr/<number>-<decision>.md`. The number has 4 digits, and each new ADR takes the next number.
- Write 1 ADR for each decision of a spec that rejects options. The spec links each ADR.
- Open the PR of an ADR with the status `Accepted`. The merge of the PR accepts the ADR.
- Do not edit an accepted ADR. To change a decision, write a new ADR that supersedes it, and change only the status line of the old ADR.

The sections of an ADR start from the sections of Michael Nygard: context, decision, status, and consequences, with the rejected options of the `documentation-and-adrs` skill. The PR of the ADR convention asks the maintainer about the sections.

In a separate PR, the decisions of the roadmap that have rejected options move into ADRs. The Decisions section of the roadmap then keeps 1 row for each ADR, with a link and the decision in 1 sentence.

## Project documents

This change writes the conventions of 2 project documents, as the [Project documents](../../ROADMAP.md#decisions) decision states:

| Document | When it exists | Content | Check |
| --- | --- | --- | --- |
| `CONSTRAINTS.md` | From the design stage of the first change | The quality bar of the project. Each rule names the command that checks it and when the check runs. | The review gate of the `plugin-review-gate` change blocks a change that lowers the bar. Until then, the maintainer checks it in the review. |
| `GLOSSARY.md` | From the first change that uses a term of the domain of the project | Each term that the code does not explain, with its meaning in 1 sentence | Each PR that adds or changes a term updates the file. A reviewer checks it from the `plugin-review-gate` change. |

The design stage writes and updates both documents. `AGENTS.md` and `ARCHITECTURE.md` are also project documents, but other changes write their conventions: the setup command creates `AGENTS.md`, and the build phase writes `ARCHITECTURE.md`.

## Stage gate

A CI job named `Stage gate` blocks the merge of an artifact that the owner did not approve, as the [Stage gate](../../ROADMAP.md#decisions) decision states.

- The job runs `scripts/check_stage_gate.py`, with Python 3.9 or later and the standard library only.
- The script reads each file that the PR adds or changes in `docs/intents/` and `docs/specs/`. It fails when the Status line of a file is not `Approved`.
- The script also fails when a spec has more than 200 lines.
- The agent changes the status to `Approved` only after the owner approves the artifact in the chat or in a review of the PR, as the [Intent](../conventions/intents.md) conventions state.
- The ready rule of the [Pull request](../conventions/pull-requests.md) conventions requires passing CI, but this job fails until the owner approves. The rule therefore excludes the `Stage gate` job, and only that job.
- The `build-plans-and-tasks` change adds `docs/plans/` to the script.

## Skills

This change copies 4 skills of agent-skills at version 0.6.17 and rewrites them for the design stage, as the Skills from agent-skills section of the roadmap states. Each copy follows the rules of `skills/THIRD_PARTY.md`.

| Skill | Part that the design stage uses | Rewrite |
| --- | --- | --- |
| `spec-driven-development` | The parts about how to build a change, such as the capability map and the delta for an existing behavior | Remove the parts that the intent already states, and write to the spec of the change instead of `SPEC.md`. |
| `api-and-interface-design` | The design of an interface before its code | Name the spec as the place of the interface. |
| `documentation-and-adrs` | The ADR part | Write ADRs in `docs/adr/` with the ADR convention. Remove the rules for comments, which the [Code comments](../../ROADMAP.md#decisions) decision replaces. |
| `constraint-driven-development` | The interview about the quality bar, and the defaults for each dimension | Write `CONSTRAINTS.md` with its convention. Remove the Node script of the skill, because scripts of this project use Python. |

The `design` skill runs the design stage for 1 change, in the same way as the `intent` skill runs the intent stage:

1. Read the approved intent of the change and the project documents.
2. Give the research to a read-only subagent, and keep each source for the References section.
3. Ask the owner about each undecided choice, 1 topic at a time, with options and a recommendation.
4. Write the spec and its ADRs with the status `Draft`, and update `CONSTRAINTS.md` and `GLOSSARY.md` when the spec changes them.
5. Make sure that the spec follows the spec convention, and fix each problem.
6. Commit, push, and open a draft PR. Mark the PR as ready when it meets each condition of a ready PR.
7. Change the status to `Approved` after the owner approves the spec, and tell the owner that the PR is ready to merge.

## Checks

| Rule | Check |
| --- | --- |
| A spec or an intent merges only with the status `Approved`. | The `Stage gate` CI job |
| A spec has at most 200 lines. | The `Stage gate` CI job |
| An accepted ADR changes only in its status line. | A follow-up task adds a CI check that compares each changed ADR with `main`. |
| Each rule of `CONSTRAINTS.md` names its check command. | A follow-up task adds the check to the `Stage gate` script. Until then, the maintainer checks it in the review. |

## Order of the work

Phase 3 delivers these PRs in this order. Each PR is 1 reviewable change.

1. This spec, written by hand from the intent
2. The spec convention, from this spec
3. The ADR convention
4. The ADRs of this repository, moved from the Decisions section of the roadmap
5. The conventions of `CONSTRAINTS.md` and `GLOSSARY.md`
6. The `Stage gate` CI job, and its exception in the ready rule of the pull request conventions
7. The copies of the 4 skills of agent-skills, rewritten for the design stage
8. The `design` skill

## Open questions

The maintainer decides this question in the review of this spec:

- The Steering Claude Code article puts the folder layout of a project in `CLAUDE.md`. The Best practices for Claude Code page calls this advice out of date, because Claude reads the code. This spec follows the Best practices page, as the Project documents decision of the roadmap already does.

## Answers

| Question | Reply |
| --- | --- |
| Where does a project keep the artifacts of each stage: 1 folder for each change, or 1 folder for each kind of artifact? | 1 folder for each kind of artifact: `docs/intents/`, `docs/specs/`, `docs/plans/`, and `docs/evidence/`, with ADRs in `docs/adr/`. |
| Which project documents does the framework require besides `ARCHITECTURE.md`? | `AGENTS.md` and `CONSTRAINTS.md`. `GLOSSARY.md` is optional, and a project creates it with its first term of the domain. |
| How does the design stage use ADRs? | ADRs go in `docs/adr/<number>-<decision>.md`. An ADR opens as `Accepted`, and the merge accepts it. An accepted ADR changes only when a new ADR supersedes it. The roadmap decisions with rejected options move into ADRs in a separate PR after the ADR convention. |
| Do you accept the changes to the Skills from agent-skills table? | Yes. `constraint-driven-development` moves to the design phase, `accessibility-engineering` joins the verify phase, the design phase copies only the parts of `spec-driven-development` about how to build and the ADR part of `documentation-and-adrs`, and `planning-and-task-breakdown` stays in the build phase. |
| Who changes the status to `Approved`, and which CI check blocks the merge? | The agent, after an explicit approval of the owner. A `Stage gate` CI job fails while an intent, spec, or plan of the PR is not `Approved`, and the ready rule of the PR conventions excludes only that job. |

## References

| Source | What this spec takes from it | Parts read only in a summary |
| --- | --- | --- |
| The 02 Design section of [The AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) | The spec answers the open questions of the intent or carries them forward, and a person decides the gate | The whole article, which the fetch tool returned only as a summary |
| [Steering Claude Code](https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more) | Procedures in skills, and rules that must always hold in hooks and CI checks | The embedded timeline and the map of hook events |
| [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) | Write in project documents only what the code does not show, and a reviewer checks the work against the written spec | None |
| [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) by Michael Nygard | 1 numbered ADR for each decision, its sections, and a new ADR that supersedes an old one instead of an edit | None |
| [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) by Malte Ubl | A short design document for a small change, and the parts of a design document | None |
| The skills of [agent-skills](https://github.com/addyosmani/agent-skills) at version 0.6.17 | The phase of each skill, the ADR sections of `documentation-and-adrs`, and the parts of `spec-driven-development` about how to build | 20 of the 26 skills, which the agent read only by their descriptions, headings, and paths |
