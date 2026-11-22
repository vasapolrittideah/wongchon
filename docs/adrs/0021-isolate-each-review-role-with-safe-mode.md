# ADR-0021: Isolate each review role with safe mode and read-only tools

Status: `Accepted`

Spec: [`docs/specs/plugin-review-gate.md`](../specs/plugin-review-gate.md)

## Context

[ADR-0010](0010-run-review-roles-in-a-review-script.md) runs each review role as a separate, read-only process, so that the main agent cannot change its prompt or its verdict. The intent of the change requires the subscription login of the maintainer and no API key. Without other flags, `claude -p` loads the hooks, the plugins, and `CLAUDE.md` of the project, and the bare mode, which skips them, accepts only an API key.

## Decision

The review script runs each role with `claude -p --safe-mode`, the tools `Read`, `Grep`, and `Glob` only, and the permission mode `dontAsk`. Safe mode turns off hooks, plugins, skills, MCP servers, and `CLAUDE.md`, and it keeps the normal login. The script reads the role file from the default branch on `origin`, not from the working tree, and gives the diff or the PR text on standard input.

## Rejected options

| Option | Reason |
| --- | --- |
| `--bare` | It needs an API key, and the intent rules out an API key. |
| `--settings '{"disableAllHooks": true}'` alone | It turns off hooks, but the reviewer still loads the plugins and `CLAUDE.md` of the project. |
| A subagent of the main agent, as the code review article of the Claude Code team uses | The main agent writes its prompt, can skip it, and reports its verdict, as ADR-0010 states. |
| The role file from the working tree | A change could then edit its own reviewer. |

## Consequences

- The reviewer cannot run commands, so it gets the diff from the script instead of `git diff`.
- The reviewer reads the conventions and the files of the project with `Read`, `Grep`, and `Glob`.
- A change to a role file takes effect only after it merges into the default branch.

## Confirmation

An integration test of the review script starts a real review whose role tries to write a file and a stamp, and it fails when either one changes.
