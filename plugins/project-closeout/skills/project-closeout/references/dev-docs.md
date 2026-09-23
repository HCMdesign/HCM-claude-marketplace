# Dev docs

The developer set does three jobs. They are often split across three files, but one file with
three clear sections is fine if the project is small. What matters is that all three are covered,
because they serve different readers arriving with different problems.

1. **Rebuild** - someone has to stand this up again, possibly after it was lost.
2. **Audit** - someone has to review or verify the code without having written it.
3. **Onboard** - someone has to start contributing.

---

## 1. The rebuild runbook

**Start from the git repo.** The repo is the source of truth, and the code, config templates and
committed scaffolding are the artifact. Do not write instructions to hand-rebuild anything that
already lives in version control; that guide will be wrong within a month and it duplicates
something git already does perfectly.

What the runbook documents is **everything that cannot live in a repo**:

- Cloud resources and how they are configured
- Identity: app registrations, service principals, OAuth clients, their permissions and consent
- Service accounts and what they are entitled to
- DNS, certificates, network rules
- External templates, tenant-level settings, third-party dashboard configuration
- Anything created by clicking in a vendor's web UI

For each, record what it is, why it is configured that way, and what breaks without it.

Then hand off to the repo: clone, configure, deploy.

### Prerequisites section

Open with what the reader needs **before step one**: accounts, roles, permissions, tooling with
versions, network access, and which secrets they will need and where to obtain them. A runbook
whose third step silently requires Global Admin has wasted the reader's evening.

### The "adapt to your instance" section

List every environment-specific knob in one place: hostnames, tenant IDs, resource names, paths,
ports, schedule times, quota limits. A reader rebuilding into a different environment should be
able to work from this list rather than grepping the whole doc for things that look like they
might be local.

Use real values in the body. Placeholders like `<your-server>` throughout make a doc unreadable
and untestable; real values plus a clear adapt list is better on both counts.

---

## 2. Code-audit orientation

This is the section most projects skip, and it is the one that decides whether anyone can safely
change the code later. Write it for a competent engineer who has never opened this repo and needs
to review it.

**Module map.** Which file owns what. A table is usually the right shape. Not every file, the ones
that carry meaning.

**Control-flow walkthrough.** The entry point, and the order things happen. What triggers a run,
what it does first, where it branches, where it ends. A reader should be able to follow one
request or one scheduled run end to end from this section alone.

**Non-obvious invariants.** The design rules that must not be broken, and the reason each exists.
This is where past bugs go: the guard that looks redundant, the ordering that looks arbitrary, the
check that looks paranoid. Each one is usually a scar. Say what happened.

Write these as statements a reviewer can check against a diff:

> Settings are merged, never overwritten. An earlier version rewrote the file wholesale and
> destroyed user configuration on every run.

> The worker runs unelevated. It was elevated once, which registered the package to the
> administrator rather than the signed-in user, and the application vanished for the actual user.

**What is deliberately not in the repo.** Secrets, infrastructure, generated artifacts, vendored
binaries. Say where each lives instead. A reviewer who does not know something is intentionally
absent will either assume it is missing or go looking for it.

---

## 3. New developer onramp

The shortest of the three, and purely sequential: clone, configure, run locally, test, deploy.

Include the things that are obvious to the author and invisible to everyone else: which language
runtime version, which package manager, how to get a working local config without production
credentials, how to run the test suite, and what a successful local run actually looks like on
screen so the reader knows whether it worked.

If local development is not possible, say so explicitly and explain how to develop against a
non-production environment instead. Silence here reads as "should be easy" and costs a day.

---

## Quality bar

Before calling the dev set done, check that a reader could:

- Rebuild the surrounding infrastructure from scratch without asking anyone
- Review a pull request and know whether it violates a design rule
- Get a local environment running unaided
- Tell which values in the doc are specific to this environment

If any answer is no, the gap is a real finding, not a nitpick.
