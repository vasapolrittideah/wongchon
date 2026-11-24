# Plan: build plans and tasks

Author: Vasapol Rittideah

Status: `Draft`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Tasks

Each task is 1 PR, in this order. After the maintainer agrees with the tasks, each task becomes 1 GitHub Issue, and this section keeps only the links to the Issues.

### Task 1: Show a review role the changes since its last round

- Result: A later round of a review gets the diff since the last round, and each role file states which findings of a later round block the commit. The writing reviewer reads the convention of each artifact that it reviews.
- Requirements: 11, 12, 13, and 17
- Files: `scripts/review.py`, `scripts/test_review.py`, `reviewers/code-reviewer.md`, `reviewers/writing-reviewer.md`, `reviewers/artifact-reviewer.md`
- Proof: Run `python3 -m unittest discover -s scripts`, which uses a fake reviewer command. The tests check that a round saves its tree and text, that the request of a later round has the diff since the last round, and that an approval and `--reset-rounds` delete the saved tree and text.
- Depends on: None

### Task 2: Accept redirections after `git commit` in the review guard

- Result: The review guard allows `git commit` with `2>&1`, or with `>`, `>>`, or `2>` and a file. It still blocks a pipe after the commit, and a second command after `&&`, `;`, or `||`.
- Requirements: 10 and 17
- Files: `hooks/review_guard.py`, `hooks/test_review_guard.py`
- Proof: Run `python3 -m unittest discover -s hooks` to check each allowed redirection and each blocked pipe and list.
- Depends on: None

### Task 3: Add the plan and GitHub Issue conventions

- Result: `docs/conventions/plans.md` and `docs/conventions/github-issues.md` define the plan, its template, the task and follow-up Issues, the milestone, the Project, and the `Blocked by` links. `.wongchon/config.json` names the Project of this repository.
- Requirements: the Plan convention, GitHub Issue convention, and Configuration parts of the Design
- Files: `docs/conventions/plans.md` (new), `docs/conventions/github-issues.md` (new), `AGENTS.md`, `.wongchon/config.json`
- Proof: Run `python3 -m json.tool .wongchon/config.json`. Check that the plan of this change and its Issues follow the 2 conventions.
- Depends on: None

### Task 4: Add the check of the Issues of a plan

- Result: `scripts/check_plan_issues.py <milestone>` fails when 2 Issues share a file and no chain of `Blocked by` links puts them in order, and when an Issue title has more than 72 characters.
- Requirements: 3 and 4
- Files: `scripts/check_plan_issues.py` (new), `scripts/test_check_plan_issues.py` (new)
- Proof: Run `python3 -m unittest discover -s scripts` with fake Issue data. Run the script on the milestone of this change.
- Depends on: task 3, because the script reads the Files section of the GitHub Issue convention

### Task 5: Check plans and small changes in the stage gate

- Result: The `Stage gate` job reads plans, runs the check of the Issues of each changed `Approved` plan, and enforces the rules of small changes.
- Requirements: 1, 2, 5, 6, and 17
- Files: `scripts/check_stage_gate.py`, `scripts/test_check_stage_gate.py`, `.github/workflows/protected-checks.yml`, `AGENTS.md`
- Proof: Run `python3 -m unittest discover -s scripts` to check each rule. After the merge, check on the next plan PR that the job reads the Issues of its milestone.
- Depends on: task 3, because both change `AGENTS.md`, and task 4, because the job runs its script

### Task 6: Make each follow-up task an Issue

- Result: The pull request conventions require an Issue number for each follow-up task, and the `PR metadata` job checks it. The `intent` skill triages the open follow-up Issues of the area of a change.
- Requirements: 7
- Files: `docs/conventions/pull-requests.md`, `.github/pull_request_template.md`, `scripts/check_pr_metadata.py`, `scripts/test_check_pr_metadata.py`, `skills/intent/SKILL.md`
- Proof: Run `python3 -m unittest discover -s scripts` to check each form of a bullet and the order of the Issue numbers.
- Depends on: task 3, because the follow-up Issue follows the GitHub Issue convention

