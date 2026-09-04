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
| Semantic scan | **not run.** The static pass plus a full read of the executable surface was the basis for publication. Recorded rather than implied — a scan that was not run is not a clean scan |
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

> [!danger] Correction — this plugin DOES have network egress
> An earlier draft of this record said "network egress: none in the plugin's own code". **That was
> wrong**, and it was found by review rather than by the scanner. There are three outbound paths,
> and the first is the one an audit will ask about.

### Data flow — what leaves the machine

| Path | Where | Assessment |
|---|---|---|
| **Conversation content is sent to an LLM for summarization** | `src/summarizer.ts` via `@anthropic-ai/claude-agent-sdk` | **The significant one.** Indexed conversation text is summarised by a model. By default that is the Claude Agent SDK, i.e. the same destination Claude Code already sends the conversation to — so it is not a *new* recipient. But it means HCM conversation content, including anything internal discussed in a session, is submitted for summarisation as a background job nobody explicitly triggers |
| **The destination is overridable by environment variable** | `EPISODIC_MEMORY_API_BASE_URL`, `EPISODIC_MEMORY_API_TOKEN` | Setting these redirects summarisation to an arbitrary endpoint with an arbitrary token. Nothing in the plugin restricts where. Unset by default — but this is the control worth knowing exists, because it turns a known destination into any destination |
| **Downloads an ML model on first run** | `src/embeddings.ts` — `Xenova/bge-small-en-v1.5` via `@huggingface/transformers` | Fetched from HuggingFace, cached locally (`useBrowserCache = false`, `allowLocalModels = true`). A new outbound destination distinct from npm and Anthropic |
| `npm install` on first use | `cli/mcp-server-wrapper.js` | See above — resolves unpinned packages from the npm registry |

### Local behaviour

| Capability | Where | Assessment |
|---|---|---|
| **Native module rebuild on install** | `scripts/postinstall.js` — `npm rebuild better-sqlite3` | Compiles or fetches a native binding against the local Node version, on every endpoint. Deliberately exits 0 even on failure so a Windows-only redirection bug cannot fail the whole install. Another reason to run the install once at deploy time |
| Reads Claude Code session transcripts | `~/.claude/projects/*/*.jsonl` | The product. Read-only |
| Reads Codex config and logs | `~/.codex/`, `CODEX_HOME` | Locates Codex conversation logs. Read-only |
| Writes a local index | SQLite via `better-sqlite3` + `sqlite-vec` | Local database of indexed conversations, including their text |
| Writes logs | `~/.config/superpowers/logs/` | |
| `SessionStart` hook, background sync | `hooks/hooks.json` — `node cli/episodic-memory.js sync --background` | The capture mechanism. Backgrounded so it does not block session start |
| Spawns a detached process | `src/sync-cli.ts` | The background sync |
| **Credential access** | none found | It reads no credential store. `EPISODIC_MEMORY_API_TOKEN` is supplied *to* it, not harvested |
| **Anti-refusal / concealment** | none found | |

### Environment variables it honours

`CLAUDE_CONFIG_DIR`, `CLAUDE_PLUGIN_ROOT`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS`, `CODEX_HOME`,
`XDG_CONFIG_HOME`, `PERSONAL_SUPERPOWERS_DIR`, `CONVERSATION_SEARCH_EXCLUDE_PROJECTS`,
`EPISODIC_MEMORY_CONFIG_DIR`, `EPISODIC_MEMORY_DB_PATH`, `EPISODIC_MEMORY_API_BASE_URL`,
`EPISODIC_MEMORY_API_TOKEN`, `EPISODIC_MEMORY_API_MODEL`, `EPISODIC_MEMORY_API_MODEL_FALLBACK`,
`EPISODIC_MEMORY_API_TIMEOUT_MS`, `EPISODIC_MEMORY_CODEX_BIN`, `EPISODIC_MEMORY_CODEX_MODEL`,
`EPISODIC_MEMORY_CODEX_SUMMARY_TIMEOUT_MS`, `EPISODIC_MEMORY_SUMMARIZER_GUARD`,
`EPISODIC_MEMORY_SUMMARY_ERROR_RETRY_HOURS`, `EPISODIC_MEMORY_MIGRATION_BATCH`,
`TEST_DB_PATH`, `TEST_PROJECTS_DIR`, `TEST_ARCHIVE_DIR`.

The database path and config directory are overridable, so an endpoint can be pointed at a
different index without changing the plugin.

> [!warning] What HCM should decide before this is firm-wide
> The summarisation path means conversation text is submitted to a model as a background job.
> Default destination is the same one Claude Code already uses, so it is not a new disclosure — but
> it is worth an explicit decision rather than an assumption, and `EPISODIC_MEMORY_API_BASE_URL`
> should be treated as a setting nobody sets without review.

## What was vendored, and what was left behind

**105 files, 1.7 MB** of upstream's ~2.1 MB.

| Kept | Why |
|---|---|
| `.claude-plugin/plugin.json`, `.mcp.json` | Manifests |
| `cli/`, `src/`, `dist/` | `dist/` runs; `src/` is kept so the code that produced it can be read |
| `scripts/postinstall.js`, `scripts/generate-version.js` | Referenced by `package.json`. `postinstall` runs during the first-use `npm install` |
| `hooks/`, `skills/`, `agents/`, `prompts/` | The capture hook and the skill surface |
| `package.json` | **Required** — the runtime `npm install` reads it |
| `LICENSE` | MIT requires it |

| Dropped | Why |
|---|---|
| `test/` (3.2 MB) | Not read at runtime. Removing it cut findings from 159 to 44 |
| `scripts/` **except** `postinstall.js` and `generate-version.js` | The e2e scripts are tests. The two kept ones are referenced by `package.json`; excluding them left a **dangling `postinstall`** that would have failed on every endpoint's first install — found by review, not by me |
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
