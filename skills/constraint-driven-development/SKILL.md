---
name: constraint-driven-development
description: Establishes a project's quality bar as a written contract and stops agents quietly lowering it. Interviews the user on which dimensions matter, supplies sane default thresholds when they have no number in mind, records everything in CONSTRAINTS.md in the format of the constraints convention, and watches the diff for a weakened bar — new @ts-ignore or eslint-disable suppressions, skipped or deleted tests, assertions stripped out, unimplemented stubs, thresholds edited down. Use in the design stage of the first change of a project, when no quality bar is written down, when the user says "set up constraints" or "define our standards", when the user wants dimensions they care about — accessibility, web performance, coverage — set up as enforced constraints, when an agent keeps silencing checks or skipping tests to get to green, when you need a coverage or performance threshold and don't know what number to pick, or when an agent writes more code than anyone will read.
---

# Constraint-Driven Development

## Overview

Other skills in this pack describe what good looks like. `code-review-and-quality` gives you five axes. `test-driven-development` gives you a cycle. `security-and-hardening` gives you a threat list. All of that lives in prose the agent reads and may or may not follow, and none of it survives the end of the session.

This skill produces something different: a written record of **this project's** bar, with numbers, that outlives the conversation and can be checked mechanically.

The reason matters. When you wrote the code, reading it told you whether it was any good. An agent writes more in an afternoon than you will read that week, so the judgement moves out of your head and into checks that run around the loop. Those checks need to exist, they need numbers you actually chose, and they need to fire close enough to the work that the agent fixes its own output.

Spec-driven development says what to build. Test-driven development proves it works. Constraint-driven development defines what "good enough to ship" means, before anyone argues about it in a pull request.

In this project, the [constraints convention](../../docs/conventions/constraints.md) defines the sections of `CONSTRAINTS.md`, the Floor rules that each project copies, and how a rule or an exception changes. The design stage writes the file in the first change of the project, and a later spec updates it in the pull request of the spec.

## When to Use

Apply this skill when:

- Starting a project or a significant feature and no quality bar is written down
- The user asks to "set up constraints", "add quality gates", "define our standards", or "stop the agent shipping junk"
- An agent is producing volume nobody is reading line by line
- CI has checks but nobody can say which ones block a merge and which ones are decoration
- Coverage, performance, or accessibility numbers get argued about per-PR instead of decided once
- You're about to run any autonomous loop, and the only thing standing between it and main is a test suite the agent also wrote

**When NOT to use:**

- The project already has a `CONSTRAINTS.md` and the user isn't changing it — read it and follow it instead
- One-off scripts, spikes, throwaway prototypes
- The user wants a code review right now (`code-review-and-quality`) or a CI pipeline built
- Pre-product-market-fit code with a two-week expected lifetime — the floor below is still worth it, the rest isn't

## Loading Constraints

The interview needs a live user. **Don't run it in non-interactive contexts** (CI, `/loop`, autonomous runs). If constraints are missing and you're in one of those, apply the Floor below, note that you did, and flag the rest for a human.

## The Process

### Step 1: Detect before you ask

Never ask what you can read. Before the first question, gather:

| What | Where to look |
|------|---------------|
| Language and stack | `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml` |
| Test runner | dev dependencies, `test` script, existing test files |
| Existing linters | `eslint.config.*`, `biome.json`, `.ruff.toml` |
| Coverage today | `coverage/` output, or run the suite once |
| CI | `.github/workflows/`, `.gitlab-ci.yml` |
| Agent harness | `.claude/`, `.codex/`, `AGENTS.md` |

Report what you found in two lines, then ask only what's left.

### Step 2: Four questions, each with a default

Follow the one-question-at-a-time discipline from `interview-me`, with one change: every question here has a default, so "I don't know" is a complete answer that still produces a working config.

```
Q1: Beyond the floor, which of these do you want enforced?
    (a) Test coverage on new code
    (b) Security scanning
    (c) Performance budgets
    (d) Accessibility
    (e) Architecture boundaries
GUESS: (a) and (b) — you have a test runner already and you're handling user input.
DEFAULT if unsure: (a) and (b).
Say what each pick costs: (c) and (d) need a running URL, (e) needs a rules file written.
```

