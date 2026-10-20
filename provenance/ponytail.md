# Provenance - ponytail

| Field | Value |
|---|---|
| Upstream | https://github.com/DietrichGebert/ponytail |
| **Pinned to** | commit `09c434ab73ca43761c5d8b0c5d341926c2fba710`, immutable, and the only thing this record binds to |
| Found on | branch `main` (**not** the `v5.3.2` tag, see "Which ref"). The branch is where the commit was taken from; it is not the pin |
| Upstream version string | `5.3.2` (from `.claude-plugin/plugin.json`) |
| Published as | `5.3.2-hcm.1` |
| Licence | MIT, Copyright (c) 2026 DietrichGebert (`LICENSE` retained verbatim) |
| Vendored | 2026-10-20 (first vendored 2026-09-03 at `4.9.0`, see the change log) |
| Reviewer | **NOT YET REVIEWED at 5.3.2, must be filled in before merge** |
| Static scan | **3 findings, all 3 accounted for** in `triage/ponytail.yaml`. 4.9.0 produced zero; see "What changed, and why it matters" |
| Semantic scan | **Not run at 5.3.2.** No API key is configured on the vendoring machine, so the semantic analyzers were skipped. The 4.9.0 semantic result does not carry over: this is a rewritten plugin with a new feature. Recorded rather than implied |
| Baselined findings | none |
| HCM changes | Subset vendored; no file contents modified |

> [!warning] This is a major-version jump with a new capability
> 4.9.0 recorded **network egress: none** and **credential access: none**. Neither is true at 5.x.
> Ponytail 5 adds "band", a per-turn metrics feature that writes a local CSV ledger **by default**
> and can POST the same row to a user-configured webhook with a bearer token. The network part is
> off unless someone sets a URL, and the whole thing is declared in the manifest rather than
> hidden. It is still the single most important difference between the two versions, and it is why
> the capability inventory below was rewritten rather than amended.

## Why HCM carries this

`ponytail` enforces a lazy-senior-developer coding style: YAGNI, stdlib first, no unrequested
abstractions. It is already deployed fleet-wide through ClaudeDeploy's Dev Bundle, previously from
the third-party `ponytail` marketplace. It is vendored here so that HCM's allowlist can be narrowed
to Anthropic's official marketplace plus HCM's own.

## Which ref, and why not the tag

The `v5.3.2` tag points at `16352ac229eb08a9598dcae48fe9f2b342567d86`. `main` is **eight commits
ahead** of it, and three of those matter on a Windows fleet:

- `#1165` give hooks a 15 second timeout, so a slow node start on Windows keeps its output
- `#1166` give the codebase map 3 seconds, for the same reason
- `#1156` raise the `git ls-files` buffer so large repos keep their tracked files
- plus `#1161` (band level after `/clear` and `/resume`), `#1135`, `#1154`, `#1164`, `#1116`

HCM runs Windows everywhere, and the first two are fixes for hooks losing their output when node
starts slowly. Ponytail's entire mechanism is three hooks; a hook that loses its output degrades
the plugin silently rather than loudly. Shipping the tag would mean shipping that bug knowingly.

This is the same call made at `4.9.0`, for the same kind of reason, and the version string on
`main` is `5.3.2` exactly as it was `4.9.0` then. Pinning is by **commit sha**, which is immutable.
A tag is not, and that ambiguity is precisely the condition this catalog exists to remove.

## What was vendored, and what was left behind

Upstream is a multi-agent repository: 214 files, 13 MB, carrying configuration for Cursor, Cline,
Codex, Devin, Grok, Kimi, Kiro, OpenCode, OpenClaw, Qoder, Windsurf, Gemini and Pi alongside Claude
Code. Only the Claude Code surface is vendored, now **35 files, 319 KB** (it was 25 files and
144 KB at 4.9.0; the growth is `hooks/band/`, the new codebase-map hook, and a Cursor hook
manifest that ships inside `hooks/`):

