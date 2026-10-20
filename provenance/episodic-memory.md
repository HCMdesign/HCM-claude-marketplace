# Provenance - episodic-memory

| Field | Value |
|---|---|
| Upstream | https://github.com/obra/episodic-memory |
| **Pinned to** | commit `274150365d83af95e1219cc39c8ffedd7d8413df` |
| Found on | tag `v1.6.0`. **Not** `HEAD` this time, see "Which ref" below |
| Published as | `1.6.0-hcm.1` |
| Licence | MIT, declared in `plugin.json` and shipped as `LICENSE` |
| Vendored | 2026-10-20 (first vendored 2026-09-04 at `1.4.2`, see the change log) |
| Reviewer | Hodahel Moinzadeh, 2026-10-20 |
| Static scan | **47 findings, all 47 accounted for** in `triage/episodic-memory.yaml`. Coverage 122/122 components, 100%, status complete. The scanner's own recommendation is `DO_NOT_INSTALL`; HCM adjudicates per finding instead |
| Semantic scan | **Not run at 1.6.0.** No API key is configured on the vendoring machine, so the semantic analyzers were skipped. The static pass plus a read of the changed executable surface was the basis for publication. Recorded rather than implied: a scan that was not run is not a clean scan |
| HCM changes | Subset vendored; no file contents modified |

> [!note] This bump closes a real security hole
> Upstream 1.5.0 fixed a defect where the background summarizer resumed the user's session **with
> their tools, MCP servers and settings loaded**, so a summarization pass could execute pending work
> and, in at least one upstream report, commit to a working repository. HCM has been shipping the
> vulnerable version fleet-wide through `autoinstall.json` since September. The fix is verified
> present in the vendored code; details below.

## Which ref, and why the tag this time

The `v1.6.0` tag points at `274150365d83af95e1219cc39c8ffedd7d8413df`, dated 2026-09-08. Upstream
`HEAD` is `7e06519`, dated 2026-09-10, and the two commits between them are a test-expectation fix
and surrounding test work. Nothing in them changes runtime behaviour.

That is the opposite of the ponytail situation, where `main` carried Windows fixes the tag did not.
Here the tag is a clean released boundary and `HEAD` adds nothing an HCM endpoint would feel, so
the tag wins. The rule is not "always prefer the tag" or "always prefer the branch": it is to look
at what the difference actually contains and say so.

Upstream has been quiet since 2026-09-10, so `v1.6.0` is also the current state of the project.

> [!note] Versioning here is still honest, with one caveat
> At `1.4.2` this was the first candidate whose tag, `HEAD` and installed sha were one commit.
> `v1.6.0` is still an unambiguous tag pointing at one commit; it simply is no longer `HEAD`.
> Every other candidate assessed for this catalog had a version label covering more than one
> commit: ponytail's tag was three commits behind at 4.9.0 and eight behind at 5.3.2, and
> superpowers-chrome's `3.0.5` covered two commits differing by a Chrome-sandbox fix.

## Why HCM carries this

It indexes past Claude Code conversations so they can be searched later. A `SessionStart` hook runs
`cli/episodic-memory.js sync --background`, which reads `~/.claude/projects/*/*.jsonl`.

That makes it **time-sensitive in a way most plugins are not**. Claude Code deletes session
transcripts after 30 days by default, and the plugin only indexes while installed. A machine that
gets it late has permanently lost everything past the retention window. This is why it is in
`autoinstall.json` rather than available on request: deferring the install defers the capture, and
the capture is the point.

## The summarizer sandbox, new in upstream 1.5.0

This is the most important difference between `1.4.2` and `1.6.0`, and the reason the bump is worth
doing on its own.

**What was wrong.** The background summarizer resumes a past session in order to summarise it.
Before 1.5.0 it resumed that session the way the user would have: built-in tools available, every
configured MCP server launched, user settings and hooks loaded. A resumed mid-task session could
therefore carry on *doing the task* instead of writing a summary. Upstream reports include a
summarization pass committing to a working repository.

**The fix, verified in the vendored code** at `src/summarizer.ts:345-371`:

