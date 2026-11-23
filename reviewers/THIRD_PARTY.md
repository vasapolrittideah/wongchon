# Third-party review roles

This file lists each role file in `reviewers/` that comes from another project. Each role file keeps the license of its source project in a `<role>.LICENSE` file next to it.

## Roles

| Role | Source | Version | Commit | License | Files copied | Changes |
| --- | --- | --- | --- | --- | --- | --- |
| `code-reviewer` | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | `0.6.17` | `8c99fa36d90068c82d547f7c12a9d67a3e95f4ee` | MIT, Copyright (c) 2025 Addy Osmani | `agents/code-reviewer.md` as `reviewers/code-reviewer.md`, and `LICENSE` as `reviewers/code-reviewer.LICENSE` | The 5 dimensions of the review, the order of reading the tests and then the spec, and the rules for a fix and for uncertain findings stay. The front matter adds the model, the effort, and the paths of the role. The Inputs, Scope, and Findings sections, the checks of code comments and of a lowered quality bar, and the severities `Important`, `Nit`, and `Pre-existing` replace the severities, the verdict template, What's Done Well, the Verification Story, and Composition, because the review script reads structured findings, as ADR-0024 states. |

## Rules

- Copy a role from the commit of a release tag, and keep its license in `<role>.LICENSE` next to the role file.
- Edit the role file for the review gate of this project, and summarize the changes in the `Changes` column of its row.
- To update a role, compare the commit in its row with the new release, apply the upstream changes that this project needs, and update its row in the same commit.
- Do not copy an agent of another project into `agents/` as a review role. Claude Code loads each file in `agents/` as a subagent, as ADR-0027 states.
