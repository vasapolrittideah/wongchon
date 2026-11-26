# Spec: build plans and tasks

Author: Vasapol Rittideah

Status: `Draft`

Intent: [`docs/intents/build-plans-and-tasks.md`](../intents/build-plans-and-tasks.md)

## Current state

The build stage has no convention and no skill. The agent wrote [`docs/plans/plugin-review-gate.md`](../plans/plugin-review-gate.md) and its Issues #32 to #39 by hand, in a milestone for the change and in the `wongchon` GitHub Project. [ADR-0014](../adrs/0014-start-small-changes-at-the-build-stage.md) waits for the checks of small changes, and [ADR-0029](../adrs/0029-self-review-with-a-self-reviewer-subagent.md) waits for the check of the tools of subagents. The stage gate of [ADR-0016](../adrs/0016-block-unapproved-artifacts-with-a-stage-gate.md) reads only intents and specs, `scripts/check_pr_metadata.py` does not read Follow-up tasks, and the [pull request](../conventions/pull-requests.md#follow-up-tasks) conventions tell the agent to ask before it creates an Issue.

The review gate of [`docs/specs/plugin-review-gate.md`](plugin-review-gate.md) blocks `git commit` with `2>&1`, because the command parser splits it into 2 commands and reads `2` as a path. `scripts/review.py` keeps only a count of the rounds of each role, as [ADR-0025](../adrs/0025-count-review-rounds-in-the-review-script.md) states, so a later round gets the whole diff again and no record of what changed since the last round. Both the writing reviewer and the artifact reviewer review each stage artifact, as [ADR-0023](../adrs/0023-choose-review-roles-from-fixed-paths.md) states. The writing reviewer reads the [English prose](../conventions/english-prose.md) and Markdown conventions, but not the convention of the artifact that it reviews.

## Requirements

| ID | Requirement | Criterion | Proof |
| --- | --- | --- | --- |
| R1 | Given a plan whose status is not `Approved`, when the `Stage gate` job runs on a PR that changes it, then the job fails and names the plan. | S5 | Unit test |
| R2 | Given a PR that changes an `Approved` plan, when the `Stage gate` job runs, then it runs the check of the Issues of the milestone of the plan. | S4 | Unit test |
| R3 | Given 2 open or closed Issues of 1 milestone whose Files sections share a path, when the check of the Issues runs, then it fails and names both Issues and the path, unless a chain of `Blocked by` links orders them. | S4 | Unit test with fake Issue data |
| R4 | Given an Issue of a milestone whose title has more than 72 characters, when the check of the Issues runs, then it fails and names the Issue. | S4 | Unit test |
| R5 | Given a plan with the Spec line `None` that has more than 1 task or links a milestone, when the `Stage gate` job runs, then it fails. | S6 | Unit test |
| R6 | Given a PR that changes `docs/adrs/**`, `ARCHITECTURE.md`, or `CONSTRAINTS.md`, when its Related artifacts section links no spec, then the `Stage gate` job fails. | S6 | Unit test |
| R7 | Given a bullet in Follow-up tasks that does not start with `#<number>: `, or Issue numbers out of ascending order, when the `PR metadata` job runs, then it fails and names the bullet. `n/a` passes. | S3 | Unit test |
| R8 | Given a file in `agents/` at the head of a PR whose `tools` field is missing or names a tool outside `Read`, `Grep`, `Glob`, `WebFetch`, and `WebSearch`, when the `Check changes` job runs, then it fails and names the file and the tool. | S7 | Unit test |
| R9 | Given a changed file in `agents/`, when the `Check changes` job runs, then it shows a warning for the file. | S7 | Unit test |
| R10 | Given `git commit` with `2>&1`, `> <file>`, `>> <file>`, or `2> <file>` and the stamps of its roles, when the review guard runs, then it allows the command. Given a pipe, `;`, `&&`, or `\|\|` after `git commit`, then it still blocks the command. | S8 | Unit test |
| R11 | Given a review that ends without an approval, when the same role reviews the same branch again, then the request holds the diff from the tree or the PR text of the last round to the current one, and the findings and replies of the last round. | S10 | Unit test with a fake reviewer command |
| R12 | Given a later round, when a role finds a new problem in text outside the diff since the last round, then it reports the problem as `Nit`, except a bug in code that loses data, opens a security hole, or crashes the program. | S10 | Manual check of the review rounds of this change |
| R13 | Given a staged stage artifact, when the writing reviewer reviews it, then it reads the convention of the artifact and reports no finding whose fix breaks that convention. | S9 | Manual check of the review rounds of this change |
| R14 | Given the follow-up tasks of the PRs that merged before this change, when the sweep ends, then each one has an Issue or a reason to close it in a table that the maintainer approved. | S2 | Manual check by the maintainer |
| R15 | Given the change `plugin-skeleton-and-setup`, when its last PR merges, then its plan came from the `plan` skill and each of its Issues from the `build` skill, without an edit of the skills or conventions of this change. | S1 | Manual check by the maintainer |
| R16 | Given the last PR of this change, when it merges, then the maintainer checks R13 of the spec of `plugin-review-gate` for each commit and each PR of this change. | S9 | Manual check by the maintainer |
| R17 | Given the existing tests, the commands that the Git guard and the review guard block, and the protected jobs, when this change merges, then each one keeps working, and a review of 1 round still gets no diff since a last round. | S8 | Unit test and CI |

