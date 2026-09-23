# Closeout Report

Template: `assets/templates/Closeout-Report.md`

Written in phase 1 from the audit, updated in phase 3 with what was done. It is the first thing the
next person reads, and the record of what was knowingly left undone.

## The one test that matters

Six months from now, could someone tell from this report exactly what state the project was left
in, and which gaps were deliberate?

## Findings must be specific enough to act on

The difference between a useful audit and a checklist is whether each finding says what is
actually missing and why it matters.

| Useless | Useful |
|---|---|
| No admin doc | No admin doc, so nobody but the author knows the job runs at 06:00 or where its log lands |
| Tests missing | No test suite and no record of manual testing; it has run in production since June without a recorded failure, which is evidence but not verification |
| Troubleshooting is a stub | `TROUBLESHOOTING.md` exists with three bullets covering install problems only; nothing about runtime failures, which is where the four support tickets came from |

The second column tells a reader what happens if they ignore it. The first does not.

## Record what you did not check

Section 1.5 is what makes the report trustworthy. An audit that assumes the tests pass because a
test directory exists is worse than one that says "tests present, not run, unverified", because
the first quietly launders an assumption into a fact.

Write "Nothing - all items above were directly verified" only when that is true. It usually is not:
a tracker may not have been reachable, a deployment may not have been inspectable, a test suite may
not have been runnable in this environment. Say so.

Equally, record the sources you checked and found clean. "No open issues" tells a reader the issue
tracker was examined. Silence does not distinguish "clean" from "never looked".

## The gate decision is the most important section

Section 1.6 records what the user was shown and what they chose.

**When the audit is clean**, say so and note that you continued without stopping. A clean project
should not be halted to be told it is clean.

**When findings were raised**, record each one, what the user decided, and the reasoning they gave.
Not to assign blame - the opposite. A recorded decision is a defensible one. An unrecorded gap
looks like negligence later, even when it was a reasonable call at the time, because nobody can
prove it was a call at all.

> Finding: no testing report, and the test suite has never been run in CI.
> Decision: accepted and skipped.
> Rationale: retiring in Q1 when the vendor migration completes; not worth the effort.

That paragraph protects everybody. "No testing report" on its own does not.

## Part 2 is not optional

It is tempting to treat the audit as the deliverable and leave part 2 empty. The part-2 sections
are what make the closeout auditable: where the docs went and why, whether the link check passed,
the PR, whether an automated review actually ran, the release decision and its reasoning, and the
tracker state.

On the automated review line specifically, record whether it *ran*, not just whether it was clean.
Review tools can exit successfully while rate-limited, unlicensed or skipped, and a clean result
from a review that never happened is the most dangerous entry this report can contain.

## Section 2.6 is the handover

"Still outstanding after closeout" is the line the next person reads first. If nothing is left,
write "Nothing." explicitly - an empty section reads as unfinished rather than complete.
