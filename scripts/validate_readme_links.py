#!/usr/bin/env python3
"""Verify relative links in the root README.md resolve to existing files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\]\(([^)#]+)\)")


def main() -> int:
    readme = Path("README.md")
    if not readme.exists():
        print("No README.md at repo root; skipping")
        return 0

    bad: list[str] = []
    for target in LINK_RE.findall(readme.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if not Path(target).exists():
            bad.append(target)

    if bad:
        print("FAIL README references files that do not exist:")
        for b in bad:
            print(f"  - {b}")
        return 1

    print("OK all README relative links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
