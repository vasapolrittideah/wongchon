# Roadmap

This roadmap states the purpose of `wongchon`, its sources, its principles and decisions, and the order of the work. Read it before you plan a change in this repository, so that each session starts with the same context.

## Purpose

`wongchon` is a Claude Code plugin that runs an AI-native software development lifecycle (SDLC) in projects of any stack and any business model. An AI-native SDLC is a lifecycle in which AI agents do most of the writing and checking, and people make the decisions at fixed gates.

The maintainer built a working agent workflow in the flowspace-api project, but that workflow depends on Go, a hexagonal architecture, and one product domain. This project takes the parts of that workflow that work in any project, improves them with the sources below, and ships them as a plugin.

The first user is the maintainer, in personal projects with different stacks. The repository is public, but version 1 does not support other users.

## Version 1

Version 1 succeeds when these results are true:

- The maintainer installs the plugin in a greenfield personal project that uses a stack other than Go. A greenfield project is a new project that has no code yet.
- In that project, 1 real change goes through the stages from intent to verify, and nobody edits a file of the plugin during the change.
- The eval suite of the plugin passes.

The review time of the maintainer is the main limit of version 1. Each gate must be a decision that the maintainer can take from a short artifact and the evidence of its checks. A higher use of tokens is acceptable when it saves review time. The design of each change must not assume that a project has no code or no documents, so that support for brownfield projects can come after version 1.

## Sources

