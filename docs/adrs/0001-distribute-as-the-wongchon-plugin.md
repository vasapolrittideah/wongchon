# ADR-0001: Distribute the framework as the wongchon Claude Code plugin

Status: `Accepted`

Spec: None

## Context

The framework must reach each personal project of the maintainer and stay easy to update to a new version. Its name must not belong to another tool for AI agents. [#3](https://github.com/vasapolrittideah/wongchon/pull/3) first recorded this decision in the roadmap.

## Decision

The project ships the framework as a Claude Code plugin named `wongchon`, the Thai word for cycle, with a marketplace in this repository. The plugin name is also the namespace of its skills and the name of its configuration folder, `.wongchon/`.

## Rejected options

| Option | Reason |
| --- | --- |
| A template that projects copy | A copy is hard to update to a new version. |
| The name `ai-dlc` | AI-DLC is the name of an AWS methodology for AI coding agents that also supports Claude Code. |
| The English names `ratchet`, `cairn`, `trellis`, `sluice`, and `plumbline` | Tools for AI agents already use them. |
| The name `pratu`, the Thai word for gate | It names only the gates and not the cycle of stages. |

## Consequences

- A project installs and updates the framework through the plugin marketplace of this repository.
- Users call each skill with the `wongchon:` namespace, such as `/wongchon:intent`.
- The plugin layout must follow the rules of Claude Code for plugins and marketplaces.

## Confirmation

No check exists yet. The `plugin-skeleton-and-setup` change adds the plugin manifest and the marketplace, and a follow-up task adds `claude plugin validate` to CI. Until then, the maintainer checks the name in the review of each PR.
