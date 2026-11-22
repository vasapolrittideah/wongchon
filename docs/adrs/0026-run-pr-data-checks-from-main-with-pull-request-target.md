# ADR-0026: Run the checks of PR data from main with pull_request_target

Status: `Accepted`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Context

A `pull_request` workflow runs from the branch of the PR, so a PR can change the CI that checks it. This repository is a public repository of a user, not of an organization, and the agent uses the token of the maintainer. Required checks match only the job name, not the workflow or the event.

## Decision

A workflow on `pull_request_target` runs `PR metadata`, `Stage gate`, and a new `Check changes` job. It checks out the default branch, has only `contents: read` and no secrets, and reads the files of the PR as data without running them. `Check changes` warns about each changed file of the CI workflows, the scripts, the hooks, the role files, and `.claude/settings.json`. It fails when a workflow of the PR defines a job with a protected name. The maintainer allows `pull_request_target` in the Actions event policy before the PR that adds the workflow.

## Rejected options

| Option | Reason |
| --- | --- |
| Required workflows in a ruleset | Only organizations and enterprises can set them. |
| Required review of code owners for the workflows | The maintainer is the only owner and cannot approve their own PR, and the agent can use the same bypass. |
| A push ruleset that restricts file paths | It exists only for private and internal repositories. |
| A check that fails until the maintainer adds a label | The build phase changes scripts and hooks in most PRs, so it costs review time on each PR. |

## Consequences

- The tests that run the code of the PR stay on `pull_request`, and a PR can still change them.
- A PR that changes a protected check gets the result of the old check until it merges.
- The PR that moves the jobs needs 2 steps: add the new workflow, and then remove the old jobs from `ci.yml`.

## Confirmation

The `Check changes` job checks the protected job names on each PR, and the `Protect main` ruleset requires it.
