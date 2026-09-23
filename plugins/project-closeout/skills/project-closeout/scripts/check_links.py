#!/usr/bin/env python3
"""Check that every relative markdown link in a doc set resolves.

Dead links are the most common defect in a doc set that was otherwise written carefully,
because paths move after the writing and nobody re-reads their own links.

Usage:
    python check_links.py <path>              # a directory (walked) or a single .md file
    python check_links.py <path> --wiki       # also flag Obsidian [[wiki-links]]

Exit codes:
    0  every link resolved
    1  at least one dead link (or, with --wiki, at least one wiki-link)
    2  the path does not exist

Checked:   relative links to files and directories, with #anchors and %20 escapes handled.
Skipped:   http(s), mailto, tel, and bare #anchors - those need a different kind of check.
"""

import argparse
import re
import sys
import urllib.parse
from pathlib import Path

# [text](target) but not ![image](target) handled the same way - images are links too here.
LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
WIKI = re.compile(r'\[\[([^\]]+)\]\]')
# Inline code spans, including ``double-backtick`` runs. Documentation about documentation
# routinely shows `[text](path.md)` as an example; those are illustrations, not links, and
# reporting them as dead is noise that trains people to ignore this tool.
CODE_SPAN = re.compile(r'(`+)(?:(?!\1).)*?\1', re.DOTALL)
SKIP_PREFIXES = ('http://', 'https://', 'mailto:', 'tel:', '#', 'data:')


def strip_code(line: str) -> str:
    return CODE_SPAN.sub('', line)


def targets(markdown: str):
    """Yield every link target in the text, ignoring fenced blocks and inline code."""
    in_fence = False
    for lineno, line in enumerate(markdown.splitlines(), 1):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in LINK.finditer(strip_code(line)):
            yield lineno, m.group(1).strip()


def resolve(target: str, source: Path) -> tuple[bool, str]:
    """Return (ok, detail) for one link target relative to the file containing it."""
    if target.startswith(SKIP_PREFIXES):
        return True, 'skipped'

    # Strip the anchor; we verify the file exists, not the heading within it.
    path_part = target.split('#', 1)[0]
    if not path_part:
        return True, 'skipped'

    # Links are URL-encoded on disk-bearing paths: "My%20Doc.md" is "My Doc.md".
    decoded = urllib.parse.unquote(path_part)
    candidate = (source.parent / decoded).resolve()
    if candidate.exists():
        return True, 'ok'
    return False, str(candidate)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('path', help='directory to walk, or a single markdown file')
    ap.add_argument('--wiki', action='store_true',
                    help='also flag [[wiki-links]], which render as dead text in most repo web UIs')
    args = ap.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f'error: {root} does not exist', file=sys.stderr)
        return 2

    files = [root] if root.is_file() else sorted(root.rglob('*.md'))
    if not files:
        print(f'No markdown files found under {root}')
        return 0

    dead, wiki_hits, checked = [], [], 0

    for f in files:
        try:
            text = f.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            text = f.read_text(encoding='utf-8', errors='replace')
            print(f'warning: {f} is not valid UTF-8; checked with replacements')

        for lineno, target in targets(text):
            ok, detail = resolve(target, f)
            if detail != 'skipped':
                checked += 1
            if not ok:
                dead.append((f, lineno, target, detail))

        if args.wiki:
            in_fence = False
            for lineno, line in enumerate(text.splitlines(), 1):
                if line.lstrip().startswith('```'):
                    in_fence = not in_fence
                    continue
                if not in_fence:
                    for m in WIKI.finditer(strip_code(line)):
                        wiki_hits.append((f, lineno, m.group(1)))

    print(f'Scanned {len(files)} file(s), checked {checked} relative link(s).')

    if dead:
        print(f'\n{len(dead)} DEAD LINK(S):\n')
        for f, lineno, target, resolved_to in dead:
            print(f'  {f}:{lineno}')
            print(f'    link:     {target}')
            print(f'    resolves: {resolved_to}')
            print()

    if wiki_hits:
        print(f'{len(wiki_hits)} WIKI-LINK(S) - these render as dead text in most repo web UIs:\n')
        for f, lineno, inner in wiki_hits:
            print(f'  {f}:{lineno}  [[{inner}]]')
        print()

    if not dead and not wiki_hits:
        print('All links resolve.')
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
