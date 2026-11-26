# Plan: backticks in commit messages

Author: Vasapol Rittideah

Status: `Approved`

Spec: None

## Tasks

Tasks are tracked in the [wongchon](https://github.com/users/vasapolrittideah/projects/5) GitHub Project. This small change is 1 task and 1 PR. The PR holds this plan and its code. The Issue states its result, files, proof, and owner action.

1. [#71 Allow backticks in commit messages and PR titles](https://github.com/vasapolrittideah/wongchon/issues/71)

## Risks

| Risk | Mitigation |
| --- | --- |
| The `Stage gate` job does not check plans and small changes until #60 merges. | The maintainer checks the status of this plan and the rules of small changes in the review of the PR. |
| The `PR metadata` job runs the script of `main`, so the title of this PR cannot have backticks. | The PR title stays plain text. The next PR after the merge uses backticks. |
