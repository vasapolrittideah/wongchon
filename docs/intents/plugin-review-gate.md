# Intent: plugin review gate

Author: Vasapol Rittideah

Status: `Draft`

## Problem

The review of each commit and each pull request (PR) of `wongchon` depends on the report of the main agent. Nothing makes the agent run a review, and nothing stops the agent from writing the prompt of its own reviewer, skipping the reviewer, or reporting a verdict that the reviewer did not give. The maintainer then finds problems in the prose, the code comments, and the format of artifacts that a reviewer could find first. Also, a PR can change the CI checks that check it, which breaks the principle "A change cannot edit its own checks" of the [Roadmap](../../ROADMAP.md).

The build phase of the roadmap writes the code of the plugin. The review gate must work before that phase starts, so that it checks that code.

## Outcome

- 3 review roles check each change before the maintainer reads it: a code reviewer, a writing reviewer, and an artifact reviewer. The code reviewer checks the code, its comments, and changes that lower the quality bar. The writing reviewer checks prose and Markdown. The artifact reviewer checks intents, specs, ADRs, `CONSTRAINTS.md`, and `GLOSSARY.md` against their conventions.
- Each review role runs apart from the main agent, from the prompt of the role and the staged change, so that the main agent cannot change either one. A role that approves the change leaves an approval for that exact content.
- A commit or a PR without the approvals of its roles is blocked.
- After 3 review rounds without an approval, the agent stops and asks the maintainer.
- The agent gives research to a read-only subagent, and it can ask a read-only subagent for a self-review that only gives advice.
- A PR cannot change the result of the checks of the PR metadata and of the stage gate on itself. A PR that changes the CI workflows, the check scripts, or the hooks shows this on the PR.
- The agent workflow uses the skills of agent-skills that the roadmap gives to this phase, rewritten for the stages of `wongchon`.

## Success criteria

- S1: In the next change, `build-plans-and-tasks`, each commit and each PR of the plugin has the approvals of its review roles, and the maintainer writes no review comment about prose, code comments, or the format of an artifact that a role should have found.
- S2: A commit or a PR is blocked when the approval of a required role for its current content is missing, and also when the check cannot read the content or the approvals.
- S3: When a role does not approve a change after 3 rounds, the agent stops and asks the maintainer instead of a fourth round.
- S4: A PR that edits the check of the PR metadata or of the stage gate gets the result of the check from `main`, not from its own edit.
- S5: A PR that changes the CI workflows, the check scripts, or the hooks shows a check result on the PR that names the changed files.
- S6: A review role cannot edit a file of the project or write its own approval.

## Affected users and systems

- The maintainer reads fewer problems in each review, and sets the Actions event policy of the repository once.
- This repository gets the review roles, the review command, the approvals, the block of commits and PRs, the protected CI checks, the research subagent, and the rewritten skills.
- Each project that installs the plugin later gets the review roles, the review command, and the block of commits and PRs with the plugin.

## Constraints

- The review time of the maintainer is the main limit, as the Version 1 section of the roadmap states. A higher use of tokens is acceptable when it saves review time.
- The review roles run with the Claude Code subscription login of the maintainer. The change needs no API key and no other paid service.
- The block catches mistakes, such as a forgotten review or a review of other content. It does not need to stop a deliberate bypass, as the Git guardrails decision of the roadmap states. When the check cannot decide, it blocks.
- The agent does not change the settings or rulesets of the repository. The maintainer allows the `pull_request_target` event of GitHub Actions in the Actions event policy of the repository before December 2, 2026, when GitHub blocks it by default in public repositories.
- Write scripts and hooks in Python 3.9 or later, with the standard library only, as the Scripts and hooks decision of the roadmap states.
- Write each role, convention, and skill so that it works in a project of any stack.

## Out of scope

- Vale, markdownlint, and the check of new code comments in each diff, which come in the build phase
- Review roles for tests, security, and performance, and evals of the review roles, which come in the verify phase
- A separate GitHub identity for the agent, which comes after version 1
- Protection of the tests that run the code of the PR itself, because a check that runs the code of a PR cannot come from `main` alone
- The plan convention and the build skills, which come in the build phase

## Open questions

The design stage decides these questions:

- Does the review use a second pass that confirms each finding, and severity tags such as Important, Nit, and Pre-existing, as the code review article of the Claude Code team describes?
- How does a review role run without the hooks and plugins of the project, when the subscription login rules out the bare mode of Claude Code?
- Can a job of the PR with the same name as a protected check make that check pass?

## Answers

| Question | Reply |
| --- | --- |
| What result shows that the review gate works? | The next change, `build-plans-and-tasks`: each of its commits and PRs passes the approvals of the code reviewer and the writing reviewer, the block works, and the maintainer has no review comment that a role should have found. |
| Must the block stop only mistakes, or also a deliberate bypass? | Only mistakes, but it fails closed: when it cannot read the content or the approvals, it blocks. |
| Does the protection against a PR that edits its own checks belong to this change, and what result is enough? | Yes. The checks of the PR metadata and of the stage gate run from `main`, and a PR that changes the CI workflows, the check scripts, or the hooks shows it. The maintainer sets the Actions event policy that allows `pull_request_target`. |
| Do the review roles use the subscription login or an API key? | The subscription login. The change uses no API key. |
| Which review roles does this change add? | 3 roles: a code reviewer for correctness, code comments, and a lowered quality bar; a writing reviewer for prose and Markdown; and an artifact reviewer for intents, specs, ADRs, `CONSTRAINTS.md`, and `GLOSSARY.md`. Roles for tests, security, and performance come in the verify phase. |

## References

| Source | What this intent takes from it | Parts read only in a summary |
| --- | --- | --- |
| [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) by Addy Osmani, Morgan Westlee Lunt, and Qing Wang | An approval covers 1 exact version of a change, a reviewer stops after 3 rounds, and the second pass and the severity tags of the open questions | The whole article, which the fetch tool returned as a summary with short quotes |
| [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) | The bare mode skips hooks and plugins but needs an API key, which leads to the second open question | The parts other than the bare mode and the permission modes |
| [Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) | A `pull_request_target` workflow runs from the default branch, and GitHub blocks it by default in public repositories from December 2, 2026 | None |
