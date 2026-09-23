# <Project Name> - Closeout Report

> **Audited:** <YYYY-MM-DD>
> **Auditor:** <who ran this>
> **Project profile:** <which profile from project-profiles.md was used, and why>
> **Verdict:** <complete / complete with accepted gaps / not ready to close>

This report is written in phase 1 from the audit, then updated in phase 3 with what was done. The
next person to touch this project should be able to start by reading it.

---

## Part 1 - Audit findings

### 1.1 What this project is

<Two to four sentences. What it does, who uses it, what depends on it, and whether it is still
alive. Written from reading the project, not from asking the owner.>

| | |
|---|---|
| **Repository** | <url> |
| **Main branch** | <name> |
| **Last commit** | <date and subject> |
| **Runs on** | <where> |
| **Touches other systems?** | <yes and which / no> |
| **Non-technical users?** | <yes / no> |

### 1.2 Outstanding work

| Source | Item | Status | Blocks closeout? |
|---|---|---|---|
| <tracker / issues / PRs / branches / code markers> | <what it is> | <open, in progress> | Yes / No |

<Write "None found" for any source checked that was clean, so a reader knows it was checked rather
than skipped. If no tracker was available in this session, say so explicitly here - a missing
check is not a passing check.>

### 1.3 Documentation state

| Document | Required? | Present? | Assessment |
|---|---|---|---|
| Dev Guide | <yes/no> | <missing / stub / adequate> | <what specifically is missing> |
| Admin Guide | | | |
| User Guide | | | |
| Stakeholder Brief | | | |
| Troubleshooting | | | |
| Testing Report | | | |
| Integration Registry | | | |

<Judge content, not filenames. A `TROUBLESHOOTING.md` with three bullet points is a stub. Say what
is actually absent: "no admin doc, so nobody but the author knows the job runs at 06:00 or where
its log lands" is a finding; "no admin doc" is not.>

### 1.4 Repository state

| Check | Result |
|---|---|
| Uncommitted changes | <none / list> |
| Unpushed commits | <none / count and branch> |
| Branches ahead of main | <none / list> |
| Stray files (logs, scratch, duplicates) | <none / list> |
| Secrets committed | <none found / what and where> |
| `.gitignore` coverage | <adequate / gaps> |

### 1.5 What could not be verified

<Anything assumed rather than checked, and why. Tests present but not run. A deployment that could
not be reached. A tracker with no available tool. This section is what makes the rest of the
report trustworthy - an audit that quietly assumes is worse than one that admits the gap.>

<Write "Nothing - all items above were directly verified." only if that is true.>

### 1.6 Gate decision

<If the audit was clean: "No outstanding work found. Proceeded to documentation without stopping.">

<If findings were raised: record what was shown to the user and what they chose.>

| Finding | User decision | Rationale given |
|---|---|---|
| <what was found> | <fixed now / accepted and skipped / stopped> | <why> |

<Anything knowingly skipped must appear here. Six months from now, the difference between "we
decided to skip the testing report" and "nobody noticed there was no testing report" matters
enormously to whoever is reading this.>

---

## Part 2 - What was done

<Left empty during phase 1. Filled in during phase 3.>

### 2.1 Documents written

| Document | Location | New or updated |
|---|---|---|
| <name> | <path or vault location> | <new / updated> |

**Docs location rationale:** <which of the four resolution rules applied - vault, existing
convention, asked, or repo fallback - so a reader knows why they are where they are.>

### 2.2 Link check

```
<output of scripts/check_links.py>
```

<Any dead links found and whether they were fixed.>

### 2.3 Repository

| | |
|---|---|
| **Commits made** | <count and summary> |
| **Stray files removed** | <list, or "none needed"> |
| **Pull request** | <url> |
| **Automated review** | <ran and clean / ran with findings, addressed / did not run - why> |
| **Merged** | <no - awaiting human approval / yes by whom> |

<Never merge on the author's behalf. If the PR is open and waiting, say so.>

### 2.4 Release

| | |
|---|---|
| **Warranted?** | <yes / no> - <one-line reasoning> |
| **User asked?** | <yes, answered X> |
| **Tag** | <version, or "none cut"> |
| **Release notes** | <url, or not applicable> |

### 2.5 Tracker

| | |
|---|---|
| **Tool used** | <whichever was available> |
| **Project card** | <moved to done / updated / no tool available> |
| **Roll-up card** | <updated / created / no tool available> |
| **Work items closed** | <list> |
| **Work items left open** | <list and why> |

### 2.6 Still outstanding after closeout

<Anything deliberately left. If nothing, write "Nothing." This is the handover line - the next
person reads it first.>