| Option | What it stops | Upstream issue |
|---|---|---|
| `tools: []` | Every built-in tool is unavailable, so a resumed mid-task session cannot keep executing the task | `#116`, `#134` |
| `strictMcpConfig: true` | MCP servers declared in `~/.claude.json` are not launched for the subprocess | `#106` |
| `settingSources: []` | User settings are not loaded, which otherwise pulled in every enabled plugin (each with its own MCP server) plus the user's Stop and Notification hooks | `#136` |
| `persistSession: false` | Summarization stops writing fake session transcripts into `~/.claude/projects/` and polluting the session list | `#83` |

**Why this one matters more at HCM than it would elsewhere.** Two reasons, and both are specific to
how these machines are set up.

First, this plugin is in `autoinstall.json`. It is on every endpoint, so the vulnerable version was
not a personal risk, it was a fleet one. HCM endpoints carry MCP servers with write access to
Zendesk, Plane, Hudu, Proxmox and the git host. "The summarizer resumes your session with your
tools loaded" reads very differently against that list than it does on a laptop with no connectors.

Second, the `#106` comment in the source is explicit that without `strictMcpConfig`, concurrent
summarizations "fans out to hundreds of processes on MCP-heavy installs". Process churn is the
documented SentinelOne trigger on these machines, and an HCM workstation is about as MCP-heavy as
they come. This fix is as much an EDR improvement as a security one.

## The one behaviour that genuinely matters

> [!danger] It runs `npm install` inside its own directory on first use
> `cli/mcp-server-wrapper.js` probes for six runtime packages and, if any are missing, spawns
> `npm install --no-audit --no-fund` in the plugin root:
>
> `@anthropic-ai/claude-agent-sdk`, `@huggingface/transformers`, `better-sqlite3`,
> `onnxruntime-node`, `proper-lockfile`, `sqlite-vec`
>
> Upstream still ships **no lockfile**, and every dependency is a caret range: 8 runtime, 8 more in
> `devDependencies`, 16 in total, zero pinned exactly. So what gets installed is whatever npm
> resolves at that moment. `better-sqlite3` and `onnxruntime-node` are native modules, meaning
> compilation or prebuilt-binary downloads, and `@huggingface/transformers` pulls ML models.
>
> **Improved in 1.6.0, and the improvement is an EDR one.** Previously, when the wrapper had to run
> `npm install` and the connection timed out, the install child was orphaned and kept running, and
> each retry started another; several could end up competing and starving each other so none
> finished. The wrapper now holds a **single-install lock** and **kills its install child on exit**
> (`SIGTERM`, `SIGINT`, `SIGHUP`), both verified in `cli/mcp-server-wrapper.js`. Stacked, competing
> `npm install` processes are exactly the churn signature that has twice produced a false-positive
> ransomware alert on these machines, so this is worth more here than its release note suggests.
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

> [!danger] Correction: this plugin DOES have network egress
> An earlier draft of this record said "network egress: none in the plugin's own code". **That was
> wrong**, and it was found by review rather than by the scanner. There are three outbound paths,
> and the first is the one an audit will ask about.

### Data flow, what leaves the machine

| Path | Where | Assessment |
|---|---|---|
| **Conversation content is sent to an LLM for summarization** | `src/summarizer.ts` via `@anthropic-ai/claude-agent-sdk` | **The significant one.** Indexed conversation text is summarised by a model. By default that is the Claude Agent SDK, i.e. the same destination Claude Code already sends the conversation to, so it is not a *new* recipient. But it means HCM conversation content, including anything internal discussed in a session, is submitted for summarisation as a background job nobody explicitly triggers |
| **The destination is overridable by environment variable** | `EPISODIC_MEMORY_API_BASE_URL`, `EPISODIC_MEMORY_API_TOKEN` | Setting these redirects summarisation to an arbitrary endpoint with an arbitrary token. Nothing in the plugin restricts where. Unset by default, but this is the control worth knowing exists, because it turns a known destination into any destination |
| **Downloads an ML model on first run** | `src/embeddings.ts`, `Xenova/bge-small-en-v1.5` via `@huggingface/transformers` | Fetched from HuggingFace, cached locally (`useBrowserCache = false`, `allowLocalModels = true`). A new outbound destination distinct from npm and Anthropic |
| `npm install` on first use | `cli/mcp-server-wrapper.js` | See above, resolves unpinned packages from the npm registry |

### Local behaviour

