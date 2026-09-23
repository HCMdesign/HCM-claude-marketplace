---
name: project-closeout
description: Close out a finished project properly - audit what is actually done, write the documentation set (dev, admin, user, troubleshooting, testing, integration registry), clean the git history, open the PR, cut the release, and update the tracker. Use this skill whenever a project is finishing, finished, shipped, deployed, handed off, or being revived for the first time since it was abandoned, and whenever someone asks to "close out", "wrap up", "finish", "call it done", "ship it", "hand it over", or asks whether a project is complete or what is left before it can be. Also use it when someone asks for a rebuild runbook, a troubleshooting guide, a testing report, an integration or audit record, or asks what documentation a project still needs. Do not wait to be asked for an "audit" by name; the moment a project is described as done, this is the process that decides whether that is true.
---

# Project closeout

A project is not done when it ships. It is done when a stranger can rebuild it, operate it, or
fix it at 3am from the documentation alone, without finding the person who built it.

That is the only bar that matters here. Every rule below exists to serve it, and when a rule and
the bar disagree, the bar wins.

## Why this is worth doing properly

The person this protects is usually the author, eighteen months later, with no memory of the
project and a production incident in progress. The second person it protects is whoever inherits
it when the author leaves. Documentation written at completion is cheap because the context is
still loaded; documentation written six months later is archaeology, and mostly does not happen.

That is also why the audit comes first. A half-finished project that gets a beautiful doc set is
still a half-finished project, and now it is one that *looks* closed on the board.

## Three phases

**Phase 1, audit.** Read-only. Work out what this project is, what state it is really in, and what
is still outstanding. Produce a report.

**Phase 2, author.** Write the documentation that is missing, to the standard in `references/`.

**Phase 3, closeout.** Git hygiene, link check, PR, release if warranted, tracker update.

Do them in order. Writing docs for a project with eleven open issues wastes the writing, because
the answers change.

---

## Phase 1: audit

Nothing about the project is modified in this phase. No commits, no edits to existing files, no
tracker changes. The point is to find out whether this project is actually finishable today, and
the audit is worthless if it has already started changing the thing it is measuring.

The one thing you do write is the closeout report itself. That is the output of the audit, not a
change to the project, and it belongs on disk rather than only in the conversation so the next
person can read it. Create it; do not edit anything else.

### Fetch before you compare anything

Run `git fetch --all` before reading any branch or remote state.

Remote-tracking refs are a local cache. They are as old as the last fetch, which on a project
nobody has touched for a month means they can be wildly wrong. Comparing against them and reporting
the result as fact produces confident, specific, completely false findings, and "your production
code is not in version control" is exactly the kind of false alarm that costs somebody a bad
afternoon.

This has already happened once. An audit reported that a project's live script existed only in an
untracked folder and that the remote held a month-old version. The remote actually held the current
code with full history; the local clone had simply never been fetched. The report's own
"could not verify" section correctly said Forgejo had not been contacted directly, and the verdict
was written as though it had been.

If you cannot reach the remote, that is a finding in its own right. Say the comparison could not be
made, rather than quietly falling back to the cache.

### Establish what the project is

Read the repo. `README`, the entry point, the config, the commit history, any existing docs.
Work out what it does, who uses it, what it connects to, and whether it is still alive. Start
there rather than opening with questions: the repo answers most of them, and a summary given from
memory is usually less accurate than the code. Ask about what the repo genuinely cannot tell you,
which is normally intent, history and who relies on it.

Identify two things specifically, because they decide which docs are required at all:

- **Do standard, non-technical people interact with it?** If yes, user docs are in scope. If it
  is an invisible backend, they are not, and manufacturing them is noise.
- **Does it connect two or more systems?** If yes, the integration registry is in scope. This is
  the record an auditor or a business owner asks for, and technical docs reliably omit exactly
  the fields they want.

### Find what is outstanding

Check, in this order, and report what you find rather than fixing it:

1. **The tracker.** Look at which project-management tools you actually have available in this
   session. Use whichever is registered. If several are, ask which one this project lives in. If
   none are, say so in the report and flag that the board will need updating by hand.
   Look for: the project's own card or board, its status, open work items, and whether the
   firm-wide roll-up card exists and is current. Every project is expected to carry a card on the
   roll-up board that leadership reads, even when it also has its own dedicated project.
2. **Open issues and pull requests** on the repo. An unmerged PR or an open bug is outstanding
   work regardless of what the board says.
3. **Uncommitted or unpushed work**, and any branch that is ahead of the main branch. Finished
   work stranded on a feature branch is a common and quiet failure.
4. **TODO, FIXME and HACK markers** in the source. Not all of them matter; the ones that describe
   unfinished behaviour do.
5. **The six doc types.** Which exist, and for each that exists, whether it is real or a stub.
   A file called `TROUBLESHOOTING.md` containing three bullet points is a gap, not a doc.
   Judge each against its reference file, not against whether a file is present.

### Produce the report

