# ADR-0017: Keep the plugin in the plugin folder

Status: `Accepted`

Spec: None

## Context

At install, Claude Code copies only the plugin folder into the cache of each user, and it warns about a `CLAUDE.md` file at the root of a plugin. This repository also holds the roadmap, the stage artifacts of its own changes, and `evals/`. [#14](https://github.com/vasapolrittideah/wongchon/pull/14) first recorded this decision.

## Decision

The plugin lives in `plugin/`, and `.claude-plugin/marketplace.json` at the root points to it. The skills, hooks, scripts, and conventions move into `plugin/` in the build phase.

## Rejected options

| Option | Reason |
| --- | --- |
| The plugin at the root of this repository | The install then copies this roadmap, the stage artifacts, and `evals/` into each project with the plugin, and Claude Code warns about a `CLAUDE.md` file at the root of a plugin. |

## Consequences

- Each file that a skill reads in another project must be under `plugin/`.
- The links in this repository to the conventions, skills, and hooks change when the files move.

## Confirmation

No check exists yet. A follow-up task adds `claude plugin validate` to CI after the `plugin-skeleton-and-setup` change creates the layout.
