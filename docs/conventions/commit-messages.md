# Commit message conventions

This convention defines the message of each checkpoint commit, which saves 1 step of the work on a branch. People and agents write checkpoint commits. The maintainer squash merges each pull request (PR) into `main`, and the squash commit has only the PR title. The PR title follows the subject rules of this convention, as the [Pull request](pull-requests.md) conventions state.

## Template

A message has a type, a scope, a breaking marker, a description, a body, Issue footers, and co-author trailers.

```text
<type of change>(<scope, if any>)<breaking marker, if any>: <description of the change>

<body, if any>

<Issue footer, if any>

Co-authored-by: <co-author name, if any> <<co-author email>>
```

### Type

- Use the type of the main change.
- If a change only edits documentation, use `docs`. If the project ships the changed Markdown files as its product, use the type of the change to the product, such as `feat` or `fix`. Examples are the skills and conventions of a plugin.
- If a change edits code or configuration for agents, such as a script or a hook, use the type of that change.
- Use one of the [Types](#types).
- Do not use `feat` only because the change adds a file.

### Scope

- Choose the scope with these steps, and stop after the first match:
  1. Use the first scope in the `commit.scopes` list of `.wongchon/config.json` that covers all of the main change. A scope covers a change when its `paths` match each changed file. If its `paths` list is empty, the scope covers a change that its `area` describes.
  2. If no scope covers all of the main change, omit the scope.
- If the project has no `.wongchon/config.json` file or no `commit.scopes` list, omit the scope.
- If a PR adds an area that no scope covers, such as a new service, add a scope for the area to `commit.scopes` in the same PR.
- Write each scope in `commit.scopes` as an object with `name`, `area`, and `paths` fields. The `area` states what the scope covers, and `paths` lists glob patterns from the repository root. Order the scopes from the most specific to the most general, because the first match wins.
- Use only the names in `commit.scopes`. A scope can have the same name as a type, such as `build(build)`.
- Do not combine scope names.

### Breaking marker

- Write the marker as `!` directly before the colon.
- If the change breaks the users of a public interface, add the marker. Examples are an API, a command, the format of a configuration file, and the name of a skill that users call.
- Do not add the marker for an incompatible change that affects only the developers of the project, such as a renamed environment variable for local development. Explain such a change in the PR description.

### Description

- Start the description with a lowercase verb in the imperative mood, such as `add` or `reject`.
- Name the specific change, such as `reject task updates based on an outdated version`. If you use a general verb, such as `update`, give it a specific object, such as `update Python to 3.13`.
- Do not end the description with a period.
- Do not write a description that names no change, such as `misc` or `fix things`.

### Body

- Put the body after the subject, separated by a blank line.
- Wrap prose lines at 72 characters.
- Separate paragraphs with 1 blank line.
- Start each bullet item with a hyphen and a space, and indent its wrapped lines by 2 spaces.
- Start each numbered item with its number, a period, and a space, and indent its wrapped lines by 3 spaces.
- Write a body only when the subject does not explain the step. Write for a reviewer who reads the PR 1 commit at a time. Explain what the step changes, and the reason or trade-off when the subject does not make it clear. You can name the tests that the step adds, because they are part of the step.
- If the subject of a checkpoint commit matches the PR title, apply the body rule above. This rule also applies to the only commit of a PR.
- Do not repeat text or add process history, abandoned methods, hypothetical objections, or unrelated files.
- Do not refer to the commit, the writer, or the time of writing, such as "This commit adds", "I", "we", "now", or "currently". State each change directly. The required first body line in [Commits that revert a commit](#commits-that-revert-a-commit) is an exception.

### Issue footers

- Put the footers after the body, or after the subject when there is no body, separated by a blank line.
- Write each footer as `Refs: #<Issue number>`.
- Write 1 footer for each Issue, and repeat the key on each line.
- Order the footers by ascending Issue number.
- If a checkpoint commit belongs to an Issue, add a `Refs` footer for it.
- Do not leave blank lines between Issue footers.
- Do not add a period at the end of an Issue footer.
- Do not use `Closes` in a commit. The PR description closes each Issue when the PR merges.

### Co-author trailers

- Put the trailers after a blank line at the end of the message.
- Order the trailers by name in alphabetical order.
- Add 1 trailer for each person or agent, other than the commit author, who contributed to the commit.
- For a person, spell the key as `Co-authored-by`, and use their name and the email that GitHub links to their account, such as their `users.noreply.github.com` address.
- For an agent, copy the attribution trailer that its harness gives, without changes. If the harness gives none, use the trailer in [Agent trailers](#agent-trailers).
- Keep the existing trailers when you amend or squash commits. GitHub copies the trailers of the checkpoint commits to the squash commit.
- Do not add a trailer for a person or agent who did not contribute.

## Rules

### Format and content

- Write the whole message as plain text, including text that comes from a PR description. Do not use backticks, Markdown links, or URLs. Name a file by its path, and refer to an Issue or a PR by its number, such as `#123`.
- Keep the whole subject line at most 72 characters. Do not count the `(#<number>)` suffix and its leading space, which GitHub adds to a squash commit.
- Write the parts in the order of the [Template](#template).
- Choose the type and the scope from the main change, which is the change that the commit or the PR exists to make. An edit that only supports the main change is not part of it, such as a new row in a table of links or a status update in a roadmap.
- Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
- Do not split code or trailers. A line that holds one of them can be longer than 72 characters.

### Workflow

- If a message has more than 1 line, write it to a file outside the working tree, and pass the file with `git commit --file <message-file>` in its own command.

### Changes

- Apply a change of this convention only to new commits and to commit messages that a later PR changes. Do not rewrite commits on `main` to follow it.

## Commits that revert a commit

Follow these rules for each commit that reverts an earlier commit.

- Start the body with `This reverts commit <full SHA>.` Then give the reason in a new paragraph.
- Use the scope and the description of the reverted commit.
- Use the `revert` type.
- Do not copy the breaking marker of the reverted commit. Add the marker only when the revert itself breaks users, as the [Breaking marker](#breaking-marker) rules state.

## Reference

### Types

| Type | Purpose |
| --- | --- |
| `feat` | Add functionality |
| `fix` | Correct a bug |
| `docs` | Change documentation only |
| `refactor` | Restructure code without changing behavior |
| `test` | Add or correct tests |
| `perf` | Improve performance |
| `build` | Change build tooling, compilation, or packaging |
| `ci` | Change CI workflows or automated checks |
| `style` | Change formatting only |
| `chore` | Maintain the project when no more specific type fits |
| `revert` | Revert an earlier commit |

### Agent trailers

| Agent | Trailer |
| --- | --- |
| Claude Code | `Co-authored-by: Claude <noreply@anthropic.com>` |
| Codex | `Co-authored-by: Codex <noreply@openai.com>` |

## Examples

### Subjects

This subject uses `feat` for a change to a skill that the plugin ships:

```text
feat(intent): ask for the affected systems in the intent template
```

This subject uses `fix` for a bug fix in a hook:

```text
fix(build): keep multiline PR descriptions in the plan hook
```

This subject uses `docs` for a change to documentation that the project does not ship:

```text
docs: explain how to install the plugin from the marketplace
```

This subject has no scope, because no scope in `commit.scopes` covers the CI workflow:

```text
ci: check pull request titles
```

This subject has a breaking marker, because users must move their settings to a new file:

```text
feat!: read commit scopes from .wongchon/config.json
```

This subject reverts an earlier commit with its scope and description:

```text
revert(intent): ask for the affected systems in the intent template
```

### Checkpoint commits

This checkpoint names the tests of its step and uses `Refs` to keep its Issue open until the PR merges:

```text
feat(verify): stop the eval run when a sample project fails to build

The eval runner reads the exit code of the build command of each
sample project and stops before the test step when the code is not 0.
test_runner_stops_on_build_failure covers a sample with a broken
build.

Refs: #42

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

### Revert commits

This revert commit keeps the scope and description of the reverted commit and names the reverted commit and the reason in its body:

```text
revert(intent): ask for the affected systems in the intent template

This reverts commit 2f77dde4c1b9a6e3d5f8a0b7c2e4d6f8a1b3c5e7.

The new question made the intent interview 2 times longer.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```
