# ai-dlc

`ai-dlc` is a Claude Code plugin that runs an AI-native software development lifecycle in projects of any stack. It takes each change through 6 stages, and each stage has a gate that the change must pass before the next stage starts.

## Stages

| Stage | Covers | Version |
| --- | --- | --- |
| Intent | The intent of a change | 1 |
| Design | The design of a change | 1 |
| Build | Plans and implementation. Approval of the plan is the gate of this stage. | 1 |
| Verify | Tests, builds, visual checks, and evals | 1 |
| Deploy | Deployment | Later |
| Maintain | Maintenance after deployment | Later |

## Status

You cannot install the plugin yet. This repository holds its conventions and agent instructions, and the install steps come when the first stages work. The plugin will need the `ponytail` plugin, which you install separately.

## Repository layout

| Path | Contents |
| --- | --- |
| `AGENTS.md` | Instructions for agents that work in this repository. `CLAUDE.md` is a link to it. |
| `docs/conventions/` | Conventions for the artifacts that the plugin writes. The plugin ships these files. |
| `skills/` | Third-party skills that the plugin bundles |
| `hooks/` | Hook scripts. `git_guard.py` blocks the Git and GitHub CLI commands that only the maintainer runs. |
| `.claude/settings.json` | Claude Code settings of this repository, which run the Git guard before each shell command |
| `.ai-dlc/config.json` | Settings of this repository for the plugin, such as the commit scopes |
| `.github/pull_request_template.md` | The template for pull request descriptions |

## Contributing

Follow the [repository instructions](AGENTS.md). The maintainer reviews and squash merges each pull request.

## Credits

- The [AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) from Anthropic is the source of the lifecycle and its stages.
- The plugin will adapt some skills of [agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani.
- The bundled `simple-english` and `humanizer` skills come from other projects. [`skills/THIRD_PARTY.md`](skills/THIRD_PARTY.md) lists their sources, versions, and licenses.

## License

This project uses the MIT License, and the [`LICENSE`](LICENSE) file holds its text. Each bundled third-party skill keeps the license of its source project.
