# Integration Registry

Template: `assets/templates/Integration-Registry.md`

The business and audit record. Write it whenever the project connects two systems, holds
credentials for another system, or moves data across a boundary - and whenever a business owner or
auditor will plausibly ask about it.

## Why this exists separately

Technical documentation reliably omits exactly the fields an audit asks for, because they are not
interesting to build with: who owns it in the business, how critical it is, when it was last
reviewed, what TLS version, whether IP restrictions exist. Each is a one-line fact that lives
somewhere else or nowhere. The registry's value is having them in one place, in a shape an audit
recognises.

## The one test that matters

Could someone answer an audit questionnaire about this integration from this document alone,
without opening the code or asking the person who built it?

## Never leave a field blank

A blank reads as "unknown" and generates a follow-up question, which is the outcome this document
exists to prevent. Write the actual answer, including when the answer is nothing:

- IP restrictions: `None configured.`
- Vendor: `None - built in-house.`
- MFA: `Not applicable - service identity, no interactive sign-in.`

"None configured" is a decision a reader can evaluate. A blank is a gap in the record.

## Section notes

### Section 1, ownership

**Business owner and technical owner are different people** and auditors ask for both. The business
owner uses it and decides what it should do; the technical owner built it and keeps it running. If
IT built this for another department, say so explicitly - that is precisely the relationship being
checked.

Criticality needs its one-line justification. "High" on its own is an assertion; "High - payroll
cannot be processed without it" is a fact someone can act on.

### Section 3, authentication

Record where the secret lives, never what it is. Include scopes rather than "full access" - an
auditor's next question is always which permissions, and "full access" is the answer that starts
the difficult conversation.

If a credential is currently stored somewhere it should not be, that goes in the risk register in
section 8 and in the closeout report. Do not silently normalise it.

### Section 6, field mapping

The heart of the document and the thing most often requested. Every mapped field, with the
transformation where the value is not copied verbatim. Computed values, defaults, truncations,
format changes, timezone conversions - each is a place where data silently becomes wrong, and each
is what someone is looking for when they open this table.

### Section 7, dependencies

The "deliberately does not depend on" line saves real time during an incident. When something
breaks, people investigate everything nearby; stating what is *not* involved narrows the search.

### Section 8, risk register

Candidates worth considering for almost any integration:

- Upstream API deprecation or version change
- Schema or mapping drift, where a field changes meaning without changing name
- Vendor upgrade incompatibility
- Secret or certificate expiry
- Quota or rate-limit exhaustion
- Silent partial failure, where some records sync and nobody notices
- Single-maintainer risk

Include the ones that apply with an honest likelihood, and say "none - accepted" where there is no
mitigation rather than inventing one.

### Section 11, change history

Human-readable, not a git log. An auditor wants "added cost-centre field to the mapping" with a
date and an author, not forty commit subjects. One row per meaningful change.

## Failure modes to avoid

**Copying the technical docs.** This is a summary in a specific shape. If a section is growing into
an explanation, it belongs in the Developer Guide with a link from here.

**Writing a secret into it.** Location only, always.

**Leaving last-reviewed unset.** An undated registry cannot be trusted and will be re-derived from
scratch by whoever needs it next.

**Vague direction.** State which system is authoritative and what happens to a record deleted on
one side. Conflict behaviour is the thing that bites, and it is almost never written down.
