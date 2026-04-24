#!/usr/bin/env python3
"""Verify SKILL.md `references/*.md` links resolve to existing files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REF_RE = re.compile(r"`?references/([A-Za-z0-9_\-./]+\.md)`?")


def main() -> int:
    failures = 0
    scanned = 0
    for skill in sorted(Path(".").glob("plugins/*/skills/*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        skill_dir = skill.parent
        for match in sorted(set(REF_RE.findall(text))):
            target = skill_dir / "references" / match
            if not target.exists():
                print(f"FAIL {skill}: references/{match} does not exist")
                failures += 1
            else:
                scanned += 1
    print(f"OK verified {scanned} references/*.md link(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
