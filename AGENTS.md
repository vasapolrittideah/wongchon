# Repository instructions

Follow these repository instructions for every task. Before you make a change, read the matching convention in the [Conventions](#conventions) table.

## Project

This repository holds `wongchon`, a Claude Code plugin that runs an AI-native software development lifecycle in projects of any stack. The lifecycle has 6 stages: intent, design, build, verify, deploy, and maintain. Version 1 covers the stages from intent to verify.

Before you plan a change, read the [Roadmap](ROADMAP.md). It states the purpose, the sources, the decisions, and the order of the work.

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
- `python3 -m json.tool .wongchon/config.json > /dev/null`
- `python3 -m unittest discover -s hooks`
- `python3 -m unittest discover -s scripts`
- `PR_TITLE='<PR title>' PR_BODY="$(cat <PR description file>)" python3 scripts/check_pr_metadata.py`
- `python3 scripts/check_stage_gate.py`

The CI workflow in `.github/workflows/ci.yml` runs these checks on each PR to `main`, on Python 3.9 and the latest Python. The stage gate check fails while an intent or a spec that the PR changes is not `Approved`. This failure is expected until the owner approves the artifact, and it does not stop a PR from becoming ready, as the [Status and approval](docs/conventions/pull-requests.md#status-and-approval) rules of the pull request conventions state. No linter runs yet. The hooks are the Git guard of the [Delivery authority](#delivery-authority) section and the review guard of the [Review roles](#review-roles) section. Until the build stage adds more checks, the maintainer checks each PR against the conventions.

## Review roles

Each review role is a role file in `reviewers/`. A review role checks a staged change, or the text of a PR, in a separate read-only process, as the [plugin review gate](docs/specs/plugin-review-gate.md) spec states.

| Role | Files that it reviews |
| --- | --- |
| [Code reviewer](reviewers/code-reviewer.md) | Each file that does not end in `.md` |
| [Writing reviewer](reviewers/writing-reviewer.md) | Each `.md` file, and the title and the description of each PR |
| [Artifact reviewer](reviewers/artifact-reviewer.md) | `docs/intents/**`, `docs/specs/**`, `docs/adrs/**`, `CONSTRAINTS.md`, and `GLOSSARY.md` |

In Claude Code, the [`hooks/review_guard.py`](hooks/review_guard.py) hook blocks `git commit`, `gh pr create`, and `gh pr edit` without the approval stamps that `scripts/review.py` writes for each role. Follow these steps:

1. Stage the change with `git add`.
2. For each role that the hook names, run `python3 scripts/review.py <role>` outside the Claude Code sandbox. The reviewer needs the login of Claude Code.
3. Fix each `Important` finding, and stage the fix. Then run the role again with `--reply <file>`. The file holds the findings of the last round and your reply to each one.
4. Commit with `git commit` as the only command, without `-a` or paths.
5. Before `gh pr create` or `gh pr edit`, write the title on the first line of a file and the description after it. Then run `python3 scripts/review.py writing-reviewer --pr-text <file>`. Last, pass the same title with `--title` and a file with only the description with `--body-file`.

If a role does not approve after 3 rounds, the script refuses a fourth round. Stop, and ask the maintainer. Only the maintainer resets the count with `--reset-rounds`.

## Conventions

Read the matching convention before you write or update an artifact. If a skill gives a different rule, template, or file path, follow the convention.

The groups below follow the order of the work.

### All work

| Work | Convention |
| --- | --- |
| Writing or updating English prose, including code comments, commit messages, and the text of skills | [English prose](docs/conventions/english-prose.md) |
| Writing or updating Markdown files or the text of pull requests and Issues | [Markdown](docs/conventions/markdown.md) |
| Writing or updating code comments, docstrings, and doc comments | [Code comments](docs/conventions/code-comments.md) |
| Writing or updating convention files in `docs/conventions/` | [Convention files](docs/conventions/convention-files.md) |

### Stages

| Work | Convention |
| --- | --- |
| Writing or updating intents in `docs/intents/` | [Intents](docs/conventions/intents.md) |
| Writing or updating specs in `docs/specs/` | [Specs](docs/conventions/specs.md) |
| Writing or updating architecture decision records (ADRs) in `docs/adrs/` | [Architecture decision records](docs/conventions/adrs.md) |
| Writing or updating the rules and exceptions of `CONSTRAINTS.md` | [Constraints](docs/conventions/constraints.md) |
| Writing or updating the entries of `GLOSSARY.md` | [Glossary entries](docs/conventions/glossary-entries.md) |

### Delivery

| Work | Convention |
| --- | --- |
| Creating a short-lived branch for a pull request | [Branch names](docs/conventions/branch-names.md) |
| Writing checkpoint commit messages | [Commit messages](docs/conventions/commit-messages.md) |
| Creating or updating pull requests | [Pull requests](docs/conventions/pull-requests.md) |
| Applying labels when creating or updating Issues or pull requests | [GitHub labels](docs/conventions/github-labels.md) |
