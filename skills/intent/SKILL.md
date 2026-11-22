---
name: intent
description: Runs the intent stage of wongchon for 1 change. It interviews the owner of the change, writes the intent in docs/intents/, and opens the pull request that is the gate of the stage. Use when the user starts a new change, feature, or project, or asks you to write, change, or approve an intent.
---

# Intent

## Overview

The intent stage turns an ask into an approved intent. An intent states what a change must achieve and why, before the design of the change starts. The stage ends at a gate: the owner of the change approves the intent when they merge its pull request (PR). You work up to the gate, but you do not pass it.

Before you start, read these files:

- The [intent convention](../../docs/conventions/intents.md), which defines the file, the sections, and the status of an intent
- The [branch name](../../docs/conventions/branch-names.md), [commit message](../../docs/conventions/commit-messages.md), [pull request](../../docs/conventions/pull-requests.md), and [GitHub label](../../docs/conventions/github-labels.md) conventions, which define how the intent reaches the gate

## Steps

Do the steps in this order. If the owner must answer a question, stop your turn and wait for the answer.

1. Decide with the owner whether the change needs an intent:
   1. Estimate whether the change fits in 1 PR.
   2. If it fits, tell the owner your estimate and its reason. Propose that the change skips the intent and design stages and starts at the build stage.
   3. Let the owner decide. If the owner chooses to skip the intent, stop this skill.
2. If the intent depends on outside facts, research them before the interview. Outside facts are, for example, a law, a standard, or the behavior of another system. Also research when the owner asks for it.
   1. Give the research to a read-only subagent. Ask it for the answer, its evidence as a URL or a file and line, and the parts that it did not read in full.
   2. Tell the owner in a few sentences what the research found.
   3. Keep each source that the intent uses for the References section of the intent.
3. Create a short-lived branch from the current default branch, as the branch name conventions state.
4. Interview the owner with the [`interview-me`](../interview-me/SKILL.md) skill. Follow its steps until the owner confirms the restate with an explicit yes. The skill then writes the intent with the status `Draft`.
5. If the owner knows the problem but did not choose a direction, ask the owner whether to run the [`idea-refine`](../idea-refine/SKILL.md) skill. Also ask when the interview found 2 or more possible directions. If the owner agrees, run the skill. It writes the chosen direction into the same intent.
6. Make sure that the intent follows the intent convention. Use the list in [Verification](#verification). Fix each problem before you continue.
7. Commit the intent, as the commit message conventions state.
8. Push the branch, and open a draft PR, as the pull request conventions state. In Related artifacts, link the intent.
9. Mark the PR as ready when it meets each condition of a ready PR. Tell the owner that the PR is ready, and ask them to review the intent.
10. If the owner asks for changes, edit the intent, commit, and push. Keep the status `Draft`. Then ask for a review again.
11. If the owner approves the intent in the chat or in a review of the PR, change the status to `Approved`. Commit and push the change. Tell the owner that the PR is ready to merge.
12. Stop the skill. The owner merges the PR. The design stage starts from the approved intent after the merge.

## Changes to an approved intent

If the goal of a change moves after its intent merged, change the intent in a new PR. Follow steps 3 and 6 to 12. In the new PR, change the status to `Draft` first, as the intent convention states.

## Rules

- Write only what the change must achieve and why. The design stage decides how to build it.
- Change the status to `Approved` only after the owner approves the intent. A reply such as "sounds good" or "whatever you think" is not an approval. Ask the owner whether they approve the intent.
- Do not merge the PR. Only the owner merges it.
- Do not start the design of the change in this skill, also when the owner approves the intent.

## Verification

Before you commit the intent, make sure that each item is true:

- [ ] The file is `docs/intents/<change name>.md`, and the change name follows the Naming and location rules of the intent convention: `<scope>-<capability>` in lowercase words and numbers separated by single hyphens, with no project name or version.
- [ ] The intent has each section of the template of the intent convention, in the template order. Open questions and References are present only when they have content.
- [ ] The status is `Draft` until the owner approves the intent.
- [ ] Each success criterion is a result that a person or a check can observe.
- [ ] The intent names no file, class, function, library, or data structure, unless a constraint requires it.
- [ ] Out of scope has at least 1 item.
- [ ] Each open question names the stage that decides it, and no open question changes the problem, the outcome, the success criteria, or the scope.
- [ ] The Answers table has 1 row for each question of the interview. Each reply states the meaning of the answer of the owner in English.
- [ ] Each source in References is a source that the intent uses, and the table states the parts that you read only in a summary.
