# ADR-0005: Write scripts and hooks in Python with the standard library

Status: `Accepted`

Spec: None

## Context

The scripts and hooks of the framework must run in projects of any stack and on each platform, without an extra install for each user. [#3](https://github.com/vasapolrittideah/wongchon/pull/3) first recorded this decision in the roadmap.

## Decision

Each script and hook uses Python 3.9 or later, with the standard library only. Each hook is a separate program that reads JSON from standard input.

## Rejected options

| Option | Reason |
| --- | --- |
| Rust or Go binaries | Each platform needs its own binary. |
| Node | Projects in other stacks do not always have it. |
| Python with `uv` | Each user needs `uv`. |

## Consequences

- A project needs only Python 3.9 or later to run the hooks and checks of the framework.
- A script cannot use a third-party package, such as a YAML parser.

## Confirmation

The CI workflow in `.github/workflows/ci.yml` runs the tests of `hooks/` and `scripts/` on Python 3.9 and on the latest Python. No check yet blocks an import of a third-party package. A follow-up task adds it.
