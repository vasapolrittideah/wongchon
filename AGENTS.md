# Repository instructions

Follow these repository instructions for every task. Before you make a change, read the matching convention in the [Conventions](#conventions) table.

## Project

This repository holds `ai-dlc`, a Claude Code plugin that runs an AI-native software development lifecycle in projects of any stack. The lifecycle has 6 stages: intent, design, build, verify, deploy, and maintain. Version 1 covers the stages from intent to verify.

- Keep this file free of rules that only 1 agent can follow. Version 1 supports only Claude Code, but other agents will read this file later.
- Write scripts and hooks in Python 3.9 or later, with the standard library only.
- Write each convention in `docs/conventions/` so that it makes sense in any project. The plugin ships these files, and its skills read them in other projects.
- When you add or update a third-party skill, follow the rules in `skills/THIRD_PARTY.md`.

## Language

- Talk with the maintainer in Thai.
- Write every file in the repository in English.

## Delivery authority

- Prepare and test changes on a branch, and then submit them for review through a pull request (PR).
- The maintainer reviews and squash merges each PR.
- Do not push directly to `main`, merge a PR, enable auto-merge, or force-push.
- Do not change rulesets, branch protection, or the settings of the repository, and do not skip Git hooks with `--no-verify`.
- In Claude Code, the [`hooks/git_guard.py`](hooks/git_guard.py) hook blocks the commands that break these rules. The hook finds mistakes, but it does not stop a deliberate bypass, such as a command in a script file. Follow these rules also when no hook runs.

## Git workflow

1. Inspect the working tree, and read the documents that the task needs.
2. Preserve work that is outside the task, as the [Workflow](docs/conventions/pull-requests.md#workflow) rules of the pull request conventions state.
3. For new work, create a short-lived branch from the current `main`, in its own worktree. When you update a PR, continue on its branch.
4. Keep `main` ready for release.
5. Make small changes, and test each change.
6. Create checkpoint commits for the tested changes.
7. Keep unrelated refactoring and formatting separate from behavior changes.
8. Run the [Checks](#checks).
9. Push the branch. For new work, open a draft PR to `main`. Otherwise, update the existing PR. Then mark the PR as ready, as the [Status and approval](docs/conventions/pull-requests.md#status-and-approval) rules of the pull request conventions state.
10. Address review comments.
11. After the maintainer merges the PR, remove the branch and its worktree if they contain no work to preserve.

Keep each branch and PR limited to 1 reviewable change. Split unrelated changes into separate PRs.

## Checks

Run these commands before you open or update a PR:

- `git diff --check origin/main...HEAD`
- `python3 -m json.tool .ai-dlc/config.json > /dev/null`
- `python3 -m unittest discover -s hooks`

No linter or CI runs in this repository yet, and the only hook is the Git guard of the [Delivery authority](#delivery-authority) section. Until the build stage adds more checks, the maintainer checks each PR against the conventions.

## Review roles

No review role exists yet. The build stage adds review roles, such as a writing reviewer, and lists them in this section.

## Conventions

Read the matching convention before you write or update an artifact. If a skill gives a different rule, template, or file path, follow the convention.

The groups below follow the order of the work.

### All work

| Work | Convention |
| --- | --- |
| Writing or updating English prose, including code comments, commit messages, and the text of skills | [English prose](docs/conventions/english-prose.md) |
| Writing or updating Markdown files or the text of pull requests and Issues | [Markdown](docs/conventions/markdown.md) |
| Writing or updating convention files in `docs/conventions/` | [Convention files](docs/conventions/convention-files.md) |

### Delivery

| Work | Convention |
| --- | --- |
| Creating a short-lived branch for a pull request | [Branch names](docs/conventions/branch-names.md) |
| Writing checkpoint commit messages | [Commit messages](docs/conventions/commit-messages.md) |
| Creating or updating pull requests | [Pull requests](docs/conventions/pull-requests.md) |
| Applying labels when creating or updating Issues or pull requests | [GitHub labels](docs/conventions/github-labels.md) |
