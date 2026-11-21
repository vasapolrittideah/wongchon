# Code comment conventions

This convention defines when code has a comment and where the information goes instead. It covers comments, docstrings, and doc comments in code and configuration files of every language, such as Python, shell scripts, and YAML workflows. It excludes Markdown files, third-party files that the project copies with no changes, and generated files. The [English prose](english-prose.md) conventions cover the wording of each comment that this convention allows.

The [Code comments](../../ROADMAP.md#decisions) decision of the roadmap states the reason for this convention: a comment goes out of date because no check keeps it true, and agents copy each comment as a pattern into other code.

## Rules

### Format and content

- Write no comment by default. Put each piece of information in the place that the [Places for information](#places-for-information) table states, where a test, a check, or a review keeps it true.
- Make the code show what it does with names, such as the name of a function, a variable, or a constant, instead of a comment.
- Write a comment only when a tool reads it. Examples are a shebang line, an encoding declaration, a license header that a license tool requires, a type checker pragma, and a linter directive.
- Write a docstring or a doc comment only on a public interface whose documentation a tool generates or shows, such as API reference pages or the help text of a command. State what the interface does and its contract.
- In a linter directive that turns off a check, such as `# noqa` or `eslint-disable`, name each rule that it turns off. The directive lowers the quality bar, so state the reason in the PR description.
- Do not explain what the code does, why it does it, its history, a known limit, or work for later in a comment.
- Do not write a marker for later work, such as `TODO`, `FIXME`, `HACK`, or `shortcut:`.
- Do not leave code in a comment. Git keeps the old code.

### Workflow

- If you take a shortcut that has a known limit, write a test that fails when the limit changes. Then write the limit and when to remove it as a follow-up task in the PR description.
- If a reason states a rule that must always hold, add a check for the rule, such as a linter rule or a hook. If no check is possible yet, write the check as a follow-up task in the PR description.

### Changes

- Apply this convention to new code and to each file that a later PR changes. In that PR, move the information of each comment in the file to its place, and delete each comment that this convention does not allow.

## Differences from the ponytail skill

The [`ponytail`](https://github.com/DietrichGebert/ponytail/blob/v5.3.2/skills/ponytail/SKILL.md) skill, version 5.3.2, sets the rules for the size of a change, but this convention applies where the skill and this convention differ.

- Write no comment for a reason, as the [Format and content](#format-and-content) rules state. The skill lets you write the reason that the code cannot show in a comment of 1 line.
- Write a known limit as a test and a follow-up task, as the [Workflow](#workflow) rules state. The skill writes the limit in a comment in the form `shortcut: <the limit>, <when to upgrade>`.

## Reference

### Places for information

| Information | Place |
| --- | --- |
| What the code does | The names in the code, and the tests |
| A behavior, a limit, or an edge case of the code | A test that fails when the behavior changes |
| A rule that the code must always follow | A linter rule, a hook, or a CI check |
| A reason for the structure of the project, or a rule for its parts | `ARCHITECTURE.md` |
| A reason for a change, or a fact that the work found, such as a limit of a tool | The commit message and the PR description |
| Work for later, such as the removal of a shortcut | The Follow-up tasks of the PR description, or an Issue |
| The contract of a public interface | A docstring or a doc comment that a documentation tool reads |

## Examples

This code does not follow the convention. It explains a known limit in a comment, which the [Format and content](#format-and-content) rules forbid:

```python
def read_rows(path):
    # shortcut: reads only the first 1000 rows, page through the file when files grow
    return load(path)[:1000]
```

This code and its test follow the convention. The constant names the limit, the test fails when the limit changes, and the PR description lists the paging work as a follow-up task:

```python
MAX_ROWS = 1000


def read_rows(path):
    return load(path)[:MAX_ROWS]


def test_read_rows_stops_at_max_rows(tmp_path):
    path = write_rows(tmp_path, MAX_ROWS + 1)
    assert len(read_rows(path)) == MAX_ROWS
```

This linter directive follows the convention, because a tool reads it and it names the rule that it turns off:

```python
from .models import *  # noqa: F403
```
