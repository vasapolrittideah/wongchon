# Branch name conventions

This convention defines the name of a short-lived branch that holds 1 reviewable change outside `main`. Each branch reaches `main` through 1 pull request (PR).

## Template

A branch name has a type and a short description.

```text
<type of the change>/<short description of the change>
```

### Type

- Use the commit type of the PR title, from the [Types](commit-messages.md#types) of the commit message conventions, such as `docs` for `docs: ...`.
- Do not add the scope of the PR title.

### Short description

- Write lowercase words and numbers separated by single hyphens, such as `intent-affected-systems` or `update-python-3-13`.
- Name the change with a noun phrase or a verb phrase.
- Do not add another slash.

## Rules

- Apply a change of this convention to new branches and to existing branches that a later PR renames.
- If a tool creates the branch with a prefix, such as `claude/`, rename the branch with `git branch -m <new name>` before you push it.
- Do not add an agent or author prefix, such as `claude/` or `codex/`.
- Do not rename a branch that has an open PR.

## Examples

These branch names follow the convention:

| PR title | Branch name |
| --- | --- |
| `feat(intent): ask for the affected systems in the intent template` | `feat/intent-affected-systems` |
| `ci: check pull request titles` | `ci/check-pr-titles` |
| `docs: explain how to install the plugin from the marketplace` | `docs/marketplace-install` |

These branch names do not follow the convention. The first name uses `feature`, which is not a commit type, and breaks the Type rules. The second name adds an agent prefix, and breaks the Rules section.

| PR title | Branch name |
| --- | --- |
| `feat(intent): ask for the affected systems in the intent template` | `feature/intent-affected-systems` |
| `feat(intent): ask for the affected systems in the intent template` | `claude/intent-affected-systems` |
