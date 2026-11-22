# Glossary

This file defines each term that has a narrower or different meaning in the project than in general English.

| Term | Meaning |
| --- | --- |
| approval stamp | A file that the review script writes when a review role approves 1 exact staged tree or PR text, as [ADR-0022](docs/adrs/0022-store-approval-stamps-in-the-git-common-dir.md) states. |
| review role | A reviewer with 1 kind of work, such as the writing reviewer, whose prompt is a role file that the review script runs in a separate read-only process, as [ADR-0027](docs/adrs/0027-keep-review-roles-in-role-files.md) states. |
| review round | 1 run of 1 review role on 1 version of a change. A role has at most 3 rounds before the agent asks the maintainer, as [ADR-0025](docs/adrs/0025-count-review-rounds-in-the-review-script.md) states. |
