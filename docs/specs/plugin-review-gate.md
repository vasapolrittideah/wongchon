# Spec: plugin review gate

Author: Vasapol Rittideah

Status: `Draft`

Intent: [`docs/intents/plugin-review-gate.md`](../intents/plugin-review-gate.md)

## Current state

The [Review gate](../adrs/0010-run-review-roles-in-a-review-script.md) decision fixes the parts of the gate: a review script, a separate read-only process for each review role, approval stamps for each tree, a hook that blocks a commit or a PR without a stamp, and at most 3 rounds. The [Prose checks](../adrs/0007-check-prose-with-skills-vale-and-a-reviewer.md) and [Code comments](../adrs/0008-write-no-code-comments-by-default.md) decisions wait for a writing reviewer and a code reviewer. None of these parts exists yet, and the Review roles section of `AGENTS.md` states that no role exists.

`hooks/git_guard.py` blocks the commands of the maintainer, as [ADR-0009](../adrs/0009-block-maintainer-commands-with-a-git-guard.md) states. `.github/workflows/ci.yml` runs all CI jobs on `pull_request`, so a PR can change each check that the `Protect main` ruleset requires: `Checks (Python 3.9)`, `Checks (Python 3.x)`, `PR metadata`, and `Stage gate`.

## Requirements

1. Given staged files that match the paths of a role, when the agent runs `git commit` and no approval stamp of that role exists for the staged tree, then the hook blocks the command and names the role and the command that reviews the change. Criterion: S2. Proof: unit test.
2. Given an approval stamp of each required role for the staged tree, when the agent runs `git commit`, then the hook allows it. Criterion: S2. Proof: unit test.
3. Given a `git commit` with `-a`, `-i`, `-o`, or a path, or a staged tree that the hook cannot compute, or a stamp that it cannot read, when the hook runs, then it blocks the command. Criterion: S2. Proof: unit test.
4. Given `gh pr create` or `gh pr edit` that changes the title or the body, when no writing reviewer stamp exists for the hash of the title and the body file, or the command uses `--body` instead of 1 `--body-file`, then the hook blocks it. Criterion: S2. Proof: unit test.
5. Given a commit whose staged tree equals the tree of `HEAD`, such as a change of the message only, when the agent runs `git commit`, then the hook allows it. Criterion: S2. Proof: unit test.
6. Given a review, when the structured output of the role has no `Important` finding, then the script writes the stamp. When it has an `Important` finding, or the output is missing or does not match the schema, then the script writes no stamp and exits with a failure. Criterion: S2. Proof: unit test with a fake reviewer command.
7. Given a review role that tries to edit a file or to write a stamp, when the review runs, then no file of the project and no stamp changes. Criterion: S6. Proof: integration test with the real reviewer command.
8. Given 3 reviews of a role on a branch without an approval, when the agent starts a fourth review, then the script refuses it and tells the agent to ask the maintainer. After an approval, the count of that role starts again. Criterion: S3. Proof: unit test.
9. Given a command of the agent that resets the count of rounds, when the Git guard runs, then it blocks the command. Criterion: S3. Proof: unit test.
10. Given a PR that changes the check scripts or the workflow of `PR metadata` or `Stage gate`, when CI runs, then these jobs run the workflow and the scripts of `main`. Criterion: S4. Proof: manual check on a test PR.
11. Given a PR whose workflows define a job with the name of a protected job, when the `Check changes` job runs, then it fails and names the job. Criterion: S4. Proof: unit test.
12. Given a PR that changes `.github/workflows/**`, `scripts/**`, `hooks/**`, `reviewers/**`, or `.claude/settings.json`, when the `Check changes` job runs, then it shows a warning for each changed file of these paths. Criterion: S5. Proof: unit test and manual check on a test PR.
13. Given the change `build-plans-and-tasks`, when its last PR merges, then each of its commits and PRs had the stamps of its roles, and the maintainer wrote no review comment that a role should have found. Criterion: S1. Proof: manual check by the maintainer.
14. Given the existing tests of `hooks/` and `scripts/`, the commands that `hooks/git_guard.py` blocks, and the jobs `Checks (Python 3.9)` and `Checks (Python 3.x)`, when this change merges, then each one keeps working. Criterion: S2. Proof: unit test and CI.

