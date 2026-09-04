#!/usr/bin/env python3
"""Self-check for triage.py. Run: python .github/scripts/test_triage.py

No framework. Every case asserts the adjudicator's exit code, including the
cases that must FAIL - a gate nobody has watched reject something is not a gate.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRIAGE = HERE / "triage.py"


def finding(rule_id, path, text, severity="HIGH", line=1):
    return {
        "id": rule_id,
        "severity": severity,
        "finding": text,
        "code_snippet": text,
        "pattern": rule_id,
        "location": {"file": path, "start_line": line},
    }


def run(findings, entries, *, complete=True, uninspected=0):
    """Adjudicate an in-memory scan report and triage record; return exit code."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        report = {
            "issues": findings,
            "execution_successful": complete,
            "analysis_completeness": {"entirely_uninspected_files": uninspected},
        }
        rp = td / "scan.json"
        rp.write_text(json.dumps(report), encoding="utf-8")
        argv = [sys.executable, str(TRIAGE), str(td / "plugin"), str(rp)]
        if entries is not None:
            tp = td / "triage.yaml"
            lines = ["entries:"]
            for e in entries:
                lines.append("  - " + "\n    ".join(f"{k}: {json.dumps(v)}" for k, v in e.items()))
            tp.write_text("\n".join(lines) + "\n", encoding="utf-8")
            argv.append(str(tp))
        return subprocess.run(argv, capture_output=True, text=True)


OK = lambda r: r.returncode == 0
FAIL = lambda r: r.returncode == 1
ERR = lambda r: r.returncode == 2

CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


@case("clean scan, no triage file -> pass")
def _():
    assert OK(run([], None))


@case("finding with no triage entry -> FAIL (unaccounted)")
def _():
    r = run([finding("RA2", "src/a.js", "pList")], None)
    assert FAIL(r) and "unaccounted finding RA2" in r.stdout, r.stdout


@case("code finding with a per-finding entry -> pass")
def _():
    r = run([finding("RA2", "src/a.js", "pList")],
            [{"rule_id": "RA2", "file": "src/a.js", "matched": "pList",
              "reason": "Identifier fragment.", "verified_by": "Reviewer"}])
    assert OK(r), r.stdout


@case("code finding covered ONLY by a class entry -> FAIL")
def _():
    r = run([finding("RA2", "src/a.js", "pList")],
            [{"rule_id": "RA2", "files": "src/**", "reason": "Prose.", "verified_by": "Reviewer"}])
    assert FAIL(r) and "covered\nonly by a class entry" in r.stdout.replace(" \n", "\n") \
        or "only by a class entry" in r.stdout, r.stdout


@case("inert finding covered by a class entry -> pass")
def _():
    r = run([finding("P9", "docs/x.md", "whitespace")],
            [{"rule_id": "P9", "files": "docs/**", "reason": "Markdown tables.",
              "verified_by": "Reviewer"}])
    assert OK(r), r.stdout


@case("stale entry matching nothing -> FAIL")
def _():
    r = run([], [{"rule_id": "P9", "files": "docs/**", "reason": "Nothing here.",
                  "verified_by": "Reviewer"}])
    assert FAIL(r) and "accounts for no finding" in r.stdout, r.stdout


@case("entry missing verified_by -> FAIL")
def _():
    r = run([finding("RA2", "src/a.js", "pList")],
            [{"rule_id": "RA2", "file": "src/a.js", "matched": "pList", "reason": "x"}])
    assert FAIL(r) and "missing 'verified_by'" in r.stdout, r.stdout


@case("per-finding entry missing matched -> FAIL")
def _():
    r = run([finding("RA2", "src/a.js", "pList")],
            [{"rule_id": "RA2", "file": "src/a.js", "reason": "x", "verified_by": "R"}])
    assert FAIL(r) and "need 'matched'" in r.stdout, r.stdout


@case("entry with both file and files -> FAIL")
def _():
    r = run([finding("RA2", "src/a.js", "pList")],
            [{"rule_id": "RA2", "file": "src/a.js", "files": "src/**", "matched": "pList",
              "reason": "x", "verified_by": "R"}])
    assert FAIL(r) and "exactly one of" in r.stdout, r.stdout


@case("matched string absent from the finding -> FAIL (entry cannot claim it)")
def _():
    r = run([finding("RA2", "src/a.js", "pList")],
            [{"rule_id": "RA2", "file": "src/a.js", "matched": "somethingElse",
              "reason": "x", "verified_by": "R"}])
    assert FAIL(r), r.stdout


@case("single * does not cross a directory separator")
def _():
    r = run([finding("P9", "docs/deep/x.md", "w")],
            [{"rule_id": "P9", "files": "docs/*.md", "reason": "x", "verified_by": "R"}])
    assert FAIL(r), r.stdout


@case("** does cross directory separators")
def _():
    r = run([finding("P9", "docs/deep/x.md", "w")],
            [{"rule_id": "P9", "files": "docs/**/*.md", "reason": "x", "verified_by": "R"}])
    assert OK(r), r.stdout


@case("incomplete scan -> ERROR, never adjudicated")
def _():
    assert ERR(run([], None, complete=False))


@case("scan with uninspected files -> ERROR, never adjudicated")
def _():
    assert ERR(run([], None, uninspected=3))


def main() -> int:
    failed = 0
    for name, fn in CASES:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as exc:
            print(f"  FAIL  {name}\n        {exc}")
            failed += 1
    print(f"\n{len(CASES) - failed}/{len(CASES)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
