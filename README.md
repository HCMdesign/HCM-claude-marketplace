# HCM Claude Code Skills

The vetted catalog of Claude Code skills for HCM, and the marketplace endpoints install them from.

Nothing enters this repository without passing a security scan and a human review. See
[How a skill gets in](#how-a-skill-gets-in).

## Installing a skill

The `hcm` marketplace is registered automatically on HCM machines. To see what is available:

```
/plugin
```

To install one:

```
/plugin install <name>@hcm
```

Nothing here installs itself. Everything in this catalog is available on request, not pushed.

If the marketplace is not registered on your machine:

```
/plugin marketplace add HCMdesign/HCM-claude-marketplace
```

## How a skill gets in

1. **Ask.** Open an issue with what you want and a link to where it comes from.
2. **Triage.** It gets scanned where it lives, before anyone spends effort on it.
3. **Vendor.** The skill is copied into this repository at a pinned version, with a
   `provenance/<name>.md` record saying where it came from, which commit, and who approved it.
4. **Gate.** The pull request runs NVIDIA SkillSpector, a CodeRabbit review, and a check that no
   HCM-internal hostnames leaked into a public repository. A failing scan blocks the merge.
5. **Review.** A person reads the findings and approves. Tools rank; people decide.
6. **Publish.** Merged and versioned. It appears in `/plugin`.

## Writing your own skill

You do not need this repository to write a skill for yourself. A personal skill lives at
`~/.claude/skills/<name>/SKILL.md`, and a project skill at `.claude/skills/` inside the repo it
belongs to. Neither is a marketplace, and neither is restricted.

This catalog is for skills you want **other people** to have. Publishing one follows the same steps
above, except that it is authored rather than imported: `provenance/<name>.md` names you and the date
instead of an upstream URL. Being written in-house earns no exemption from the scan — the author is
the last person positioned to spot their own foot-gun.

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