```
Q2: When a check fails while the agent is mid-task, should it block or warn?
GUESS: Block. You're running agents unattended and a warning nobody reads is a warning.
DEFAULT if unsure: Block on the floor, and put everything else in "Measured, not yet enforced" for the first two weeks.
```

```
Q3: Do you have target numbers in mind, or should I measure where you are today and hold that line?
GUESS: Measure. Most teams don't have a number, and an invented one gets ignored.
DEFAULT if unsure: Measure and hold. See "Ratchets" below.
```

```
Q4: What's the slowest check you'll tolerate before the agent hands work back?
GUESS: About 90 seconds. Longer and you'll stop running it.
DEFAULT if unsure: 90 seconds at task end, unlimited in CI.
```

Stop at four. A twelve-question intake produces a config nobody understands and a user who regrets starting.

### Step 3: Write CONSTRAINTS.md

One file at the repo root. Any agent on any harness can read it, and a change to it shows up in review where it belongs.

Write it with the template and the rules of the [constraints convention](../../docs/conventions/constraints.md):

- **Floor** — Copy each rule of the Floor rules table of the convention, with its ID and its text. In the Check column, name the command that checks the rule, or write `None yet` and name the follow-up task in the pull request description.
- **Constraints** — 1 row for each dimension that the user picked, with a number, the command that checks it, where it runs, and the reason for the number.
- **Measured, not yet enforced** — 1 row for each measure that no rule blocks yet.
- **Exceptions** — 1 row for each exception, with an owner and a date at most 90 days away.

For a TypeScript web app, the file can look like this:

