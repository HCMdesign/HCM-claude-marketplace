# Provenance - project-closeout

| Field | Value |
|---|---|
| Upstream | **None. Authored at HCM.** This is the first first-party plugin in the catalog |
| **Pinned to** | Not applicable - there is no upstream commit to pin. The source of truth is this repository |
| Found on | Not applicable |
| Upstream version string | Not applicable |
| Published as | `1.1.0` |
| Licence | HCM internal. No third-party code is included, so no upstream licence is carried |
| Vendored | 2026-09-23 (authored, not vendored). Last changed 2026-10-20, see the change log |
| Author | HCM IT |
| Reviewer | **1.0.0:** Hodahel Moinzadeh, reviewed and merged PR #9 on 2026-09-23. **1.1.0: not yet reviewed, must be filled in before merge** |
| Static scan | **1.0.0: clean.** 0 findings, 0 unaccounted, no triage record required, verified 2026-10-19 against merge commit `2c0fe77` by the scheduled catalog scan. The three findings raised on PR #9 were removed by rewording the prose that produced them, rather than by triaging them, in `689af68`. **1.1.0: not yet scanned.** 1.1.0 adds prose that `2c0fe77` does not contain, so that clean result does not cover it; the gate runs on the pull request |
| Semantic scan | **Not run at either version.** The static pass plus review of the one executable was the basis for publication. Recorded rather than implied: a scan that was not run is not a clean scan |
| Baselined findings | none |
| HCM changes | Not applicable - HCM is the author |

> [!note] This record is shaped for vendored third-party code
> Most of the fields above exist to bind a vendored copy to an immutable upstream commit, which is
> the risk this catalog was built to manage. A first-party plugin has no upstream, so those fields
> are marked not applicable rather than removed - a missing row reads as an oversight, and the
> point of the record is that every question was asked.
>
> The scrutiny that replaces the upstream pin is ordinary code review: this plugin is developed in
> the open in this repository, and its history is the provenance.

## Why HCM carries this

HCM has a written project completion standard: a project is not done when it ships, it is done when
a stranger can rebuild it, operate it, or fix it at 3am from the documentation alone. Until now that
standard lived in one person's workspace configuration, so it applied to one machine and nobody
else's.

This plugin turns the standard into something every HCM Claude Code user has. It audits a project
before writing anything, produces a documentation set to a fixed shape, and then handles git
hygiene, the pull request, the release decision and the tracker update.

The audit-first ordering is the part that matters. A half-finished project that gets a complete
documentation set is still half-finished, and now it looks closed on the board.

## What is in it

| Path | What it is |
|---|---|
| `SKILL.md` | The three-phase workflow and the gate between audit and authoring |
| `references/project-profiles.md` | Nine project shapes, and which documents each actually needs |
| `references/*.md` | How to write each document well, with failure modes |
| `references/hcm-conventions.md` | The firm's own rules: documentation voice, publishing to the knowledge base, the tracker, and commit and review habits. The only file in the skill that names HCM's actual tools |
| `assets/templates/*.md` | Nine fill-in templates with fixed section headings |
| `scripts/check_links.py` | Walks every `](...)` target in a doc set and reports dead links |

## Design decisions worth knowing

**Fixed spine, variable content.** The file names and numbered top-level headings are fixed, so a
reader who has used one project's `Troubleshooting.md` can open another and go straight to the
symptom index. Everything inside a heading varies by project. This is the compromise between "every
project is different" and "a standard nobody follows consistently is not a standard".

**Sections that do not apply are kept and marked**, not deleted. A deleted heading cannot be told
apart from an overlooked one, and "IP restrictions: none configured" is an answer where a missing
heading is an open question.

**Tool-agnostic on project management.** The skill encodes the concept - every project carries a
card on the firm-wide roll-up board - and discovers whichever tracker is registered in the session
at run time. It names no specific product, so it survives HCM changing project-management software.

**GitHub by default**, falling back to whatever the repository's remote actually is.

## Security notes for the reviewer

**The one executable.** `scripts/check_links.py` is the only code. It reads markdown files, resolves
relative link targets against the filesystem, and prints what does not exist. It makes no network
calls, writes no files, and takes a single path argument.

**No credentials, no hostnames.** The skill instructs against writing secrets into documentation and
against recording secret values anywhere, only locations. One example in `references/admin-docs.md`
originally used a real internal service name; it was replaced with a generic one before this PR.

For the avoidance of doubt in a scan result: `references/admin-docs.md` contains the illustrative
command `systemctl is-active invoice-poller`, and several templates contain fenced blocks with
placeholder commands. None of these are executed by the skill. They are examples shown to a human
author of what a good runbook entry looks like, and `invoice-poller` is a made-up service name.

**What it can do to a repository.** This is the main thing to weigh, so it is spelled out rather
than summarised. Across its three phases the skill may:

| Phase | What it can do |
|---|---|
| 1, audit | Read the repository, run `git fetch --all`, query whichever tracker is registered, query the repository host for issues and pull requests. Writes one new file, the closeout report |
| 2, author | Create and edit documentation files, in a vault or in the repository. At HCM it may also create and edit knowledge-base articles, which is the one authoring destination outside the machine and the repository: it publishes to an IT-wide audience, and an edit there replaces the whole article body |
| 3, closeout | Commit, **delete stray files it judges to be scratch**, **edit `.gitignore`**, push a branch, open a pull request, create a tag and a release, and change work-item state on the tracker |