| Kept | Why |
|---|---|
| `.claude-plugin/plugin.json` | The manifest Claude Code reads |
| `hooks/` | Declared by the manifest; `SessionStart`, `SubagentStart`, `UserPromptSubmit` |
| `skills/` | The six skills, and `hooks/ponytail-instructions.js` reads `../skills/ponytail/SKILL.md` at runtime |
| `commands/` | The `/ponytail*` commands |
| `LICENSE` | MIT requires it |

| Dropped | Why |
|---|---|
| `.cursor/`, `.clinerules/`, `.codex-plugin/`, `.devin-plugin/`, `.grok-plugin/`, `.kimi-plugin/`, `.kiro/`, `.openclaw/`, `.opencode/`, `.qoder/`, `.qoder-plugin/`, `.windsurf/`, `.agents/`, `pi-extension/`, `gemini-extension.json`, `opencode.json` | Other agent tools. Inert here, and review surface for no benefit. `.kimi-plugin/` and `.qoder-plugin/` are new at 5.x |
| `assets/`, `benchmarks/`, `tests/`, `examples/`, `docs/`, `scripts/`, `i18n/` | Verified not read at runtime by any hook or skill. `i18n/` is new at 5.x and holds translated rule text for other hosts; the Claude Code surface reads none of it. `ponytail-mcp/` no longer exists upstream |
| `INSTALL.md`, `plugin.yaml`, `__init__.py` | Not read by Claude Code |
| `.claude-plugin/marketplace.json` | A **marketplace manifest**. Nesting one inside a plugin inside HCM's marketplace invites confusion |
| `README.md` | Not needed at runtime, and its star-history chart badge produced the only three findings in the first static scan (MEDIUM "External Transmission", 50% confidence, benign img/srcset URLs). Deleting the file was preferable to baselining a finding |
| root `plugin.json`, `plugin.yaml`, `package.json`, `__init__.py`, `.env.example`, `.github/`, `AGENTS.md`, `after-install.md`, `README.es.md`, `README.ko.md` | Not read by Claude Code |

Runtime dependencies were re-checked at 5.3.2 before dropping anything. Searching the three kept
directories for references to any dropped path returns exactly one hit, and it is a comment:
`hooks/band/logo.ts:1` notes that the band's logo was traced from `assets/logo-dark.svg`. The SVG
path data is inlined in that file, so nothing is read at runtime. Everything else in `hooks/`
resolves through `path.join(__dirname, …)` or the plugin root, and the skills reference only their
own directory.

**No file contents were modified.** Every retained file is byte-identical to upstream at
`2ed6c52`, so drift against upstream is a plain `diff`.

## Capability inventory

What this plugin actually does, established during review. None of it is hidden or unusual for a
mode-switching plugin, but it is recorded so a future reader does not have to rediscover it, and
so that a *change* in this behaviour on an upstream bump is visible as a change.

### The categories that would stop publication

| Category | Result at 5.3.2 | At 4.9.0 |
|---|---|---|
| **Network egress** | **Present, off by default.** One outbound path: `hooks/band/register.tsx` POSTs a per-turn metrics row to `userConfig.webhookUrl`. Empty by default, so nothing leaves the machine until someone sets it | none |
| **Credential access** | **Declares a credential, does not read one.** `userConfig.webhookToken` is marked sensitive, so the host stores it and hands it back; the plugin sends it as a bearer header. It reads no credential store, no `.env`, no keyring directly | none |
| **Remote content fetched or executed** | **none.** The webhook is write-only: the response is used for a status line and never executed or parsed as instructions | none |
| **Anti-refusal, safety-override or concealment instructions** | **none** | none |

The honest summary is that ponytail 5 can now talk to a network and can hold a token, where 4.9.0
could do neither. Both are opt-in, declared in the manifest where `/plugin` will show them, and
implemented with more care than the category names suggest. What follows is what review actually
found in the code.

### The band feature, which is what changed

`.claude-plugin/plugin.json` declares a second hook manifest, `hooks/claude-band.json`, whose only
content is `"modules": ["./band/register.tsx"]`. That is a Claude Code module rather than a command
hook: it runs in-process and draws a band in the interface. It computes per-turn metrics (cost,
turns, agent minutes, tokens, a reuse percentage, test counts) and then does up to two things with
them.

