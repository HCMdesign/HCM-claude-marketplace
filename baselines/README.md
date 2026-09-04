# Baselines

A baseline suppresses SkillSpector findings that a human has read and accepted. One file per
plugin, named `<plugin>.yaml`, matching the plugin's name in `marketplace.json`.

**This directory is empty, and that is the healthy state.** A baseline is an exception, not a step
in the process.

## Why baselines live here and not in the plugin directory

Everything under `plugins/` is copied byte-identical from upstream at a pinned commit, so drift is
a plain recursive `diff` with nothing to exclude. A baseline is an HCM file. Putting it inside the
plugin would break that property for the sake of one file — the same reason provenance records live
in `provenance/`.

## When a baseline is permitted

All three must hold, and the pull request must show them:

1. **Zero findings land on anything but inert content.** Only `.md`, `.markdown`, `.txt`, `.rst`,
   `.csv`, `.json`, `.yaml` and `.yml` may be suppressed. This is an allowlist, not a list of
   banned extensions — a blocklist misses anything unusual or extensionless, and this has to fail
   closed. A suppression on code means the rule has been broken, whatever reason is attached.

   **CI enforces this**; it is not left to review. The `Scan catalog` job fails the build on a
   suppression outside that set, on a non-empty `rules:`, or on a boilerplate reason.
2. **Every executable file in the vendored subset has been read in full by a human**, and that
   reading is recorded in `provenance/<plugin>.md` — what the file does, what it reaches, what it
   writes.
3. **Every entry carries a real reason.** Not "accepted finding", not "auto-generated". Name what
   was matched and why it is not a defect.

If you cannot satisfy all three, the plugin does not go in the catalog. That is the answer, not a
problem to work around.

> [!note] Known gap in the CI check
> The check reads the `file` field of each entry — which the baseline **declares about itself**. A
> baseline could name an inert `.md` path on an entry whose hash actually belongs to a finding in
> code, and the check would pass.
>
> Closing it properly means running the scan with `--show-suppressed` and verifying the paths the
> *scanner* reports for suppressed findings, rather than the paths the baseline claims. That is the
> right fix and it is deliberately not built yet: there are no baselines in this repository, so it
> could not be exercised, and a check nobody has watched fail is not a check. Build it with the
> first real baseline, and test it by planting a mismatched entry.
>
> Meanwhile the exposure is narrow: it requires an author with merge rights who is deliberately
> mislabelling an entry, and both the human review and the `baselines/*.yaml` rule in
> `.coderabbit.yaml` look at exactly that.

## Fingerprints, not glob rules

Suppress by content fingerprint. Never add entries under `rules:`.

A fingerprint is tied to the exact content that produced the finding: change the file and the hash
changes and the finding **reappears unsuppressed**. A glob rule suppresses a whole class in a path
forever, including findings that do not exist yet — which defeats the only thing that makes a
baseline safe.

## Generating one

```bash
skillspector baseline plugins/<name> --no-llm -o baselines/<name>.yaml
```

Then replace every generated `reason` with a real one before committing.

> [!warning] Known limitation, measured 2026-09-04 with SkillSpector 2.11.0
> `skillspector baseline` does not emit a fingerprint for every finding `skillspector scan`
> reports. Measured on one plugin: an unbaselined scan reported **302** findings; `baseline`
> produced **183** fingerprints; rescanning with it reported **184 suppressed and 119 remaining**.
> (Those totals do not reconcile exactly — the commands group occurrences differently — so they are
> recorded as measured rather than reasoned about.) Adding the 51 distinct fingerprints the
> remaining findings carried changed nothing: still 184 suppressed, 119 remaining. Fingerprints are
> stable between runs — two `baseline` runs gave identical sets — so this is a gap in what
> `baseline` emits, not non-determinism.
>
> **Consequence:** a plugin with many findings may be impossible to baseline to green. If that
> happens, the plugin does not go in the catalog. Do not reach for glob rules to force it.

## History

`superpowers-developing-for-claude-code` was the first plugin to need a baseline, and the reason
this directory exists. It was **not** vendored. It bundles 42 pages of Claude Code documentation and
scored risk 100 / `DO_NOT_INSTALL` on 302 findings — 137 of them "Whitespace Padding" firing on
markdown tables, and 36 "Context Window Stuffing" firing on document length. Every finding was on a
`.md` or `.json` file; none on code. Its entire executable surface, 179 lines, was read and was
clean.

It was dropped anyway, for reasons that had nothing to do with the scan: its bundled docs were nine
months stale and missing `strictKnownMarketplaces`, `blockedMarketplaces` and `syncClaudeAiSkills` —
keys HCM needed — and its plugin-development skill duplicates `plugin-dev@claude-plugins-official`,
which is already allowlisted. A stale documentation snapshot is not neutral; it is confidently
wrong.
