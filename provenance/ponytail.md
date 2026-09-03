# Provenance — ponytail

| Field | Value |
|---|---|
| Upstream | https://github.com/DietrichGebert/ponytail |
| **Pinned to** | commit `2ed6c52c9d7e5e56942508591085fd45dea277d3` — immutable, and the only thing this record binds to |
| Found on | branch `main` (**not** the `v4.9.0` tag — see "Which ref"). The branch is where the commit was taken from; it is not the pin |
| Upstream version string | `4.9.0` (from `.claude-plugin/plugin.json`) |
| Published as | `4.9.0-hcm.1` |
| Licence | MIT — Copyright (c) 2026 DietrichGebert (`LICENSE` retained verbatim) |
| Vendored | 2026-09-03 |
| Reviewer | Hodahel Moinzadeh |
| Static scan | risk **0**, LOW, **SAFE**, 0 issues, 100% coverage (25/25 files) |
| Semantic scan | risk **2**, LOW, **CAUTION**, 1 LOW issue — see below |
| Baselined findings | none |
| HCM changes | Subset vendored; no file contents modified |

## Why HCM carries this

`ponytail` enforces a lazy-senior-developer coding style — YAGNI, stdlib first, no unrequested
abstractions. It is already deployed fleet-wide through ClaudeDeploy's Dev Bundle, previously from
the third-party `ponytail` marketplace. It is vendored here so that HCM's allowlist can be narrowed
to Anthropic's official marketplace plus HCM's own.

## Which ref, and why not the tag

The `v4.9.0` tag points at `0a4dd63ad4541f4f655c4108a295916f3c1d8fda`. `main` is **three commits
ahead** of it:

- `cc37a5d` — drop `commandWindows` from `hooks.json` for Claude.ai marketplace validation
- `a2712bc` — detect VS Code Copilot via `CLAUDE_PLUGIN_ROOT` fallback
- `2ed6c52` — add Grok Build native skills adapter

Two of those are bug fixes the tag does not contain, and the copy already installed across HCM is
`2ed6c52` — the third-party marketplace was serving `main` under the label `4.9.0`. Vendoring the
tag would have shipped known-fixed bugs and changed behaviour from what the fleet already runs.

Pinning is by **commit sha**, which is immutable. A tag is not, and that ambiguity is precisely the
condition this catalog exists to remove.

## What was vendored, and what was left behind

Upstream is a multi-agent repository: 159 files, 4.3 MB, carrying configuration for Cursor, Cline,
Codex, Devin, Grok, Kiro, OpenCode, OpenClaw, Qoder, Windsurf, Gemini and Pi alongside Claude Code.
Only the Claude Code surface is vendored — **25 files, 144 KB**:

| Kept | Why |
|---|---|
| `.claude-plugin/plugin.json` | The manifest Claude Code reads |
| `hooks/` | Declared by the manifest; `SessionStart`, `SubagentStart`, `UserPromptSubmit` |
| `skills/` | The six skills, and `hooks/ponytail-instructions.js` reads `../skills/ponytail/SKILL.md` at runtime |
| `commands/` | The `/ponytail*` commands |
| `LICENSE` | MIT requires it |

| Dropped | Why |
|---|---|
| `.cursor/`, `.clinerules/`, `.codex-plugin/`, `.devin-plugin/`, `.grok-plugin/`, `.kiro/`, `.openclaw/`, `.opencode/`, `.qoder*/`, `.windsurf/`, `.agents/`, `pi-extension/`, `gemini-extension.json`, `opencode.json` | Other agent tools. Inert here, and review surface for no benefit |
| `assets/` (1.1 MB), `benchmarks/`, `tests/`, `examples/`, `docs/`, `scripts/`, `ponytail-mcp/` | Verified not read at runtime by any hook or skill |
| `.claude-plugin/marketplace.json` | A **marketplace manifest**. Nesting one inside a plugin inside HCM's marketplace invites confusion |
| `README.md` | Not needed at runtime, and its star-history chart badge produced the only three findings in the first static scan (MEDIUM "External Transmission", 50% confidence — benign img/srcset URLs). Deleting the file was preferable to baselining a finding |
| root `plugin.json`, `plugin.yaml`, `package.json`, `__init__.py`, `.env.example`, `.github/`, `AGENTS.md`, `after-install.md`, `README.es.md`, `README.ko.md` | Not read by Claude Code |

