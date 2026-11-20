# Markdown conventions

This convention defines the format of Markdown text in this project. It covers Markdown files, which include the skills, agents, and templates of this project. It also covers GitHub text, which is the text of pull requests, Issues, and their comments. It excludes commit messages, code comments, third-party files that the project copies with no changes, generated files, and replies in chat. The [English prose](english-prose.md) conventions cover the wording.

## Rules

### Format and content

- Keep each paragraph and list item on 1 physical line, regardless of length. Do not hard-wrap Markdown text.
- Write headings in sentence case. Keep the capitals of names, abbreviations, and the fixed headings that a template defines.
- Number the items of every numbered list with Arabic numerals that start at 1 and go up by 1, such as `1.`, `2.`, and `3.`. Do not use Roman numerals or letters, such as `i.`, `ii.`, or `a.`. Apply this rule to the source text. GitHub shows a numbered list inside a bullet with Roman numerals, and that display follows this rule.
- Put code, identifiers, file paths, commands, field names, and GitHub labels in backticks. If a reader types a value or a system reads it exactly, also put the value in backticks. Examples are a status value and a configuration value. Use backticks only for these items.
- Use bullets for 2 or more rules, checks, choices, or facts that readers can follow independently. To test the choice, remove or reorder the items. If each remaining item is still clear, use bullets. If there is only 1 item, write a paragraph.
- If a paragraph states the result or the context that all bullets of a list share, put it directly before the list. Do not write more than 1 such paragraph for a list.
- Give each bullet 1 main point. Keep its conditions, explanations, and exceptions in the same bullet, even when it takes several sentences.
- Use a numbered list when readers must follow steps in order or apply rules by precedence.
- If each item has the same 2 or more attributes, such as a name and a meaning, use a table instead of bullets.
- Do not put product names or ordinary words in backticks, such as PostgreSQL or Issue.
- Do not use bold or italic text.
- Do not put a bullet list inside another list. Only a numbered list can go inside a bullet.

### Links and tracking

- Link a reference only when both conditions hold. The reader needs the target to understand the text or to make sure that it is correct. The reader cannot find the target easily without the link. Examples are the specification that a change depends on, the CI run that shows a result, and a heading in another file.
- Under each heading, link only the first reference to a target. Write each later reference to the same target without a link.
- When a reference to a heading has no link, write the heading text as the heading spells it, without backticks, such as "the Follow-up tasks section". If a heading has the same text as a value that a system reads exactly, keep the backticks on the value, such as the `Draft` status.
- In Markdown files, link to a tracked file with a relative path, and link to an Issue or a pull request with its full URL. In GitHub text, link to a file with its full GitHub URL on `main`. Refer to an Issue or a pull request with its number, such as `#123`.
- Use only the name of the target as the link text. For a section, use its heading text, such as "Follow-up tasks". For a document, use its title without a word that names the kind of document, such as "English prose" instead of "English prose conventions". If the sentence needs such a word, such as "section" or "conventions", put the word outside the link. For a file, you can use its path in backticks instead of its title, such as `README.md`.
- Do not link a heading that the reader can already see, such as a section of the same PR description.
- Do not use bare URLs or link text such as "here" or "this link".

### Changes

- Apply this convention to the text that you add or change. If you change part of a paragraph or a bullet, make the whole paragraph or bullet follow this convention. Do not change other text only to make it follow this convention, unless the PR exists for that change.

## Differences from the simple-english skill

The [`simple-english`](../../skills/simple-english/SKILL.md) skill, version 2.1.2, sets rules for the format of a document, but this convention applies where the skill and this convention differ.

- Use bullets for 2 or more items, as the [Format and content](#format-and-content) rules state. The skill uses a vertical list only for 3 or more items.