### Task 7: Turn the follow-up tasks of merged PRs into Issues

- Result: Each follow-up task of the PRs that merged before this change has an Issue or a reason to close it.
- Requirements: 14
- Files: None
- Proof: The maintainer approves 1 table of all old follow-up tasks, and each row has an Issue or a reason.
- Owner action: Approve the table in the chat.
- Depends on: task 6

### Task 8: Check that each subagent has only read-only tools

- Result: The `Check changes` job fails on a subagent in `agents/` with a tool outside the allowlist, and warns about each changed file of `agents/`.
- Requirements: 8 and 9
- Files: `scripts/check_changes.py`, `scripts/test_check_changes.py`
- Proof: Run `python3 -m unittest discover -s scripts` to check a missing `tools` field, a tool outside the allowlist, and the warning.
- Depends on: None

### Task 9: Copy the planning, incremental, and test-driven skills

- Result: `planning-and-task-breakdown`, `incremental-implementation`, and `test-driven-development` are copied at version 0.6.17 and rewritten, as the Copied skills part states.
- Requirements: the Copied skills part of the Design
- Files: `skills/planning-and-task-breakdown/` (new), `skills/incremental-implementation/` (new), `skills/test-driven-development/` (new), `.claude/skills/` (new links), `skills/THIRD_PARTY.md`
- Proof: Check that each copied skill has its `LICENSE` file and a row in `skills/THIRD_PARTY.md` with the upstream commit.
- Depends on: None

### Task 10: Add the plan and build skills

- Result: `/plan` writes the plan and the Issues of a change, and `/build` builds its Issues in single or chain mode, as the Plan skill and Build skill parts state.
- Requirements: the Plan skill and Build skill parts of the Design, for requirement 15
- Files: `skills/plan/SKILL.md` (new), `skills/build/SKILL.md` (new), `.claude/skills/` (new links)
- Proof: Check each step of both skills against the spec. Then run `scripts/check_plan_issues.py` from the `plan` skill on the milestone of this change.
- Depends on: task 4, because both skills run its script, and task 9, because both change `.claude/skills/`

### Task 11: Record the end of `build-plans-and-tasks` in the roadmap

- Result: The phase 5 row of the roadmap links the PRs of `build-plans-and-tasks`, and the maintainer checked requirement 16.
- Requirements: 16
- Files: `ROADMAP.md`
- Proof: Check that each Issue of the milestone is closed.
- Owner action: Check requirement 13 of the spec of `plugin-review-gate` for each commit and each PR of this change.
- Depends on: tasks 1 to 10

## Checkpoints

- After task 2: A later review round gets the diff since the last round, and a commit with `2>&1` passes the review guard.
- After task 6: A PR with a follow-up task without an Issue fails the `PR metadata` job.
- After task 10: Each requirement of the spec has its proof, with 2 exceptions. The change `plugin-skeleton-and-setup` proves requirement 15, and the maintainer checks requirement 16 in task 11.

## Risks

| Risk | Mitigation |
| --- | --- |
| The review script reads the role files from the default branch, so the rule of later rounds starts only after task 1 merges. | Task 1 merges first. |
| The token of a `pull_request_target` job may not read the `Blocked by` links of Issues. | Task 5 proves it on the next plan PR, and the job fails when it cannot read the Issues. |
| No local copy of agent-skills 0.6.17 exists. | Task 9 reads the skills from GitHub at the commit that `skills/THIRD_PARTY.md` states. |
| Task 7 creates many Issues at once. | The maintainer approves 1 table first, and each closed row records its reason. |

## Open questions

Requirement 15 is proved only in the change `plugin-skeleton-and-setup`. The maintainer checks it at the end of that change.