Runtime dependencies were checked before dropping anything: hooks reference only their own
directory (`path.join(__dirname, …)`) and `../skills/ponytail/SKILL.md`. Nothing reaches into the
dropped paths.

**No file contents were modified.** Every retained file is byte-identical to upstream at
`2ed6c52`, so drift against upstream is a plain `diff`.

## Capability inventory

What this plugin actually does, established during review. None of it is hidden or unusual for a
mode-switching plugin, but it is recorded so a future reader does not have to rediscover it — and
so that a *change* in this behaviour on an upstream bump is visible as a change.

| Capability | Where | Assessment |
|---|---|---|
| Writes mode state outside the plugin directory | `$CLAUDE_CONFIG_DIR` / `~/.claude`, `$XDG_CONFIG_HOME/ponytail` / `~/.config/ponytail`, `~/.qoder` | **Expected.** Mode has to survive between sessions, and a plugin directory is replaced on update. Small, non-secret state |
| Session state file created and deleted | `hooks/ponytail-runtime.js` (`setMode` / `clearMode`) | Expected, same reason |
| **Reads the user's `settings.json`** | `hooks/ponytail-activate.js` reads `$CLAUDE_CONFIG_DIR/settings.json` | Reads Claude Code's own configuration to decide whether to prompt for statusline setup. Read-only, and the file is not transmitted anywhere — no network egress exists in this plugin |
| Writes a one-time "nudge" flag file | `hooks/ponytail-activate.js` | Marks that the setup prompt was already shown, so it is not repeated |
| Runs on `SessionStart`, `SubagentStart`, `UserPromptSubmit` | `hooks/claude-codex-hooks.json` | Broad, but inherent: the plugin's whole purpose is to inject a coding style into every session. 5s timeouts |
| `ponytail-debt` writes a ledger file | `PONYTAIL-DEBT.md` in the working repository | Writes into the user's project. Visible, named, and the skill is invoked deliberately |
| Skills instruct `grep` and `git blame` across the repository | `ponytail/SKILL.md`, `ponytail-debt/SKILL.md` | Read-only source inspection. The agent asks before running commands |
| `ponytail-audit` scans the whole repository | `ponytail-audit/SKILL.md` | Read-only, and the point of an audit skill |
| **Proposes a persistent `statusLine` command for the user's `settings.json`** | `hooks/ponytail-activate.js` | See the HCM note below — the most consequential item in this table |
| Skills instruct host-level update commands | `skills/ponytail-help/SKILL.md` | `/plugin marketplace update ponytail`, `/reload-plugins`, `npm install -g @anthropic-ai/claude-code@latest`, `brew upgrade claude-code`. Suggested to the user, not executed. See the staleness note below |
| **Network egress** | none found | |
| **Credential access** | none found | |
| **Remote content fetched or executed** | none found | |
| **Anti-refusal / concealment instructions** | none found | The category that would stop publication outright |

> [!warning] The statusline offer, and why it matters on an HCM endpoint
> On first activation, if no statusline is configured, `ponytail-activate.js` writes a one-time
> flag file and appends text to its hook output telling the agent to *proactively offer* to add a
> `statusLine` entry to the user's `settings.json`. On Windows the proposed command is:
>
> ```
> powershell -ExecutionPolicy Bypass -File "<plugin>/hooks/ponytail-statusline.ps1"
> ```
>
> The plugin does **not** write this itself — it prints the snippet and asks the agent to offer.
> The path is guarded by an `isShellSafe()` check, and if the install path contains shell
> metacharacters the snippet is withheld and the agent is told to wire it up by hand. That is
> careful engineering, not a trick.
>
> It is still worth HCM knowing, for two reasons. First, accepting the offer means a command runs
> on **every statusline refresh**, persisted in the user's own settings where it outlives the
> plugin. Second, `powershell -ExecutionPolicy Bypass -File` is a command shape SentinelOne scores,
> and it would be attributed to the host editor's process tree.
>
> **Not a reason to reject the plugin** — it is opt-in, visible, and the user is asked. It is a
> reason for whoever accepts the offer to know what they are accepting.