**The ledger, on by default.** `userConfig.ledger` defaults to `true` and appends a row per turn to
`~/.config/ponytail/band/<project>.csv`. The columns are fixed and worth knowing, because one of
them is not a number:

```
key,started,project,name,cost_usd,turns,agent_minutes,tokens_total,tokens_output,
reuse_pct,reused,new,callers_open,tests,level,model
```

`name` is the task's name, which is its title in the Claude Code sidebar or, failing that, **its
first prompt**. So prompt-derived text lands in a local CSV by default. No conversation body is
written, only that one field. The file never leaves the machine on its own.

**The webhook, off by default.** If `userConfig.webhookUrl` is non-empty, the same row is POSTed as
JSON after every turn. Reading `hooks/band/metrics.ts`, the implementation is careful rather than
casual:

- the URL is parsed, and a non-URL is refused with a visible status message
- **HTTPS is enforced**, with a deliberate exception for `localhost`, `127.0.0.1` and `[::1]` so a
  board running on the same machine can use plain HTTP
- the token, if set, goes in an `authorization: Bearer` header and nowhere else
- `userConfig.sendNames` defaults to `true`; setting it false blanks the `name` field before the
  body is serialised, which is the knob that stops prompt-derived text leaving
- the request is deliberately not awaited, so a slow endpoint cannot hold up a turn, and failures
  surface as a status line rather than an exception

> [!warning] What HCM should decide before this goes fleet-wide
> This plugin is in `autoinstall.json`, so it reaches every endpoint. Two settings deserve an
> explicit decision rather than a default:
>
> 1. **`webhookUrl` should be pinned empty** in managed settings unless HCM actually wants a board.
>    Left unmanaged, any user can point per-turn metrics, including task names, at any HTTPS
>    endpoint they choose. Nothing in the plugin restricts the destination, which is the same shape
>    as the `EPISODIC_MEMORY_API_BASE_URL` decision recorded for the other autoinstalled plugin.
> 2. **`ledger` is on by default** and writes prompt-derived task names to disk under the user
>    profile. That is almost certainly fine, and it is also the sort of thing nobody wants to
>    discover during an audit rather than read here first.

### Commands the plugin declares

All are `node` running a script **inside the plugin directory**. Nothing else is invoked.

| Manifest | Event | Command | Timeout |
|---|---|---|---|
| `hooks/claude-codex-hooks.json`, **read by Claude Code** | `SessionStart` (`startup\|resume\|clear\|compact`) | `node -e "require(<plugin root>/hooks/ponytail-activate.js)"` | 15s |
| | `SubagentStart` | `node -e "require(... /hooks/ponytail-subagent.js)"` | 15s |
| | `UserPromptSubmit` | `node -e "require(... /hooks/ponytail-mode-tracker.js)"` | 15s |
| `hooks/claude-band.json`, **also read by Claude Code, new at 5.x** | none | No commands. Declares `"modules": ["./band/register.tsx"]`, loaded in-process | n/a |
| `hooks/copilot-hooks.json`, inert here | `sessionStart`, `userPromptSubmitted` | `node "${PLUGIN_ROOT}/hooks/..."` (`bash` and `powershell` variants) | 5s |
| `hooks/cursor-hooks.json`, inert here, new at 5.x | | Cursor equivalents | |
| `hooks/qoder-hooks.json`, inert here | | `node PONYTAIL_DIR/hooks/...` | |

`.claude-plugin/plugin.json` now declares **two** manifests, `./hooks/claude-codex-hooks.json` and
`./hooks/claude-band.json`, where 4.9.0 declared one. The Copilot, Cursor and Qoder manifests are
shipped but never read on an HCM machine. They are inventoried anyway, because "present but
currently inert" is a fact a future reader needs: the manifest could start being read after an
upstream bump, which is exactly what `claude-band.json` just did.

