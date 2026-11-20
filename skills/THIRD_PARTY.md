# Third-party skills

This file lists each skill in `skills/` that comes from another project. Each skill keeps the license of its source project.

## Skills

| Skill | Source | Version | Commit | License | Files copied | Changes |
| --- | --- | --- | --- | --- | --- | --- |
| `simple-english` | [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) | `v2.1.2` | `300432a9e4c473229a7049ab61b8ca2522d9214c` | MIT, Copyright (c) 2026 AminBlg | `skills/simple-english/` and `LICENSE` | None |
| `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) | `v4.0.0` | `b48c832f0f809c1b5658edbb838c2521b72f2413` | MIT, Copyright (c) 2025 Siqi Chen | `SKILL.md` and `LICENSE` | None |

## Rules

- Copy the files of a skill from the commit of a release tag, and keep its `LICENSE` file next to its `SKILL.md` file.
- If a skill works for this project as it is, do not edit its files. If a rule of this project differs from the skill, write the difference in the convention that uses the skill.
- If a skill must read or write the artifacts of this project, edit its files directly. In the `Changes` column of its row, summarize the changes.
- To update an unchanged skill, copy the files of the new release. To update an edited skill, compare the commit in its row with the new release, and apply the upstream changes that this project needs. In both cases, update its row in this file in the same commit.
- Claude Code loads each skill in this repository through a symbolic link in `.claude/skills/`, which points to the skill folder in `skills/`.
