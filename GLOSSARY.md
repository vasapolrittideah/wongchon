# Glossary

This file defines each term that has a narrower or different meaning in the project than in general English.

| Term | Meaning |
| --- | --- |
| approval stamp | A file that the review script writes when a review role approves 1 exact staged tree or PR text, as [ADR-0022](docs/adrs/0022-store-approval-stamps-in-the-git-common-dir.md) states. |
| chain mode | The mode of the `build` skill that builds the Issues of a milestone one after another, 1 merged PR at a time, as [ADR-0032](docs/adrs/0032-build-1-issue-at-a-time-in-single-or-chain-mode.md) states. |
| follow-up task | Work for later that a PR leaves and that no plan holds, as [ADR-0031](docs/adrs/0031-make-each-follow-up-task-an-issue-without-a-milestone.md) states. |
| review guard | The hook that blocks a commit or a PR without the approval stamps of its review roles, as [ADR-0028](docs/adrs/0028-block-unstamped-commits-in-a-separate-hook.md) states. |
| review role | A reviewer with 1 kind of work, such as the writing reviewer, whose prompt is a role file that the review script runs in a separate read-only process, as [ADR-0027](docs/adrs/0027-keep-review-roles-in-role-files.md) states. |
| review round | 1 run of 1 review role on 1 version of a change. A role has at most 3 rounds before the agent asks the maintainer, as [ADR-0025](docs/adrs/0025-count-review-rounds-in-the-review-script.md) states. |
| single mode | The mode of the `build` skill that builds 1 Issue up to a ready PR, as [ADR-0032](docs/adrs/0032-build-1-issue-at-a-time-in-single-or-chain-mode.md) states. |
| small change | A change of 1 PR without an intent and a spec, as [ADR-0014](docs/adrs/0014-start-small-changes-at-the-build-stage.md) and [ADR-0034](docs/adrs/0034-detect-a-small-change-from-its-plan-and-its-related-artifacts.md) state. |
| stage gate | The CI job named `Stage gate`, which fails while a stage artifact of the PR is not `Approved`, as [ADR-0016](docs/adrs/0016-block-unapproved-artifacts-with-a-stage-gate.md) states. |
| task | 1 unit of work of a plan, which is 1 GitHub Issue and 1 PR, as [ADR-0038](docs/adrs/0038-give-a-milestone-only-to-a-change-with-a-spec.md) states. |
