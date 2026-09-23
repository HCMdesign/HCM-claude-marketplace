# <Project Name> - Admin Guide

> **Audience:** whoever operates this day to day, including at 3am during an incident.
> **Last reviewed:** <YYYY-MM-DD>

## 1. What it does, in one paragraph

<Plain description for an operator. Not architecture. What it does, when, and what depends on it.>

## 2. When it runs

| | |
|---|---|
| **Trigger** | <schedule, event, or manual> |
| **Frequency** | <e.g. every weekday 06:00 EDT> |
| **Typical duration** | <e.g. 40-90 seconds> |
| **Runs as** | <the account or identity> |
| **Host** | <where it executes> |

## 3. Is it running right now?

The first check, before anything else.

```
<The exact command or query. Not "check the logs" - the literal thing to run.>
```

**Healthy looks like:** <specific output>
**Unhealthy looks like:** <specific output>

## 4. Logs and analytics

### 4.1 Where the logs are

| Log | Location | Retention |
|---|---|---|
| <name> | <exact path or console location> | <how long> |

### 4.2 Queries to read them

<For each question an operator actually asks, give the literal query. Not a description of how to
search - the query itself, ready to paste.>

**Did the last run succeed?**
```
<query>
```

**What failed in the last 24 hours?**
```
<query>
```

**<Other question this project's operators ask>**
```
<query>
```

### 4.3 What normal volume looks like

<Numbers, so an operator can tell "quiet" from "broken". E.g. "normally 200-400 records per run;
under 50 means the upstream export is late.">

## 5. Routine operations

### 5.1 Disable it

```
<commands or console steps>
```
<What happens while it is disabled. What backs up, what is simply skipped.>

### 5.2 Re-enable it

```
<commands or console steps>
```
<Whether it catches up on missed work automatically, or whether something must be replayed.>

### 5.3 Clean up after a bad run

<Exact steps. What is safe to delete, what must be preserved, what needs replaying, and in what
order. This is the section people need when they are already stressed, so be concrete.>

### 5.4 Re-run manually

```
<commands>
```

## 6. Secrets and rotation

| Secret | Where it lives | Rotation schedule | Expires | Who can rotate it |
|---|---|---|---|---|
| <name> | <location, never the value> | <cadence> | <date if known> | <role> |

**How to rotate:** <the procedure, including anything that must be restarted afterwards>

<Never record a secret's value here. If one is currently stored somewhere it should not be, say so
and treat it as a finding.>

## 7. Contacts

| Role | Who | When to involve them |
|---|---|---|
| Technical owner | <role or team> | <e.g. code changes, failures that survive the troubleshooting guide> |
| Business owner | <role or team> | <e.g. changes to what it should do> |
| Vendor support | <name and channel> | <e.g. platform outages> |

<Use roles or teams rather than individual names where possible, so the doc survives people
changing jobs.>

## 8. Related documents

- [Troubleshooting](Troubleshooting.md) - start here when something is broken
- [Developer Guide](Dev-Guide.md) - rebuild and code review
- <Add others that exist for this project>