## Design

### Plan convention

`docs/conventions/plans.md` defines `docs/plans/<change name>.md`, with the format of the plan of `plugin-review-gate`: a title `# Plan: <name>`, an Author line, a Status line of `Draft` or `Approved`, a Spec line, Tasks, Checkpoints, Risks with the columns Risk and Mitigation, and Open questions. Tasks starts with 1 sentence that names the Project and, for a change with a spec, the milestone. It then lists 1 numbered link for each Issue in the order of the build. While the plan PR is a draft, each task is written in full, with the sections of an Issue, and the Issues replace them before the owner approves the plan. A small change has the Spec line `None` and 1 task, and the change has its plan and its code in 1 PR. The Template section of the convention is the plan template. Tracking stays in GitHub for version 1, as [ADR-0038](../adrs/0038-give-a-milestone-only-to-a-change-with-a-spec.md) states.

### GitHub Issue convention

`docs/conventions/github-issues.md` defines Issues, milestones, the Project, and `Blocked by` links.

| Part | Contract |
| --- | --- |
| Title | At most 72 characters. It names the change that the task makes and the thing that it changes, such as `Add the check of plan Issues`, so a reader understands it without the body. |
| Task Issue body | A `Plan:` line with the link of the plan on `main`, then Result, Requirements, Files, Proof, and Owner action. Files lists 1 path in backticks in each bullet, with ` (new)` after a path that the task creates. Proof is a checklist that ends with "Review the CI results on the PR." |
| Follow-up Issue body | A `Source:` line with the link of the PR, then Result and Why. It has no milestone, as [ADR-0031](../adrs/0031-make-each-follow-up-task-an-issue-without-a-milestone.md) states. |
| Labels | The labels of the PR of the task, as the GitHub label conventions state |
| Milestone | 1 for each change with a spec, named after the change, with the link of the plan on `main` as its description. The Issue of a small change has no milestone, as [ADR-0038](../adrs/0038-give-a-milestone-only-to-a-change-with-a-spec.md) states. |
| Order | `Blocked by` links of GitHub only, from each Issue that shares a file with an earlier Issue |
| Project | Each Issue joins the Project of `github.project` in `.wongchon/config.json`, with the statuses `Todo`, `In Progress`, and `Done`. Without that key, the skills skip the Project. |

### Configuration

`.wongchon/config.json` gets an optional `github.project` object with `owner` and `number`, the owner of the Project and its number. This repository sets `vasapolrittideah` and `5`.

### Plan skill