| Source | What this project takes from it |
| --- | --- |
| [The AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) by Louis Claxton, Anthropic, August 21, 2026 | The 6 stages, 1 committed artifact for each stage, a human gate at the end of each stage, hooks that enforce rules instead of conventions alone, and an eval suite that runs when the agent configuration changes |
| [All Code Is Slop (Except Mine)](https://newsfilter.io/interviews/all-code-is-slop-except-mine-lauren-tan-spacexsi-342ba344fb715c56825bd332d28d494c), a summary of a keynote by Lauren Tan (Poteto), November 14, 2026 | Trust in the environment instead of the agent, the conversion of each correction into a deterministic rule, a clean codebase as the main input of agents, code without comments, because comments go out of date and agents copy them, and review of verification artifacts instead of each line of code |
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) by Erik Schluntz and Barry Zhang, Anthropic | The evaluator-optimizer, routing, and parallelization patterns that the review roles of flowspace-api use |
| flowspace-api, a private project of the maintainer | The reference implementation: conventions, review roles, approval stamps, the Git guard, and the build modes. Agents read it but never change it. |
| [agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani, version 0.6.17, MIT License | Engineering skills that this project copies selectively and rewrites for its stages |

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
- The framework fixes the rules, and each project follows them. A project cannot change a convention, a stage, or the path of a framework document. `.wongchon/config.json` holds only facts that the framework cannot know, such as the commit scopes and the build and test commands of the project.
- Each rule in `ARCHITECTURE.md` needs a deterministic check in the stack of the project, such as a linter rule or a dependency check. The framework cannot write these checks, because it does not know the stack. Its reviewers ask for a check when a rule has none.
- Use trunk-based development with short-lived branches, squash merges by the maintainer only, Semantic Versioning, and release-please.
- Give research and self-review to read-only subagents. A research subagent returns the answer, its evidence as a file and line or a URL, and the parts that it did not check. A self-review before the review gate only gives advice.
- Talk with the maintainer in Thai, and write every file in English.
- Make the smallest change that does the whole job.

## Decisions

Each decision of this project that rejects options is an architecture decision record (ADR) in `docs/adrs/`. This table links each ADR.

| Topic | Decision | ADR |
| --- | --- | --- |
| Distribution | The framework is a Claude Code plugin named `wongchon`, with a marketplace in this repository. | [ADR-0001](docs/adrs/0001-distribute-as-the-wongchon-plugin.md) |
| Agents | Version 1 supports only Claude Code, and `AGENTS.md` stays free of rules for 1 agent. | [ADR-0002](docs/adrs/0002-support-only-claude-code-in-version-1.md) |
| Scope of version 1 | Version 1 covers the intent, design, build, and verify stages in greenfield projects. | [ADR-0003](docs/adrs/0003-cover-4-stages-in-greenfield-projects.md) |
| Stage names | The stages are `intent`, `design`, `build`, `verify`, `deploy`, and `maintain`. | [ADR-0004](docs/adrs/0004-name-the-stages.md) |
| Scripts and hooks | Scripts and hooks use Python 3.9 or later with the standard library only. | [ADR-0005](docs/adrs/0005-write-scripts-and-hooks-in-python.md) |
| Skills | The project copies and rewrites the skills of agent-skills, and the plugin depends on `ponytail`. | [ADR-0006](docs/adrs/0006-copy-agent-skills-and-depend-on-ponytail.md) |
| Prose checks | Prose is written with `simple-english` and `humanizer` and checked with Vale and a writing reviewer. | [ADR-0007](docs/adrs/0007-check-prose-with-skills-vale-and-a-reviewer.md) |
| Code comments | Code has no comments by default, except the comments that a tool reads. | [ADR-0008](docs/adrs/0008-write-no-code-comments-by-default.md) |
| Git guardrails | The `hooks/git_guard.py` hook blocks the commands that only the maintainer runs. | [ADR-0009](docs/adrs/0009-block-maintainer-commands-with-a-git-guard.md) |
| Review gate | A script runs each review role as a separate process, and a hook blocks a commit or a PR without its stamp. | [ADR-0010](docs/adrs/0010-run-review-roles-in-a-review-script.md) |
| Project documents | A project has `AGENTS.md`, `CONSTRAINTS.md`, and `ARCHITECTURE.md` at its root, and `GLOSSARY.md` after its first term of the domain. | [ADR-0011](docs/adrs/0011-require-4-project-documents.md) |
| Stage artifacts | Each kind of stage artifact has its own folder, such as `docs/specs/`, and all files of 1 change share its name. | [ADR-0012](docs/adrs/0012-keep-1-folder-for-each-kind-of-artifact.md) |
| Decision records | The design stage records each decision that rejects options in an ADR, which the merge of its PR accepts. | [ADR-0013](docs/adrs/0013-record-decisions-in-adrs.md) |
| Small changes | A change of 1 PR that changes no ADR, `ARCHITECTURE.md`, or `CONSTRAINTS.md` starts at the build stage. | [ADR-0014](docs/adrs/0014-start-small-changes-at-the-build-stage.md) |
| Setup command | A project runs `/wongchon:setup` 1 time to write `.wongchon/config.json` and `AGENTS.md` and to create the labels. | [ADR-0015](docs/adrs/0015-set-up-a-project-with-wongchon-setup.md) |
| Stage gate | A `Stage gate` CI job fails while an intent, a spec, or a plan of the PR is not `Approved`. | [ADR-0016](docs/adrs/0016-block-unapproved-artifacts-with-a-stage-gate.md) |
| Plugin layout | The plugin lives in `plugin/`, and the marketplace at the root points to it. | [ADR-0017](docs/adrs/0017-keep-the-plugin-in-a-plugin-folder.md) |
| Stage skill names | Each stage skill has the name of its stage, such as `/wongchon:verify`. | [ADR-0018](docs/adrs/0018-name-each-skill-after-its-stage.md) |
| Change names | Each change has the name `<scope>-<capability>`, such as `design-specs-and-adrs`. | [ADR-0019](docs/adrs/0019-name-each-change-after-its-scope-and-capability.md) |
| Changes of this repository | From phase 3, each phase of this roadmap is 1 change or more, with its own intent, spec, plan, and evidence. | [ADR-0020](docs/adrs/0020-split-version-1-into-1-change-for-each-phase.md) |

## Phases

Do the phases in this order. A phase starts after the maintainer merges the PRs of the phase before it.

| Phase | Work | Change | Status |
| --- | --- | --- | --- |
| 0. Bootstrap | Conventions for prose, Markdown, branches, commits, PRs, and labels. `AGENTS.md`, `README.md`, the license, and the bundled skills. | None | Done in [#1](https://github.com/vasapolrittideah/wongchon/pull/1) |
| 1. Git guardrails | Deny rules in `.claude/settings.json` and the `hooks/git_guard.py` hook with tests. As extra work before phase 3, a minimal CI gate runs the checks of `AGENTS.md` and the PR metadata check of `scripts/check_pr_metadata.py`, which checks the title and the description, on each PR, so that the result does not depend on the report of the agent. | None | Done in [#2](https://github.com/vasapolrittideah/wongchon/pull/2) and [#10](https://github.com/vasapolrittideah/wongchon/pull/10) |
| 2. Intent | Write the intent of the framework by hand, from an interview with the maintainer. Then turn it into the intent convention, the intent template, and the `intent` skill. Copy and rewrite the skills of this phase from the [Skills from agent-skills](#skills-from-agent-skills) section. | None | Done in [#5](https://github.com/vasapolrittideah/wongchon/pull/5), [#7](https://github.com/vasapolrittideah/wongchon/pull/7), [#8](https://github.com/vasapolrittideah/wongchon/pull/8), and [#9](https://github.com/vasapolrittideah/wongchon/pull/9) |
| 3. Design | Write the intent of the change, and then its spec. Plan the layout of the plugin, which is the planned project structure of this repository, and decide the location of stage artifacts in a project. Read each skill in the Skills from agent-skills section, and confirm or change its phase. Then turn the spec into the spec convention and template and the `design` skill, and copy and rewrite the skills of this phase. The [spec](docs/specs/design-specs-and-adrs.md#order-of-the-work) lists the PRs of this phase. | `design-specs-and-adrs` | In progress |
| 4. Agent workflow | Write and approve the plan of the workflow that the subagent principle and the Review gate decision describe. Add the research subagent, the self-review, the review script, the approval stamps, the hook that blocks a commit or a PR without a stamp, and the first review roles, such as a code reviewer and a writing reviewer. Stop a PR from editing its own checks: a `pull_request` workflow runs from the branch of the PR, so a PR can change the CI that checks it, which breaks the principle "A change cannot edit its own checks". Research the options first, such as required workflows in a ruleset and required review of each change to `.github/workflows/**`. Copy and rewrite the skills of this phase, which all stages use. Do this phase before the build phase, so that the review gate checks the code of the plugin. | `plugin-review-gate` | Planned |
| 5. Build | Write and approve the plan of each change. In `build-plans-and-tasks`, turn the plan of phase 4 into the plan convention, the plan template, and the `plan` and `build` skills, and add the CI checks of small changes. In `plugin-skeleton-and-setup`, create the plugin skeleton in `plugin/`, move the skills, hooks, scripts, and conventions into it, and add the setup command. Then copy and rewrite the skills of this phase, and add Vale, markdownlint, a check of the new code comments in each diff, and the other CI checks. After the plugin layout exists, write `ARCHITECTURE.md` from the reasons and rules of the design. Add each check in this order: standalone, embedded in a stage skill, chained, and then required on each PR. Make the CI checks required in the ruleset of `main`. | `plugin-skeleton-and-setup` and `build-plans-and-tasks` | Planned |
| 6. Verify | Add the verify skill, and copy and rewrite the skills of this phase. The verify skill collects end-to-end, property, and differential test results as evidence. Add a commit gate that starts in observe mode before it enforces. Add an eval suite of 20 to 50 real tasks, and evals of the reviewers from past failures. Add the sample project in another stack under `evals/`. Run the evals when a skill, a hook, or `AGENTS.md` changes. | `verify-evidence-and-evals` | Planned |
| 7. Release of version 1 | Release version 1 with release-please, and write the install steps in `README.md` | Decided in phase 7 | Planned |

After version 1, the work continues with these items:

- The deploy and maintain stages
- Support for brownfield projects
- Support for other agents, such as Codex
- A separate GitHub identity for the agent, such as a bot account or a GitHub App
- Vale rules that target projects can turn on

## Skills from agent-skills

This table states the phase in which this project copies and rewrites each skill of agent-skills. The design phase read each skill at version 0.6.17 and confirmed the table. The skills of phase 4 do not belong to 1 stage, because each stage uses them.

| Phase | Skills |
| --- | --- |
| 2. Intent | `interview-me` and `idea-refine` |
| 3. Design | `spec-driven-development`, `api-and-interface-design`, `documentation-and-adrs`, and `constraint-driven-development` |
| 4. Agent workflow | `source-driven-development`, `doubt-driven-development`, and `context-engineering` |
| 5. Build | `planning-and-task-breakdown`, `incremental-implementation`, `test-driven-development`, `debugging-and-error-recovery`, `code-simplification`, `git-workflow-and-versioning`, and `frontend-ui-engineering` |
| 6. Verify | `code-review-and-quality`, `security-and-hardening`, `performance-optimization`, `browser-testing-with-devtools`, and `accessibility-engineering` |
| After version 1, deploy stage | `shipping-and-launch` and `ci-cd-and-automation` |
| After version 1, maintain stage | `observability-and-instrumentation` and `deprecation-and-migration` |

- Copy only the parts of `spec-driven-development` about how to build a change, because the intent states what the change must achieve.
- Copy only the ADR part of `documentation-and-adrs`. The [Code comments](#decisions) decision replaces its rules for comments.
- Copy `constraint-driven-development` in the design phase, because it writes `CONSTRAINTS.md`. The review gate of phase 4 uses its check of a lowered quality bar.
- Keep `planning-and-task-breakdown` in the build phase, because the approval of the plan is the gate of the build stage.
- Do not copy `using-agent-skills`, because it defines a lifecycle of its own.

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

- How does a brownfield project move its project documents into the paths of the framework? This question waits until after version 1.
- Does a link with `${CLAUDE_PLUGIN_ROOT}` in a skill open a convention outside the folder of the skill? The documentation implies it, but nobody tested it. The `plugin-skeleton-and-setup` change tests it.
- Does Claude Code install the `ponytail` plugin from another marketplace as a dependency, as the documentation states? The `plugin-skeleton-and-setup` change tests it.
- How does the CI of a project run the checks of the plugin, such as the `Stage gate` job? The `plugin-skeleton-and-setup` change decides this. A possible answer is a workflow that the setup command writes, which checks out this repository at the installed version.

## Changes to this roadmap

- Update this roadmap in the PR that finishes a phase, changes a decision, or answers an open question.
- Keep the details of each stage in the artifacts of the stage. This roadmap only links them.
