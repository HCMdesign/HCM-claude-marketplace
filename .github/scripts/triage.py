#!/usr/bin/env python3
"""Adjudicate SkillSpector findings against HCM's triage records.

SkillSpector provides evidence. HCM owns the verdict.

The scanner's exit code is deliberately NOT the gate. It blocks above risk 50,
where three HIGH findings - which can be three string matches on prose - reject
a plugin outright. Its own `baseline` command cannot enumerate all the findings
`scan` reports, so its suppression mechanism cannot be driven to completion.

The rule here instead: EVERY finding must be accounted for by a triage entry.
Nothing is waived by a score, a threshold, or an opaque hash.

Usage:  triage.py <plugin-dir> <scan-report.json> [triage-file.yaml]
Exit:   0 pass, 1 unaccounted/stale/under-evidenced, 2 could not adjudicate
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("::error::PyYAML is required to adjudicate triage records.")
    sys.exit(2)

# Content that cannot execute. Only these may be covered by a class entry;
# anything else needs a per-finding entry naming the literal string matched.
# An allowlist, not a blocklist: unusual or extensionless files fail closed.
INERT_SUFFIXES = (
    ".md", ".markdown", ".txt", ".rst", ".csv", ".json", ".yaml", ".yml",
)


def is_inert(path: str) -> bool:
    return path.lower().endswith(INERT_SUFFIXES)


def glob_to_regex(pattern: str) -> re.Pattern[str]:
    """Translate a path glob to a regex.

    `**` crosses directory separators, `*` does not, `?` is one non-separator
    character. Written out rather than using fnmatch, whose `*` matches `/` and
    would silently make every pattern broader than it reads.
    """
    out = ["^"]
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif c == "*":
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(c))
            i += 1
    out.append("$")
    return re.compile("".join(out))


class Entry:
    """One triage record, and how many findings it accounted for."""

    def __init__(self, raw: dict, index: int):
        self.raw = raw
        self.index = index
        self.rule_id = str(raw.get("rule_id") or "").strip()
        self.file = str(raw.get("file") or "").strip()
        self.files = str(raw.get("files") or "").strip()
        self.matched = str(raw.get("matched") or "").strip()
        self.reason = str(raw.get("reason") or "").strip()
        self.verified_by = str(raw.get("verified_by") or "").strip()
        self.hits = 0
        self._files_re = glob_to_regex(self.files) if self.files else None

    @property
    def is_class(self) -> bool:
        """A class entry covers a rule across a path glob, not one finding."""
        return bool(self.files)

    @property
    def label(self) -> str:
        return f"entry #{self.index} ({self.rule_id} {self.file or self.files})"

    def structural_errors(self) -> list[str]:
        errs = []
        if not self.rule_id:
            errs.append("missing 'rule_id'")
        if bool(self.file) == bool(self.files):
            errs.append("needs exactly one of 'file' (per-finding) or 'files' (class glob)")
        if not self.reason:
            errs.append("missing 'reason'")
        if not self.verified_by:
            errs.append("missing 'verified_by'")
        if not self.is_class and not self.matched:
            errs.append("per-finding entries need 'matched' - the literal string the scanner matched")
        return errs

    def covers(self, rule_id: str, path: str, found_text: str) -> bool:
        if rule_id != self.rule_id:
            return False
        if self.is_class:
            return bool(self._files_re and self._files_re.match(path))
        if path != self.file:
            return False
        # `matched` must actually appear in what the scanner reported, so an
        # entry cannot claim to cover a finding it does not describe.
        return self.matched in found_text


def load_findings(report_path: Path) -> list[dict]:
    with report_path.open(encoding="utf-8") as fh:
        report = json.load(fh)
    if not report.get("execution_successful", True):
        print(f"::error::{report_path}: the scan did not complete. "
              f"An incomplete scan is not evidence of anything.")
        sys.exit(2)
    completeness = report.get("analysis_completeness") or {}
    if completeness.get("entirely_uninspected_files"):
        print(f"::error::{report_path}: "
              f"{completeness['entirely_uninspected_files']} file(s) were never inspected. "
              f"Refusing to adjudicate a partial scan.")
        sys.exit(2)
    return report.get("issues") or []


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("::error::usage: triage.py <plugin-dir> <scan-report.json> [triage-file.yaml]")
        return 2

    plugin_dir, report_path = argv[1], Path(argv[2])
    triage_path = Path(argv[3]) if len(argv) > 3 else None
    name = Path(plugin_dir).name

    findings = load_findings(report_path)

    entries: list[Entry] = []
    if triage_path and triage_path.exists():
        with triage_path.open(encoding="utf-8") as fh:
            doc = yaml.safe_load(fh) or {}
        raw_entries = doc.get("entries")
        if raw_entries is None:
            raw_entries = []
        if not isinstance(raw_entries, list):
            print(f"::error file={triage_path}::'entries' must be a list.")
            return 2
        entries = [Entry(r, i + 1) for i, r in enumerate(raw_entries) if isinstance(r, dict)]

    failed = False

    # Structural validity first: a malformed record cannot be reasoned about.
    for entry in entries:
        for err in entry.structural_errors():
            print(f"::error file={triage_path}::{entry.label}: {err}")
            failed = True
    if failed:
        return 1

    unaccounted = []
    for finding in findings:
        loc = finding.get("location") or {}
        path = loc.get("file") or ""
        rule_id = finding.get("id") or ""
        found_text = " ".join(
            str(finding.get(k) or "") for k in ("finding", "code_snippet", "pattern")
        )
        covering = [e for e in entries if e.covers(rule_id, path, found_text)]

        if not covering:
            unaccounted.append((rule_id, path, loc.get("start_line"),
                                finding.get("severity"), str(finding.get("finding") or "")[:80]))
            continue

        # Executable content is never waived wholesale. A class entry may cover
        # prose; code needs someone to name the literal string and sign for it.
        if not is_inert(path) and all(e.is_class for e in covering):
            print(f"::error file={triage_path}::{rule_id} on executable file '{path}' is covered "
                  f"only by a class entry. Code needs a per-finding entry with 'matched' and "
                  f"'verified_by' - see triage/README.md.")
            failed = True

        for e in covering:
            e.hits += 1

    for rule_id, path, line, severity, text in unaccounted:
        where = f"{path}:{line}" if line else path
        print(f"::error::{name}: unaccounted finding {rule_id} [{severity}] at {where} "
              f"- matched {text!r}. Every finding must have a triage entry, or the plugin "
              f"does not ship.")
        failed = True

    # A record that matches nothing means the content moved underneath it.
    # Left alone these accumulate and quietly widen over time.
    for entry in entries:
        if entry.hits == 0:
            print(f"::error file={triage_path}::{entry.label} accounts for no finding. "
                  f"Either the content changed and it must be re-verified, or it was never "
                  f"accurate. Stale triage records are not left in place.")
            failed = True

    accounted = len(findings) - len(unaccounted)
    print(f"{name}: {len(findings)} finding(s), {accounted} accounted for, "
          f"{len(unaccounted)} unaccounted, {len(entries)} triage entr(y/ies)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
