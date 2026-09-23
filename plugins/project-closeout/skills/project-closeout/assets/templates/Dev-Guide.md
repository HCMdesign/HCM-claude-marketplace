# <Project Name> - Developer Guide

> **Audience:** an engineer who has never seen this project and needs to rebuild it, review it, or
> start contributing to it.
> **Last reviewed:** <YYYY-MM-DD>

## 1. What this is

<Two to four sentences. What the project does, who it serves, and what would break or go undone if
it stopped running. Written so someone outside the team understands it.>

**Repository:** <url>
**Runs on:** <where it executes - a server, a scheduler, a workstation, a cloud service>
**Language and runtime:** <e.g. Python 3.12, Node 20 LTS, PowerShell 5.1>

## 2. Before you start

Everything the reader needs in hand before step one of anything below.

| Requirement | Detail | How to get it |
|---|---|---|
| <Account or role> | <e.g. Contributor on subscription X> | <who grants it> |
| <Tool and version> | <e.g. Docker 24+> | <install source> |
| <Network access> | <e.g. VPN, allowlisted IP> | <how> |
| <Secret> | <name only, never the value> | <where it lives> |

<If there are no prerequisites beyond a clone, write: "Nothing beyond a git clone and <runtime>.">

## 3. Rebuild runbook

The repository is the source of truth. Everything in version control is rebuilt by cloning, not by
hand. This section documents only what cannot live in a repo.

### 3.1 Infrastructure that must exist first

<For each resource that was created outside the repo - cloud resources, app registrations, service
accounts, DNS, certificates, vendor dashboard configuration - give a subsection with: what it is,
how it is configured, why it is configured that way, and what breaks without it. Use real names
and real values.>

<If the project needs no external infrastructure, write: "None. This project is entirely
self-contained in the repository.">

### 3.2 Build and deploy from the repo

```
<The literal commands, in order, from clone to running. Real commands that work.>
```

### 3.3 Verify the rebuild worked

<How the reader confirms success. The exact command or check, and what correct output looks like.
"It should work" is not a verification step.>

### 3.4 Adapt to your instance

Every value below is specific to this environment. Change these and nothing else.

| Setting | Where it lives | This environment's value | Notes |
|---|---|---|---|
| <name> | <file or console path> | <value> | <constraints> |

## 4. Code audit orientation

For a reviewer who needs to verify the code without having written it.

### 4.1 Module map

| Path | Owns |
|---|---|
| <path/to/file> | <what this file is responsible for> |

<Only the files that carry meaning. Do not list every file.>

### 4.2 Control flow

<Walk one complete execution end to end: what triggers it, what happens first, where it branches,
where it ends. A reader should be able to follow a single run through the code from this alone.>

### 4.3 Invariants and past-bug guards

Design rules that must not be broken. Each one states the rule, then why it exists.

| Invariant | Why - what went wrong when it was violated |
|---|---|
| <the rule> | <the incident or reasoning behind it> |

<This is where scars go. A guard that looks redundant, an ordering that looks arbitrary, a check
that looks paranoid - each is usually the result of a real failure. Say what the failure was, so a
future reviewer does not "simplify" it away.>

### 4.4 Deliberately not in the repository

| What | Where it lives instead | Why it is excluded |
|---|---|---|
| <e.g. API credentials> | <e.g. the password manager, under entry name X> | <e.g. secrets must never be committed> |

## 5. New developer onramp

### 5.1 Clone and configure

```
<commands>
```

<How to get a working local configuration without production credentials.>

### 5.2 Run locally

```
<commands>
```

<What a successful run looks like on screen, so the reader knows whether it worked.>

<If local development is not possible, say so plainly here and explain how to develop against a
non-production environment instead. Do not leave this silent - silence reads as "should be easy".>

### 5.3 Run the tests

```
<commands>
```

<What passing looks like. Current expected result, e.g. "48 passed, 2 skipped".>

### 5.4 Deploy

<How a change reaches production, including who approves it.>

## 6. Related documents

- [Admin Guide](Admin-Guide.md) - operating it day to day
- [Troubleshooting](Troubleshooting.md) - symptom-first fixes
- [Testing Report](Testing-Report.md) - what was tested and what it proved
- <Add Integration Registry, User Guide or Stakeholder Brief if they exist for this project>
