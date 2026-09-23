# <Project Name> - Troubleshooting

> **Audience:** a technician with a broken thing, right now. Start fixing within seconds of
> landing here. Architecture lives in the [Developer Guide](Dev-Guide.md); this document is for
> getting it working again.
> **Last reviewed:** <YYYY-MM-DD>

## 1. Is it even running?

Before diagnosing anything, confirm it is actually running. Most "it is broken" reports are "it
never started".

```
<The exact starter command or query.>
```

**Running and healthy:** <what you see>
**Running but failing:** <what you see>
**Not running at all:** <what you see> -> go to [<symptom row>](#2-symptom-index)

## 2. Symptom index

Find the row that matches what you are seeing. Each links to its fix below.

| What you observe | Most likely cause | First move |
|---|---|---|
| <the observable symptom, in the words someone would use to report it> | <cause> | [<short action>](#31-symptom-heading) |

<Write symptoms the way a person reports them - "the report never arrived", "it says access
denied", "it runs but the numbers are wrong" - not the way a developer names them. The whole point
of this table is that someone can find their row without understanding the system.>

## 3. Fixes by symptom

### 3.1 <Symptom stated as the user experiences it>

**Cause:** <what is actually happening underneath>

**Check:**
```
<the command that confirms this is the cause>
```

**Fix:**
```
<the commands, in order>
```

**Verify:** <how to confirm it is fixed>

**If that did not work:** <the next thing to try, or who to escalate to>

<Repeat this block for each symptom in the index. Keep each one short and cross-reference the
Admin or Developer guide for depth rather than re-explaining the system here.>

## 4. Symptom to source map

Which log message or behaviour comes from which part of the code. This serves a technician tracing
a message, and a code auditor tracing a behaviour.

| Log message or behaviour | Source | Meaning |
|---|---|---|
| `<the literal string as it appears in the log>` | `<file>:<function>` | <what it indicates> |

<Use the literal text from the logs, so it can be found by searching. Paraphrased messages make
this table useless.>

## 5. Known issues and accepted quirks

| Behaviour | Status | Notes |
|---|---|---|
| <the thing that looks wrong but is not> | <accepted / open / wontfix> | <why, and what would change it> |

<This section prevents the same false alarm being investigated repeatedly. If something looks like
a bug every time and is not, it belongs here.>

<If there are none, write: "None recorded.">

## 6. Escalation

| Situation | Who | How |
|---|---|---|
| <e.g. still failing after the above> | <role> | <channel> |
| <e.g. suspected data loss> | <role> | <channel> |
| <e.g. security concern> | <role> | <channel> |

## 7. Related documents

- [Admin Guide](Admin-Guide.md) - routine operation, logs, rotation
- [Developer Guide](Dev-Guide.md) - architecture and code
- <Add others that exist for this project>
