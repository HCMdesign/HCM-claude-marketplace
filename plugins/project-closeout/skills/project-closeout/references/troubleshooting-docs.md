# Troubleshooting

Template: `assets/templates/Troubleshooting.md`

Separate from the Admin Guide on purpose. Admin is for running it; this is for when it is broken
and someone needs to start fixing within seconds of landing on the page.

## The one test that matters

Can a technician who has never seen this project find their symptom in the index and be executing
a fix **without reading anything else on the page**?

If they have to read the architecture first, the document has failed at its only job.

## Write symptoms in the reporter's words, not the system's

This is the single thing that determines whether the index works. Someone arrives knowing what
they *observed*, not what component failed. If the rows are named after internal causes, they
cannot find their row.

| Bad row | Good row |
|---|---|
| Token refresh failure | "It says access denied" |
| Upstream schema drift | "It runs but the numbers are wrong" |
| Scheduler misfire | "The report never arrived" |
| Appx registration to wrong SID | "It says it installed but the app isn't there" |

The cause goes in the second column. The first column is how a human describes it out loud.

## How to find the content

The best source is history, not imagination:

1. **Read the issue tracker and support tickets.** Real reported symptoms, in real wording. This
   is the highest-value source and the most commonly ignored.
2. **Read the commit history for bug fixes.** Every fixed bug was a symptom once, and can recur.
3. **Read the error-handling code.** Every raised error and logged failure is a potential row.
4. **Ask what has actually gone wrong.** If the project has an owner, one question - "what breaks
   most often?" - is worth an hour of reading.

Do not invent failure modes to pad the index. A short index of real symptoms beats a long one of
imagined ones, because the imagined rows dilute the real ones and cost the reader time.

## Section notes

### Section 1, "Is it even running?"

Most "it is broken" reports turn out to be "it never started". Putting this check first saves more
time than any other part of the document. It can be the same check as Admin section 3; duplicate
the command here rather than linking, because this is the one place where making the reader
navigate is worse than repeating two lines.

### Section 3, fixes

Keep each one short: cause, check, fix, verify, what to do if that failed. Cross-reference the
Admin or Developer guide for depth rather than re-explaining the system. A fix that turns into an
essay stops being usable under pressure.

Always include the verify step. A technician needs to know whether they are done.

### Section 4, symptom to source map

Use the **literal string** as it appears in the log, because the reader will paste it into a
search box. A paraphrase makes the table unfindable.

This table does double duty: a technician traces a message to its cause, and a code auditor traces
a behaviour to its source. Both need file and function, not just a module name.

### Section 5, known issues

The purpose is to stop the same false alarm being investigated over and over. A benign warning
that appears on every run, a vendor quirk, an error that is safely retried - each costs somebody an
hour every time it is rediscovered.

If a known issue has a real cause that was investigated and accepted, say who accepted it and why.
"ERROR 53 on a DFS namespace stub is expected and the ignore is correct" saves the next person the
whole investigation.

## Failure modes to avoid

**Leading with architecture.** The reader is in an incident. Diagrams go in the Developer Guide.

**Symptoms only the author would recognise.** If you cannot imagine a user saying the row title out
loud, rewrite it.

**Fixes with no verification.** "Restart the service" without "then confirm X" leaves the reader
guessing whether it worked.

**An index that does not match the fixes.** Every row in section 2 must link to a real subsection
in section 3. Run the link checker.