`skills/plan/SKILL.md` writes the plan from the approved spec, or from the request of the owner for a small change. It splits the work with `planning-and-task-breakdown`, opens the draft PR, and creates the milestone, the Issues, their `Blocked by` links, and their Project items after the owner agrees with the tasks. It runs `scripts/check_plan_issues.py <milestone>` before the status becomes `Approved`, and stops at the gate.

### Build skill

`skills/build/SKILL.md` has the 2 modes of [ADR-0032](../adrs/0032-build-1-issue-at-a-time-in-single-or-chain-mode.md). Single mode builds 1 Issue and stops, in these steps:

1. Take the first Issue in the order of the plan that is open and whose blockers are closed.
2. Run the check of the Issues.
3. Create the branch, and move the Project item to `In Progress`.
4. Build with `incremental-implementation` and `test-driven-development`, and pass the review gate.
5. Open the PR with `Closes #<number>`, and mark it ready after CI passes.
6. Check the checkpoint of the plan that comes after the task, if the plan has one.

Chain mode repeats single mode after the owner merges each PR, until the milestone has no open Issue. It never opens a PR on top of an unmerged PR.

### Copied skills

This change copies 3 skills of agent-skills at version 0.6.17, as `skills/THIRD_PARTY.md` states:

| Skill | Rewrite |
| --- | --- |
| `planning-and-task-breakdown` | Write the plan and the Issues in the format of the plan and GitHub Issue conventions. Remove its plan template and its `tasks/` files, and keep its vertical slices, task sizes, and order. |
| `incremental-implementation` | Keep each slice inside 1 Issue, make a checkpoint commit after each tested slice, and pass the review gate before each commit. |
| `test-driven-development` | Keep the cycle of red, green, and refactor. Add the choice of a test level and the Prove-It pattern of `test-engineer`. Remove the browser testing, which the verify phase adds. |

### Follow-up tasks

The pull request conventions change Follow-up tasks: each bullet is `- #<number>: <remaining work>.`, and the agent creates the follow-up Issue without asking the maintainer first. A step of the next stage, such as the spec after an intent, is not a follow-up task. `scripts/check_pr_metadata.py` checks only the form and the order of the bullets, not the Issues.

At the start of each change, the `intent` skill lists the open Issues without a milestone that have the area label of the scope of the change, with `gh issue list`. The owner decides each one: join the change, wait, or close it with `gh issue close --comment <reason>`. The `plan` skill gives each joined Issue the milestone of the change, and the Answers table of the intent records each decision.

### Check of plan Issues

`python3 scripts/check_plan_issues.py <milestone>` reads each Issue of the milestone and its `Blocked by` links with `gh api`. It fails for each pair of Issues that share a path of Files without a chain of `Blocked by` links between them, and for each title longer than 72 characters. It exits with `0` for a pass, `1` for a failure, and `2` when it cannot read the Issues, as [ADR-0033](../adrs/0033-check-the-order-of-plan-issues-in-skills-and-the-stage-gate.md) states.

### Stage gate

`scripts/check_stage_gate.py` reads `docs/plans/` with intents and specs. For each changed plan that is `Approved`, it runs the check of the plan Issues on the milestone of the plan. For a plan with the Spec line `None`, it fails when the plan has more than 1 task or links a milestone. It takes the PR body from `PR_BODY`, and fails when the PR changes `docs/adrs/**`, `ARCHITECTURE.md`, or `CONSTRAINTS.md` and Related artifacts links no spec, as [ADR-0034](../adrs/0034-detect-a-small-change-from-its-plan-and-its-related-artifacts.md) states. The `Stage gate` job gets `issues: read`, `GH_TOKEN`, and `PR_BODY`.

### Check changes

`scripts/check_changes.py` adds `agents/` to the paths that it warns about. It reads each file of `agents/` at the head of the PR, and fails when the `tools` field is missing or names a tool outside the allowlist of R8, as [ADR-0035](../adrs/0035-check-the-tools-of-subagents-with-an-allowlist.md) states.

