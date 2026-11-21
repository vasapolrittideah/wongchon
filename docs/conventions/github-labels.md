# GitHub label conventions

This convention defines the name, color, and description of each label, and which labels to apply to GitHub Issues and pull requests (PRs). The labels come from the [Types](commit-messages.md#types) of the commit message conventions and from the `commit.scopes` list of `.wongchon/config.json`, so no separate label list exists.

## Rules

### Naming and location

- Name each type label `type:<type>`, with a type from the Types table.
- Name each area label `area:<scope>`, with a scope name from `commit.scopes`.
- Name the label for a breaking change `breaking`.

### Format and content

- Give each label the color that the [Colors](#colors) table states.
- For the description of a type label, use the purpose of the type from the Types table. For an area label, use the `area` of the scope. For `breaking`, use "Breaks the users of a public interface".
- Keep each `area` in `commit.scopes` at most 100 characters, because GitHub limits a label description to 100 characters.

### Workflow

- Before you apply a label that does not exist on GitHub, create it with `gh label create <name> --color <color> --description "<description>"`.

### Links and tracking

- Apply exactly 1 type label, with the type of the PR title.
- If the PR title has a scope, apply the area label of that scope, and no other area label.
- If the PR title has no scope, apply the area label of each scope that covers part of the main change, as the [Scope](commit-messages.md#scope) rules of the commit message conventions define "covers". If no scope covers any part of the main change, apply no area label.
- If the PR title has a breaking marker, apply `breaking`.
- For an Issue, apply the labels that the PR of the task will have. Choose them from the main change that the Issue plans.
- Use only the labels that this convention defines.

### Changes

- If a PR renames or removes a scope or a type, write the change to its label in the Follow-up tasks of the PR description. Do not rename or delete a label on GitHub before the PR merges.
- Apply a change of this convention to new Issues and PRs, and to open Issues and PRs when you edit them. Do not change the labels of closed Issues or merged PRs.

## Reference

### Colors

| Label | Color |
| --- | --- |
| `type:feat` | `0E8A16` |
| `type:fix` | `D93F0B` |
| `type:docs` | `0075CA` |
| `type:refactor` | `5319E7` |
| `type:test` | `FBCA04` |
| `type:perf` | `006B75` |
| `type:build` | `BFD4F2` |
| `type:ci` | `C2E0C6` |
| `type:style` | `D4C5F9` |
| `type:chore` | `CFD3D7` |
| `type:revert` | `000000` |
| Each `area:<scope>` label | `BFDADC` |
| `breaking` | `B60205` |

## Examples

These PRs have the labels that the convention requires:

| PR title | Labels |
| --- | --- |
| `feat(intent): ask for the affected systems in the intent template` | `type:feat`, `area:intent` |
| `ci: check pull request titles` | `type:ci` |
| `feat!: read commit scopes from .wongchon/config.json` | `type:feat`, `area:agents`, `area:plugin`, `breaking` |
| `chore: add the bootstrap conventions and agent instructions` | `type:chore`, `area:agents`, `area:conventions`, `area:deps` |
| `feat(intent): add the intent convention` | `type:feat`, `area:intent` |
| `chore(repo): rename the plugin from ai-dlc to wongchon` | `type:chore`, `area:repo` |