Write it using `references/audit-report.md`. It is the artifact the user reads to decide what
happens next, so it needs to be honest and specific: "no admin doc" is useless, "no admin doc, so
nobody but you knows the job runs on a 6am timer or where its log lands" is the finding.

### The gate

**If nothing is outstanding, keep going.** A clean project should not be stopped to be told it is
clean. Say so and move into phase 2.

**If something is outstanding, stop and report it.** Show the user what you found and ask what
they want to do: fix it now, close it out anyway, or stop here. Then continue either way.

When the user chooses to proceed past a finding, record that in the report as a knowing decision,
with what was skipped and that they accepted it. The purpose is not to shame anyone into
compliance; it is that six months later the difference between "we decided to skip the testing
report" and "nobody noticed there was no testing report" matters enormously to whoever is reading.

---

## Phase 2: author

Write what is missing. Read the relevant reference file before writing each doc; they carry the
shape, the required content and the failure modes for each type.

| Output file | Template to copy | Reference | Required when |
|---|---|---|---|
| `README.md` | `assets/templates/README.md` | `references/doc-set-index.md` | Always |
| `Dev-Guide.md` | `assets/templates/Dev-Guide.md` | `references/dev-docs.md` | Always |
| `Admin-Guide.md` | `assets/templates/Admin-Guide.md` | `references/admin-docs.md` | Always |
| `User-Guide.md` | `assets/templates/User-Guide.md` | `references/user-and-stakeholder.md` | Only if non-technical people use it |
| `Stakeholder-Brief.md` | `assets/templates/Stakeholder-Brief.md` | `references/user-and-stakeholder.md` | When there is no User-Guide |
| `Troubleshooting.md` | `assets/templates/Troubleshooting.md` | `references/troubleshooting-docs.md` | Always |
| `Testing-Report.md` | `assets/templates/Testing-Report.md` | `references/testing-docs.md` | Always |
| `Integration-Registry.md` | `assets/templates/Integration-Registry.md` | `references/integration-registry.md` | When it connects two systems, or an auditor or business owner will ask |
| `Closeout-Report.md` | `assets/templates/Closeout-Report.md` | `references/audit-report.md` | Always, written in phase 1 and updated in phase 3 |

### Fixed spine, variable content

Projects genuinely differ. A scheduled automation, an MCP server, a deployment script and a web
app do not need the same material, and pretending otherwise produces padded docs full of
"N/A" that nobody trusts. At the same time, if every project invents its own layout, the doc set
stops being a standard and becomes nine unrelated documents.

So the split is: **the numbered top-level headings are fixed, everything inside them is yours.**

**Fixed - never change these:**

- The output file names in the table above
- The numbered top-level headings (`## 1. What this is`, `## 2. Before you start`, ...) - exact
  wording, exact order
- The audience and last-reviewed block at the top of each template

A reader who has used one project's `Troubleshooting.md` can then open any other project's and go
straight to section 2 for the symptom index. That property is worth more than any local
improvement to the layout, which is why the spine is not yours to optimise.

**Variable - expected to differ per project:**

- Everything under a heading: subsections, tables, rows, commands, depth
- How long each section is. A section can be one line or three pages
- Project-specific subsections, added *inside* the relevant numbered section rather than as new
  top-level ones
- Which optional documents exist at all (User Guide, Integration Registry)

**When a section genuinely does not apply**, keep the heading and write `Not applicable - <reason
in one line>.` Do not delete it. A deleted heading is indistinguishable from an overlooked one,
and the reason something is empty is often the most useful line on the page: "IP restrictions:
none configured" is an answer, a missing IP restrictions heading is an open question an auditor
will ask you about later.

Use judgement about how much "not applicable" is reasonable. If most sections of a document are
empty, that usually means the document was not required for this project in the first place, or
the project is not as finished as it looks. Say so in the report rather than shipping a hollow doc.

### Other rules for writing each doc

**Read the template file and copy it.** Do not reconstruct it from memory or from the reference
file's prose. The file on disk is the authority.

**Work out the project's shape first.** Read `references/project-profiles.md` before writing
anything. It covers the common project types and, for each, which documents are required, which
sections carry the weight, and which are routinely not applicable. This is what stops a scheduled
automation being documented as though it were a web application.

**Fill every placeholder.** Templates use `<angle brackets>` for content you supply. If any `<...>`
survives into a finished document, it is not finished. Search for `<` before calling it done.

**Match the existing doc set if the project already has one.** If a project already has docs under
different names, keep its names and map the template's sections into them rather than creating a
parallel set. Consistency inside one project beats consistency with the template, and two
overlapping doc sets is the worst outcome available. Note the mapping in the report.

The reference files explain how to fill each section well, with examples of what good and bad
content looks like. Read the relevant one before writing that doc.

### Where the docs go

Resolve in this order, and stop at the first that applies:

1. **An Obsidian vault**, if the workspace has one. Docs go in the vault under the project's own
   folder, matching the layout already in use there.
2. **The user's existing convention**, if there is no vault but the repo or their `CLAUDE.md`
   shows an established pattern. Follow what they already do rather than imposing a new layout on
   someone's repo.