### Review guard

`hooks/review_guard.py` treats a redirection after `git commit` as part of the command, not as a second command or a path: `2>&1`, `>` or `2>` with a file, and `>>` with a file. A pipe or a command list operator after `git commit` still blocks the commit.

### Review rounds

When a review ends without an approval, `scripts/review.py` saves its tree, or its PR text, next to the count of rounds. The next round adds the diff from that tree or text to the current one, after the findings and replies of the last round. An approval or `--reset-rounds` deletes the saved tree or text with the count. Each role file states the rule of R12, and the agent fixes each `Nit` of a later round or creates a follow-up Issue for it, as [ADR-0036](../adrs/0036-show-a-review-role-the-changes-since-its-last-round.md) states.

### Writing reviewer

`reviewers/writing-reviewer.md` reads the convention of each staged artifact that has one, such as an intent, a spec, a plan, an ADR, or a convention file. It applies the order of rules of the English prose conventions, in which the convention of the artifact comes first, as [ADR-0037](../adrs/0037-make-the-writing-reviewer-apply-the-convention-of-each-artifact.md) states.

## Rules

| Rule | Check |
| --- | --- |
| Each follow-up task of a PR has an Issue number. | The `PR metadata` CI job |
| Issues of 1 milestone that share a file have an order of `Blocked by` links, and each Issue title has at most 72 characters. | `scripts/check_plan_issues.py`, in the `plan` and `build` skills and the `Stage gate` CI job |
| A small change has 1 task, and only a PR that links a spec changes an ADR, `ARCHITECTURE.md`, or `CONSTRAINTS.md`. | The `Stage gate` CI job |
| Each subagent in `agents/` has only read-only tools. | The `Check changes` CI job |

## Boundaries

- Ask first: Close a follow-up Issue that the maintainer did not approve to close.
- Never: Change the limit of 3 review rounds in this change.

## Decisions

| Decision | ADR |
| --- | --- |
| Superseded by ADR-0038. | [ADR-0030](../adrs/0030-track-tasks-as-github-issues-in-a-milestone.md) |
| Each follow-up task is an Issue without a milestone, which the agent creates. | [ADR-0031](../adrs/0031-make-each-follow-up-task-an-issue-without-a-milestone.md) |
| The `build` skill builds 1 Issue at a time, in single or chain mode. | [ADR-0032](../adrs/0032-build-1-issue-at-a-time-in-single-or-chain-mode.md) |
| A script checks the order of the Issues of a plan in the skills and in the `Stage gate` job. | [ADR-0033](../adrs/0033-check-the-order-of-plan-issues-in-skills-and-the-stage-gate.md) |
| A small change is a plan with the Spec line `None`, and a PR that changes an ADR links a spec. | [ADR-0034](../adrs/0034-detect-a-small-change-from-its-plan-and-its-related-artifacts.md) |
| `Check changes` checks the tools of each subagent against an allowlist. | [ADR-0035](../adrs/0035-check-the-tools-of-subagents-with-an-allowlist.md) |
| A later review round gets the diff since the last round, and a new problem outside that diff is a `Nit`, except a bug that loses data, opens a security hole, or crashes the program. | [ADR-0036](../adrs/0036-show-a-review-role-the-changes-since-its-last-round.md) |
| The writing reviewer applies the convention of each artifact that it reviews. | [ADR-0037](../adrs/0037-make-the-writing-reviewer-apply-the-convention-of-each-artifact.md) |
| Version 1 tracks the tasks of a plan as GitHub Issues, with a milestone only for a change with a spec. | [ADR-0038](../adrs/0038-give-a-milestone-only-to-a-change-with-a-spec.md) |

## Concerns

| Concern | Resolution |
| --- | --- |
| A later round can miss a real problem in prose or format that the first round did not report. | The maintainer accepts it. The first round can block on each line, and the agent fixes or files each later `Nit`. |
| An edit of an Issue after its plan merged does not run the `Stage gate` job again. | The maintainer accepts it, because the `build` skill runs the check before each Issue. |

