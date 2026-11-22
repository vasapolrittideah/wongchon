# ADR-0015: Set up a project with /wongchon:setup

Status: `Accepted`

Spec: None

## Context

A project runs a setup command 1 time to give the framework the facts that it cannot know. Claude Code registers the hooks of a plugin when it loads the plugin, and it has a built-in `/init` command. A greenfield project has no stack and no check commands yet. [#14](https://github.com/vasapolrittideah/wongchon/pull/14) first recorded this decision.

## Decision

The setup command is `/wongchon:setup`, and only a person starts it. It writes `.wongchon/config.json` from the facts of the project, creates or extends `AGENTS.md` with the `CLAUDE.md` link, creates the GitHub labels, and opens a PR. The plugin registers its own hooks.

## Rejected options

| Option | Reason |
| --- | --- |
| `CONSTRAINTS.md` in the setup command | A greenfield project has no check commands yet. |
| A setup command that only writes files | Each change reaches `main` through a PR. |
| The name `init` | Claude Code has a built-in `/init` command. |

## Consequences

- The design stage of the first change writes `CONSTRAINTS.md`.
- The setup command installs no hooks.

## Confirmation

No check exists yet. The `plugin-skeleton-and-setup` change adds the skill with `disable-model-invocation: true`, which Claude Code enforces.
