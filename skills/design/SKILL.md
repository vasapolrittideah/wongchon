---
name: design
description: Runs the design stage of wongchon for 1 change. It reads the approved intent, asks the owner about each undecided choice, writes the spec in docs/specs/ and its ADRs in docs/adrs/, and opens the pull request that is the gate of the stage. Use when a change has an approved intent and no spec, or when the user asks you to write, change, or approve a spec.
---

# Design

## Overview

The design stage turns an approved intent into an approved spec. The intent states what a change must achieve and why. The spec states how to build it, and its architecture decision records (ADRs) state the reasons for its decisions. The stage ends at a gate: the owner of the change approves the spec when they merge its pull request (PR). You work up to the gate, but you do not pass it.

Before you start, read these files:

- The [spec convention](../../docs/conventions/specs.md), which defines the file, the sections, and the status of a spec
- The [ADR convention](../../docs/conventions/adrs.md), which defines the file, the sections, and the life cycle of an ADR
- The [constraints](../../docs/conventions/constraints.md) and [glossary entry](../../docs/conventions/glossary-entries.md) conventions, which define `CONSTRAINTS.md` and `GLOSSARY.md`
- The [branch name](../../docs/conventions/branch-names.md), [commit message](../../docs/conventions/commit-messages.md), [pull request](../../docs/conventions/pull-requests.md), and [GitHub label](../../docs/conventions/github-labels.md) conventions, which define how the spec reaches the gate

## Steps

Do the steps in this order. If the owner must answer a question, stop your turn and wait for the answer.

1. Read the intent of the change in `docs/intents/`. If its status is not `Approved`, or if it has not merged, stop the skill, and tell the owner that the intent stage must end first.
2. Read the project documents that the change builds on or changes: `ARCHITECTURE.md`, `CONSTRAINTS.md`, `GLOSSARY.md`, and the ADRs in `docs/adrs/`, where they exist.
3. Check the scope of the change, as Phase 0 of the [`spec-driven-development`](../spec-driven-development/SKILL.md) skill states. If the requirements form groups that can ship and be tested apart, propose a capability map to the owner, and follow [Split a change](#split-a-change).
4. Give the research to a read-only subagent. Research is, for example, the parts of the code that the change builds on, the behavior of a tool, or a standard.
   1. Ask the subagent for the answer, its evidence as a URL or a file and line, and the parts that it did not read in full.
   2. Tell the owner in a few sentences what the research found.
   3. Keep each outside source that the spec uses for the References section of the spec.
5. Ask the owner about each undecided choice, 1 topic at a time, with the options and your recommendation. Ask also each open question of the intent that the design stage must decide.
6. Create a short-lived branch from the current default branch, as the branch name conventions state.
7. Write the spec with the `spec-driven-development` skill, with the status `Draft`. Write 1 row in the Answers table of the spec for each question of step 5.
8. Write the other artifacts of the design in the same PR:
   - If a part of the change is an interface, such as an API or a module boundary, design its contract with the [`api-and-interface-design`](../api-and-interface-design/SKILL.md) skill, and write it in the Design section of the spec.
   - Write 1 ADR for each decision that rejects options, with the [`documentation-and-adrs`](../documentation-and-adrs/SKILL.md) skill, and list it in the Decisions section of the spec.
   - If the project has no `CONSTRAINTS.md`, and it has the commands of its stack, such as a test command, write the file with the [`constraint-driven-development`](../constraint-driven-development/SKILL.md) skill. If the project has no commands yet, write an open question for the change that adds them.
   - If the spec adds or changes a rule of `CONSTRAINTS.md`, update the file, as the constraints convention states.
   - If the spec uses a new term or changes the meaning of a term, add or update its row in `GLOSSARY.md`, as the glossary entry convention states.
9. Make sure that the spec and the ADRs follow their conventions. Use the list in [Verification](#verification). Fix each problem before you continue.
10. Commit the spec and the other artifacts, as the commit message conventions state.
11. Push the branch, and open a draft PR, as the pull request conventions state. In Related artifacts, link the intent, the spec, and each ADR.
12. Mark the PR as ready when it meets each condition of a ready PR. If the project has a `Stage gate` CI job, it fails until the spec is `Approved`, and the pull request conventions allow this failure in a ready PR. Tell the owner that the PR is ready, and ask them to review the spec and the ADRs.
13. If the owner asks for changes, edit the artifacts, commit, and push. Keep the status `Draft`. Then ask for a review again.
14. If the owner approves the spec in the chat or in a review of the PR, change the status to `Approved`. Commit and push the change. Tell the owner that the PR is ready to merge when CI passes.
15. Stop the skill. The owner merges the PR. The build stage starts from the approved spec after the merge.

## Split a change

If the owner approves a capability map in step 3, split the change before you write a spec:

1. Stop the design of the change.
2. Change the intent of the change in a new PR with the `intent` skill, as its [Changes to an approved intent](../intent/SKILL.md#changes-to-an-approved-intent) section states. Keep only the first change of the build order in it.
3. Write the intent of each other change of the map with the `intent` skill, with the change name from the map.
4. After each intent merges with the status `Approved`, run this skill again for that change, in the build order of the map.

## Changes to an approved spec

If the design of a change must change after its spec merged, and before the last PR of the change merged, change the spec in a new PR. Follow steps 5 to 15. In the new PR, change the status to `Draft` first, as the spec convention states. To change a decision, write a new ADR that supersedes the old ADR, as the ADR convention states.

After the last PR of the change merged, do not change its spec. Start a new change with the `intent` skill.

## Rules

- Write how to build the change. Do not repeat the problem, the outcome, or the success criteria of the intent. Link the intent instead.
- Do not list the files to change, the order of the work, or the names of tests in the spec. The plan of the build stage states them.
- Change the status to `Approved` only after the owner approves the spec. A reply such as "sounds good" or "whatever you think" is not an approval. Ask the owner whether they approve the spec.
- If another PR merges an ADR with the same number before this PR merges, give the ADRs of this PR the next free numbers, and update their links.
- Do not merge the PR. Only the owner merges it.
- Do not write the plan or the code of the change in this skill, also when the owner approves the spec.

## Verification

Before you commit the spec, make sure that each item is true:

- [ ] The file is `docs/specs/<change name>.md`, with the change name of the intent.
- [ ] The spec has each section of the template of the spec convention, in the template order. Decisions, Answers to the intent, and References are present only when they have content, as the spec convention states.
- [ ] The spec has at most 200 lines, blank lines included.
- [ ] The status is `Draft` until the owner approves the spec.
- [ ] Each success criterion of the intent has at least 1 requirement, and each requirement names its criterion ID and a test level.
- [ ] A requirement names each existing behavior that must not change.
- [ ] Each Design subsection states the contract of its part, and links the ADR of each decision that rejects options.
- [ ] Each rule in the Rules section names a deterministic check, or the follow-up task that adds it.
- [ ] Each open question of the intent has a row in Answers to the intent.
- [ ] No concern and no open question changes a requirement, a part, or a decision.
- [ ] The Answers table has 1 row for each question to the owner. Each reply states the meaning of the answer of the owner in English.
- [ ] Each ADR follows the ADR convention, has the status `Accepted`, and has a row in the Decisions section of the spec.
- [ ] `CONSTRAINTS.md` and `GLOSSARY.md` follow their conventions, if the PR changes them.
- [ ] Each source in References is a source that the spec uses, and the table states the parts that you read only in a summary.