## Assumptions and open questions

- `gh issue list --milestone` and the `blocked_by` endpoint work with the `GITHUB_TOKEN` of a `pull_request_target` job that has `issues: read`. The PR that changes the `Stage gate` job proves it.
- The verify phase measures how often a role needs a reset of its rounds, and then decides the limit of rounds.

## Answers to the intent

| Open question of the intent | Answer |
| --- | --- |
| Does the check of `Blocked by` links run in CI, which then needs to read Issues, or only in the plan and build skills? | Both. The skills run it before the approval of a plan and before each Issue, and the `Stage gate` job runs it for each changed `Approved` plan. |
| How does a check know that a PR belongs to a change without an intent? | Its plan has the Spec line `None`. Also, a PR that changes an ADR, `ARCHITECTURE.md`, or `CONSTRAINTS.md` must link a spec. |

## Answers

| Question | Reply |
| --- | --- |
| Does the change split into several changes? | No. It stays 1 change with several PRs. |
| What does a plan hold? | The format of the plan of `plugin-review-gate`: short, with links to Issues that hold the details. Draft tasks are written in full until the Issues exist. |
| How are the Issue convention, follow-up Issues, and the Project arranged? | 1 file, `docs/conventions/github-issues.md`, for Issues, milestones, the Project, and `Blocked by`. A follow-up Issue has no milestone, an area label, and a `Source:` line. The Project is optional, with its owner and number in `.wongchon/config.json`. Other trackers, such as Jira or GitLab, come after version 1. |
| Where does the check of `Blocked by` links run? | In the `plan` and `build` skills and in the `Stage gate` job. |
| How does a check find a small change? | From a plan with the Spec line `None`, and from a PR that changes an ADR, `ARCHITECTURE.md`, or `CONSTRAINTS.md` without a link to a spec. |
| How does a later review round block only on changed text? | The script saves the tree or text of each failed round and sends the diff since then, and each role file states the rule. A bug in code that loses data, opens a security hole, or crashes the program still blocks. The limit stays at 3 rounds. |
| How do the writing reviewer and the artifact reviewer stop conflicting? | The writing reviewer reads the convention of each artifact and follows the existing order of rules, and the change of its role file goes with the change of review rounds. |
| Where does the check of the tools of subagents run? | In the `Check changes` job, with an allowlist of read-only tools. |
| What counts as a follow-up task, and what does the check read? | Only work that no plan or Issue holds. The check reads only the form `#<number>: ` and the order of the bullets. |
| What do the `plan` and `build` skills and the 3 copied skills do? | As the Plan skill, Build skill, and Copied skills parts state. Chain mode waits for each merge before the next Issue. |
| How are `2>&1`, Issue titles, the triage, the configuration, and the glossary handled? | Redirections pass and pipes and lists still block, the check of the Issues checks the length of each title, the `intent` skill triages open follow-up Issues of its area, the Project is in `github.project`, and the glossary gets the new terms. |
| Does a small change need a milestone? | No. A milestone shows the progress of a change across its tasks, and a milestone with 1 Issue shows only the state of that Issue. Each small change would add 1 more milestone. The `Stage gate` job fails on the plan of a small change that links a milestone. |

## References

| Source | What this spec takes from it | Parts read only in a summary |
| --- | --- | --- |
| [The AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) | 1 system as the source of truth for tasks, and tasks that share files run one after another | The whole article, which the fetch tool returned as a summary with short quotes |
| [Issue dependencies](https://docs.github.com/en/rest/issues/issue-dependencies) and [Creating issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies) | The `blocked_by` endpoints, the `gh` options for `Blocked by` links, and the limit of 50 links | The limit of 50 links, which only the changelog of August 21, 2025 states |
| [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) | A later round reviews only the changed lines and does not repeat a finding | The whole article, which the fetch tool returned as a summary with short quotes |