| Capability | Where | Assessment |
|---|---|---|
| **Native module rebuild on install** | `scripts/postinstall.js`, `npm rebuild better-sqlite3` | Compiles or fetches a native binding against the local Node version, on every endpoint. Deliberately exits 0 even on failure so a Windows-only redirection bug cannot fail the whole install. Another reason to run the install once at deploy time |
| Reads Claude Code session transcripts | `~/.claude/projects/*/*.jsonl` | The product. Read-only |
| Reads Codex config and logs | `~/.codex/`, `CODEX_HOME` | Locates Codex conversation logs. Read-only |
| Writes a local index | SQLite via `better-sqlite3` + `sqlite-vec` | Local database of indexed conversations, including their text |
| Writes logs | `~/.config/superpowers/logs/` | |
| `SessionStart` hook, background sync | `hooks/hooks.json`, `node cli/episodic-memory.js sync --background` | The capture mechanism. Backgrounded so it does not block session start |
| Spawns a detached process | `src/sync-cli.ts` | The background sync |
| **Credential access** | none found | It reads no credential store. `EPISODIC_MEMORY_API_TOKEN` is supplied *to* it, not harvested |
| **Anti-refusal / concealment** | none found | |

### Environment variables it honours

Enumerated from the vendored `src/` and `cli/` at 1.6.0:

`CLAUDE_CONFIG_DIR`, `CLAUDE_PLUGIN_ROOT`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS`, `CODEX_HOME`,
`XDG_CONFIG_HOME`, `PERSONAL_SUPERPOWERS_DIR`, `CONVERSATION_SEARCH_EXCLUDE_PROJECTS`,
`EPISODIC_MEMORY_CONFIG_DIR`, `EPISODIC_MEMORY_DB_PATH`, `EPISODIC_MEMORY_API_BASE_URL`,
`EPISODIC_MEMORY_API_TOKEN`, `EPISODIC_MEMORY_API_MODEL`, `EPISODIC_MEMORY_API_MODEL_FALLBACK`,
`EPISODIC_MEMORY_API_TIMEOUT_MS`, `EPISODIC_MEMORY_CODEX_BIN`, `EPISODIC_MEMORY_CODEX_MODEL`,
`EPISODIC_MEMORY_CODEX_SUMMARY_TIMEOUT_MS`, `EPISODIC_MEMORY_SUMMARIZER_GUARD`,
`EPISODIC_MEMORY_SUMMARY_ERROR_RETRY_HOURS`, `EPISODIC_MEMORY_MIGRATION_BATCH`,
`TEST_DB_PATH`, `TEST_PROJECTS_DIR`, `TEST_ARCHIVE_DIR`.

**New at 1.5.0 and 1.6.0**, and three of these are controls HCM may actually want:

| Variable | What it does | Worth knowing |
|---|---|---|
| `EPISODIC_MEMORY_DISABLE_AUTO_SYNC` | Turns off the `SessionStart` background sync entirely. A manual `sync` still works | **The real off switch.** Unlike `SKIP_SUMMARIES` it stops the copy and index work too, so it is the setting to reach for if the hook ever becomes a problem on an endpoint |
| `EPISODIC_MEMORY_SKIP_SUMMARIES` | Indexes without summarising | Stops conversation text being sent to a model at all, while keeping search working |
| `EPISODIC_MEMORY_ALLOW_METERED_API` | Acknowledges and silences a new warning | 1.5.0 added a one-time warning that a global `ANTHROPIC_API_KEY` causes background summaries to bill the metered API rather than a subscription. The warning is the useful part |
| `EPISODIC_MEMORY_SUMMARY_TIMEOUT_MS` | Caps one summary's runtime | A wedged summary used to stall every later sync |
| `EPISODIC_MEMORY_MAX_MESSAGE_BYTES` | Skips oversized messages before embedding, default 256 KB | Added because third-party tools embedding a whole transcript into one prompt produced multi-megabyte single "messages"; in one upstream report, 97% of a 3 GB index |
| `EPISODIC_MEMORY_EMBED_THREADS` | Embedding thread count | Relevant to CPU load on an endpoint |
| `EPISODIC_MEMORY_OPENCODE_*` | Locate opencode data, db and transcripts | Part of the new sources below |
| `CLAUDE_CODE_USE_BEDROCK` | Routes summarisation through AWS Bedrock | A fourth possible destination for conversation content. Unset here |

**New conversation sources, and they switch themselves on.** 1.5.0 added Cursor (with a one-time
`import-cursor-history` backfill from Cursor's local database) and opencode; 1.6.0 added Oh My Pi.
Alongside Claude Code and Codex that is five harnesses across seven directories.

> [!warning] There is no opt-in step. Discovery is existence-based.
> An earlier draft of this record said "none is enabled by HCM", which implies a switch that does
> not exist. `getConversationSourceDirs()` in `src/paths.ts` builds a fixed candidate list and ends
> with `.filter(d => fs.existsSync(d))`. **If the directory is there, it is indexed.** No setting,
> no consent step, no HCM decision anywhere in the path. `src/indexer.ts` calls it on every index
> run, including the one the `SessionStart` hook triggers in the background.
>
> The candidate directories are:
>
> | Harness | Directory |
> |---|---|
> | Claude Code | `<claude dir>/projects`, `<claude dir>/transcripts` |
> | Codex | `<codex dir>/sessions` |
> | Cursor | `<cursor dir>/projects`, plus the legacy export dir under `~/.config/superpowers/` |
> | opencode | the opencode transcript dir under `~/.config/superpowers/` |
> | Oh My Pi | `<omp dir>/agent/sessions` |
>
> `import-cursor-history` additionally reads Cursor's own SQLite state database (`state.vscdb`, at
> a different path per OS), and the opencode sync opens the opencode SQLite database directly.
>
> **Why this is worth stating plainly.** On a machine where someone has also used Cursor or
> opencode, this plugin indexes those conversations too, and HCM never chose that. It is not
> malicious and it is arguably the product working as intended, since the point is to search your
> history. But the scope of "your history" grew in 1.5.0 and 1.6.0 without any corresponding
> decision, and the earlier wording in this record would have let a reader believe otherwise.

**The Cursor backfill reads an unconfined path.** `src/cursor-legacy.ts` locates Cursor's
`state.vscdb` at a different path per operating system, and `import-cursor-history --db <path>`
accepts **any** path the user gives it rather than validating it against the expected locations. It
also walks `$CURSOR_HOME/projects/*/agent-transcripts/`, defaulting to `~/.cursor/projects`. This
is a user-invoked one-time command rather than anything the hook runs, and the unconfined `--db`
is a convenience for a non-standard install, not a hole someone else can reach through. Recorded
because "reads an arbitrary SQLite file the user names" belongs in an inventory.

**The bundled agent has a broad trigger.** `agents/search-conversations.md` carries a description
wide enough to activate on ordinary engineering questions rather than on an explicit request to
search past conversations. Same class of issue as ponytail's trigger breadth, same disposition:
not modified, because changing it creates drift on vendored content for a quality problem rather
than a security one. Worth knowing when a session reaches for conversation history unprompted.

The database path and config directory are overridable, so an endpoint can be pointed at a
different index without changing the plugin.

> [!warning] What HCM should decide before this is firm-wide
> The summarisation path means conversation text is submitted to a model as a background job.
> Default destination is the same one Claude Code already uses, so it is not a new disclosure, but
> it is worth an explicit decision rather than an assumption, and `EPISODIC_MEMORY_API_BASE_URL`
> should be treated as a setting nobody sets without review.

## What was vendored, and what was left behind

**122 files, 2.1 MB** of upstream's 5.6 MB (it was 105 files and 1.7 MB at 1.4.2).

| Kept | Why |
|---|---|
| `.claude-plugin/plugin.json`, `.mcp.json` | Manifests |
| `cli/`, `src/`, `dist/` | `dist/` runs; `src/` is kept so the code that produced it can be read |
| `scripts/postinstall.js`, `scripts/generate-version.js` | Referenced by `package.json`. `postinstall` runs during the first-use `npm install` |
| `hooks/`, `skills/`, `agents/`, `prompts/` | The capture hook and the skill surface |
| `package.json` | **Required**, the runtime `npm install` reads it |
| `LICENSE` | MIT requires it |

| Dropped | Why |
|---|---|
| `test/` (3.2 MB) | Not read at runtime. Removing it cut findings from 159 to 44 |
| `scripts/` **except** `postinstall.js` and `generate-version.js` | The e2e scripts are tests. The two kept ones are referenced by `package.json`; excluding them left a **dangling `postinstall`** that would have failed on every endpoint's first install. Found by review, not by me |
| `docs/`, `CHANGELOG.md`, `README.md`, `CLAUDE.md` | Not read at runtime |
| `.agents/`, `.codex-plugin/`, `vitest.config.ts`, `tsconfig.json`, `.version-bump.json` | Other tooling; not read by Claude Code |

Every retained file is byte-identical to upstream at the pinned commit, verified by per-file
SHA-256, zero mismatches.

## Findings

All 47 are accounted for in `triage/episodic-memory.yaml`. Most are substring matches: this plugin
searches conversations, so its vocabulary *is* the scanner's keyword list. The identifier fragment
`pList` alone produces 12, and a SQL parameterised-query placeholder list is reported as "Context
Window Stuffing".

**Two are real.** `SC1` and `SC4` on `package.json` flag unpinned dependency ranges. That is
accurate, it is the same issue as the `npm install` behaviour above, and it is accepted with the
risk recorded, not dismissed as noise.

## Upstream drift

Owner: Hodahel Moinzadeh. Checked quarterly.

```bash
git clone https://github.com/obra/episodic-memory.git /tmp/em
git -C /tmp/em checkout 274150365d83af95e1219cc39c8ffedd7d8413df
diff -r plugins/episodic-memory /tmp/em | grep -v '^Only in /tmp/em'
```

`Only in /tmp/em` lines are the deliberately-dropped paths above. Anything else is a real upstream
change to a file HCM ships, and needs a new pull request at a new commit, never a quiet `git pull`.
Re-vendoring also forces re-triage automatically: changed content changes findings, which leaves
triage entries stale and findings unaccounted, and the build fails until someone looks again.

## Change log

### 1.6.0-hcm.1, 2026-10-20

Re-vendored from `1.4.2-hcm.1` at upstream `274150365` (tag `v1.6.0`), 32 commits and 121 files on
from the previous pin.

**The reason for the bump is the summarizer sandbox in 1.5.0**, documented in its own section
above. HCM had been shipping the vulnerable version to every endpoint through `autoinstall.json`
since September, on machines whose MCP servers can write to Zendesk, Plane, Hudu, Proxmox and the
git host. That is the finding that made this upgrade worth doing ahead of anything else in the
catalog.

Also arriving with it:

1. **Stacked `npm install` processes are fixed** by a single-install lock and killing the install
   child on exit. Directly relevant to the EDR churn problem on these machines.
2. **Sync no longer re-embeds everything on every run**, only new messages. On a long-lived
   transcript this turns minutes of repeated work per sync into seconds.
3. **A real off switch exists**, `EPISODIC_MEMORY_DISABLE_AUTO_SYNC`, which stops the copy and
   index work rather than only the summarisation.
4. **Oversized messages are skipped before embedding**, capped at 256 KB, after an upstream report
   of a single embedded transcript accounting for 97% of a 3 GB index.
5. **Three more conversation sources**: Cursor, opencode and Oh My Pi, which widen what gets
   indexed on a machine where those tools are installed.
6. **Findings went from 44 to 47.** The 39 triage entries written for 1.4.2 all still match; three
   new entries were added, and none of the three is a real issue.

**One file left the subset, and that is a correction rather than a change.**
`plugins/episodic-memory/src/version.ts` is gone. Upstream generates it with
`scripts/generate-version.js` at build time and **gitignores it**, so it is not in the repository at
`v1.6.0`. The 1.4.2 vendoring shipped a copy of it, which means that subset contained a file with no
upstream counterpart to compare against: a small hole in the byte-identity guarantee, now closed.
Nothing breaks, because the import that matters resolves inside `dist/`, where upstream does commit
the generated `version.js`. `src/` is kept so the code that produced `dist/` can be read, not run.

What did **not** change: there is still no lockfile, every dependency is still a caret range, and
the first-use `npm install` still resolves whatever npm offers at that moment. The reasoning in
"Why building `dist/` in CI was rejected" therefore stands unaltered.

The open HCM decision on `EPISODIC_MEMORY_API_BASE_URL` also stands. It is still the setting that
turns a known summarisation destination into an arbitrary one, and it should still be treated as
something nobody sets without review.

### 1.4.2-hcm.1, 2026-09-04

First vendoring, at upstream `10757690`. 44 findings, all accounted for across 39 triage entries.