> [!note] The self-update instructions are stale for HCM
> `skills/ponytail-help/SKILL.md` tells users to run `/plugin marketplace update ponytail`. Under
> HCM's catalog this plugin is `ponytail@hcm`, and once the two-marketplace allowlist is enforced
> the `ponytail` marketplace will not exist on an HCM machine at all. Following that instruction
> will fail confusingly.
>
> Left unmodified, because editing it creates drift on a file for a cosmetic wrong instruction.
> **Generalise this**: any vendored skill may carry self-update instructions pointing at the
> marketplace it originally shipped from. Check for it on every vendoring, and record it here.

> [!note] Two over-broad activation phrases
> `ponytail-debt` triggers on "list the shortcuts" and "what did we mark to do later"; `ponytail-audit`
> on a bare "find bloat"; `ponytail-review` on "what can we delete". None carries a skill-specific
> token, so each may activate on an unrelated question. Independently found by both SkillSpector
> (`SQP-1`) and CodeRabbit. Accepted — an annoyance, not a risk, and fixing it means modifying
> upstream. Worth raising with the author.

> [!warning] One dangling reference caused by the subset
> `skills/ponytail-gain/SKILL.md:19` cites "`benchmarks/` and the README" as the source of its
> figures, and neither is vendored. Nothing breaks: the benchmark numbers are inline in
> `commands/ponytail-gain.toml`, and the skill states they are published medians, not values it
> computes. It is a citation pointing at paths that exist only upstream. Accepted rather than
> vendoring 299 KB of benchmark data for a footnote — the upstream URL at the top of this record is
> where those sources live.

## Scan detail

**Static (`--no-llm`, the CI gate):** risk 0, SAFE, zero issues. All twenty-plus static analyzers
completed 25/25 — prompt injection, anti-refusal, data exfiltration, privilege escalation,
excessive agency, memory poisoning, output handling, system-prompt leakage, tool misuse, rogue
agent, SSRF, deserialization, supply chain, agent snooping, harmful content and YARA.

**Semantic (`SKILLSPECTOR_PROVIDER=claude_cli`):** risk 2, CAUTION, one LOW finding.

> `SQP-1` at `skills/ponytail-debt/SKILL.md:6-8`, confidence 0.5 — two of the skill's trigger
> phrases, "list the shortcuts" and "what did we mark to do later", contain no skill-specific
> token. The former plausibly matches a question about keyboard shortcuts, the latter any generic
> TODO or backlog question. The description gives no exclusion conditions.

**Accepted, not fixed.** It is a trigger-scoping quality issue, not a security one, and correcting
it would mean modifying upstream content and creating drift for a LOW/0.5-confidence finding. The
practical consequence is that `ponytail-debt` may occasionally activate on an unrelated question —
an annoyance, not a risk. Worth raising upstream.

> [!warning] The semantic pass was not complete
> `semantic_security_discovery` finished **degraded**: 11 files fully inspected, 13 partially,
> stopped by `LLMRuntimeLimitError` — a configured runtime limit, not a clean bill of health.
> `semantic_developer_intent` and `semantic_quality_policy` both completed 24/24, and every static
> analyzer completed 25/25, so no file went entirely uninspected.
>
> Recorded because a partial result reported as "clean" is the exact failure this catalog exists to
> prevent. The static gate — which is what actually blocks a merge — was complete.

## Upstream drift

Owner: Hodahel Moinzadeh. Checked against upstream quarterly.

A fork stops receiving upstream fixes the day it is made; that is the cost of the two-marketplace
policy. Because no file was modified, checking drift is:

Nothing HCM-written lives inside `plugins/ponytail/` — this record sits outside it, in
`provenance/`. That is deliberate: the plugin directory stays byte-identical to upstream, so drift
checking is an exact comparison with no exclusions to remember.

```bash
git clone https://github.com/DietrichGebert/ponytail.git /tmp/pt
diff -r plugins/ponytail /tmp/pt | grep -v '^Only in /tmp/pt'
```

`Only in /tmp/pt` lines are the paths deliberately not vendored (see the table above). **Anything
else that reports is a real upstream change to a file HCM ships**, and needs a new pull request
against a new commit sha — never a quiet `git pull`.

Verified at vendoring time: the comparison reported **zero** differing files.
