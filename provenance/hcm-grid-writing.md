# Provenance - hcm-grid-writing

| Field | Value |
|---|---|
| Upstream | **None. Authored at HCM.** |
| **Pinned to** | Not applicable - there is no upstream commit to pin. The source of truth is this repository |
| Found on | Not applicable |
| Upstream version string | Not applicable |
| Published as | `1.0.0` |
| Licence | HCM internal. No third-party code is included, so no upstream licence is carried |
| Vendored | 2026-11-18 (authored, not vendored) |
| Author | HCM IT |
| Reviewer | Hodahel Moinzadeh (catalog owner), at review of the pull request that adds this record |
| Static scan | **1.0.0: clean.** 0 findings, scanned 2026-11-18 with skillspector `v2.11.0`, the same version CI pins. No triage record required. CI re-runs this on the pull request, which is the result that gates the merge |
| Semantic scan | **Not run.** The plugin is prose only, with no scripts, hooks or MCP servers. Recorded rather than implied: a scan that was not run is not a clean scan |
| Baselined findings | none |
| HCM changes | Not applicable - HCM is the author |

## Why HCM carries this

HCM IT publishes guidance for every employee on The Grid, the firm's intranet, and those pages have
a consistent voice: a definition or purpose first, the reason behind every rule, full sentences,
"we" for IT and "you" for the reader, Title Case topic headings, and a responsibility reminder at
the close. Drafts written without that guidance tend to come out as terse cheat sheets, which IT
leadership has rejected as not sounding like HCM IT.

This plugin writes the voice down so that anyone drafting a Grid page or post with Claude gets it by
default. It separates three forms that share a vocabulary but differ in tone: reference or how-to
pages, policy or philosophy pages, and announcement posts.

## What is in it

| Path | What it is |
|---|---|
| `SKILL.md` | The three forms, the voice and structure rules, policy-page and post specifics, and a four-step workflow |
| `references/examples.md` | Short excerpts of each form from HCM IT's published Grid pages, with page IDs |

## Security notes for the reviewer

**No executables, hooks or MCP servers.** The plugin is two markdown files.

**What it can do.** It shapes how Claude writes. Its workflow tells Claude to check current Grid
pages with The Grid connector when one is registered, which is a read-only lookup, and to deliver a
draft plus a separate list of editor notes. It does not publish anything to the Grid; a person pastes
the page in.

**Content in a public repository.** `references/examples.md` quotes one- or two-sentence excerpts
from HCM IT's intranet pages and posts (for example the definition on the Standard Tools page and the
opening line of the ChatGPT Enterprise launch post). They were chosen as style samples and contain no
credentials, hostnames, addresses, client or project information. A reviewer should still read that
file with the question "is this fine to be public?" in mind. If any excerpt is not, the fix is to
paraphrase it; the skill works from the rules in `SKILL.md`, and the examples only illustrate them.

**It can be entered without the word "Grid".** The description deliberately triggers on any user
guide, FAQ, policy page, course lesson or announcement for HCM staff, and on "this doesn't sound like
HCM IT", because those requests are usually Grid content arriving under another name. It excludes
Hudu knowledge-base articles, vault documentation, SOQs and proposals. The cost of a false trigger is
low: the skill only changes writing style and adds one read-only lookup, and touches nothing outside
the draft.

**Names.** The skill names no IT staff, per the firm rule. It refers to roles only.

## Testing

Run on 2026-11-18 with two prompts, each written once with the skill and once without (same model,
no Grid access): a how-to page on Microsoft Authenticator number matching, and a short post
announcing Codex with guardrails.

| Check | With the skill | Without |
|---|---|---|
| Definitional or purpose opener | Yes, both | No (page opened conversationally) |
| Title Case topic headings at Grid levels (`####`) | Yes | No, sentence-case `##` |
| Reason given for every rule | Yes | Mostly |
| Metaphors or punchy asides on a page | None | "Think of it as a collaborator", "a small change that does a lot of good" |
| Responsibility language | Yes, both | No |
| Invented contact details | None; Contact block left to the editor | Invented an email address that does not exist |
| Separate editor notes (facts to verify, Contact block, placement) | Yes, both | No |
| Em-dashes | 0 | 0 |

One defect was found and fixed before publication: the page run cited the AI Policy on a page that
had nothing to do with AI, because the vocabulary list presented that link without a condition. The
rule now says to use it only when the subject involves AI.

## Change log

### 1.0.0, 2026-11-18

First release.

## Not in `autoinstall.json`

Deliberately. It is useful to the people who write for the Grid, not to every endpoint. It is
available on request via `/plugin install hcm-grid-writing@hcm`.