## Design

### Review roles

Each review role is 1 Markdown file in `reviewers/`: `code-reviewer.md`, `writing-reviewer.md`, and `artifact-reviewer.md`, as [ADR-0027](../adrs/0027-keep-review-roles-in-role-files.md) states. The front matter has `name`, `description`, `model`, `effort`, and `paths`. The body is the prompt: what the role checks, the conventions and ADRs that it applies, and the format of its findings.

| Role | Checks | Paths | Model and effort |
| --- | --- | --- | --- |
| Code reviewer | Correctness, code comments as ADR-0008 states, and a lowered quality bar as the `constraint-driven-development` skill describes | Each file that does not end in `.md` | `opus`, `medium` |
| Writing reviewer | Prose and Markdown, as ADR-0007 and the English prose and Markdown conventions state | Each `.md` file, and the title and the body of a PR | `sonnet`, `high` |
| Artifact reviewer | Intents, specs, ADRs, `CONSTRAINTS.md`, and `GLOSSARY.md` against their conventions | `docs/intents/**`, `docs/specs/**`, `docs/adrs/**`, `CONSTRAINTS.md`, and `GLOSSARY.md` | `opus`, `medium` |

The framework fixes the paths of each role, and a project cannot change them, as [ADR-0023](../adrs/0023-choose-review-roles-from-fixed-paths.md) states. The PR of the roles lists them in the Review roles section of `AGENTS.md`.

### Review script

`python3 scripts/review.py <role> [--pr-text <file>] [--reply <file>]` reviews the staged tree, or with `--pr-text` the title on the first line of the file and the body after it.

1. It reads the role file from the default branch on `origin`, not from the working tree, so that a change cannot edit its own reviewer. If the file is missing there, it fails.
2. It computes the staged tree with `git write-tree` on a copy of the index, and the diff from `HEAD` to that tree.
3. It runs `claude -p --safe-mode --tools "Read,Grep,Glob" --permission-mode dontAsk --no-session-persistence --output-format json --json-schema <schema> --model <model> --effort <effort>`, with the prompt of the role and the diff or the PR text on standard input, as [ADR-0021](../adrs/0021-isolate-each-review-role-with-safe-mode.md) states. `--reply` adds the findings of the last round and the replies of the agent.
4. The schema has `summary` and a list of findings. Each finding has `severity` (`Important`, `Nit`, or `Pre-existing`), `file`, `line`, `rule`, `problem`, and `fix`. The script approves the change only when no finding is `Important`, as [ADR-0024](../adrs/0024-decide-the-verdict-from-structured-findings.md) states. A finding without a `rule` does not block.
5. It prints the findings and exits with `0` for an approval, `1` for requested changes, and `2` for an error or a refused round.

### Approval stamps and rounds

The script writes each stamp as a JSON file in `<git common dir>/wongchon/reviews/<role>/`, as [ADR-0022](../adrs/0022-store-approval-stamps-in-the-git-common-dir.md) states. The name is the tree hash, or `text-<sha256 of the PR text>`. The file holds the role, the model, the effort, the time, and the findings. The PR description of each change states the result and the rounds of each role in Verification.

The script counts the reviews of each role that end without an approval in `<git common dir>/wongchon/reviews/<role>/rounds/<branch>`, as [ADR-0025](../adrs/0025-count-review-rounds-in-the-review-script.md) states. It refuses a fourth review, and an approval deletes the count. Each round is a new process. The maintainer runs `python3 scripts/review.py <role> --reset-rounds` in a terminal after they decide, and `hooks/git_guard.py` blocks this option for the agent.

### Review guard hook

`hooks/review_guard.py` is a `PreToolUse` hook for `Bash` in `.claude/settings.json`, apart from the Git guard, as [ADR-0028](../adrs/0028-block-unstamped-commits-in-a-separate-hook.md) states. It uses the command parser of `hooks/git_guard.py`, and the path rules and the stamp names of `scripts/review.py`. It checks `git commit`, `gh pr create`, and `gh pr edit`, as requirements 1 to 5 state, and it reads each stamp to confirm the role and the key. Each error blocks the command with exit code `2` and a message that names the missing stamp. It does not check `git push`, because each commit already has its stamps.

### Protected checks