Two details of the command shape are worth recording. The timeout went from 5 to 15 seconds,
because a slow node start on Windows was truncating hook output (upstream `#1165`), which is part
of why `main` was pinned over the tag. And the command is written as
`node -e "require(require('path').join(process.env.CLAUDE_PLUGIN_ROOT.split(String.fromCharCode(92)).join('/'), ...))"`.
`String.fromCharCode(92)` is a backslash: it is there because a literal backslash cannot be written
cleanly inside a JSON string inside a shell command, and the path has to be normalised on Windows.
It reads like obfuscation and is not. It is called out here so that a future scan flagging it finds
an answer already written down.

### State and configuration paths outside the plugin

| Path | Chosen when | Purpose |
|---|---|---|
| `$CLAUDE_CONFIG_DIR` or `~/.claude` | default | Mode state, statusline nudge flag |
| `$COPILOT_PLUGIN_DATA` (falls back to `~/.claude`) | `COPILOT_PLUGIN_DATA` set | Copilot host |
| `$PLUGIN_DATA` | `PLUGIN_DATA` set (Codex) | Codex host |
| `~/.qoder` | `QODER_SESSION_ID` set | Qoder host |
| `$XDG_CONFIG_HOME/ponytail` or `~/.config/ponytail` | config lookup | Persisted default mode |
| `$APPDATA` | Windows | Config directory resolution |

**Expected, and necessary.** Mode has to survive between sessions, and the plugin directory is
replaced on update, so state cannot live there. The data is a mode name: small, non-secret, and
never transmitted.

### Reads, writes and instructed commands

| Capability | Where | Assessment |
|---|---|---|
| **Reads the user's `settings.json`** | `hooks/ponytail-activate.js`, at `$CLAUDE_CONFIG_DIR/settings.json` | Checks whether a statusline is already configured. Read-only; not transmitted (there is no egress) |
| Writes a one-time nudge flag | `hooks/ponytail-activate.js` → `<claudeDir>/.ponytail-statusline-nudged` | Stops the setup offer repeating every session |
| Creates and deletes session state | `hooks/ponytail-runtime.js` (`setMode` / `clearMode`) | Mode persistence |
| **Proposes a persistent `statusLine` command** | `hooks/ponytail-activate.js`, running `powershell -ExecutionPolicy Bypass -File "<plugin>/hooks/ponytail-statusline.ps1"` on Windows, `bash "<plugin>/hooks/ponytail-statusline.sh"` elsewhere | See the HCM note below, the most consequential item on this page |
| `ponytail-debt` writes a ledger | `PONYTAIL-DEBT.md` in the working repository | Writes into the user's project. Named, visible, and the skill is invoked deliberately |
| Skills instruct `grep` and `git blame` | `ponytail/SKILL.md`, `ponytail-debt/SKILL.md` | Read-only source inspection; the agent asks before running commands. The debt scan does not exclude `node_modules`, `.git` or build output, so it can be slow on a large repo |
| `ponytail-audit` scans the whole repository | `ponytail-audit/SKILL.md` | Read-only, and the point of an audit skill |
| Skills instruct host-level update commands | `skills/ponytail-help/SKILL.md` | `/plugin marketplace update ponytail`, `/reload-plugins`, `npm install -g @anthropic-ai/claude-code@latest`, `brew upgrade claude-code`. Suggested to the user, never executed. See the staleness note below |

### Environment variables read

`PONYTAIL_DEFAULT_MODE`, `PONYTAIL_HIDE_STATUS`, `PONYTAIL_QUIET_STARTUP`, `PONYTAIL_SUBAGENT_MATCHER`,
`CLAUDE_CONFIG_DIR`, `CLAUDE_PLUGIN_ROOT`, `XDG_CONFIG_HOME`, `APPDATA`, `PLUGIN_DATA`,
`COPILOT_PLUGIN_DATA`, `QODER_SESSION_ID`.

Read for host detection and configuration only. The plugin does not enumerate the environment, and
with no network egress there is nowhere for a value to go.

