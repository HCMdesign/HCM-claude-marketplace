# Project profiles

Read this before writing any document. It decides which documents this project needs and where the
weight should fall, so the doc set fits the project instead of being padded out to a uniform shape.

Pick the closest profile. Many projects are a blend; take the dominant one and borrow from the
other. If none fit, use the "Judging an unlisted project" section at the end.

State in the closeout report which profile you used. A reviewer needs to know what you assumed.

---

## Quick selection

| If the project... | Profile |
|---|---|
| Runs on a schedule with nobody watching | [Scheduled automation](#scheduled-automation) |
| Exposes tools to an AI client over MCP | [MCP server](#mcp-server) |
| Is a command or script people run themselves | [CLI tool or script](#cli-tool-or-script) |
| Is deployed to many machines by an RMM or installer | [Fleet deployment](#fleet-deployment) |
| Serves a UI or API to users over the network | [Web application or service](#web-application-or-service) |
| Is imported by other code | [Library or package](#library-or-package) |
| Moves data between two systems | [Integration or sync](#integration-or-sync) |
| Produces documents, config or policy, not running code | [Documentation or configuration](#documentation-or-configuration) |
| Was built to answer a question and may not continue | [Proof of concept or pilot](#proof-of-concept-or-pilot) |

---

## Scheduled automation

Runs unattended. The defining risk is silent failure: it stops working and nobody notices for
weeks.

**Required:** Dev, Admin, Troubleshooting, Testing, Stakeholder Brief
**Also required if it touches two systems:** Integration Registry
**User Guide:** no, unless humans interact with its output in a way that needs explaining

**Where the weight goes:**
- Admin section 3 (*Is it running right now?*) and section 4 (*Logs and analytics*) are the most
  important pages in the whole set. An operator needs to answer "did it run last night?" in one
  command.
- Admin 4.3 (*normal volume*) matters more here than anywhere else. Without numbers, nobody can
  tell "quiet day" from "broken for a week".
- Admin 5.3 (*clean up after a bad run*) - unattended jobs fail halfway and leave partial state.
- Troubleshooting 5 (*known issues*) - recurring benign warnings waste enormous time if
  undocumented.

**Usually light:** Dev 5 (*onramp*) if it is a small script.

**Commonly missed:** what happens to missed runs. If the machine was off at 06:00, does it catch
up, skip, or double-process? Answer it in Admin 5.2.

---

## MCP server

Exposes tools to an AI client. Two audiences: the person installing it, and the model calling it.

**Required:** Dev, Admin, Troubleshooting, Testing
**Also required:** Integration Registry, if it reaches a third-party system on the user's behalf
**User Guide:** yes if non-technical staff install or use it; often they do

**Where the weight goes:**
- Dev 4.1 (*module map*) should list every exposed tool, what it does, and its permission level.
  This is the surface area, and it is what a reviewer checks first.
- Dev 4.3 (*invariants*) - any read-only or guardrail constraint belongs here, explicitly. If the
  server refuses certain operations by design, that is an invariant, not a limitation.
- Admin 6 (*secrets*) - per-user tokens and OAuth flows, including what happens when one expires.
- Troubleshooting - registration problems dominate: server not appearing in the client, auth
  failures, stale config after an update.

**Commonly missed:** how the user confirms it is registered and working, as distinct from
installed. Put an explicit check in Admin 3.

---

## CLI tool or script

A person runs it deliberately.

**Required:** Dev, Admin, Troubleshooting, Testing, User Guide
**Integration Registry:** only if it connects systems

**Where the weight goes:**
- User Guide carries this profile. Every flag, realistic examples, and what each error message
  means.
- Dev 3.4 (*adapt to your instance*) if it is run across different environments.
- Troubleshooting 4 (*symptom to source map*) - users report error text verbatim, so that table is
  how support finds the cause fast.

**Usually light:** Admin sections about scheduling and unattended operation. Keep the headings,
write "Not applicable - run on demand by a person."

---

## Fleet deployment

Installed onto many machines by an RMM, installer or management tool. The defining risk is that a
failure is multiplied by the size of the fleet, and a rollback is expensive.

**Required:** all of Dev, Admin, Troubleshooting, Testing, Stakeholder Brief
**User Guide:** usually yes, even if brief - end users see the result

**Where the weight goes:**
- Dev 3 (*rebuild runbook*) must cover the management-tool side: the exact step configuration,
  parameters and schedule, because that half does not live in the repo.
- Dev 4.3 (*invariants*) - privilege model, install scope, per-user versus machine-wide. These are
  where deployment bugs come from and they are rarely obvious from the code.
- Admin 5 (*routine operations*) needs a genuine rollback procedure, not just "disable".
- Testing must distinguish what was proven on a real endpoint from what was only proven offline.
  An untested assumption at fleet scale is the single most expensive defect class here.
- Troubleshooting needs an explicit "it reported success but did not work" entry, because that is
  the characteristic fleet failure.

**Commonly missed:** the difference between "the script ran" and "the thing is installed and
usable by the person at the keyboard". Say how to verify the second.

---

## Web application or service

Serves users over the network.

**Required:** Dev, Admin, Troubleshooting, Testing, User Guide
**Integration Registry:** if it talks to other systems, which it usually does

**Where the weight goes:**
- Dev 3.1 (*infrastructure*) - hosting, DNS, certificates, reverse proxy, identity provider.
- Admin 4 (*logs*) - application, web server and platform logs are different places; say which
  answers which question.
- Admin 5 (*routine operations*) - restart, deploy, roll back.
- Troubleshooting - user-visible symptoms first: cannot log in, page is blank, slow, error 502.

**Commonly missed:** certificate and secret expiry dates. Put them in Admin 6 with real dates.

---

## Library or package

Imported by other code. The audience is a developer who will depend on it.

**Required:** Dev, Testing, User Guide (as API documentation)
**Admin:** usually thin, but keep it for release and versioning policy
**Troubleshooting:** integration problems rather than runtime incidents

**Where the weight goes:**
- Dev 4 (*code audit orientation*) and the public API surface.
- Versioning and breaking-change policy - put it in Admin.
- Testing - coverage of the public interface specifically.

**Usually not applicable:** most of Admin 3, 4 and 5. It does not run on its own. Keep the
headings and say so.

---

## Integration or sync

Moves data between two systems. This profile always produces an Integration Registry, and that
document is the deliverable a business owner or auditor actually asks for.

**Required:** all six, without exception

**Where the weight goes:**
- Integration Registry, in full. The field-mapping table is the heart of it.
- Dev 4.3 (*invariants*) - idempotency, deduplication, what happens on partial failure, whether a
  re-run is safe.
- Troubleshooting - mapping drift, upstream schema changes, auth expiry.
- Testing - evidence that a failed sync recovers correctly, not only that a good sync works.

**Commonly missed:** direction and authority. Which system wins on conflict, and what happens to a
record deleted on one side. State it explicitly.

---

## Documentation or configuration

Produces documents, policy or configuration rather than running code.

**Required:** Dev (thin - what it is, where it lives, how to change it), Stakeholder Brief
**Testing:** becomes a validation record - who reviewed it, against what, and when
**Admin and Troubleshooting:** usually thin

**Where the weight goes:**
- Who owns the content and how a change gets approved.
- Where the authoritative copy lives, and how copies elsewhere are kept from drifting. Duplicated
  documentation rots, and this profile is where that happens most.

**Usually not applicable:** anything about runtime, logs or incidents. Keep the headings, say so.

---

## Proof of concept or pilot

Built to answer a question. May be promoted, may be retired. The most common documentation failure
here is treating it as permanent, and the second most common is leaving no record when it is
retired.

**Required:** Stakeholder Brief (carrying the finding), Dev (thin), Testing (the evidence for the
conclusion)
**Everything else:** proportionate - a pilot does not need a 3am runbook

**Where the weight goes:**
- The Stakeholder Brief must state the question, the answer, and the recommendation. That is the
  entire value of the project.
- Say plainly whether it is still running, and if so, who is paying for it and when it gets
  reviewed.
- If it is being retired, say what was turned off, what was kept, and where the data went.

**Commonly missed:** an explicit status. A pilot with no recorded decision becomes permanent
infrastructure by accident, and nobody can later say who agreed to that.

---

## Judging an unlisted project

If nothing above fits, decide each document on its own merits with these questions:

- **Dev** - always required. Someone will need to rebuild or review it.
- **Admin** - does it run on its own, or hold state, or need credentials? If any yes, required.
- **User Guide** - do non-technical people interact with it directly? Only then.
- **Stakeholder Brief** - required when there is no User Guide. Someone non-technical should be
  able to learn what this is and why it exists in one page.
- **Troubleshooting** - can it fail in a way somebody has to fix? Then required.
- **Testing** - always required. If nothing was tested, that is itself the finding, and it belongs
  in the report rather than being quietly omitted.
- **Integration Registry** - does it connect two systems, hold credentials for another system, or
  move data across a boundary? Then required.

When in doubt, write the document. A thin document with honest "not applicable" lines is more
useful than a missing one, because it proves the question was asked.