`.github/workflows/protected-checks.yml` runs on `pull_request_target`, as [ADR-0026](../adrs/0026-run-pr-data-checks-from-main-with-pull-request-target.md) states. It checks out the default branch, has only `contents: read` and no secrets, and reads the files of the PR as data with `git fetch` and `git show`. It never runs the code of the PR.

| Job | Contract |
| --- | --- |
| `PR metadata` | Runs `scripts/check_pr_metadata.py` of `main` on the title and the body of the event |
| `Stage gate` | Runs `scripts/check_stage_gate.py --head <PR head SHA>` of `main`, which reads each changed artifact from that commit |
| `Check changes` | Writes a warning annotation for each changed file of the paths of requirement 12, and fails when a workflow of the PR defines a job named `PR metadata`, `Stage gate`, or `Check changes` |

`ci.yml` keeps the jobs `Checks (Python 3.9)` and `Checks (Python 3.x)` on `pull_request`, because they run the code of the PR.

### Subagents and skills

Each subagent is 1 file in `agents/`, which `.claude/agents/` links, in the same way as `.claude/skills/` links `skills/`.

- `researcher`: tools `Read`, `Grep`, `Glob`, `WebFetch`, and `WebSearch`. It returns the answer, its evidence as a URL or a file and line, and the parts that it did not read in full.
- `self-reviewer`: tools `Read`, `Grep`, and `Glob`. It reviews a decision or a diff with a role file of `reviewers/` as its checklist, and it gives advice only, as [ADR-0029](../adrs/0029-self-review-with-a-self-reviewer-subagent.md) states.

This change copies 3 skills of agent-skills at version 0.6.17, as `skills/THIRD_PARTY.md` states:

| Skill | Rewrite |
| --- | --- |
| `source-driven-development` | Give research to `researcher`, and put each source in the References section of the artifact. |
| `doubt-driven-development` | Run the self-review with `self-reviewer`, and state that it gives no stamp and does not replace the gate. |
| `context-engineering` | Keep the rules for where each instruction goes and for loading context in parts. Remove the template of `CLAUDE.md` and the project map, which `AGENTS.md` and `ARCHITECTURE.md` cover. |

The `intent` and `design` skills name `researcher` in their research steps.

## Rules

| Rule | Check |
| --- | --- |
| A commit or a PR of the agent has the stamps of its roles. | `hooks/review_guard.py` |
| A role does not review a fourth round before the maintainer decides. | `scripts/review.py` and `hooks/git_guard.py` |
| The checks of PR data run from `main`, and no workflow of a PR uses a protected job name. | The `Check changes` CI job |

## Boundaries

- Ask first: Change the Git guard in a way that unblocks a command that it blocks today.
- Never: Give a review role or `self-reviewer` a tool that can write, such as `Edit`, `Write`, or `Bash`.

## Decisions

| Decision | ADR |
| --- | --- |
| Each review role runs with `--safe-mode`, read-only tools, and its role file from the default branch. | [ADR-0021](../adrs/0021-isolate-each-review-role-with-safe-mode.md) |
| Approval stamps live in the Git common directory, keyed by tree hash or PR text hash. | [ADR-0022](../adrs/0022-store-approval-stamps-in-the-git-common-dir.md) |
| Fixed path rules of the framework choose the roles of each commit. | [ADR-0023](../adrs/0023-choose-review-roles-from-fixed-paths.md) |
| The script decides the verdict from structured findings, without a second pass. | [ADR-0024](../adrs/0024-decide-the-verdict-from-structured-findings.md) |
| The review script counts the rounds and refuses a fourth round. | [ADR-0025](../adrs/0025-count-review-rounds-in-the-review-script.md) |
| A `pull_request_target` workflow runs the checks of PR data from `main`. | [ADR-0026](../adrs/0026-run-pr-data-checks-from-main-with-pull-request-target.md) |
| Each review role is a role file in `reviewers/` with its model and effort. | [ADR-0027](../adrs/0027-keep-review-roles-in-role-files.md) |
| A separate hook blocks a commit or a PR without its stamps. | [ADR-0028](../adrs/0028-block-unstamped-commits-in-a-separate-hook.md) |
| The self-review uses `doubt-driven-development` with a `self-reviewer` subagent. | [ADR-0029](../adrs/0029-self-review-with-a-self-reviewer-subagent.md) |

