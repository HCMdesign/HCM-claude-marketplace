# HCM conventions

The rest of this skill is deliberately tool-agnostic, so it survives HCM changing software. This
file is where the firm's actual tools and standards live. Read it during phase 2 before writing,
and again in phase 3 before touching the tracker.

If you are running this skill outside HCM, skip this file. Nothing else in the skill depends on it.

Everything here is a default, not an override. These are the firm's standing conventions, and they
apply when nobody has said otherwise. A person asking for something different in the moment has
asked for something different: do what they asked, and say which convention you set aside so the
decision is visible rather than silent.

## Writing for an HCM audience

**Refer to people by role, never by name.** "IT", "IT leadership", "your IT admin", "the project
owner". A named individual in a document goes stale the moment they change jobs, and it turns a
reference document into a directory entry. This one is a firm policy rather than a style
preference.

**Keep endpoint IP addresses out.** Write `<public IP withheld>` and say where the real value
lives. Private-range addresses are a judgement call and usually fine inside an internal runbook;
a public-facing address is not. Before calling a doc set done, search it for anything shaped like
an address, the same way you run the link check. Computer names are fine and often necessary.

**Never write an em-dash.** Restructure instead of substituting a different dash: a comma for an
aside, a colon to introduce, parentheses for a parenthetical, or two sentences. Hyphens in
compound words and en-dashes in numeric ranges are both fine. This applies to every artifact the
closeout produces, including commit messages, PR bodies and release notes.

**Give the reader the actual steps.** When a document asks someone to do something in a UI, write
the exact click path, a copy-pasteable command, and what success looks like when it worked. "Enable
the setting in the admin portal" is not a step; it is a reminder to someone who already knew.

**Check that scripts and policy files carry a version.** A version and a short changelog, on line
one of a config, printed at runtime by a script. A reader who cannot tell which version of a file
they are looking at cannot tell whether the documentation matches it.

Where that is missing, record it in the closeout report as outstanding work. Adding it is a change
to the project's own code, which is outside what a documentation closeout should do on its own
initiative, so propose it and let the owner decide rather than editing the script in passing.

**"Publishable-ready" is a hedge, not a status.** Something built generically so that publishing
stays an option later is publishable-ready. It is not open source, and a document should never
imply a licence decision that nobody has made.

## Publishing to Hudu

Hudu is HCM's knowledge base and the destination for documentation that IT operates from. It is an
IT-only audience, which changes how the same facts get written.

**Every article HCM Development maintains opens with the maintenance callout.** It is the very
first element: above the `<h1>`, or first inside the `<body><div class="text-section scrollable">`
wrapper when the article has one. Use this wording exactly, and resist adding a line about where
to send corrections.

```html
<div class="callout callout-info">
<p><strong>Maintained by HCM Development</strong></p>
<p>This article is kept in step with the live system and republished whenever it changes, so edits made directly here will be overwritten. Send corrections instead.</p>
</div>
```

**Re-add it on every edit, not only on create.** A Hudu article edit replaces the whole body, and
the vault source does not carry the callout. Publishing vault content straight over an existing
article silently deletes it. To check coverage across the knowledge base, search Hudu for
`Maintained by HCM Development`.

**Only on articles HCM Development actually maintains.** A colleague's draft or migrated vendor
content belongs to someone else; adding the callout there claims ownership that is not ours.

**Hudu articles are self-contained.** A reader in an incident should not be sent to a repository to
understand what to do, so put the content in the article rather than linking out to source control
for it. Linking to a repo as a pointer to the code itself is fine; linking to it in place of an
explanation is not.

**Never write "tell IT" or "contact IT" in a Hudu article.** The reader is IT. Say what to do.

## Updating the tracker

HCM uses Plane. Three things about it are easy to get wrong and expensive to undo.

**`comment_html` and `description_html` take raw HTML.** Pass `<p><b>x</b></p>`, never the
entity-escaped form. JSON string encoding already handles the quoting, so escaping on top makes
Plane store the markup as literal text. It then renders as visible tags in Plane's own interface
and imports broken everywhere else. On 2026-09-17 this was found in 42 records across 9 projects
and repaired by hand.

To audit an existing record: the `comment_stripped` and `description_stripped` fields are meant to
be tag-free, so if either contains `<` tags, that record is malformed.

This applies to anything posting to Plane through the API, including scheduled services, not only
interactive sessions.

**There is no "Launched" state.** A launched project is Completed.

**Reach Plane through the hosted connector.** The locally installed MCP server has a broken TLS
chain. If Plane tools are missing from the session entirely, say so in the report rather than
recording the tracker step as done.

**Both roll-up boards matter.** Every project carries a card on the firm-wide "ALL Projects" board
even when it has its own dedicated Plane project, and Design Technologies work also carries one on
"DT Projects". A dedicated board does not excuse a stale roll-up card, because the roll-up is what
leadership reads. Move the card in real time rather than batching the updates at the end, and leave
a completion note saying what shipped and where the documentation lives.

**Every documentation update gets its tracker update in the same pass.** A vault change that never
reached the board is invisible to everyone who is not reading the vault.

## Git and review

**Never add a Claude co-author trailer or byline** to a commit message or a pull request body, in
any repository.

**Commit before running a code review.** Reviewing an uncommitted tree with `--include-untracked`
produces findings about files that are not really part of the change, and chasing those wastes the
review. Commit the work, then review the committed tree.

**A rate-limited review is not a review.** The CodeRabbit allowance is shared across every pull
request under the organisation, and the CLI has a separate cap of its own. A green check that says
it was rate limited has reviewed nothing. Confirm the review ran before you treat it as a gate that
passed. This is the HCM-specific version of the general warning in phase 3.

**Pull request review runs on GitHub.** Projects hosted elsewhere follow the same closeout steps
through their own host, but expect the automated review to be absent there, and say so in the
report rather than implying a gate ran.