The deletions and the `.gitignore` edits in phase 3 are the only non-documentation changes it makes
to a project's own files, and they are the ones a reviewer should look hardest at. Both are driven
by the model's judgement about what counts as scratch, which is a judgement it can get wrong.

**What the HCM reference adds, stated plainly.** `references/hcm-conventions.md` is the only file
that directs work at named systems, and it does so in three places. It has the skill create and
edit knowledge-base articles, where an edit replaces the whole article body and reaches an IT-wide
audience, and where it is told to re-add the maintenance callout on every edit because publishing
source content over an article silently removes it. It has the skill write comments and change
card state in the tracker, which was already within phase 3 but is now specific about the format a
comment body has to take. And it tells the skill never to put a Claude co-author trailer or byline
on a commit or a pull request, which is a deliberate HCM publication decision rather than an
incidental style rule: it keeps AI involvement out of commit history, it is visible to the person
running the skill, and it conceals nothing from them. Every convention in that file is a default
that an explicit instruction overrides, and the skill is told to name any convention it sets aside.

**It can be entered without asking for a closeout.** The description deliberately also triggers on
requests for a rebuild runbook, a troubleshooting guide, a testing report, an integration record, or
"what documentation does this still need". That is intentional, because those requests are usually
the closeout arriving under another name, but it means somebody asking only for a troubleshooting
guide can find themselves in a workflow whose later phases touch git and the tracker. Reviewers
should weigh the trigger breadth and the phase-3 permissions together rather than separately.

**Mitigations are in the workflow, not in code.** Phase 1 changes nothing but its own report.
Phase 3 is instructed never to merge a pull request on the author's behalf, to stop for a human, and
to ask before cutting a release. These are instructions to a model, not enforced constraints, and
should be treated as such.

## Scan findings, and why there is no triage record

The first CI run flagged three `EA2` [MEDIUM] findings. All three were prose, and all three were
**reworded at source rather than triaged**, so this plugin ships with no `triage/` record. That is
a decision a reviewer should check rather than take on trust, so here is exactly what changed.

| File | Scanner matched | Now reads |
|---|---|---|
| `SKILL.md:70` | `Do not\nask the user` | "Start there rather than opening with questions: the repo answers most of them..." |
| `references/dev-docs.md:100` | `without asking` | "Rebuild the surrounding infrastructure from scratch, unaided" |
| `references/troubleshooting-docs.md:86` | `no verification` | "Fixes that skip the verify step." |

**Why reword instead of triage.** Two reasons, and the second is the important one.

First, the scanner had a fair point on the one that mattered. `EA2` looks for language that steers
an agent away from involving the user, and in a file whose entire purpose is instructing an agent,
"Do not ask the user" is exactly the right shape to flag. The original line meant "read the repo
before asking, it is more accurate than a summary from memory", but that is not what it said. The
replacement says what was meant, and says it better. The other two were incidental collisions in
descriptions of documentation quality, and the new wording is clearer in both cases.

Second, the triage mechanism requires `verified_by` - a named person who read the file and
confirmed the finding is benign. Nobody had. Filing three entries under someone's name to turn the
build green would have been forging the exact attestation this catalog exists to collect, which is
a considerably worse outcome than a red build.

**What was not done:** no behaviour changed, nothing was renamed to obscure what it does, and no
capability was removed from the documentation. The meanings are identical or clearer. If a reviewer
disagrees with any of the three, the honest fix is to restore the original wording and file a
proper triage entry with their own name on it.

## Change log

### 1.1.0, 2026-10-20

Added `references/hcm-conventions.md` and three pointers to it from `SKILL.md`, in the writing
section of phase 2 and the git and tracker sections of phase 3.

The skill encoded HCM's completion standard but none of the firm conventions that decide whether
its output is publishable. Several of those were written down after the plugin was, and they lived
in one person's workspace configuration, which is the exact situation this plugin exists to fix.
The ones that mattered most were not stylistic: a Plane comment posted as escaped HTML is stored as
literal markup, which was found in 42 records across 9 projects and repaired by hand; and a
knowledge-base article republished from its source silently drops the maintenance callout, because
an edit replaces the whole body.

They are in a reference rather than in `SKILL.md` for two reasons. `SKILL.md` is always in context
and the references load when they are needed, so the firm specifics cost nothing until the skill is
actually writing or closing out. More importantly, keeping them out preserves the tool-agnostic
design decision recorded above: the workflow still names no product, and the one file that does is
explicitly skippable outside HCM.

### 1.0.0, 2026-09-23

First release. Merged as PR #9.

## Review status

**1.0.0** was opened as a pull request by the author's own session, reviewed by the catalog owner,
and merged as PR #9 on 2026-09-23. The static gate ran on that pull request and has run on every
scheduled catalog scan since; it is clean.

**1.1.0 has not been reviewed or scanned yet.** It adds prose that the scanned tree does not
contain, and prose is what produced every finding this plugin has ever raised, so the clean
1.0.0 result says nothing about it. Fill in the reviewer and the static result before merging.

The semantic pass is outstanding at both versions. CI runs the scanner with `--no-llm`, so that
pass is a local step the reviewer performs, and it has not been done for this plugin at all. That
is a known gap rather than an oversight: do not read this file's presence, or a clean static
result, as evidence that it happened.

## Not in `autoinstall.json`

Deliberately. Adding a name there is a fleet deployment rather than a catalogue entry, and this
plugin has not been used on a real project by anyone but its author yet. It is available on request
via `/plugin install project-closeout@hcm`. Promoting it to the auto-install list should be a
separate, deliberate decision once it has some mileage.