## Concerns

| Concern | Resolution |
| --- | --- |
| The code review article filters out findings about style, but the writing reviewer checks style against the conventions. | The maintainer keeps the writing reviewer. Each finding must cite a rule, and a finding without a rule does not block. |
| A `pull_request_target` workflow has more trust than a `pull_request` workflow. | The maintainer accepts it with `contents: read`, no secrets, and no run of the code of the PR. |
| The hook and the script run from the working tree, so the agent can edit them in its branch. | The maintainer accepts it, because the gate only catches mistakes. `Check changes` shows each such edit on the PR. |

## Assumptions and open questions

- `--safe-mode` keeps the hooks of installed plugins off in print mode, as the CLI reference states. A test on 2026-11-23 proved it only for the hooks of a project. The integration test of requirement 7 proves it.
- When 2 check runs on 1 commit have the same name, GitHub does not document which one a required check uses. `Check changes` makes such a PR fail, but the maintainer must read its result.

## Answers to the intent

| Open question of the intent | Answer |
| --- | --- |
| Does the review use a second pass that confirms each finding, and severity tags? | It uses the tags `Important`, `Nit`, and `Pre-existing`, and no second pass. The verify phase measures the noise with evals before it adds one. |
| How does a review role run without the hooks and plugins of the project, with the subscription login? | With `--safe-mode`, which keeps the normal login and turns off hooks, plugins, and `CLAUDE.md`. |
| Can a job of the PR with the same name as a protected check make that check pass? | Yes, because required checks match only the job name. `Check changes` fails on such a PR. |

## Answers

| Question | Reply |
| --- | --- |
| When must the maintainer allow `pull_request_target`? | Before the PR that adds the protected checks workflow. The intent keeps its date, and the spec states the order. |
| Does the change split into 2 changes, 1 for the review gate and 1 for the protected checks? | No. It stays 1 change with several PRs. |
| Where do the stamps live, and what are their keys? | In the Git common directory, keyed by the hash of the staged tree, or by the hash of the PR text. Each stamp holds the report. |
| Which roles must approve which command? | Roles by fixed path rules: the writing reviewer for Markdown and PR text, the artifact reviewer for stage artifacts and project documents, and the code reviewer for other files. |
| How does the script decide the verdict? | From structured output with the tags `Important`, `Nit`, and `Pre-existing`. Only `Important` blocks, a finding must cite a rule, and no second pass runs. |
| How does the limit of 3 rounds work? | The script counts the rounds of each role on each branch and refuses a fourth. Only the maintainer resets the count, and each round is a new process. |
| Where do the files of the gate live? | Roles in `reviewers/`, the script in `scripts/`, a separate hook in `hooks/`, and subagents in `agents/` with links in `.claude/agents/`. |
| How do the self-review and the 3 skills work? | `doubt-driven-development` runs the self-review with `self-reviewer`, `source-driven-development` uses `researcher`, and `context-engineering` keeps the rules for where instructions go. Phase 3 is Done when this spec needs no edit of a skill or a convention. |
| How does the change stop a PR from editing its own checks? | A `pull_request_target` workflow runs `PR metadata`, `Stage gate`, and a new `Check changes` job from `main`. `Check changes` warns about changed check files, and fails on a protected job name. |
| In which order do the PRs of the build come? | Roles, script, hook, protected checks, removal of the old jobs, subagents with 2 skills, the third skill with the edits of the stage skills, and then the roadmap. |
| Which model does each role use? | `opus` with `medium` effort for the code and artifact reviewers, and `sonnet` with `high` effort for the writing reviewer. |

## References

| Source | What this spec takes from it | Parts read only in a summary |
| --- | --- | --- |
| [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) | The severity tags, a fresh-context self-review before the gate, and an approval for 1 exact version | The whole article, which the fetch tool returned as a summary with short quotes |
| [CLI reference](https://code.claude.com/docs/en/cli-reference) and [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) | `--safe-mode`, `--tools`, `--permission-mode dontAsk`, `--json-schema`, and the limit of `--bare` | The parts other than these flags |
| [Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) and [Troubleshooting rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/troubleshooting-rules) | A `pull_request_target` workflow runs from the default branch, and required checks match only the job name | None |
