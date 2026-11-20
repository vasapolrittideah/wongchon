# English prose conventions

This convention defines how to write English prose in the text that this project writes. It covers Markdown files, code comments in every language, commit messages, pull request and Issue text, and the skills, agents, and templates of this project. It excludes third-party files that the project copies with no changes, generated files, string values in code and configuration, and replies in chat. The [Markdown](markdown.md) conventions cover the format of Markdown text.

## Rules

### Format and content

- Use American spelling, such as "color", "organize", and "center" instead of "colour", "organise", and "centre".
- Use straight quotation marks (`"`) and straight apostrophes (`'`). Do not use curly ones (`“`, `”`, `‘`, and `’`).
- Put a word or a phrase that you quote from prose in double quotation marks, such as "This commit adds".
- Write each number with numerals, such as 3 or 11, and not as a word, such as "three" or "eleven". If a number starts a sentence, reorder the sentence so that it starts with another word. Keep "one" when it is a pronoun and not a count, such as in "each one" or "no one". Keep ordinal words, such as "first" or "second".
- In code comments, keep the comment syntax and each marker that a tool reads. Examples are a doc-comment tag, a symbol name that a documentation tool requires at the start, and a linter directive.
- When you edit prose, keep code, identifiers, commands, file paths, tool directives, template placeholders, and quoted output unchanged.
- Aim for the sentence limits of the `simple-english` skill: 25 words for a descriptive sentence and 20 words for a procedural sentence, which tells the reader what to do. If a longer sentence is clearer than 2 short ones, keep it.
- Write 1 idea in each paragraph. If a sentence depends on an earlier sentence, such as through "so", "but", or "this approach", keep both sentences in the same paragraph. Start a new paragraph for each new idea, such as a limit, a rejected option, or a decision.

### Workflow

- Before you write English prose, read the [`simple-english`](../../skills/simple-english/SKILL.md) skill and the [`humanizer`](../../skills/humanizer/SKILL.md) skill. An agent reads them once in each session, and again when a skill file changes.
- Write the text with these steps:
  1. Write the text with the `simple-english` skill in Plain mode.
  2. Edit the text with the `humanizer` skill so that it reads naturally. Do not add a fact, name, number, date, or quote that the source or the user did not give.
  3. Make sure that the text follows the `simple-english` skill.
- If 2 rules conflict, apply the rule that comes first in this order:
  1. The rules of another convention for the artifact, and the formats that a tool requires. Examples are a template heading, the subject format of a commit message, and an attribution line that an agent harness adds.
  2. The rules in this convention.
  3. The `simple-english` skill.
  4. The `humanizer` skill.

### Changes

- Apply this convention to the text that you add or change. If you change part of a paragraph or a bullet, make the whole paragraph or bullet follow this convention. Do not change other text only to make it follow this convention, unless the PR exists for that change.

## Skills, agents, and templates

An AI agent reads the text of a skill, an agent, or a template as instructions. Write this text as procedural text, and follow the [Instructions for AI agents](../../skills/simple-english/references/use-cases.md#instructions-for-ai-agents-prompts-agentsmd-skills) section of the `simple-english` use cases.

- Apply this convention to the `description` field in the frontmatter of a skill or an agent, although it is a YAML string. An agent reads the field to decide when to use the skill or the agent.

## Differences from the simple-english skill

The [`simple-english`](../../skills/simple-english/SKILL.md) skill, version 2.1.2, sets the rules for English prose, but this convention applies where the skill and this convention differ.

- Treat the sentence limits as aims, as the [Format and content](#format-and-content) rules state. The skill treats them as maximums and splits each longer sentence.
- Write numbers with numerals, as the Format and content rules state. The skill has no rule for numbers, and its own text writes small numbers as words, such as "three or more".

## Differences from the humanizer skill

The [`humanizer`](../../skills/humanizer/SKILL.md) skill, version 4.0.0, sets the rules for the editing step, but this convention applies where the skill and this convention differ.

- Do not add a fact that the source or the user did not give, as the [Workflow](#workflow) rules state. The skill lets you add a specific detail that you know to be true when the text is generic.
