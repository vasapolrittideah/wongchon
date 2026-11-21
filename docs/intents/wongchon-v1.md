# Intent: wongchon version 1

Author: Vasapol Rittideah

Status: `Approved`

## Problem

The maintainer has a working agent workflow in the flowspace-api project, but the workflow depends on Go, a hexagonal architecture, and 1 product domain. The next personal project of the maintainer is a new project in another stack, and the flowspace-api workflow does not work there. Without a framework, the maintainer must build the workflow again for each project.

## Outcome

`wongchon` is a Claude Code plugin that the maintainer installs in each personal project. The [Roadmap](../../ROADMAP.md) states its purpose, principles, and decisions. Version 1 has these results:

- Each change goes through the intent, design, build, and verify stages. The maintainer approves the gate of each stage when they merge its pull request (PR).
- Agents get the context of each project from the project documents that the framework requires. `ARCHITECTURE.md` at the root is one of them.
- A change has these files: an intent, a design with architecture decision records (ADRs) when the design rejects options, a plan, the code and its tests, and the verification evidence. The evidence is a committed file. The Verification section of the PR summarizes the evidence and links the file.
- A small change that fits in 1 PR skips the intent and design stages and starts at the build stage. It still goes through the review gate and the verify stage.
- A setup command, which a project runs 1 time, creates `.wongchon/config.json` with the facts that the framework cannot know, such as the commit scopes and the build and test commands. It also installs the hooks of the framework. It does not create `ARCHITECTURE.md`, because a greenfield project writes that file after the build. A greenfield project is a new project that has no code yet.

## Success criteria

- The maintainer installs the plugin in a greenfield personal project that uses a stack other than Go.
- In that project, 1 real change goes through the stages from intent to verify, and nobody edits a file of the plugin during the change.
- The eval suite of the plugin passes.

## Affected users and systems

- The maintainer is the only user, in personal projects with different stacks.
- Claude Code is the only agent that runs the plugin.
- GitHub holds the PRs whose merges approve the gates, and the CI checks of each project.
- Each target project holds its stage artifacts, its project documents, its `.wongchon/config.json` file, and the checks of the rules in its `ARCHITECTURE.md`.
- This repository holds the source of the plugin and the sample project of the eval suite.
- The flowspace-api project is the reference implementation. Agents read it but never change it.

## Constraints

- The review time of the maintainer is the main limit. Make each gate a decision that the maintainer can take from a short artifact and the evidence of its checks.
- Accept a higher use of tokens when it saves review time. In the study of spec-driven development in the References section, 1 team reported 2 to 3 times the tokens of its earlier work.
- Do not assume in the design that a project has no code or no documents, so that support for brownfield projects can come after version 1. A brownfield project is an existing project that has code and documents.
- Follow the Principles and Decisions sections of the roadmap. They fix, for example, the agent, the language of scripts, and the rule that a project cannot change a convention, a stage, or a framework path.

## Out of scope

- Brownfield projects in version 1. The Project documents decision of the roadmap still states how a brownfield project moves its architecture document later.
- The deploy and maintain stages, agents other than Claude Code, and a separate GitHub identity for the agent, as the roadmap states.
- Users other than the maintainer.

## Open questions

The design phase decides these questions:

- Where does a project keep the artifacts of each stage? The design phase can choose 1 folder for each kind of artifact, such as `docs/intents/`, or 1 folder for each change that holds all its files. This intent uses `docs/intents/` until the design phase decides.
- Which deterministic rule decides that a change is small enough to start at the build stage?
- Which project documents does the framework require besides `ARCHITECTURE.md`? The roadmap lists this question.
- What are the name and the steps of the setup command?
- Who changes the status of an intent to `Approved`, and which CI check blocks the merge of an intent that has another status?

## Answers

| Question | Reply |
| --- | --- |
| What tells you that version 1 succeeded? | The maintainer installs the plugin in another personal project in a stack other than Go, and takes at least 1 real change from intent to verify without editing the plugin during the change. The eval suite passes. |
| Which real project uses version 1 first, and is it greenfield or brownfield? | A new personal project in a stack other than Go, with no code yet and no deadline. |
| Does version 1 support brownfield projects, or can that wait? | It can wait until after version 1, because the first project is greenfield. The design of version 1 must not assume that a project has no code or no documents. |
| Can a small change skip stages? | Yes. A small change that fits in 1 PR skips the intent and design stages and starts at the build stage. It still goes through the review gate and the verify stage. The design phase writes the rule that decides which changes are small. |
| Is the verification evidence a committed file, or only text in the PR? | A committed file, so that the verify stage has its own artifact. The Verification section of the PR summarizes the evidence and links the file. The design phase decides where the file goes. |
| Does version 1 have a setup command that a project runs 1 time? | Yes. It creates `.wongchon/config.json` from the facts of the project and installs the hooks. It does not create `ARCHITECTURE.md`. The design phase decides its name and steps. |
| What is the main constraint of the framework? | The review time of the maintainer, not the cost of tokens. Each gate must be a decision from a short artifact and the evidence of its checks. |
| Where does this first intent go until the design phase decides the location of stage artifacts? | In `docs/intents/`, 1 folder for the intents. |
| Does an intent have a status? | Yes. An intent has an Author line and a Status line, and a CI check blocks the merge of an intent until its status is `Approved`. |

## References

| Source | What this intent takes from it | Parts read only in a summary |
| --- | --- | --- |
| The Plan stage of [The AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) | The fields of an intent: the problem, the outcome, the affected users and systems, the constraints, and the open questions. Also the Author and Status lines, and the merge as the gate. | None |
| [`interview-me`](https://github.com/addyosmani/agent-skills/blob/main/skills/interview-me/SKILL.md) of agent-skills, version 0.6.9 | The interview with 1 question at a time and a guess for each answer, and the Success criteria and Out of scope sections | None |
| The Brainstorm with Claude first section of [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) | An interview that ends in a spec file, and a new session that builds from the file, so that the build starts with a clean context | The sections after Steer the session |
| [Spec-Driven Development as Prescribed and as Practiced](https://arxiv.org/abs/2608.25202) by Agarwal and others, 2026 | Keep what to build in the intent, and how to build it in the design and the plan, because implementation detail makes a spec go out of date sooner. Most practitioners skip specs for small tasks, but no team in the study had a rule for which changes need a spec. A person writes or approves the acceptance criteria, and 1 agent does not write the spec, the code, and the tests. | Appendices B to J |
