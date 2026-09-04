# Provenance — episodic-memory

| Field | Value |
|---|---|
| Upstream | https://github.com/obra/episodic-memory |
| **Pinned to** | commit `10757690210574421f1df5f35835af8d0c74d984` |
| Found on | tag `v1.4.2` — which **equals** `HEAD` **and** the sha already installed across HCM |
| Published as | `1.4.2-hcm.1` |
| Licence | MIT — declared in `plugin.json` and shipped as `LICENSE` |
| Vendored | 2026-09-04 |
| Reviewer | Hodahel Moinzadeh |
| Static scan | risk 100 / CRITICAL unadjudicated; **44 findings, all 44 accounted for** in `triage/episodic-memory.yaml` |
| HCM changes | Subset vendored; no file contents modified |

> [!note] The first plugin whose versioning was honest
> `v1.4.2`, `HEAD` and the installed sha are the same commit. Every other candidate assessed for
> this catalog had a version label covering more than one commit — ponytail's tag was three commits
> behind, superpowers-chrome's `3.0.5` covered two commits differing by a Chrome-sandbox fix.

## Why HCM carries this

It indexes past Claude Code conversations so they can be searched later. A `SessionStart` hook runs
`cli/episodic-memory.js sync --background`, which reads `~/.claude/projects/*/*.jsonl`.

That makes it **time-sensitive in a way most plugins are not**. Claude Code deletes session
transcripts after 30 days by default, and the plugin only indexes while installed. A machine that
gets it late has permanently lost everything past the retention window. This is why it is in
`autoinstall.json` rather than available on request — deferring the install defers the capture, and
the capture is the point.

## The one behaviour that genuinely matters

> [!danger] It runs `npm install` inside its own directory on first use
> `cli/mcp-server-wrapper.js` probes for six runtime packages and, if any are missing, spawns
> `npm install --no-audit --no-fund` in the plugin root:
>
> `@anthropic-ai/claude-agent-sdk`, `@huggingface/transformers`, `better-sqlite3`,
> `onnxruntime-node`, `proper-lockfile`, `sqlite-vec`
>
> Upstream ships **no lockfile**, and all 16 declared dependencies are caret ranges. So what gets
> installed is whatever npm resolves at that moment. `better-sqlite3` and `onnxruntime-node` are
> native modules — compilation or prebuilt-binary downloads — and `@huggingface/transformers` pulls
> ML models.
>
> Two consequences, stated plainly:
>
> 1. **The pinned, scanned plugin directory modifies itself at runtime with unreviewed code.** For a
>    catalog whose premise is "what runs is what was reviewed at a pinned commit", this plugin is a
>    documented exception. Vendoring pins the plugin; it does not pin what the plugin fetches.
> 2. **`npm install` building native modules on a SentinelOne endpoint** is the process-churn shape
>    HCM's own EDR guidance calls out.
>
> Accepted deliberately, with the reasoning recorded rather than buried: the alternative was losing
> conversation history permanently, which is the harm this plugin exists to prevent.
>
> **Mitigation available and recommended:** ClaudeDeploy should run that `npm install` once at
> deploy time, under controlled conditions, rather than letting it fire unpredictably mid-session
> across the fleet. Raised with the ClaudeDeploy session 2026-09-04.

## Why building `dist/` in CI was rejected

The original plan was to build `dist/` from vendored `src/` in CI rather than shipping compiled
output. On inspection that makes the supply chain **worse**:

- no `package-lock.json`, so `npm ci` cannot run at all
- **zero** exact-pinned dependencies; all 16 are caret ranges, including `typescript@^5.9.3` and
  `esbuild@^0.25.11`
- the build is `tsc && esbuild --bundle`

A CI build would resolve 16 unpinned packages from npm at build time and bundle them into what every
endpoint runs. The committed `dist/` is at least fixed bytes at a reviewed commit. Shipping it is
the safer of the two, which inverts the intuition.

`dist/` is a genuine runtime dependency, not dead weight: `cli/index-conversations.js` and
`cli/search-conversations.js` spawn `../dist/*.js`, and the MCP wrapper launches
`dist/mcp-server.js`.

> **Residual risk:** the compiled output is not independently verified, and upstream provides no way
> to reproduce it. Its findings are compiled copies of `src/` matches that were verified by reading
> the source, but the correspondence between the two cannot be proven. An upstream issue asking for
> a lockfile would reopen the build option properly.

## Capability inventory

| Capability | Where | Assessment |
|---|---|---|
| **Runs `npm install` on first use** | `cli/mcp-server-wrapper.js` | See above. The item that matters |
| Reads Claude Code session transcripts | `~/.claude/projects/*/*.jsonl` | The product. Read-only |
| Reads Codex config | `~/.codex/config.toml` | Locates Codex conversation logs. Read-only |
| Writes a local index | SQLite via `better-sqlite3` + `sqlite-vec` | Local database of the indexed conversations |
| `SessionStart` hook, background sync | `hooks/hooks.json` | The capture mechanism. Backgrounded so it does not block session start |
| Spawns a detached process | `src/sync-cli.ts` | The background sync |
| **Network egress** | none in the plugin's own code | The only outbound traffic is npm's, during the install above |
| **Credential access** | none | |
| **Anti-refusal / concealment** | none | |

## What was vendored, and what was left behind

**105 files, 1.7 MB** of upstream's ~2.1 MB.

| Kept | Why |
|---|---|
| `.claude-plugin/plugin.json`, `.mcp.json` | Manifests |
| `cli/`, `src/`, `dist/` | `dist/` runs; `src/` is kept so the code that produced it can be read |
| `hooks/`, `skills/`, `agents/`, `prompts/` | The capture hook and the skill surface |
| `package.json` | **Required** — the runtime `npm install` reads it |
| `LICENSE` | MIT requires it |

| Dropped | Why |
|---|---|
| `test/` (3.2 MB), `scripts/` | Not read at runtime. Removing them cut findings from 159 to 44 |
| `docs/`, `CHANGELOG.md`, `README.md`, `CLAUDE.md` | Not read at runtime |
| `.agents/`, `.codex-plugin/`, `vitest.config.ts`, `tsconfig.json`, `.version-bump.json` | Other tooling; not read by Claude Code |

Every retained file is byte-identical to upstream at the pinned commit — verified by per-file
SHA-256, zero mismatches.

## Findings

All 44 are accounted for in `triage/episodic-memory.yaml`. Most are substring matches: this plugin
searches conversations, so its vocabulary *is* the scanner's keyword list. The identifier fragment
`pList` alone produces 12, and a SQL parameterised-query placeholder list is reported as "Context
Window Stuffing".

**Two are real.** `SC1` and `SC4` on `package.json` flag unpinned dependency ranges. That is
accurate, it is the same issue as the `npm install` behaviour above, and it is accepted with the
risk recorded — not dismissed as noise.

## Upstream drift

Owner: Hodahel Moinzadeh. Checked quarterly.

```bash
git clone https://github.com/obra/episodic-memory.git /tmp/em
git -C /tmp/em checkout 10757690210574421f1df5f35835af8d0c74d984
diff -r plugins/episodic-memory /tmp/em | grep -v '^Only in /tmp/em'
```

`Only in /tmp/em` lines are the deliberately-dropped paths above. Anything else is a real upstream
change to a file HCM ships, and needs a new pull request at a new commit — never a quiet `git pull`.
Re-vendoring also forces re-triage automatically: changed content changes findings, which leaves
triage entries stale and findings unaccounted, and the build fails until someone looks again.
