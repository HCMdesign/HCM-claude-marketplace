# Triage records

**SkillSpector provides evidence. HCM owns the verdict.**

CI runs the scanner, ignores its exit code, and applies the triage record for each plugin. The gate
is one sentence:

> Every finding must be accounted for by a triage entry, or the plugin does not ship.

Nothing is waived by a score, a threshold, or an opaque hash.

## Why the scanner's exit code is not the gate

It blocks above risk 50 and scores HIGH at +25, so **three HIGH findings reject a plugin** — and a
HIGH finding can be a string match on prose. Measured on real plugins:

| What the scanner called it | What it actually matched |
|---|---|
| Session Persistence ×19 | the identifier fragment `pList` |
| Context Window Stuffing | `?, ?, ?, …` — a SQL **parameterised-query placeholder list** |
| Self-Modification | the word `self-update` in a `plugin.json` **description field** |
| Whitespace Padding ×137 | markdown tables in bundled documentation |
| Tool Parameter Abuse | `/plugin marketplace remove /path/to/plugin` in a troubleshooting guide |

Its own `baseline` command cannot enumerate the findings `scan` reports — measured at 183
fingerprints for 302 findings, with the remainder refusing to suppress even when added by hand — so
its suppression mechanism cannot be driven to completion. Depending on it meant legitimate plugins
were unshippable for reasons unrelated to their safety.

So HCM adjudicates. The scanner still does the work it is good at: finding things to look at.

## Writing a record

`triage/<plugin>.yaml`, named for the plugin in `marketplace.json`.

```yaml
# Optional, documentation only: the upstream commit these were verified against.
plugin_commit: 10757690210574421f1df5f35835af8d0c74d984

entries:
  # PER-FINDING entry. Required for anything that is not inert content.
  - rule_id: RA2
    file: src/doctor.ts
    matched: "pList"                  # the literal string the scanner matched
    reason: "Identifier fragment, not session-persistence behaviour."
    verified_by: Hodahel Moinzadeh    # who read the file and confirmed it

  # CLASS entry. Inert content only. Covers one rule across a path glob.
  - rule_id: P9
    files: "skills/**/*.md"
    reason: "Markdown table formatting in bundled documentation."
    verified_by: Hodahel Moinzadeh
```

`matched` must genuinely appear in what the scanner reported. An entry cannot claim a finding it
does not describe — CI checks this, so a record cannot be pointed at the wrong thing.

## The rules CI enforces

1. **Every finding is accounted for.** An unaccounted finding fails the build. There is no
   threshold to slip under.
2. **Executable content needs a per-finding entry**, with `matched` and `verified_by`. A class
   entry may cover prose; it may never cover code. Inert content is `.md`, `.markdown`, `.txt`,
   `.rst`, `.csv`, `.json`, `.yaml`, `.yml` — an allowlist, so unusual or extensionless files fail
   closed.
3. **Stale entries fail.** A record matching no finding means the content moved underneath it.
   Re-verify it or remove it; dead suppressions are not left lying around to widen over time.
4. **Every entry needs `reason` and `verified_by`.** CI cannot judge whether the reasoning is
   sound — that is what review is for — but it will not let anything be waived anonymously.
5. **A partial scan is never adjudicated.** If the scan did not complete, or left files
   uninspected, the build fails rather than reporting a pass on incomplete evidence.

## Re-vendoring forces re-triage

Nothing needs to enforce this separately. `plugins/` is byte-identical to upstream, so re-vendoring
at a new commit changes file contents, which changes findings, which leaves entries stale and
findings unaccounted. The build fails until someone looks again. `plugin_commit` is recorded for
humans, not as a check.

## What this does not fix

It does not make the scanner smarter. A plugin with 302 findings still needs 302 accounted for, and
class entries only help where the findings are in prose. That is a real limit: a documentation
bundle remains impractical to publish, which is the right outcome when the documentation is
available elsewhere and current.

## The adjudicator

`.github/scripts/triage.py`, with a self-check in `.github/scripts/test_triage.py` that **CI runs on
every build**. Fourteen cases, and most of them assert a *failure* — a gate nobody has watched
reject something is not a gate. Run it locally:

```bash
python .github/scripts/test_triage.py
```

## History

This replaced a `baselines/` mechanism built on SkillSpector's own suppression format. That
mechanism had two defects found by review, both fixed and both instructive: a baseline entry's
`file:` field is not what the fingerprint matches, so an entry could declare `SKILL.md` while
suppressing a finding in `evil.js` (reproduced, not theorised); and the check accepted a stale
report if the scan failed after one had been committed. Both are structurally impossible here — the
adjudicator reads the scanner's own reported paths and re-derives everything each run.

It was replaced anyway, because the underlying command could not enumerate its own findings.
