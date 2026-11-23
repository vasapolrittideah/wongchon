# Plan: plugin review gate

Author: Vasapol Rittideah

Status: `Draft`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Tasks

Each task is 1 PR, in this order. After the owner approves the plan, each task becomes 1 GitHub Issue, and this section keeps only the links to the Issues.

### Task 1: Add the review roles

- Result: `reviewers/` has the role files of the code reviewer, the writing reviewer, and the artifact reviewer, with the front matter and the prompts that the Review roles part of the spec states. The Review roles section of `AGENTS.md` lists them, and the `plugin` scope covers `reviewers/**` and `agents/**`.
- Requirements: the Review roles part of the Design, for requirements 1 to 6 and 13
- Files: `reviewers/code-reviewer.md` (new), `reviewers/writing-reviewer.md` (new), `reviewers/artifact-reviewer.md` (new), `AGENTS.md`, `.wongchon/config.json`
- Proof: Run `python3 -m json.tool .wongchon/config.json` to check the scopes. Check that each role names the conventions and ADRs that it applies, its paths, its model, and its effort, as the spec states.
- Depends on: None

### Task 2: Add the review script

- Result: `scripts/review.py` reviews the staged tree or the PR text with 1 role, decides the verdict from the structured findings, writes the approval stamp, and counts the rounds.
- Requirements: 6, 7, and 8
- Files: `scripts/review.py` (new), `scripts/test_review.py` (new)
- Proof: Run `python3 -m unittest discover -s scripts` to check the verdict for each severity and for invalid output, the stamps, the count of rounds, and the refusal of a fourth round, with a fake reviewer command. Run the integration test of requirement 7 with the real reviewer command on the machine of the maintainer, because CI has no login of Claude Code.
- Depends on: Task 1, because the script reads the role files from the default branch

### Task 3: Block commits and PRs without stamps

- Result: `hooks/review_guard.py` blocks a commit or a PR without the stamps of its roles, and `hooks/git_guard.py` blocks `--reset-rounds` for the agent. From this PR on, each commit and each PR of the agent passes the gate.
- Requirements: 1, 2, 3, 4, 5, 9, and 14
- Files: `hooks/review_guard.py` (new), `hooks/test_review_guard.py` (new), `hooks/git_guard.py`, `hooks/test_git_guard.py`, `.claude/settings.json`
- Proof: Run `python3 -m unittest discover -s hooks` to check each blocked and allowed command. In a session, check that a commit without a stamp is blocked and that a commit with its stamps passes.
- Depends on: Task 2

### Task 4: Run the checks of PR data from main

- Result: `.github/workflows/protected-checks.yml` runs `PR metadata`, `Stage gate`, and `Check changes` from `main` on `pull_request_target`.
- Requirements: 10, 11, and 12
- Files: `.github/workflows/protected-checks.yml` (new), `scripts/check_changes.py` (new), `scripts/test_check_changes.py` (new), `scripts/check_stage_gate.py`, `scripts/test_check_stage_gate.py`
- Proof: Run `python3 -m unittest discover -s scripts` to check `--head` of the stage gate, the warnings for changed check files, and the failure on a protected job name. After the merge, open a test PR that changes `scripts/check_stage_gate.py`, and check that `Stage gate` runs the script of `main` and that `Check changes` names the file.
- Owner action: Allow `pull_request_target` in the Actions event policy of the repository before this PR opens.
- Depends on: None

### Task 5: Remove the old jobs of PR data from CI

- Result: `ci.yml` keeps only the jobs that run the code of the PR, and the protected workflow alone reports `PR metadata` and `Stage gate`.
- Requirements: 10 and 14
- Files: `.github/workflows/ci.yml`, `AGENTS.md`
- Proof: Check on the PR that `PR metadata` and `Stage gate` come only from the protected workflow, and that `Checks (Python 3.9)` and `Checks (Python 3.x)` still run.
- Owner action: After the merge, add `Check changes` to the required checks of the `Protect main` ruleset.
- Depends on: Task 4

### Task 6: Add the research and self-review subagents

- Result: `agents/` has the `researcher` and `self-reviewer` subagents, which `.claude/agents/` links. The `source-driven-development` and `doubt-driven-development` skills are copied at version 0.6.17 and rewritten to use them.
- Requirements: the Subagents and skills part of the Design
- Files: `agents/researcher.md` (new), `agents/self-reviewer.md` (new), `.claude/agents/` (new links), `skills/source-driven-development/` (new), `skills/doubt-driven-development/` (new), `.claude/skills/` (new links), `skills/THIRD_PARTY.md`
- Proof: Check that the tools of each subagent match the spec, and that each copied skill has its `LICENSE` file and a row in `skills/THIRD_PARTY.md`.
- Depends on: Task 1, because `self-reviewer` uses the role files

### Task 7: Copy context-engineering and name the researcher in the stage skills

- Result: The `context-engineering` skill is copied at version 0.6.17 and rewritten, and the `intent` and `design` skills give research to `researcher`.
- Requirements: the Subagents and skills part of the Design
- Files: `skills/context-engineering/` (new), `.claude/skills/` (new link), `skills/THIRD_PARTY.md`, `skills/intent/SKILL.md`, `skills/design/SKILL.md`
- Proof: Check that `context-engineering` has no template of `CLAUDE.md` and no project map, and that the research steps of `intent` and `design` name `researcher`.
- Depends on: Task 6

### Task 8: Mark phase 4 as done

- Result: The roadmap shows phase 4 as done, with a link to each PR of the change.
- Requirements: None
- Files: `ROADMAP.md`
- Proof: Check that each Issue of the milestone of the change is closed.
- Depends on: Tasks 1 to 7

## Checkpoints

- After task 3: A commit of the agent without a stamp is blocked, and the PR of task 3 states the result and the rounds of each role in Verification.
- After task 5: A test PR that edits a protected check gets the result of the check of `main`, and `Check changes` is a required check.
- After task 7: Each requirement of the spec has its proof, except requirement 13, which the change `build-plans-and-tasks` proves.

## Risks

| Risk | Mitigation |
| --- | --- |
| The script reads the role files from the default branch, so the gate cannot review before task 1 merges. | Task 1 merges first, and the maintainer reviews tasks 1 and 2 without the gate. |
| Without the Actions event policy, the protected jobs do not run, and their required checks stay pending. | The owner action of task 4 comes before its PR opens. |
| CI has no login of Claude Code, so it cannot run the integration test of requirement 7. | The test skips when the reviewer command is missing, and the PR of task 2 states the local result. |
| Each review uses the limit of the subscription of the maintainer. | The paths of each role keep a review to its own files, and the writing reviewer uses `sonnet`. |

## Open questions

- Requirement 13 is proved only in the change `build-plans-and-tasks`, after task 8 marks phase 4 as done. The maintainer checks it at the end of that change.