```markdown
# Constraints

This file states the quality bar of the project. Each rule names the check that enforces it.

## Floor

| ID | Rule | Check |
| --- | --- | --- |
| F1 | Each linter directive that turns off a check names each rule that it turns off, and the PR description states the reason. | None yet |
| F2 | The code has no unimplemented stub, no empty error handler, and no marker for later work, such as `TODO` or `FIXME`. | None yet |
| F3 | No change skips or deletes a test or removes an assertion, unless Exceptions has a row for it. | None yet |
| F4 | No file has a secret, such as a password, a private key, or an access token. | `gitleaks dir . --redact --no-banner` |
| F5 | No change weakens this file, unless Exceptions has a row for it. A change can tighten a rule. | None yet |

## Constraints

| ID | Dimension | Rule | Check | Runs at | Reason |
| --- | --- | --- | --- | --- | --- |
| C1 | Types | Zero type errors | `tsc --noEmit` | edit | A type error is a bug that the compiler already found. |
| C2 | Lint | Zero errors from our config | `biome check` | edit | The config is the agreed style. |
| C3 | Coverage | Changed lines at least 80% covered | `vitest run --coverage` + git diff | task end, CI | 80% forces a test and allows a config line. |
| C4 | Security: code | Zero findings of severity `ERROR` | `npm run check:security` | CI | Lower severities are mostly noise. |
| C5 | Security: deps | Nothing at high or above | `osv-scanner scan source -r .` | CI | Lower severities are mostly noise. |
| C6 | Accessibility | Zero axe violations | `npm run check:a11y` | CI | `axe --exit` cannot filter by impact. |
| C7 | Performance | LCP at most 2500ms, CLS at most 0.1 | `lighthouse $PREVIEW_URL --output=json` | CI | The Core Web Vitals "good" thresholds. |

## Measured, not yet enforced

| ID | Dimension | Measure | Command | Target |
| --- | --- | --- | --- | --- |
| M1 | Project coverage | Line coverage of the project | `vitest run --coverage` | 62.4% or more |
| M2 | Bundle size | Size of the main bundle | `size-limit --json` | 184 kB or less |

## Exceptions

| ID | Rule | Path | Reason | Owner | Expires |
| --- | --- | --- | --- | --- | --- |
| E1 | C2 | `src/legacy/**` | The legacy module breaks `no-explicit-any`. A rewrite with typed models replaces it. | Kim Lee | 2027-02-15 |
```

Every row names the command that produces the verdict. A dimension with a
number and no command in this column is an aspiration, not a constraint.

Then add one line to `AGENTS.md` and `CLAUDE.md`: `Read CONSTRAINTS.md before writing code. Do not weaken it to make a change pass.`

### Step 4: Install what each dimension needs

Picking a dimension means installing something. Don't leave the user with a number and no mechanism, and don't invent your own checker when a de facto one exists — these tools are listed because their rule formats and thresholds are what everything else in the ecosystem targets, so the team's existing config keeps working.

| Dimension | Tool | Install | Run | Gate on |
|-----------|------|---------|-----|---------|
| Types (TS) | tsc | already there | `tsc --noEmit` | any error |
| Types (Python) | mypy | `pip install mypy` | `mypy .` | any error |
| Lint | your existing config | already there | `eslint .` / `biome check` / `ruff check` | any error |
| Coverage (JS) | your test runner | Vitest: `npm i -D @vitest/coverage-v8`; Jest: already there | `vitest run --coverage` (or `jest --coverage`) | coverage of changed lines |
| Coverage (Python) | pytest-cov | `pip install pytest-cov` | `pytest --cov --cov-report=lcov` | same |
| Security: code | Semgrep | `pipx install semgrep` | `npm run check:security` (below) | severity `ERROR` |
| Security: secrets | gitleaks | `brew install gitleaks` | `gitleaks dir . --redact --no-banner` | any finding |
| Security: dependencies | osv-scanner | `brew install osv-scanner` | `osv-scanner scan source -r .` | high or above |
| Performance: page | Lighthouse | `npm i -D lighthouse` | `lighthouse $URL --output=json --quiet` | LCP, CLS, performance score |
| Performance: bundle | size-limit | `npm i -D size-limit` | `size-limit --json` | per-entry byte budget |
| Accessibility | axe-core | `npm i -D @axe-core/cli` | `npm run check:a11y` (below) | zero violations |
| Architecture | dependency-cruiser | `npm i -D dependency-cruiser` | `depcruise src` | any violation |
| Assertion quality | Stryker | `npm i -D @stryker-mutator/core` | `stryker run --mutate <changed files>` | mutation score |

Five things that will bite you if you skip them:

1. **`--redact` on gitleaks is not optional.** Without it the matched secret lands in the agent's transcript, which is how a leaked key ends up in a log, a summary, or a commit message. Report the rule and the location, never the value.
2. **Lighthouse and axe need a URL.** They only work against a running app, so they belong in the runtime stage against a preview deploy or a local server you start first. If the project has no URL to hit — a CLI, a library, a desktop app — say so and drop the dimension rather than inventing a check that can't run.
3. **Scope the expensive ones to the diff.** `stryker run --mutate` on the whole repo takes hours and gets turned off; on the files a change touched it takes under a minute. Same for Semgrep, which takes a path list.
4. **Coverage needs no second test run.** Read the lcov your suite already writes and intersect it with `git diff`. Running the suite twice to get a number is the fastest way to make people hate this.
5. **Semgrep's registry rules are free to run; check the licence before redistributing them.** `opengrep` is a drop-in fork with the same rule format and JSON output if that matters to your legal team.

`semgrep scan` and `axe` exit 0 on findings by default. Pass `--error` to `semgrep scan` and `--exit` to `axe`, so that a finding fails the command. The `--exit` flag of `axe` fails on any violation and cannot filter by impact, so the accessibility rule is zero violations.

Add each one to the project's own script so it's reproducible without an agent:

```json
{
  "scripts": {
    "check:fast": "tsc --noEmit && eslint . && gitleaks dir . --redact --no-banner",
    "check:task": "npm run check:fast && vitest run --coverage",
    "check:security": "semgrep scan --config p/default --strict --error --severity ERROR",
    "check:a11y": "axe \"$PREVIEW_URL\" --tags wcag2a,wcag2aa,wcag21aa --exit",
    "check:full": "npm run check:task && npm run check:security && osv-scanner scan source -r ."
  }
}
```

That mapping matters more than the tools. `check:fast` is what runs after an edit (`edit` in the Runs at column), `check:task` when the agent thinks it's done (`task end`), `check:full` in CI (`CI`). Run `check:a11y` after the preview is reachable, with `PREVIEW_URL` set (the example uses POSIX shell syntax).

Before calling any row enforced, run its actual CI command against a known violation and a clean control. Confirm that the violation fails, the control passes, and scanner errors fail too. For a severity threshold, also confirm a below-threshold finding passes. Apply this to every dimension, including coverage and Lighthouse: generating a report alone does not enforce the number in `CONSTRAINTS.md`.

The commands now live in two places — the Check column in `CONSTRAINTS.md` and these scripts. `CONSTRAINTS.md` is the canonical source: it carries the reason alongside each command and it shows up in review. The scripts are convenience wrappers that must mirror it, not a second source of truth; if they drift, the file wins.

### Step 5: Wire it to the lifecycle

The single biggest mistake is running everything everywhere. A check that stalls the agent gets switched off, and a gate people switched off is worse than no gate, because the bar still looks like it exists.

| Runs at | What runs | Budget |
|---------|-----------|--------|
| `edit` | Types, lint, secrets, the floor | under 5s, changed file only |
| `task end` | Related tests, coverage on changed lines | under 90s |
| `CI` | Everything, plus the guards below, direction checks, and no regressions | minutes |

The [Runs at values](../../docs/conventions/constraints.md#runs-at-values) table of the constraints convention defines each value.

Two rules that keep this tolerable:

1. **Scope to the diff.** Check the lines this change touched, not the whole repo. Coverage of changed lines is a number the agent can move; project coverage is one it inherited.
2. **Cost decides placement.** Anything over a few seconds moves out of the edit loop. Mutation testing on a whole repo takes hours; on the files a change touched it takes under a minute, which is the difference between a check people run and one they don't.

### Step 6: Guard the bar itself

Someone will point out that if the agent writes the code and the checks, the checks prove nothing. Half right, and worth engineering around.

Agents don't craft clever loopholes. They hit a red check and take the cheapest road to green. Watch for these five moves in the diff, at review time:

1. **The threshold moved.** A budget lowered, a severity dropped, a check removed from the fast stage. Compare `CONSTRAINTS.md` against its state at the branch point.
2. **A test got easier.** `.skip` added, a test file deleted, assertions pulled out of tests that stayed.
3. **A checker got silenced.** New `@ts-ignore` or `eslint-disable`. Four suppressions deserve special attention because they switch off a check you're relying on: `istanbul ignore` drops code from coverage instead of testing it, `Stryker disable` hides a surviving mutant, `nosemgrep` and `gitleaks:allow` do it for security findings.
4. **Work is unfinished.** A stub that throws, an empty `catch` turning a failure into silence, a `TODO` standing where the implementation should be.
5. **An exception appeared.** A new row in the Exceptions table nobody discussed.

None of this needs tooling beyond `git diff`. Tightening the bar should be silent; loosening it should be loud.

Unlike the numbered dimensions, the floor has no de facto tool of its own, so an agent asked to enforce it tends to write a checker from scratch, and two agents write two different ones. This project does not ship a check of the Floor rules yet. Until it does, write `None yet` in the Check column of each Floor rule that no command checks, and check these moves in the review.

**Not all checks are equally circular.** Rank them by one question: can the agent make this pass by writing code that doesn't work?

- **External** — axe-core encodes WCAG, `osv-scanner` reads a vulnerability database, Lighthouse measures a real browser. The agent can't argue with these.
- **Project** — your lint rules, your layer boundaries. A human owns the file.
- **Suite** — your own tests. Most useful, and the only genuinely circular one.

A bar made entirely of the third kind is worth less than one with an outside opinion in it. Check that at least one external constraint is present.

### Step 7: Ratchets, when you don't have a number

Set 80% coverage on a codebase at 62% and you get a red build forever, then a team that learns to ignore red builds.

The alternative asks for no decision: record where you are, then refuse to get worse. Put it in the "Measured, not yet enforced" table, with today's number and a direction in the Target column, such as "62.4% or more". Every check compares against the recorded value, not an aspiration. When a number improves, update it; when it drops, that's the finding.

This also answers a fair objection to training. Models are rewarded for passing tests, which you can evaluate in seconds. Architectural rot shows up over months and never reaches the weights. A ratchet is the missing penalty, written down where the build can see it.

## Sane Defaults

When the user has no opinion, use these. They're chosen to be met by most codebases on day one.

| Constraint | Default | Why this number |
|------------|---------|-----------------|
| Coverage of changed lines | ≥ 80% | High enough to force a test, low enough to allow a config line |
| Project coverage | today's value, must not fall | No argument needed to adopt |
| Mutation score (if used) | ≥ 60% to start | Typical for a suite never mutated before; 80% is mature |
| Dependency vulnerabilities | nothing at high or above | Below that is mostly noise |
| LCP | ≤ 2500 ms | Core Web Vitals "good" threshold |
| CLS | ≤ 0.1 | Same |
| Accessibility | zero axe violations | The `--exit` flag of `axe` cannot filter by impact; turn off a debatable rule with `--disable` and state the reason |
| Exception lifetime | 90 days | Long enough to plan the fix, short enough to remember |
| Ratchet tolerance | 0.5% | Absorbs drift when an unrelated file moves the number |

State the number and the reason together. A threshold without a rationale gets deleted by the next person who hits it.

## Escalation Path

Constraints work at three levels of teeth. Start at the first.

1. **Written only.** `CONSTRAINTS.md` exists and agents read it. Costs nothing, catches the honest mistakes, relies on the agent complying.
2. **Scripted.** An `npm run check` (or `make check`) that runs the fast checks, wired into your agent's post-edit hook and your CI. Deterministic, no new dependency.
3. **Tool-backed.** A dedicated runner that handles diff scoping, budgets, ratchets, and the guard checks. Use when the config outgrows a shell script.

Most projects should stop at 2. Move to 3 when you're maintaining more than about thirty lines of check-running shell.

**A first run can be floor-only.** The floor needs no installs, so you can apply it on day one and add numbered dimensions as you install each tool, rather than standing up every checker before the first commit is protected. Security tools that install machine-wide (gitleaks, osv-scanner) can also run CI-only if you'd rather keep laptops clean; declare where each dimension runs in the `Runs at` column.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We'll add constraints once the code settles" | Code settles around whatever was allowed while it was moving |
| "The tests are the constraints" | Tests you wrote prove you agree with yourself; they say nothing about coverage of new code, dependency risk, or bundle growth |
| "We can't hit 80% coverage" | Then don't set 80%. Set today's number and hold it |
| "This will slow the agent down" | Only if you put slow checks in the fast loop. That's a placement error, not an argument against constraints |
| "I'll remember what our standards are" | The agent won't, and it's writing most of the code |
| "Constraints will block us shipping" | An exception with an owner and a date unblocks you. Deleting the constraint unblocks everyone forever |

## Red Flags

Stop and reconsider if you notice:

- The interview ran past four questions, or produced a config the user can't explain
- A budget was set that the codebase fails today, with no plan to reach it
- A dimension was written into CONSTRAINTS.md with a number but no tool behind it
- A checker was hand-rolled when a de facto one exists, so the team's existing config is ignored
- Every constraint is checked by the project's own test suite, with no external opinion
- `CONSTRAINTS.md` changed in the same commit as the feature that was failing
- An exception has no owner, or an expiry more than 90 days out
- The agent proposed relaxing a threshold instead of fixing the code
- Slow checks landed in the edit loop and someone has started passing `--no-verify`
- Nobody has opened `CONSTRAINTS.md` since it was written

## Verification

The skill was applied correctly when:

- [ ] `CONSTRAINTS.md` exists, follows the [constraints convention](../../docs/conventions/constraints.md), and every number in it has a stated reason
- [ ] The Floor has each rule of the convention, and each Floor rule with a check passes on the current codebase without changes
- [ ] Every dimension the user picked has a tool installed and a command that runs today
- [ ] Each constraint says where it runs, and the fast stage stays under a few seconds
- [ ] At least one constraint is external (not judged by this project's own tests)
- [ ] Measured-only metrics record today's value and a direction in the Target column
- [ ] Exceptions have an owner and an expiry date at most 90 days away
- [ ] `AGENTS.md` or `CLAUDE.md` points at the file
- [ ] A trial run on the current branch produces no failures the user disagrees with
- [ ] Each enforced command fails on a deliberate violation and scanner error, passes a clean control, and preserves the agreed severity threshold

## See Also

- `interview-me` — the one-question-at-a-time discipline this skill's intake borrows
- `code-review-and-quality` — how to review; this skill decides what the review enforces
- `test-driven-development` — the suite that coverage and mutation constraints measure
- `security-and-hardening` — what the security dimension should contain
- `performance-optimization` — where the performance numbers come from
