# ADR-0037: Make the writing reviewer apply the convention of each artifact

Status: `Accepted`

Spec: [`docs/specs/build-plans-and-tasks.md`](../specs/build-plans-and-tasks.md)

## Context

Both the writing reviewer and the artifact reviewer review each stage artifact, as [ADR-0023](0023-choose-review-roles-from-fixed-paths.md) states. The English prose conventions state that the convention of the artifact wins over their own rules. The writing reviewer read only the English prose and Markdown conventions, so it asked for more paragraphs in the Problem of an intent, and the artifact reviewer then blocked the intent for its number of paragraphs.

## Decision

The writing reviewer reads the convention of each staged file that has one, such as an intent, a spec, a plan, an ADR, or a convention file. It follows the order of rules of the English prose conventions, in which the convention of the artifact comes first, so it reports no finding whose fix breaks that convention.

## Rejected options

| Option | Reason |
| --- | --- |
| The artifact reviewer as the only role for stage artifacts | It then also checks the prose of each artifact, and its prompt grows. |
| 1 role that merges both | A change of the prose rules then changes the review of each artifact. |

## Consequences

- The writing reviewer reads 1 more convention for each stage artifact, so a review uses more tokens.
- A conflict between 2 conventions goes to the owner of the conventions instead of the author of the change.

## Confirmation

No tool can check the findings of a role. The maintainer checks the rounds of this change until the verify phase adds evals of the reviewers.
