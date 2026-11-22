# Intent: design documents and ADRs

Author: Vasapol Rittideah

Status: `Approved`

## Problem

The maintainer can take a change through the intent stage of `wongchon`, but the change cannot go further. Nothing tells an agent how to write the design of a change from its approved intent, so each design is written by hand without a fixed format. Nothing blocks the merge of a design that the owner did not approve.

The next phase of the [Roadmap](../../ROADMAP.md), the agent workflow phase, starts with the design of its own change. The design stage must work before that phase starts.

## Outcome

- An agent writes the design of a change from its approved intent, in a fixed format, and the owner approves the design when they merge its pull request (PR).
- The design records each decision that rejects options in its own architecture decision record (ADR). An ADR is a short file that states 1 decision, its context, and the rejected options.
- The decisions of this repository that have rejected options move from the roadmap into ADRs, and the roadmap links them.
- The design stage writes and updates the project documents for the quality bar and the terms of a project, in a fixed format.
- A CI check blocks the merge of a design that the owner did not approve.
- The design stage uses the skills of agent-skills that the roadmap gives to the design phase, rewritten for the stages of `wongchon`.

## Success criteria

- An agent writes the design of the agent workflow change with the design skill, and the maintainer approves it without an edit to a skill or a convention of the plugin during that change.
- Each design has at most 200 lines.
- The CI check fails on a PR that changes a design whose status is not `Approved`, and passes after the status changes to `Approved`.

## Affected users and systems

- The maintainer reviews and approves each design and each ADR at the gate of the design stage.
- This repository gets the conventions, skills, ADRs, and CI check of the design stage.
- Each project that installs the plugin later gets the conventions and skills of the design stage with the plugin.

## Constraints

- The review time of the maintainer is the main limit, as the Version 1 section of the roadmap states. Each design must be short enough to review in 1 sitting.
- Write the CI check in Python 3.9 or later, with the standard library only, as the Scripts and hooks decision of the roadmap states.
- Write each convention so that it works in a project of any stack.
- Follow the Principles and Decisions sections of the roadmap. They fix, for example, `CONSTRAINTS.md` and `GLOSSARY.md` as the project documents for the quality bar and the terms, and the skills of agent-skills for the design phase.

## Out of scope

- Review roles that check a design or an ADR before the maintainer reads it. They come in the agent workflow change, because they need its review script, approval stamps, and hook.
- The layout of the plugin and the setup command, which come in the build phase
- The check of the rule for small changes, which comes in the build phase, because it reads plans
- `ARCHITECTURE.md` of this repository, which the build phase writes after the plugin layout exists
- Brownfield projects, which come after version 1

## Answers

| Question | Reply |
| --- | --- |
| What result shows that the design stage works? | The design of the next change, the agent workflow change, is written with the design skill instead of by hand, and the maintainer approves it without an edit to a skill or a convention during that change. |
| Which work does this change include? | All 7 parts: the design convention, the ADR convention, the move of the roadmap decisions into ADRs, the conventions of `CONSTRAINTS.md` and `GLOSSARY.md`, the CI check that blocks a design without approval, the rewritten skills of agent-skills, and the design skill. |
| How long can a design be so that the maintainer can review it fast? | At most 200 lines. |
| Do review roles for designs and ADRs belong to this change? | No. They come in the agent workflow change. The layout of the plugin, the setup command, the check of small changes, `ARCHITECTURE.md`, and brownfield support also stay out, in their own phases. |

## References

| Source | What this intent takes from it | Parts read only in a summary |
| --- | --- | --- |
| [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) by Malte Ubl | A short design of 1 to 3 pages for a small change, which led to the question about the length of a design | None |
