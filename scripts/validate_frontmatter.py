#!/usr/bin/env python3
"""Validate YAML frontmatter on SKILL.md files and command .md files."""

from __future__ import annotations

import sys
from pathlib import Path

from _common import parse_frontmatter


def main() -> int:
    skill_files = sorted(Path(".").glob("plugins/*/skills/*/SKILL.md"))
    command_files = sorted(Path(".").glob("plugins/*/commands/*.md"))

    if not skill_files:
        print("FAIL: No SKILL.md files found under plugins/*/skills/*/")
        return 1

    failures = 0

    for f in skill_files:
        fm = parse_frontmatter(f)
        if fm is None:
            print(f"FAIL {f}: missing or invalid YAML frontmatter")
            failures += 1
            continue

        for key in ("name", "description"):
            if key not in fm or not fm[key]:
                print(f"FAIL {f}: missing or empty '{key}'")
                failures += 1

        name = fm.get("name")
        if isinstance(name, str) and ":" in name:
            print(f"FAIL {f}: skill name {name!r} must not contain ':'")
            failures += 1

        print(f"OK  {f}")

    for f in command_files:
        fm = parse_frontmatter(f)
        if fm is None:
            print(f"FAIL {f}: missing or invalid YAML frontmatter")
            failures += 1
            continue

        if not fm.get("description"):
            print(f"FAIL {f}: missing or empty 'description'")
            failures += 1

        print(f"OK  {f}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