3. **Ask**, if there is no vault and no discernible convention. One question, then remember the
   answer for the rest of the run.
4. **The repo**, as the fallback. A self-contained doc set that travels with the code.

Say in the report where the docs ended up. Someone reading the report later should not have to
search for them.

### How to write, regardless of type

**Write for someone who has never seen this.** The test is not "is this accurate", it is "could a
competent stranger act on this alone". If a reader would have to come find the author to proceed,
it is not finished.

**State prerequisites and access up front.** What accounts, permissions, tools and secrets are
needed before step one. Nothing is more useless at 3am than a runbook whose first step silently
assumes an admin role the reader does not have.

**Explain the why, not only the what.** The non-obvious decisions, the gotchas, the bugs that were
fixed and must not come back. A reader who knows why can adapt when reality differs from the doc.
A reader who only knows what gets stuck at the first divergence. This is the single largest
quality difference between docs that work and docs that technically exist.

**Cross-reference rather than duplicate.** Each fact gets one home; everything else links to it.
Duplicated facts rot, because one copy gets updated and the other quietly becomes a lie.

**Use real values and real paths**, with a clearly marked section for whatever is
environment-specific, so a reader knows which parts to change and which to trust.

**Never write a secret into a doc.** Record where each credential lives, never its value. If you
encounter a live secret while reading the project, do not copy it into anything, and mention in
the report that it is exposed if it is sitting somewhere it should not be.

**Use markdown links inside repos**, `[text](relative/path.md)`, with spaces URL-encoded as `%20`.
Obsidian-style `[[wiki-links]]` render as dead text in most repo web UIs, so they are fine only in
vault notes that never ship inside a repo.

---

## Phase 3: closeout

### Git

Assume GitHub unless the repo's remote says otherwise; if it is hosted somewhere else, the same
steps apply through that host's equivalent and its own CLI or web UI.

1. **Commit everything of value** with messages that explain why, not just what.
2. **Remove stray files** - scratch output, downloaded duplicates, stale logs - and extend
   `.gitignore` so the category cannot come back.
3. **Confirm no secrets are committed**, including in history if anything looks like it was
   committed and later deleted.
4. **Run the link check.** The script ships with this skill, so call it at its own location, not
   relative to the project you are auditing:

   ```
   python "${CLAUDE_PLUGIN_ROOT}/skills/project-closeout/scripts/check_links.py" <docs-root> --wiki
   ```

   If `CLAUDE_PLUGIN_ROOT` is not set, the skill is installed directly rather than as a plugin; use
   the path to this skill's own directory instead. It walks every `](...)` target and reports the
   ones that do not resolve, and `--wiki` additionally flags `[[wiki-links]]`, which render as dead
   text in most repo web UIs. Dead links are the most common defect in a doc set that was otherwise
   written carefully, because paths move after the writing and nobody re-reads their own links.
5. **Open a pull request** into the main branch rather than pushing to it directly. The PR body
   should say what the project is and what this change closes out, so the PR itself is a readable
   record.
6. **Let the repo's review run**, and work through whatever it reports. If an automated reviewer
   is configured, confirm it actually ran rather than trusting a clean result; review tools can
   exit successfully while having been rate-limited, unlicensed or skipped, and "no findings" then
   means "not reviewed".
7. **Do not merge on the author's behalf.** A human approves and merges. Say the PR is ready and
   leave it.

### Release

Decide whether a release is warranted, then ask before cutting one.

A release makes sense when the project ships something a person installs, deploys or pulls: a
package, a binary, a container image, a script that gets distributed. It does not make sense for a
documentation-only change, an internal automation that simply runs, or a project whose delivery
mechanism is the main branch itself.

Make the call, explain the reasoning in one line, and ask. If yes, tag it and write notes drawn
from the change history rather than from the raw commit log, because a reader wants to know what
changed for them, not which files moved.

### Tracker

Update whichever project-management tool is in use:

- Move the project's card to done, with a completion note saying what shipped and where the docs
  are.
- Update the firm-wide roll-up card so it reflects the finished state. The roll-up is what
  leadership reads, and a dedicated project board does not excuse a stale card on it.
- Close any work items the closeout actually resolved. Leave the ones it did not, and say so.

### Final report

Update the audit report from phase 1 with what was done: which docs were written and where, what
the link check found, the PR link, the release if one was cut, and the tracker state. Include
anything knowingly skipped at the gate.

That closing report is what makes this repeatable. The next person to touch the project starts by
reading it.

---

## When the project is not yours

This skill gets used on projects the reader did not build, and on other people's machines where
the conventions differ. Two habits matter there.

Prefer discovery over assumption: read what the repo and the workspace already do, and match it.
An imposed layout that fights the existing one makes the doc set harder to maintain than no doc
set at all.

And be straight in the report about what you could not verify. An audit that quietly assumes the
tests pass because a test directory exists is worse than one that says "tests present, not run,
unverified". The value of this whole process is that its output can be trusted.