> [!warning] The statusline offer, and why it matters on an HCM endpoint
> On first activation, if no statusline is configured, `ponytail-activate.js` writes a one-time
> flag file and appends text to its hook output telling the agent to *proactively offer* to add a
> `statusLine` entry to the user's `settings.json`. On Windows the proposed command is:
>
> ```
> powershell -ExecutionPolicy Bypass -File "<plugin>/hooks/ponytail-statusline.ps1"
> ```
>
> The plugin does **not** write the settings entry itself: it prints the snippet and asks the agent
> to offer. The path is guarded by an `isShellSafe()` check, and if the install path contains shell
> metacharacters the snippet is withheld and the agent is told to wire it up by hand. That is
> careful engineering, not a trick.
>
> It is still worth HCM knowing, for two reasons. First, accepting the offer means a command runs
> on **every statusline refresh**, persisted in the user's own settings where it outlives the
> plugin. Second, `powershell -ExecutionPolicy Bypass -File` is a command shape SentinelOne scores,
> and it would be attributed to the host editor's process tree.
>
> **Changed at 5.x, and this part is new.** The proposed command no longer points into the plugin
> directory. Claude Code deletes that versioned cache directory on update, which left accepted
> statuslines blank after every upgrade (upstream `#1032`), so `ponytail-activate.js` now **copies
> `ponytail-statusline.ps1` into the Claude config directory** (`~/.claude` by default) and
> **refreshes that copy on every session start** where the file already exists. The copy is written
> to a temp name and renamed, so a concurrent session never runs a half-written script and a
> symlink at the destination is replaced rather than written through.
>
> So on a 5.x endpoint there is a PowerShell script living in the user profile, rewritten at
> session start. The mechanics are sound and the reason is a real bug fix. It is recorded here
> because "a `.ps1` in `~/.claude` that changes by itself" is precisely the kind of thing an
> endpoint-security review asks about, and the answer should already be written down.
>
> **Not a reason to reject the plugin.** It is opt-in, visible, and the user is asked. It is a
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
> (`SQP-1`) and CodeRabbit. Accepted: an annoyance, not a risk, and fixing it means modifying
> upstream. Worth raising with the author.

> [!warning] One dangling reference caused by the subset
> `skills/ponytail-gain/SKILL.md:19` cites "`benchmarks/` and the README" as the source of its
> figures, and neither is vendored. Nothing breaks: the benchmark numbers are inline in
> `commands/ponytail-gain.toml`, and the skill states they are published medians, not values it
> computes. It is a citation pointing at paths that exist only upstream. Accepted rather than
> vendoring 299 KB of benchmark data for a footnote. The upstream URL at the top of this record is
> where those sources live.

## Scan detail

**Static at 5.3.2 (`--no-llm`, the CI gate):** **3 findings, coverage 35/35 components, 100%,
status complete.** All three are accounted for in `triage/ponytail.yaml` and are reproduced there
with the reasoning. In summary: `PE3` on the word "keychain" in the `webhookToken` description,
`RA2` on the `ledger` description that accurately states it writes a per-turn row to
`~/.config`, and `OH1` on `exec(output` which is `RegExp.prototype.exec` parsing test-runner text.

Two of those three are the scanner correctly noticing the new band feature. Only `OH1` is noise.

> [!note] The scanner's own verdict on this plugin is `DO_NOT_INSTALL`
> So is its verdict on `episodic-memory`. Neither is a reason not to ship, and that is the whole
> premise of `triage/README.md`: the exit code blocks above risk 50 and scores HIGH at +25, so two
> HIGH findings on accurate feature descriptions are enough to condemn a plugin. HCM adjudicates
> every finding individually instead. Recorded here so nobody reads the raw scanner output later
> and concludes the catalog shipped something it was told not to.

**4.9.0 for comparison:** risk 0, SAFE, zero issues, 25/25. The jump from zero findings to three
is not a decline in quality; it is a new feature that touches a network and a token, which is
exactly what the scanner exists to surface.

**Semantic at 5.3.2: not run.** No API key is configured on the vendoring machine, so the three
semantic analyzers were skipped. The 4.9.0 semantic result below is kept for history and **does not
carry forward**: ponytail 5 is a stated ground-up rewrite with a feature 4.9.0 did not have, so a
semantic pass over the old content says nothing about the new. Treat the semantic row as open.

