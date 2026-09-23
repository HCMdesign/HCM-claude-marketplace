# Admin Guide

Template: `assets/templates/Admin-Guide.md`

This is the 3am document. The reader is tired, under pressure, and did not build the thing. Every
sentence should be usable in that state.

## The one test that matters

Could someone who has never seen this project answer **"did it run last night, and did it work?"**
using only section 3 and section 4, in under a minute?

If not, nothing else in the document rescues it.

## How to find the content

Most of this cannot be read off the code. Work through it in this order:

1. **Run it, or read a real log.** The literal output is what belongs in "healthy looks like".
   Paraphrasing loses the exact string an operator will search for.
2. **Find the schedule definition** - cron, Task Scheduler, a cloud trigger, a CI workflow. Quote
   the real schedule, in a named timezone. "Nightly" is not a schedule.
3. **Find where output goes** - log files, a logging service, a table, an email. Then work out the
   query that answers each operator question, and *run it* so you know it is correct.
4. **Find the identity it runs as**, and what that account can do.
5. **List every credential it uses**, and where each is stored.

## Section notes

### Section 3, "Is it running right now?"

Give a literal command, not a description of one. The difference:

> Bad: Check the service status in the portal.

> Good:
> ```
> systemctl is-active invoice-poller
> ```
> Healthy: `active`. Anything else means it is down; go to Troubleshooting 3.1.

If there is genuinely no single check, give the two or three that together answer it, in order.

### Section 4.2, queries

Write the query, ready to paste, with real table names, real log paths, real field names. An
operator at 3am cannot construct a query from a description of one.

Include a query for each question people actually ask. At minimum: did the last run succeed, what
failed recently, and whatever the project-specific question is.

### Section 4.3, normal volume

This is the section people skip and then miss outages with. Without a baseline, nobody can tell a
quiet period from a broken one. Give real numbers from real runs and say what a suspicious number
looks like.

> Normally 200-400 records per run. Under 50 means the upstream export is late rather than the
> sync being broken - check the source first.

### Section 5.3, clean up after a bad run

Write this as though the reader has already made a mess, because they have. Be explicit about
order, about what is safe to delete, and about what must be preserved for diagnosis. If a re-run
is idempotent, say so plainly; if it will double-process, say that louder.

### Section 6, secrets

Record the location, never the value. Include expiry dates where they exist, because an expired
credential is one of the most common causes of a silent failure and one of the easiest to prevent.

If you find a credential stored somewhere inappropriate while writing this, do not quietly move on.
Record it as a finding in the closeout report.

### Section 7, contacts

Prefer roles and teams to individual names. People change jobs and a doc naming a person who left
is worse than one naming a team, because the reader wastes time before realising.

## Failure modes to avoid

**"Check the logs."** The entire value of this document is saying *which* logs and *what query*.

**Aspirational content.** Do not document a monitoring alert that was planned and never built. If
nobody is notified on failure, the correct entry is "No alerting configured - failures are noticed
when someone checks", which is honest and immediately tells a reader what risk they are carrying.

**Describing the architecture.** That is the Developer Guide. An operator does not need the module
map to restart a service, and putting it here buries the parts they do need.
