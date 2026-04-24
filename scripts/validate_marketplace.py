#!/usr/bin/env python3
"""Validate .claude-plugin/marketplace.json schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_OWNER_FIELDS = {"name", "email"}
ALLOWED_OBJECT_SOURCE_TYPES = {"github", "url", "git-subdir", "npm"}


def main() -> int:
    path = Path(".claude-plugin/marketplace.json")
    if not path.exists():
        print(f"FAIL {path} does not exist")
        return 1

    mp = json.loads(path.read_text(encoding="utf-8"))

    for key in ("name", "owner", "plugins"):
        if key not in mp:
            print(f"FAIL marketplace.json missing key: {key}")
            return 1

    owner = mp["owner"]
    if not isinstance(owner, dict) or "name" not in owner:
        print("FAIL marketplace.json: 'owner' must be an object with 'name'")
        return 1
    extra = set(owner) - ALLOWED_OWNER_FIELDS
    if extra:
        print(
            f"FAIL marketplace.json: 'owner' has unexpected fields: {extra} "
            f"(allowed: {ALLOWED_OWNER_FIELDS})"
        )
        return 1

    plugins = mp["plugins"]
    if not isinstance(plugins, list) or not plugins:
        print("FAIL marketplace.json: 'plugins' must be a non-empty list")
        return 1

    seen: set[str] = set()
    for plugin in plugins:
        for key in ("name", "source"):
            if key not in plugin:
                print(f"FAIL marketplace plugin entry missing: {key}")
                return 1
        name = plugin["name"]
        if name in seen:
            print(f"FAIL duplicate plugin name: {name}")
            return 1
        seen.add(name)

        source = plugin["source"]
        if isinstance(source, str):
            if not source.startswith("./"):
                print(
                    f"FAIL plugin {name}: string 'source' must start with './', "
                    f"got {source!r}"
                )
                return 1
            plugin_dir = Path(source)
            if not plugin_dir.is_dir():
                print(f"FAIL plugin {name}: source path {source!r} does not exist")
                return 1
            pj = plugin_dir / ".claude-plugin" / "plugin.json"
            if not pj.exists():
                print(f"FAIL plugin {name}: {pj} missing")
                return 1
        elif isinstance(source, dict):
            if "source" not in source:
                print(
                    f"FAIL plugin {name}: object 'source' must have inner 'source' "
                    "discriminator"
                )
                return 1
            if source["source"] not in ALLOWED_OBJECT_SOURCE_TYPES:
                print(f"FAIL plugin {name}: unknown source type {source['source']!r}")
                return 1
        else:
            print(f"FAIL plugin {name}: 'source' must be string or object")
            return 1

        if "category" in plugin and not isinstance(plugin["category"], str):
            print(f"FAIL plugin {name}: 'category' must be a string")
            return 1

    print(f"OK marketplace.json ({len(plugins)} plugin(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
