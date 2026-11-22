# ADR-0008: Write no code comments by default

Status: `Accepted`

Spec: None

## Context

No check keeps a code comment true, so a comment goes out of date, and agents copy each comment as a pattern into other code. [#11](https://github.com/vasapolrittideah/wongchon/pull/11) first recorded this decision in the roadmap together with the [Code comments](../conventions/code-comments.md) conventions.

## Decision

Code has no comments by default. Each piece of information goes where a test, a check, or a review keeps it true: tests, linter rules and hooks, `ARCHITECTURE.md`, commit messages and PR descriptions, and follow-up tasks. A comment stays only when a tool reads it, such as a linter directive or the doc comment of a public interface.

## Rejected options

| Option | Reason |
| --- | --- |
| Comments for reasons that the code cannot show, as the `ponytail` skill allows | No check keeps them true, and agents copy them as a pattern. |
| `shortcut:` comments for known limits | No check keeps them true, and agents copy them as a pattern. |

## Consequences

- A known limit of the code needs a test and a follow-up task instead of a comment.
- The code comment conventions override the comment rules of the `ponytail` skill.

## Confirmation

No check exists yet. The `plugin-review-gate` change adds a reviewer that enforces the rule, and the build phase adds a check of the new comments in each diff. Until then, the maintainer checks it in the review of each PR.
