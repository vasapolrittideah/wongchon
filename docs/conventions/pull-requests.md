# Pull request conventions

This convention defines how to write a pull request (PR) and how to prepare it for review. The maintainer squash merges each PR, and the squash commit has only the PR title, so the PR description holds the details of the change.

## Template

A PR has a title, [Result](#result), [What changed](#what-changed), [Why](#why), [Breaking changes](#breaking-changes), [Verification](#verification), [Risks or limitations](#risks-or-limitations), [Follow-up tasks](#follow-up-tasks), [Related artifacts](#related-artifacts), [Related issues](#related-issues), and an attribution line.

```markdown
<PR title>

## Result

<lasting effect of the PR on main>

## What changed

- <change that a reviewer must know>

## Why

<problem and the reason for the change>

## Breaking changes

<what breaks and what users must change>

## Verification

- <check>: <result>

## Risks or limitations

<revert safety, security risks, or remaining limits>

## Follow-up tasks

- <remaining work>

## Related artifacts

- <link to an artifact>

## Related issues

<Issue line>

<attribution line, if any>
```

### Title

- Use only the subject line of the commit message [Template](commit-messages.md#template), with the same [Types](commit-messages.md#types) and scopes.
- Describe the result, not the branch or the changed files.
- Do not include a body or a footer.

### Result

- Write 1 paragraph of 1 to 3 sentences, without bullets or tables.
- State the lasting effect of the merged PR on `main`, for a later reader of `main`.
- Do not list the changes. List them in [What changed](#what-changed).
- Do not write `n/a`, because each PR has an effect on `main`.

### What changed

- List each change that a reviewer must know to review the PR. Use only bullets and tables, also when there is only 1 change. The `Reverts` line of a revert PR is the only exception.
- If the PR changes an existing value, such as a configuration value, a default, a limit, or an API field, show the value in a table, also when it is the only changed value. Give the table the columns `Value`, `Before`, and `After`, in this order, and name each changed value in the `Value` column.
- If the PR title has the `revert` type, start the section with `Reverts <full SHA>.`, and give the reason in [Why](#why). Write the SHA without backticks, so that GitHub links the reverted commit.
- Do not put a value that the PR adds or removes in the table, because its `Before` or `After` cell has no value. List the added or removed values in bullets.
- Do not list every changed file, because the diff shows them.
- Do not describe process history, such as a rebase or a method that did not work.

### Why

- State the problem that the PR solves and the reason for the chosen change.
- Do not repeat the content of an artifact. Link the artifact in [Related artifacts](#related-artifacts) instead.

### Breaking changes

- If the PR title has a breaking marker, state what breaks and the changes that users must make.
- State each other incompatible change, such as a renamed environment variable, and the changes that the affected people must make.
- If nothing breaks, write `n/a`.

### Verification

- Write 1 bullet for each check that the [Workflow](#workflow) rules require and for each other check that you ran, as `- <check>: <result>.` Write a command in backticks, and describe a manual check in words, such as "Each link in the changed files opens".
- Write the result as `passed`, `failed`, or `did not run`. If the output of the check gives a count or a short summary, add it in parentheses after the result, such as `passed (32/32 tests)` or `failed (2 files with trailing spaces)`. For a failure, state the cause. For a check that did not run, state the reason.
- Order the bullets by the source of the check:
  1. The checks that `AGENTS.md` lists.
  2. The verification commands of the related Issues.
  3. The other checks that you ran, such as a regression test or a check of the facts and links in changed documentation.
  4. The CI checks that failed and stay unresolved.
- Show the evidence for each unresolved failure with these steps:
  1. Before the PR opens, put the local output that shows the failure in a code block under its bullet, because no CI run exists for the PR.
  2. After the first CI run finishes, replace the output with a link to that run.
- If a CI check fails and the failure stays unresolved, add a bullet for it, and link the run.
- Do not write `n/a`, because each PR has at least the checks that the Workflow rules require.

### Risks or limitations

- If a revert of the PR is not safe, such as after a data migration, state why and what a revert needs.
- If the PR changes code or configuration that more than 1 part of the project uses, name the parts that a failure of the change affects.
- Write each security risk and remaining limit. Write each check result in [Verification](#verification), and each compatibility effect in [Breaking changes](#breaking-changes).
- When a limitation has follow-up work, describe the limitation and refer to [Follow-up tasks](#follow-up-tasks) instead of repeating the work.
- If there is nothing to report, write `n/a`.
- Do not paste routine logs.
- Do not describe failed attempts that the PR resolved.

### Follow-up tasks

- If the work has an open Issue, write `- #<Issue number>: <remaining work>.` If the work has no open Issue, write `- <remaining work>.`, such as `- Add the paths of the stage scopes to .wongchon/config.json.`
- Write 1 bullet for each piece of work for later, even when there is only 1.
- Write the remaining work as 1 sentence that names the work. GitHub shows only the number of an Issue, so the sentence must name the work.
- Put the bullets with an Issue first, in ascending Issue number. Then put the bullets without an Issue.
- Before you create an Issue for the work, follow these steps:
  1. Ask the maintainer.
  2. If the maintainer approves, create the Issue.
  3. If the maintainer does not approve it, or the session has no chat, write the work without an Issue number.
- If the PR leaves no work for later, write `n/a`.
- Do not put `Closes`, `Fixes`, or `Resolves` before the Issue number, because GitHub then closes the Issue when the PR merges.

### Related artifacts

- Write 1 bullet for each lifecycle artifact that the PR implements, changes, or depends on, such as an intent, a specification, or a plan.
- Use the path of the artifact in backticks as the link text.
- Order the bullets by the stage of the artifact, from the earliest stage to the latest.
- If no artifact is related, write `n/a`.

### Related issues

- Write 1 line for each Issue, and repeat the keyword on each line, because GitHub ignores an Issue that follows a comma. Put the lines without blank lines between them, and end each line with a period.
- Put the `Closes` lines before the `Refs` lines, and order each group by ascending Issue number.
- Write `Closes #<Issue number>.` for each Issue that the PR completes. GitHub closes the Issue after the PR merges into `main`.
- Write `Refs #<Issue number>.` for each Issue that stays open. An example is a PR that updates a specification before the implementation.
- If no Issue is related, write `n/a`.
- Do not use `Fixes`, although GitHub accepts it. Use `Closes` for consistency.
- Do not repeat a follow-up Issue.

### Attribution line

- If the agent harness gives an attribution line for PR descriptions, put it at the end of the description, after [Related issues](#related-issues).

## Rules

### Format and content

- Start the description from the [`.github/pull_request_template.md`](../../.github/pull_request_template.md) template, and complete every section.
- Delete the HTML comments of the template.
- Write [Result](#result) as the lasting record for a later reader of `main`. Write the other sections for the reviewer and the merge decision.
- If a section has content, replace its `n/a`.
- Do not copy CI output or measurements, such as test coverage, into the description. Link the CI run instead. The summary in a [Verification](#verification) result, such as `passed (32/32 tests)`, is not a measurement, because it states the result of 1 check.

### Workflow

- For a documentation-only change, make sure that the facts, examples, links, and formatting are correct. Tests of the application are unnecessary unless executable behavior changes.
- For a behavior fix, add a focused regression test.
- Keep changes that belong to another task out of your commits, and keep them in the working tree.
- Before each commit, inspect the staged diff. Exclude unrelated changes, secrets, local environment files, and unwanted build output.
- Before you open or update a PR, run the checks that `AGENTS.md` lists and each verification command of each related Issue. If a focused check proves behavior that these commands do not cover, also run it.
- Before you open or update a PR, inspect the complete PR diff with the same exclusions as for a commit.
- If the repository has CI, handle it after each push with these steps:
  1. Wait for the CI checks to finish.
  2. If the job log shows that a failure comes from the runner, the network, or an external service, such as a registry timeout, rerun the failed job 1 time.
  3. If it fails again, state the cause and link the run in [Verification](#verification).
  4. Fix every other failure in the PR.
- Do not weaken a command or hide a failure.

### Links and tracking

- Follow the [GitHub label](github-labels.md) conventions.
- In the description, do not link a file that the PR changes, because the diff shows it. Related artifacts is an exception, because the link records which artifact the change belongs to.
- Do not set an assignee or a reviewer, and do not add the PR to a GitHub Project.

### Status and approval

- Open the PR as a draft.
- After the PR meets each condition of a ready PR, run `gh pr ready`, and tell the maintainer that the PR is ready. A ready PR has a complete description and the correct labels, the checks of the [Workflow](#workflow) rules pass, and CI passes when the repository has CI.
- If the PR cannot become ready, keep it as a draft, and tell the maintainer which condition fails and why.
- If the session has a chat, tell the maintainer there. If the session has no chat, tell the maintainer in a PR comment.

### Changes

- When the work changes, update the title, the description, and the labels before you tell the maintainer that the PR is ready again.
- If a pushed commit needs a fix, add a new commit. Do not amend or rebase a pushed commit, and do not force-push.
- If the PR has merge conflicts or needs a change that is on `main`, merge `main` into the branch.
- After the PR merges, edit its description only to fix a wrong fact, because the description is the lasting record of the change.
- Apply a change of this convention to new PRs, and to open PRs when their description changes. Do not edit merged PRs to follow it.

## Examples

This title describes the result instead of the branch:

```text
Branch: fix/plan-hook-multiline
Title:  fix(build): keep multiline PR descriptions in the plan hook
```