**Semantic at 4.9.0, historical (`SKILLSPECTOR_PROVIDER=claude_cli`):** risk 2, CAUTION, one LOW
finding.

> `SQP-1` at `skills/ponytail-debt/SKILL.md:6-8`, confidence 0.5: two of the skill's trigger
> phrases, "list the shortcuts" and "what did we mark to do later", contain no skill-specific
> token. The former plausibly matches a question about keyboard shortcuts, the latter any generic
> TODO or backlog question. The description gives no exclusion conditions.

**Accepted, not fixed.** It is a trigger-scoping quality issue, not a security one, and correcting
it would mean modifying upstream content and creating drift for a LOW/0.5-confidence finding. The
practical consequence is that `ponytail-debt` may occasionally activate on an unrelated question,
an annoyance, not a risk. Worth raising upstream.

> [!warning] The semantic pass was not complete
> `semantic_security_discovery` finished **degraded**: 11 files fully inspected, 13 partially,
> stopped by `LLMRuntimeLimitError`: a configured runtime limit, not a clean bill of health.
> `semantic_developer_intent` and `semantic_quality_policy` both completed 24/24, and every static
> analyzer completed 25/25, so no file went entirely uninspected.
>
> Recorded because a partial result reported as "clean" is the exact failure this catalog exists to
> prevent. The static gate, which is what actually blocks a merge, was complete.

## Upstream drift

Owner: Hodahel Moinzadeh. Checked against upstream quarterly.

A fork stops receiving upstream fixes the day it is made; that is the cost of the two-marketplace
policy. Because no file was modified, checking drift is:

Nothing HCM-written lives inside `plugins/ponytail/`. This record sits outside it, in
`provenance/`. That is deliberate: the plugin directory stays byte-identical to upstream, so drift
checking is an exact comparison with no exclusions to remember.

```bash
git clone https://github.com/DietrichGebert/ponytail.git /tmp/pt
diff -r plugins/ponytail /tmp/pt | grep -v '^Only in /tmp/pt'
```

`Only in /tmp/pt` lines are the paths deliberately not vendored (see the table above). **Anything
else that reports is a real upstream change to a file HCM ships**, and needs a new pull request
against a new commit sha, never a quiet `git pull`.

Verified at vendoring time: the comparison reported **zero** differing files.

## Change log

### 5.3.2-hcm.1, 2026-10-20

Re-vendored from `4.9.0-hcm.1` at upstream `09c434ab`. A major version jump: upstream describes
ponytail 5 as a ground-up rewrite, and the delta from the previous pin is 153 commits across
182 files.

What a reviewer should take from this bump, in order of importance:

1. **The plugin can now reach a network and hold a token.** Both were recorded as "none" at 4.9.0.
   See the band section above. The network path is off until someone sets a URL, and HCM should
   decide whether to pin it empty in managed settings rather than leave it to each user.
2. **The ledger writes prompt-derived task names to a local CSV, on by default.**
3. **A PowerShell statusline script is now copied into `~/.claude` and refreshed each session**,
   where 4.9.0 only wrote a flag file. The reason is a real upstream bug fix.
4. **Findings went from 0 to 3**, two of which are the scanner correctly describing the above.
   `triage/ponytail.yaml` is new; the plugin never needed one before.
5. **Vendored size roughly doubled**, 25 files to 35, 144 KB to 319 KB.

Everything the 4.9.0 record flagged was re-verified rather than carried over, and all of it still
holds at 5.x: the statusline offer still exists, `skills/ponytail-help/SKILL.md` still tells users
to run `/plugin marketplace update ponytail` which will not work on an HCM machine, the
`ponytail-gain` skill still cites `benchmarks/` which is not vendored, and `ponytail-audit` still
triggers on a bare "find bloat".

### 4.9.0-hcm.1, 2026-09-03

First vendoring, at upstream `2ed6c52`. Risk 0, zero findings, no triage record required.
