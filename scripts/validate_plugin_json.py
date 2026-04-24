#!/usr/bin/env python3
"""Validate every plugins/*/.claude-plugin/plugin.json in the monorepo."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    failures = 0
    files = sorted(Path(".").glob("plugins/*/.claude-plugin/plugin.json"))
    if not files:
        print("No plugins/*/.claude-plugin/plugin.json files found")
        return 0

    for pj in files:
        try:
            meta = json.loads(pj.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"FAIL {pj}: invalid JSON ({exc})")
            failures += 1
            continue

        for key in ("name", "version", "description"):
            if key not in meta:
                print(f"FAIL {pj}: missing {key}")
                failures += 1

        name = meta.get("name", "")
        if ":" in name:
            print(f"FAIL {pj}: name must not contain ':'")
            failures += 1

        author = meta.get("author")
        if not isinstance(author, dict) or "name" not in author:
            print(f"FAIL {pj}: 'author' must be an object with 'name'")
            failures += 1

        print(f"OK  {pj} name={name} v={meta.get('version')}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
