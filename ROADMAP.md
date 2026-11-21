# Roadmap

This roadmap states the purpose of `ai-dlc`, its sources, its principles and decisions, and the order of the work. Read it before you plan a change in this repository, so that each session starts with the same context.

## Purpose

`ai-dlc` is a Claude Code plugin that runs an AI-native software development lifecycle (SDLC) in projects of any stack and any business model. An AI-native SDLC is a lifecycle in which AI agents do most of the writing and checking, and people make the decisions at fixed gates.

The maintainer built a working agent workflow in the flowspace-api project, but that workflow depends on Go, a hexagonal architecture, and one product domain. This project takes the parts of that workflow that work in any project, improves them with the sources below, and ships them as a plugin.

The first user is the maintainer, in personal projects with different stacks. The repository is public, but version 1 does not support other users.

## Sources

| Source | What this project takes from it |
| --- | --- |
| [The AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) by Louis Claxton, Anthropic, August 21, 2026 | The 6 stages, 1 committed artifact for each stage, a human gate at the end of each stage, hooks that enforce rules instead of conventions alone, and an eval suite that runs when the agent configuration changes |
| [All Code Is Slop (Except Mine)](https://newsfilter.io/interviews/all-code-is-slop-except-mine-lauren-tan-spacexsi-342ba344fb715c56825bd332d28d494c), a summary of a keynote by Lauren Tan (Poteto), November 14, 2026 | Trust in the environment instead of the agent, the conversion of each correction into a deterministic rule, a clean codebase as the main input of agents, and review of verification artifacts instead of each line of code |
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) by Erik Schluntz and Barry Zhang, Anthropic | The evaluator-optimizer, routing, and parallelization patterns that the review roles of flowspace-api use |
| flowspace-api, a private project of the maintainer | The reference implementation: conventions, review roles, approval stamps, the Git guard, and the build modes. Agents read it but never change it. |
| [agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani, version 0.6.9, MIT License | Engineering skills that this project copies selectively and rewrites for its stages |

The bundled `simple-english` and `humanizer` skills are also sources. [`skills/THIRD_PARTY.md`](skills/THIRD_PARTY.md) lists their versions and licenses.

## Principles

- Each stage commits 1 artifact, and the next stage reads it. The Git history is the audit trail of each change.
- Trust the environment, not the agent. If a rule must always hold, a deterministic check enforces it, such as a hook, a linter, or a CI check. A convention without a check is advice.
- When the maintainer corrects an agent, turn the correction into a rule, and then into a check where a check is possible.
- Expect verification to be most of the work. Lauren Tan reports that verification uses about 70% of the daily tokens of her team. Each stage skill ends with the checks of its own stage, and the maintainer reviews the evidence of the checks.
- A change cannot edit its own checks. Hooks and CI read their checks from `main`, not from the branch that they check.
- Put each instruction where its force matches the rule. Keep always-on context in `AGENTS.md` under 200 lines, put procedures in skills, and enforce each rule that must always hold with a hook or a permission.
- Agents work up to each gate, but they do not pass it. The maintainer approves a gate when they merge its pull request (PR).
- Build each stage by hand on this repository first. If a convention, a template, or a skill causes a problem, write the fix as a follow-up task in the PR description. Then turn these fixes into templates, conventions, and skills. Do not record a lesson that leads to no fix.
- Keep each rule free of a language, a framework, or a cloud provider. A sample project in another stack, under `evals/`, proves this.
- Make the smallest change that does the whole job.

## Decisions

| Topic | Decision | Rejected options |
| --- | --- | --- |
| Distribution | A Claude Code plugin named `ai-dlc`, with a marketplace in this repository | A template that projects copy, because a copy is hard to update to a new version |
| Agents | Claude Code only in version 1. `AGENTS.md` stays free of rules for 1 agent, so that other agents can follow it later. | Claude Code and Codex from the start, because each agent needs its own review runner and hook, and Codex skips project hooks until the user trusts them |
| Scope of version 1 | The intent, design, build, and verify stages. The deploy and maintain stages come after version 1. | All 6 stages, because the deploy and maintain stages depend most on the stack and the cloud provider of a project |
| Stage names | `intent`, `design`, `build`, `verify`, `deploy`, and `maintain`. Approval of the plan is the gate of the build stage. | The names Plan and Test of the playbook, because `plan` is also the name of a skill and verification covers more than tests. A split into 7 stages, because a separate plan stage takes the plan gate away from the build stage. |
| Scripts and hooks | Python 3.9 or later, with the standard library only. Each hook is a separate program that reads JSON from standard input. | Rust or Go binaries, because each platform needs its own binary. Node, because projects in other stacks do not always have it. Python with `uv`, because each user needs `uv`. |
| Git workflow | Trunk-based development, short-lived branches, squash merges by the maintainer only, Semantic Versioning, and release-please | None recorded |
| Skills | Copy the needed skills of agent-skills into this repository and rewrite them for the stages. Do not depend on the agent-skills plugin. Depend on the `ponytail` plugin. Bundle `simple-english` and `humanizer`. | A dependency on the agent-skills plugin, because its own lifecycle competes with the stages in the context of the agent, and its updates change behavior without the evals of this project |
| Prose checks | The `simple-english` and `humanizer` skills for writing, Vale with rules from the conventions of this project, and a writing reviewer for meaning. The writing reviewer comes in the agent workflow phase, and Vale comes in the build phase. | Vale alone, because it cannot judge meaning. The skills alone, because nothing enforces them. The stock Vale styles, because they conflict with the conventions of this project. textlint, write-good, and alex, because they need Node. |
| Git guardrails | The agent uses the GitHub token of the maintainer, so GitHub cannot tell the agent from the maintainer. The `hooks/git_guard.py` hook blocks the commands that only the maintainer runs. A separate identity for the agent comes after version 1. | A separate identity for the agent now, because it is too much setup for 1 maintainer |
| Subagents | The main agent uses read-only subagents for 2 jobs. The first job is research during the work, such as reading documentation or searching code across many files. A subagent returns the answer, its evidence as a file and line or a URL, and the parts that it did not check. The second job is a self-review before the review gate. A self-review only gives advice. | None recorded |
| Review gate | A script runs each review role as a separate, read-only process. The script takes the prompt from the file of the role and the diff from the staged tree, so the main agent cannot change them. If the role approves, the script writes a stamp for the tree, and a hook blocks a commit or a PR that has no stamp. The main agent fixes the findings and sends the change back to the same reviewer, for at most 3 rounds. After the third round, the main agent stops and asks the maintainer. | A subagent as the reviewer of the gate, because the main agent writes its prompt, can skip it, and reports its verdict |
| Language | Agents talk with the maintainer in Thai and write every file in English. | None recorded |

## Phases

Do the phases in this order. A phase starts after the maintainer merges the PRs of the phase before it.

| Phase | Work | Status |
| --- | --- | --- |
| 0. Bootstrap | Conventions for prose, Markdown, branches, commits, PRs, and labels. `AGENTS.md`, `README.md`, the license, and the bundled skills. | Done in [#1](https://github.com/vasapolrittideah/ai-dlc-framework/pull/1) |
| 1. Git guardrails | Deny rules in `.claude/settings.json` and the `hooks/git_guard.py` hook with tests | Done in [#2](https://github.com/vasapolrittideah/ai-dlc-framework/pull/2) |
| 2. Intent | Write the intent of the framework by hand, from an interview with the maintainer. Then turn it into the intent convention, the intent template, and the `intent` skill. Copy and rewrite the skills of this phase from the [Skills from agent-skills](#skills-from-agent-skills) section. | Next |
| 3. Design | Write the design of the framework from its intent. Decide the layout of the plugin and the location of stage artifacts in a project. Read each skill in the Skills from agent-skills section, and confirm or change its phase. Then turn the design into the design convention, template, and skill, and copy and rewrite the skills of this phase. | Planned |
| 4. Agent workflow | Write and approve the plan of the workflow that the Subagents and Review gate decisions describe. Add the research subagent, the self-review, the review script, the approval stamps, the hook that blocks a commit or a PR without a stamp, and the first review roles, such as a code reviewer and a writing reviewer. Copy and rewrite the skills of this phase, which all stages use. Do this phase before the build phase, so that the review gate checks the code of the plugin. | Planned |
| 5. Build | Write and approve the plan. Turn the plan of phase 4 into the plan convention, the plan template, and the `plan` and `build` skills. Create the plugin skeleton, copy and rewrite the skills of this phase, and add Vale, markdownlint, and CI. Add each check in this order: standalone, embedded in a stage skill, chained, and then required on each PR. Make the CI checks required in the ruleset of `main`. | Planned |
| 6. Verify | Add the verify skill, and copy and rewrite the skills of this phase. The verify skill collects end-to-end, property, and differential test results as evidence. Add a commit gate that starts in observe mode before it enforces. Add an eval suite of 20 to 50 real tasks, and evals of the reviewers from past failures. Add the sample project in another stack under `evals/`. Run the evals when a skill, a hook, or `AGENTS.md` changes. | Planned |
| 7. Release of version 1 | Release version 1 with release-please, and write the install steps in `README.md` | Planned |

After version 1, the work continues with these items:

- The deploy and maintain stages
- Support for other agents, such as Codex
- A separate GitHub identity for the agent, such as a bot account or a GitHub App
- Vale rules that target projects can turn on

## Skills from agent-skills

This table proposes the phase in which this project copies and rewrites each skill of agent-skills. The design phase reads each skill and confirms the table. The skills of phase 4 do not belong to 1 stage, because each stage uses them.

| Phase | Skills |
| --- | --- |
| 2. Intent | `interview-me` and `idea-refine` |
| 3. Design | `spec-driven-development`, `api-and-interface-design`, and `documentation-and-adrs` |
| 4. Agent workflow | `source-driven-development`, `doubt-driven-development`, `constraint-driven-development`, and `context-engineering` |
| 5. Build | `planning-and-task-breakdown`, `incremental-implementation`, `test-driven-development`, `debugging-and-error-recovery`, `code-simplification`, `git-workflow-and-versioning`, and `frontend-ui-engineering` |
| 6. Verify | `code-review-and-quality`, `security-and-hardening`, `performance-optimization`, and `browser-testing-with-devtools` |
| After version 1, deploy stage | `shipping-and-launch` and `ci-cd-and-automation` |
| After version 1, maintain stage | `observability-and-instrumentation` and `deprecation-and-migration` |

This project does not copy `using-agent-skills`, because it defines a lifecycle of its own.

## Research in each phase

Start each phase with research, so that the decisions of the phase rest on sources and not on the memory of an agent. Follow these steps:

1. Search for sources about the stage of the phase. Look first at the official documentation of Anthropic and Claude Code, and then at articles by teams that use the practice.
2. Keep a source only if all these conditions hold. A reader can open it without a registration. You read the whole source, not only its summary. It adds a point that the playbook and the keynote of Lauren Tan do not cover.
3. In the artifact of the phase, write a References section. For each source, state what the phase takes from it, and state which parts you read only in a summary.
4. If 2 sources conflict, write the conflict as an open question in the artifact. The maintainer decides it.

Keep only the main sources in the Sources section of this roadmap. The table below lists the sources that agents already read for later phases. Start the research of each phase with them.

| Phase | Sources already read |
| --- | --- |
| 3. Design | [Steering Claude Code](https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more) and [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) |
| 4. Agent workflow | [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) |
| 6. Verify | [How the Claude Code team thinks about verification](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/) and [Building verification loops in Claude Code with skills](https://claude.com/resources/articles/building-verification-loops-in-claude-code-with-skills) |

## Open questions

- Can a Claude Code plugin declare a dependency on another plugin? If it cannot, `README.md` lists the install steps for the `ponytail` plugin.
- Where does a project keep the artifacts of each stage? The design phase decides this.
- Does the design stage use architecture decision records (ADRs)? If it does, move each decision of this roadmap that has rejected options into an ADR, and link the ADR from the Decisions table. The design phase decides this.
- Claude Code has a built-in `/verify` skill. Does the skill of the verify stage keep the name `verify`, or does it get another name? The design phase decides this.

## Changes to this roadmap

- Update this roadmap in the PR that finishes a phase, changes a decision, or answers an open question.
- Keep the details of each stage in the artifacts of the stage. This roadmap only links them.
