# <Project Name> - Testing and Validation Report

> **Audience:** anyone deciding whether to trust this project in production.
> **Evidence window:** <YYYY-MM-DD> to <YYYY-MM-DD>
> **Last reviewed:** <YYYY-MM-DD>

This is a record of what was actually tested and what the results proved. A list of tests that
*could* be run belongs in section 5; everything above it describes what was run and what happened.

## 1. Summary

| | |
|---|---|
| **Test cases executed** | <n> |
| **Passed** | <n> |
| **Defects found** | <n> |
| **Defects fixed and evidenced** | <n> |
| **Open / accepted** | <n> |
| **Verdict** | <fit for production / fit with caveats / not yet> |

<One paragraph in plain language: what was tested, how thoroughly, and what a reader should
conclude. If the verdict has caveats, state them here rather than burying them.>

## 2. Functional test cases

| # | What was tested | How it was verified | Result | Date |
|---|---|---|---|---|
| 1 | <the behaviour> | <the exact check performed - a command, a query, an observation> | Pass / Fail | <date> |

<"How it was verified" is the column that gives this document its value. "Tested the sync" proves
nothing. "Ran the sync against 40 records and compared the destination table row-for-row against
the source export" is evidence.>

## 3. Defects found and resolved

Repeat this block for each defect. A defect is not closed until its exact failure condition has
been reproduced and behaved correctly.

### 3.1 <Short defect title>

| | |
|---|---|
| **Symptom** | <what was observed> |
| **Root cause** | <what was actually wrong, not where it surfaced> |
| **Fix** | <what changed, with a commit or PR reference> |
| **Evidence it works** | <the failure condition recurring and being handled correctly, with date and where observed> |
| **Observed in production?** | Yes / No - <if no, say what was done instead> |

<Evidence is the point of this section. "Fixed and tested locally" is weaker than "the same
condition occurred again on 2026-09-03 and the job completed normally". Where only a local check
exists, say so plainly rather than implying more.>

## 4. Production evidence

| | |
|---|---|
| **In production since** | <date> |
| **Runs or transactions observed** | <n> |
| **Successes** | <n> |
| **Failures** | <n, and what happened to each> |
| **Edge cases encountered and handled** | <list> |
| **Unresolved failures** | <list, or "none"> |

<If it is not in production yet, write "Not yet in production" and say what the pre-production
evidence consists of. Do not leave this section implying production experience it does not have.>

## 5. Test plan for future changes

What to run before the next deploy. This is the forward-looking half.

| Category | What to run | When |
|---|---|---|
| <e.g. regression> | <the suite or the manual steps> | <e.g. every deploy> |

## 6. Known gaps in testing

| Not tested | Why | Risk if it matters |
|---|---|---|
| <what> | <reason - no test environment, cost, low likelihood> | <consequence> |

<An honest gap list is what makes the rest of this document credible. If everything claims to be
tested, an experienced reader stops believing the whole report. If there are genuinely no gaps,
write "None identified." and be prepared to defend it.>

## 7. Related documents

- [Developer Guide](Dev-Guide.md) - how to run the tests
- [Troubleshooting](Troubleshooting.md) - symptoms these defects produced
- <Add others that exist for this project>
