# Doc set README

Template: `assets/templates/README.md`

The front door. Its only job is to get a reader to the right document in seconds, so it should be
short and almost entirely navigation.

## The one test that matters

Can a reader who does not know what any of these documents contain still pick the right one on
their first try?

That is why the routing table is phrased as **"if you want to..."** rather than as a list of
document names. A reader knows what they want; they do not know what you called it.

## Section notes

### The routing table

Keep the order roughly by audience breadth: the non-technical reader first, the technician in an
incident early, the developer later. Someone in trouble should not have to scroll past the module
map to find Troubleshooting.

Remove a row only when the document genuinely does not exist for this project. Never link to a
document that was not written - a dead link in the index is worse than an absent row, because it
sends a reader looking for something that is not there.

### At a glance

Six or seven facts that answer the questions asked most often about any project: where the code
lives, where it runs, what triggers it, who owns it, what it touches. If a reader only ever reads
this table, they should still know roughly what they are dealing with.

### The 30-second version

Written for someone who landed here mid-incident. What it does, when it runs, and the first thing
to check if it looks broken, with a link straight into the relevant Troubleshooting section.

This is the highest-traffic paragraph in the whole doc set. Write it last, once you know what the
most common failure actually is.

## Where this file goes

Beside the rest of the doc set, whether that is a vault folder or a directory in the repo.

If the repo already has a root `README.md` serving a different purpose - describing the software
rather than indexing its documentation - do not overwrite it. Put the doc set index alongside the
other documents and add one link from the root README pointing at it. Overwriting a project's
front page is the kind of "improvement" that gets the whole doc set reverted.

## Failure modes to avoid

**Turning it into a summary.** If the index explains the project, readers stop clicking through and
the real documents rot unread.

**Listing documents by name only.** "Admin Guide" does not tell a new reader whether it is what
they need.

**Letting it go stale.** It is the most-read and least-updated file in any doc set. Check it last,
after everything else is written, and confirm every link resolves.
