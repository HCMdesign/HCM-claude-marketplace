# HCM Claude Code Skills

The vetted catalog of Claude Code skills for HCM, and the marketplace endpoints install them from.

Nothing enters this repository without passing a security scan and a human review. See
[How a skill gets in](#how-a-skill-gets-in).

## Installing a skill

> [!important] You need to add the marketplace yourself, for now
> Automatic registration through the standard HCM deployment **is not live yet**. Until it is,
> `/plugin` will not show this catalog until you add it:
>
> ```text
> /plugin marketplace add HCMdesign/HCM-claude-marketplace
> ```
>
> One-off, per machine. This note comes out when the deployment does it for you.

Then, to see what is available:

```text
/plugin
```

To install one:

```text
/plugin install <name>@hcm
```

Some plugins are meant to arrive on every machine without being asked for; the rest wait until you
install them. Which is which is recorded in [`autoinstall.json`](autoinstall.json) — though until
automatic deployment is live, *nothing* installs on its own and everything is a manual
`/plugin install`.

## Pushed, or available on request

| | What is intended |
|---|---|
| **Named in `autoinstall.json`** | Installed on every endpoint, unasked |
| **Everything else in the catalog** | Appears in `/plugin`, installs only when someone chooses it |

> [!warning] Not in effect yet
> The deployment side of this is **not built**. `autoinstall.json` currently records an intention
> that nothing acts on: no endpoint reads it, and no plugin installs itself. Today every install is
> a manual `/plugin install <name>@hcm`. The file is written and CI-checked now so the deployment
> has something correct to read when it lands.

This is an **HCM convention, not a Claude Code feature.** Claude Code marketplaces cannot
auto-install anything: adding a marketplace only registers the catalog, and `defaultEnabled`
controls whether an *installed* plugin is switched on, not whether it gets installed. Installation
has to be driven from the endpoint, which is why it needs a deployment step at all.

Once deployment is live, adding a name to `autoinstall.json` **will** push that plugin to the whole
fleet. Treat an addition as a deployment, not a catalogue entry, even now — the list is what the
deployment will act on the day it ships. CI fails the build if a name there is not actually
published.

## How a skill gets in

Two ways in.

### Open an issue — someone looks at it manually

Say what the skill is, where it comes from, and **why you want it**. Nothing automatic happens: no
scan runs and no bot replies. One person picks it up alongside other work, so if it's urgent, say so.

### Or open a pull request — the scan runs automatically

Vendor it yourself and the full gate runs on your PR: every plugin scanned, every finding has to be
accounted for, a provenance record is required, and no HCM-internal hostnames may appear. This is
the faster route if you're comfortable doing the vendoring. See
[`triage/README.md`](triage/README.md) for what accounting for a finding means.

### Either way

1. **Is it actually a plugin?** This settles a lot of requests. Plenty of useful things are *tools
   that install a skill* rather than Claude Code plugins — no `plugin.json`, and installing them
   writes a skill straight into your own `~/.claude/skills/` folder. Those can't live here; they go
   into the standard HCM deployment instead. You still get the skill, just by another route.
2. **Scan it against the upstream project**, before anyone spends effort vendoring. On the issue
   route this is **someone running the scanner by hand** — it is not the automated gate, which
   only exists once there is a pull request (step 4).
3. **Vendor it** at a pinned commit, byte-identical to upstream, with a `provenance/<name>.md`
   record saying where it came from, which commit, who approved it, and anything worth knowing about
   what it does.
4. **The gate runs**, and unaccounted findings block the merge.
5. **A person reviews and merges.** Tools rank; people decide.

This catalog governs what HCM distributes to *everyone*.

## Why skills are scanned

A skill is prose an AI agent obeys. It can carry instructions to ignore its own rules, to send
your data somewhere, or to run commands you never see. The research behind
[NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector), the scanner this repository runs,
reports that **26.1% of published skills contain vulnerabilities and 5.2% show likely malicious
intent**. Reviewing them by eye does not scale, and reading a skill as though it were documentation
misses the point of it entirely.

## Licensing

Each plugin under `plugins/` keeps the licence it was published under; see the `LICENSE` file
inside each one. This repository applies no licence of its own, because it would misstate the terms
of the vendored content.

## Repository layout

| Path | What it is |
|---|---|
| `.claude-plugin/marketplace.json` | The catalog. Adding a plugin here is what publishes it |
| `plugins/<name>/` | One vendored plugin, **byte-identical to its upstream commit**. Nothing HCM-written lives here, so drift against upstream is a plain `diff` |
| `provenance/<name>.md` | Where that plugin came from, which commit, who approved it, what the scans said, and what was dropped. CI fails if a published plugin has no record |
| `tests/tripwire/` | A deliberately malicious fixture. CI asserts the scanner still catches it |
| `.github/workflows/` | The gate |

## Contacts

Open an issue, or contact HCM IT.
