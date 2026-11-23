# Intent: build plans and tasks

Author: Vasapol Rittideah

Status: `Approved`

## Problem

The build stage of `wongchon` has no convention and no skill. The agent wrote the plan of the `plugin-review-gate` change by hand, and no check read the plan or its Issues. The build showed only then that 2 tasks changed the same file with no order between them. The follow-up tasks of merged pull requests (PRs) are bullets without an Issue, 54 bullets in 25 PRs on November 23, 2026, so nobody tracks them. Several checks that the decisions of the [Roadmap](../../ROADMAP.md) promise do not exist yet: the checks of small changes, the stage gate for plans, and the check that a subagent cannot write. The review guard also blocks a `git commit` whose output goes to a file or a pipe with `2>&1`, although the commit has its approvals. A review role also finds new problems in text that did not change since its last round, so a role often uses its 3 rounds on findings that it could have given in the first round.

The next change, `plugin-skeleton-and-setup`, needs a plan and a build. This change also gives the evidence for the first success criterion (S1) of the intent of `plugin-review-gate`.

## Outcome

- A plan convention and a plan template state how a plan of a change looks.
- A plan skill writes the plan of a change from its approved spec. It creates 1 Issue for each task in the milestone of the change, and it records the order of the tasks as `Blocked by` links. The title of each Issue has at most 72 characters, and it names the change and the thing that the task changes.
- A build skill builds 1 Issue, or several Issues one after another in their order, up to the PR of each Issue.
- The skills of agent-skills that the plan and build skills use, `planning-and-task-breakdown`, `incremental-implementation`, and `test-driven-development`, are copied and rewritten for the stages of `wongchon`.
- Each follow-up task of a PR is an Issue, which the agent creates without asking the maintainer first.
- At the start of each change, the intent skill lists the open follow-up Issues of its area. The owner of the change decides for each one: join the change, wait, or close it with a reason.
- The follow-up tasks of the merged PRs become Issues, or close with a reason, after the maintainer approves 1 table of all of them.
- From the second round of a review, a review role blocks a change only for the text that changed since the last round and for the findings of the last round that are not fixed. A new finding on unchanged text does not block.
- Checks enforce the rules of the build stage and the rules that earlier decisions promise, as the success criteria state.

## Success criteria

- S1: The change `plugin-skeleton-and-setup` writes its plan with the plan skill and builds each of its Issues with the build skill. No PR of that change edits the plan convention, the plan and build skills, or the 3 copied skills to make them work.
- S2: Each follow-up task of each PR that merged before this change has an Issue or a reason to close it, and the maintainer approved each one.
- S3: The check of the PR metadata fails on a PR with a follow-up task that has no Issue number.
- S4: A check fails when 2 Issues of 1 milestone change or create the same file and no `Blocked by` link orders them.
- S5: The stage gate fails on a PR that changes a plan whose status is not `Approved`.
- S6: A check fails on a change that has no intent and either has a plan with more than 1 task or has a PR that changes an ADR, `ARCHITECTURE.md`, or `CONSTRAINTS.md`.
- S7: A check fails when a subagent of the plugin has a tool that can write.
- S8: The review guard allows a `git commit` with `2>&1` when the commit has the approvals of its review roles.
- S9: When the last PR of this change merges, the maintainer checks requirement 13 of the spec of `plugin-review-gate`. Each commit and each PR of this change had the approvals of its roles, and the maintainer wrote no review comment that a role should have found.
- S10: In the second or a later round, a review role reports a new problem in text that did not change since the last round as a finding that does not block.

## Affected users and systems

- The maintainer approves 1 table of the old follow-up tasks, reviews the plan of each change, and decides the open follow-up Issues at the start of each change.
- This repository gets the plan convention and template, the plan and build skills, the 3 copied skills, the Issues of the follow-up tasks, and the new checks.
- The review roles of this repository block in a later round only for changed text and unfixed findings.
- Each project that installs the plugin later gets the plan and build skills and the checks of the build stage with the plugin.

## Constraints

- The review time of the maintainer is the main limit, as the [Version 1](../../ROADMAP.md#version-1) section of the roadmap states.
- Follow the Scripts and hooks, Protected checks, and Small changes decisions in the [Decisions](../../ROADMAP.md#decisions) section of the roadmap, and [ADR-0014](../adrs/0014-start-small-changes-at-the-build-stage.md).
- The agent does not change the settings or rulesets of the repository.
- Write each rule, convention, and skill so that it works in a project of any stack.

## Out of scope

- Build modes that run several Issues at the same time, which come after version 1
- The plugin layout, the setup command, the license files, the other 4 skills of the build phase, Vale, markdownlint, and the check of new code comments, which come in the change `plugin-skeleton-and-setup`
- The evidence of a change and the verify skill, which come in the verify phase

## Open questions

The design stage decides these questions:

- Does the check of `Blocked by` links run in CI, which then needs to read Issues, or only in the plan and build skills?
- How does a check know that a PR belongs to a change without an intent?

## Answers

| Question | Reply |
| --- | --- |
| Which change of phase 5 comes first? | `build-plans-and-tasks`, because the spec of `plugin-review-gate` names it as the next change, and `plugin-skeleton-and-setup` can then use the plan convention and the plan and build skills. |
| What result shows that the build stage works? | The change `plugin-skeleton-and-setup` writes its plan with the plan skill and builds each Issue with the build skill, and nobody edits these skills or the plan convention to make them work. Each follow-up task has an Issue. |
| Which skills of agent-skills does this change copy? | `planning-and-task-breakdown`, `incremental-implementation`, and `test-driven-development`, because the plan and build skills use them. The other 4 skills of the build phase stay in `plugin-skeleton-and-setup`, and the roadmap changes to match. |
| How are the old follow-up tasks decided? | The agent proposes 1 table of all of them, with an Issue title or a reason to close for each one, and the maintainer approves the table once and corrects the rows that they do not agree with. The agent creates each new follow-up Issue without asking the maintainer first, and the pull request conventions change to match. |
| How many Issues does the build skill build at the same time? | 1 Issue, or several Issues one after another in 1 session. Parallel modes come after version 1, because each parallel PR adds review time. The check of `Blocked by` links stays in this change, because the order of the Issues matters in a sequence too. |
| Does the limit of 3 review rounds change? | No. The maintainer often reset the count after 3 rounds, and the next round then approved. The cause is new findings on unchanged text in later rounds, so from the second round a role blocks only for changed text and unfixed findings. A higher limit would hide this cause. |

## References

| Source | What this intent takes from it | Parts read only in a summary |
| --- | --- | --- |
| [The AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) | Nothing is built without an accepted plan, tasks split by the files that they touch, and tasks that share files run one after another | The whole article, which the fetch tool returned as a summary with short quotes |
| [Issue dependencies](https://docs.github.com/en/rest/issues/issue-dependencies) of the GitHub REST API | Issues can record `Blocked by` links that a script can read | None |
| [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) | After the first round, a reviewer reviews only the changed lines and does not repeat a finding | The whole article, which the fetch tool returned as a summary with short quotes |
