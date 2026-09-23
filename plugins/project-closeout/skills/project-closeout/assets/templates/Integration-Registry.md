# <Project Name> - Integration Registry

> **Audience:** a business owner, auditor or reviewer asking what this connects to, who owns it,
> and what happens when it breaks.
> **Last reviewed:** <YYYY-MM-DD>

This is the business and audit record. Most of its content is one or two lines sourced from the
other documents; its value is having those facts in one auditable place, in a shape an audit
recognises.

Answer every field. Where something is not configured, write "None configured" rather than leaving
it blank - a blank reads as "unknown" to an auditor and generates a follow-up question.

## 1. Ownership and status

| Field | Value |
|---|---|
| **Integration name** | <name> |
| **Business owner** | <the role or team who *uses* it and decides what it should do> |
| **Technical owner / maintainer** | <the role or team who *built and supports* it> |
| **Built by** | <say explicitly if one team built it for another> |
| **Support contact** | <role and channel> |
| **Vendor** | <if a third-party product is involved, else "None - built in-house"> |
| **Environment** | <production / staging / pilot> |
| **Status** | <active / paused / retired> |
| **Criticality** | <high / medium / low> - <one-line justification> |
| **Last reviewed** | <YYYY-MM-DD> |

<Business owner and technical owner are different people and auditors ask for both. If IT built
this for another department, that distinction is exactly what they are checking.>

## 2. Systems and direction

| Field | Value |
|---|---|
| **Source system** | <name and environment> |
| **Destination system** | <name and environment> |
| **Direction** | <one-way source to destination / bidirectional> |
| **Integration type** | <REST API / CSV / database / built-in connector / file share> |
| **Authority on conflict** | <which system wins when both changed, or "not applicable"> |

## 3. Authentication

| Field | Value |
|---|---|
| **Method** | <OAuth 2.0 / API token / certificate / service account> |
| **Identity used** | <the account or app registration name> |
| **Secret location** | <where it is stored - never the value> |
| **Expiry** | <date, or "does not expire"> |
| **MFA** | <enabled / not applicable for service identity> |
| **Permissions granted** | <the specific scopes or roles, not "full access"> |

<Record where each secret lives, never what it is. If a credential is currently stored somewhere
inappropriate, that belongs in the risk register in section 8.>

## 4. Schedule

| Field | Value |
|---|---|
| **Trigger** | <schedule / event / manual> |
| **Frequency** | <e.g. every 15 minutes, weekdays 06:00 EDT> |
| **Typical duration** | <e.g. 40 seconds> |
| **Volume** | <e.g. 200-400 records per run> |

## 5. Data flow

<Two to five sentences describing what data moves, in what order, and what transforms happen on
the way. A reader should understand the shape of it before reaching the field table.>

## 6. Field mapping

| Source field | Destination field | Transformation |
|---|---|---|
| <field> | <field> | <none / the rule applied> |

<This table is the heart of the registry and the thing most often asked for. Include every mapped
field. Where a value is computed or defaulted rather than copied, say how.>

## 7. Dependencies

| Depends on | For what | Impact if unavailable |
|---|---|---|
| <system or service> | <what it provides> | <what happens> |

**Deliberately does not depend on:** <things a reader might assume are involved but are not. This
prevents wasted investigation during an incident.>

## 8. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <e.g. source API deprecation> | <low/med/high> | <consequence> | <what is in place, or "none - accepted"> |

<Standard candidates worth considering for every integration: upstream API outage, schema or
mapping drift, vendor upgrade incompatibility, secret or certificate expiry, quota exhaustion,
silent partial failure, and the maintainer leaving.>

## 9. Security

| Field | Value |
|---|---|
| **Roles and permissions** | <who or what can invoke it> |
| **Encryption in transit** | <e.g. TLS 1.2+> |
| **Encryption at rest** | <where data lands and how it is protected> |
| **TLS version** | <explicit version> |
| **IP restrictions** | <the allowlist, or "None configured"> |
| **Data classification** | <what sensitivity of data passes through> |
| **Personal data involved** | <yes and what / no> |

## 10. Recovery procedure

<What to do when it fails and data is missing or wrong. Whether a re-run is safe and idempotent,
how to replay a specific window, and what must be cleaned up first. Cross-reference the Admin
Guide rather than repeating its detail.>

## 11. Change history

| Date | Version | Change | Author |
|---|---|---|---|
| <YYYY-MM-DD> | <version> | <what changed, in a sentence a non-engineer understands> | <role> |

<Human-readable, not a git log. An auditor wants "added cost-centre field to the mapping", not
forty commit subjects.>

## 12. Related documents

- [Developer Guide](Dev-Guide.md)
- [Admin Guide](Admin-Guide.md)
- [Troubleshooting](Troubleshooting.md)
- [Testing Report](Testing-Report.md)
