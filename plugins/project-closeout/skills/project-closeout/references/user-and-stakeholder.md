# User Guide and Stakeholder Brief

Templates: `assets/templates/User-Guide.md`, `assets/templates/Stakeholder-Brief.md`

## Which one to write

**User Guide** - only when standard, non-technical people interact with the thing directly. If
they open it, run it, or act on its output, they need one.

**Stakeholder Brief** - when there is no User Guide. One page so a non-technical reader can
understand what this is and why it exists.

**Both** - when users operate it *and* someone above them decides whether to keep funding it.

Do not manufacture a User Guide for an invisible backend. A guide for a thing nobody touches is
noise that makes the rest of the doc set look padded, and it will never be read or maintained.
The Brief covers that case properly in a page.

## User Guide

### The one test that matters

Could someone in the target audience complete their first real task using only this document?

### Write tasks the way users name them

Users arrive wanting to do something, not wanting to use a feature. Name sections after the goal.

| Bad | Good |
|---|---|
| Using the proximity query | Find who sits near me |
| Configuring the export profile | Send the report to someone else |
| Invoking the batch endpoint | Process more than one at a time |

### Use the exact text users see

In the "when something goes wrong" table, quote error messages verbatim. A user in trouble
searches the page for the words on their screen. A paraphrase makes the row unfindable, which
means the row may as well not exist.

### Keep jargon out, genuinely

Not "minimal jargon" - none. If a reader would have to ask what a word means, replace the word.
Internal system names, protocol names and infrastructure terms all fail this test. Say "the
seating map" rather than the repo name.

### Include what success looks like

After each procedure, say what the reader should see. Without it they cannot tell whether it
worked, and a surprising amount of support load is people who succeeded and did not realise.

## Stakeholder Brief

### The one test that matters

Could a manager who has never heard of this decide, from one page, whether it is worth keeping?

### Quantify the "before"

The brief is much stronger with a comparison. What did people do before, and what does this
change? Hours saved, errors avoided, a delay removed, a manual step gone. A brief that only
describes the thing gives a reader no basis for judgement.

### Be honest about limitations

The "risks and limitations" section is not a weakness. A reader deciding whether to depend on
something needs to know where it stops, and discovering a limitation later - during an incident,
or after building on it - is far more damaging than reading it here.

### Say what happens if it stops

This is the line leadership reads when prioritising during an outage. State the business
consequence and the manual fallback if one exists. "Nothing urgent - the weekly report is late" and
"payroll cannot run" get very different responses, and only one of them should.

### Set a review date

Especially for pilots. A project with no recorded review date becomes permanent infrastructure by
accident, and later nobody can say who agreed to that.

## Failure modes to avoid

**A User Guide that is a feature tour.** Organise by what the reader wants to do.

**A Brief that is a technical summary with shorter words.** The audience is deciding, not learning.

**Screenshots with no text.** They go stale silently and are unsearchable. Use them to support
written steps, never to replace them.

**Naming individuals.** Use roles and teams, so the document survives people changing jobs.
