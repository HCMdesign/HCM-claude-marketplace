# Provenance - project-closeout

| Field | Value |
|---|---|
| Upstream | **None. Authored at HCM.** This is the first first-party plugin in the catalog |
| **Pinned to** | Not applicable - there is no upstream commit to pin. The source of truth is this repository |
| Found on | Not applicable |
| Upstream version string | Not applicable |
| Published as | `1.0.0` |
| Licence | HCM internal. No third-party code is included, so no upstream licence is carried |
| Vendored | 2026-09-23 (authored, not vendored) |
| Author | HCM IT |
| Reviewer | **NOT YET REVIEWED - must be filled in before merge** |
| Static scan | **NOT YET RUN - result must be recorded here before merge** |
| Semantic scan | **NOT YET RUN - result must be recorded here before merge** |
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
| 2, author | Create and edit documentation files, in a vault or in the repository |
| 3, closeout | Commit, **delete stray files it judges to be scratch**, **edit `.gitignore`**, push a branch, open a pull request, create a tag and a release, and change work-item state on the tracker |

The deletions and the `.gitignore` edits in phase 3 are the only non-documentation changes it makes
to a project's own files, and they are the ones a reviewer should look hardest at. Both are driven
by the model's judgement about what counts as scratch, which is a judgement it can get wrong.

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

## Review status

Opened as a pull request by the author's own session. Per this repository's rules the gate runs on
the PR and a person reviews and merges; neither has happened yet at the time this record was
written. Fill in the reviewer and both scan results before merging, and do not treat this file's
presence as evidence that either step was completed.

## Not in `autoinstall.json`

Deliberately. Adding a name there is a fleet deployment rather than a catalogue entry, and this
plugin has not been used on a real project by anyone but its author yet. It is available on request
via `/plugin install project-closeout@hcm`. Promoting it to the auto-install list should be a
separate, deliberate decision once it has some mileage.
