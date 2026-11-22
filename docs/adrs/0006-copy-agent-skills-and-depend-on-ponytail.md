# ADR-0006: Copy and rewrite the skills of agent-skills, and depend on ponytail

Status: `Accepted`

Spec: None

## Context

The framework needs engineering skills, such as an interview and a spec workflow, and agent-skills has them. The agent-skills plugin also has its own lifecycle, and its updates change the behavior of its skills. [#3](https://github.com/vasapolrittideah/wongchon/pull/3) first recorded this decision in the roadmap, and [#14](https://github.com/vasapolrittideah/wongchon/pull/14) added how the plugin depends on `ponytail`.

## Decision

The project copies the needed skills of agent-skills into this repository and rewrites them for the stages, as `skills/THIRD_PARTY.md` states. The plugin does not depend on the agent-skills plugin. It depends on the `ponytail` plugin through the `dependencies` field of `plugin.json`, and the marketplace of this repository lists the marketplace of `ponytail` in `allowCrossMarketplaceDependenciesOn`. The plugin bundles the `simple-english` and `humanizer` skills.

## Rejected options

| Option | Reason |
| --- | --- |
| A dependency on the agent-skills plugin | Its own lifecycle competes with the stages in the context of the agent, and its updates change behavior without the evals of this project. |

## Consequences

- `skills/THIRD_PARTY.md` records the source, version, commit, license, and changes of each copied skill.
- An update of a copied skill is a manual comparison with the upstream release.

## Confirmation

No check exists yet. A follow-up task adds a check that each folder of a third-party skill has a row in `skills/THIRD_PARTY.md` and a `LICENSE` file. The `plugin-skeleton-and-setup` change tests the dependency on `ponytail`.
