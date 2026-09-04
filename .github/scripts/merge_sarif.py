#!/usr/bin/env python3
"""Merge per-plugin SARIF reports into one repo-relative run.

Two problems this solves, both found by watching the upload fail:

1. Code scanning refuses multiple SARIF runs sharing a category, so one file per
   plugin stops working the moment the catalog has a second plugin.
2. SkillSpector writes artifact URIs relative to the directory it scanned -
   "dist/mcp-server.js", not "plugins/episodic-memory/dist/mcp-server.js". Left
   alone, every annotation lands on the wrong path or nowhere. That was already
   true with one plugin; nobody had checked.

Results are merged into a single run and each URI is prefixed with the plugin
directory the report came from. Rules are unioned by id, and `ruleIndex` is
dropped: it points into a per-run rules array that no longer exists, and SARIF
permits a result to reference its rule by `ruleId` alone.

Usage: merge_sarif.py <sarif-dir> <output-file>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("::error::usage: merge_sarif.py <sarif-dir> <output-file>")
        return 2

    sarif_dir, out_path = Path(argv[1]), Path(argv[2])
    files = sorted(p for p in sarif_dir.glob("*.sarif") if p.resolve() != out_path.resolve())
    if not files:
        print(f"No SARIF reports in {sarif_dir}; nothing to merge.")
        return 0

    driver: dict | None = None
    rules_by_id: dict[str, dict] = {}
    merged: list[dict] = []

    for path in files:
        plugin = path.stem                       # sarif/<plugin>.sarif
        prefix = f"plugins/{plugin}/"
        with path.open(encoding="utf-8") as fh:
            doc = json.load(fh)

        # Upload only findings nobody accounted for. Adjudicated ones are a
        # recorded decision, not an open alert; leaving them in code scanning
        # would bury the ones that matter.
        keep: set | None = None
        una = Path("reports") / f"{plugin}.unaccounted.json"
        if una.exists():
            with una.open(encoding="utf-8") as fh:
                keep = {(e["rule_id"], e["file"], e.get("line")) for e in json.load(fh)}
            print(f"  {plugin}: {len(keep)} unaccounted finding(s) will be uploaded")

        for run in doc.get("runs") or []:
            drv = (run.get("tool") or {}).get("driver") or {}
            if driver is None:
                driver = {k: v for k, v in drv.items() if k != "rules"}
            for rule in drv.get("rules") or []:
                rid = rule.get("id")
                if rid and rid not in rules_by_id:
                    rules_by_id[rid] = rule

            for result in run.get("results") or []:
                if keep is not None:
                    loc0 = (result.get("locations") or [{}])[0].get("physicalLocation") or {}
                    uri = (loc0.get("artifactLocation") or {}).get("uri") or ""
                    line = (loc0.get("region") or {}).get("startLine")
                    if (result.get("ruleId"), uri, line) not in keep:
                        continue
                # ruleIndex points into this run's rules array, which does not
                # survive the merge. ruleId is what identifies the rule.
                result.pop("ruleIndex", None)
                for loc in result.get("locations") or []:
                    art = (loc.get("physicalLocation") or {}).get("artifactLocation")
                    if art and "uri" in art and not art["uri"].startswith(prefix):
                        art["uri"] = prefix + art["uri"].lstrip("./")
                merged.append(result)

        print(f"  {path.name}: {len(doc.get('runs') or [])} run(s) -> prefixed with {prefix}")

    if driver is None:
        driver = {"name": "skillspector"}
    driver["rules"] = list(rules_by_id.values())

    combined = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{"tool": {"driver": driver}, "results": merged}],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(combined, fh, indent=2)

    print(f"Merged {len(files)} report(s) into {out_path}: "
          f"1 run, {len(merged)} result(s), {len(rules_by_id)} rule(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
