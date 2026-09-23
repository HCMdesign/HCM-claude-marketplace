# Testing Report

Template: `assets/templates/Testing-Report.md`

The distinction that defines this document: a test **plan** says what could be run; this is a
record of what **was** run and what it proved. Most projects ship the plan and call it testing.

## The one test that matters

Could a reader decide whether to trust this in production, and know exactly what that trust rests
on?

## Evidence, not intent

A defect is not closed when the fix is written. It is closed when the exact failure condition has
occurred again and the system behaved correctly. That distinction is the whole value of this
document, and it is where honesty matters most.

Strength of evidence, weakest to strongest:

1. "Fixed" - no evidence at all
2. "Tested locally" - the code path ran once, under conditions you chose
3. "The failure condition was reproduced and handled correctly" - real evidence
4. "The same condition recurred in production on <date> and it behaved" - the strongest

Write which one you actually have. Claiming 4 when you have 2 is the failure mode that makes an
entire report worthless, because a reader who catches one overstatement stops believing all of it.

## How to find the content

1. **Read the commit history for fixes.** Each one is a defect row: what was the symptom, what was
   the root cause, what changed.
2. **Read the issue tracker**, including closed items.
3. **Run the test suite** and record the real result. Do not write "tests pass" without running
   them; if you cannot run them, say so in section 6 and in the closeout report.
4. **Look for production evidence** - logs showing runs, successes and handled edge cases.
5. **Ask what is not tested.** This is section 6 and it is the section that makes the rest
   credible.

## Section notes

### Section 2, functional test cases

The "how it was verified" column carries the document. Compare:

> Bad: Tested the sync. Pass.

> Good: Ran the sync against 40 source records, then compared the destination table row-for-row
> against the source export. All 40 matched including the two with null cost centres. Pass.

The second tells a reader what was actually established. The first tells them somebody felt good
about it.

### Section 3, defects

Root cause means the actual cause, not where it surfaced. "Fixed the null check in the report
writer" is a location; "the upstream export omits the cost-centre column for contractors, which
the writer assumed was always present" is a cause. Only the second prevents the next instance.

### Section 4, production evidence

If it is not in production, say so plainly rather than leaving the section implying experience it
does not have. "Not yet in production; pre-production evidence consists of X" is a legitimate and
useful answer.

### Section 6, known gaps

Counter-intuitively, this is what makes the report believable. A report claiming complete coverage
reads as unexamined to anyone experienced. Name what was not tested and why: no test environment,
cost, needs production data, low likelihood.

## The evidence window

The date range at the top tells a reader how fresh this is. A report with no window silently ages
into fiction: the numbers were true once and nobody can tell when. Set it, and set a review date
if the project is long-lived.

## Failure modes to avoid

**A plan wearing a report's title.** If every row is future tense, this is not a testing report.

**Unrun tests reported as passing.** If you did not execute it, you do not know.

**Defects with no evidence.** A fix list without evidence is a changelog.

**Silence about gaps.** An empty section 6 on a real project is nearly always an unexamined one.
