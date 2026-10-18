"""Read-only artifact triage for the Web reverse-engineering profile."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections.abc import Iterator

PROFILE = 'web'
MATCHED_SUFFIXES = frozenset(['.css', '.htm', '.html', '.js', '.map', '.mjs', '.wasm'])


def matches(path: Path) -> bool:
    """Return whether a path's final extension is useful to this profile."""
    return path.suffix.lower() in MATCHED_SUFFIXES


def scan(root: Path) -> Iterator[Path]:
    """Yield matching files under root without opening or executing them."""
    for path in sorted(root.rglob("*")):
        if path.is_file() and matches(path):
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="directory containing local artifacts")
    parser.add_argument("--relative-to", type=Path, help="emit paths relative to this directory")
    args = parser.parse_args()
    base = args.relative_to or args.root
    for path in scan(args.root):
        try:
            display = path.relative_to(base)
        except ValueError:
            display = path
        print(json.dumps({"profile": PROFILE, "path": str(display), "suffix": path.suffix.lower()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
