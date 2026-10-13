#!/usr/bin/env python3
"""Show the error.log lines from the last game run that concern this mod.

Keeps lines that mention a file this mod ships or an HSP_ identifier,
strips timestamps, and collapses repeats with a count. Also reports whether
the mod was enabled in that run and whether the log predates the latest
edit to the mod, since either makes the log useless for checking a change.

Usage: python3 tools/mod_errors.py [--all]   (--all: don't filter to the mod)
"""
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

MOD_ROOT = Path(__file__).resolve().parent.parent
USER_DIR = Path(os.environ.get(
    "HOI4_USER_DIR",
    Path.home() / ".local/share/Paradox Interactive/Hearts of Iron IV"))
DESCRIPTOR = "mod/habsburg_spain.mod"
PREFIX = re.compile(r"^\[[^\]]*\]\[[^\]]*\]\[([^\]]*)\]:\s*")
MOD_ID = re.compile(r"\bHSP_|\bhsp_|Habsburg", re.I)


def main(argv):
    show_all = "--all" in argv
    log = USER_DIR / "logs" / "error.log"
    if not log.exists():
        print(f"no error.log at {log}; launch the game once first")
        return 1

    mod_files = [p.relative_to(MOD_ROOT).as_posix() for p in MOD_ROOT.rglob("*")
                 if p.is_file() and p.suffix in (".txt", ".yml", ".gfx", ".gui", ".mod")
                 and not {".git", "tools", ".claude"} & set(p.parts)]

    log_time = datetime.fromtimestamp(log.stat().st_mtime)
    newest = max((MOD_ROOT / f for f in mod_files), key=lambda p: p.stat().st_mtime)
    print(f"error.log written {log_time:%Y-%m-%d %H:%M}")
    if newest.stat().st_mtime > log.stat().st_mtime:
        print(f"WARNING: {newest.relative_to(MOD_ROOT)} was edited after this log; "
              "relaunch the game to test the current files")
    try:
        enabled = json.loads((USER_DIR / "dlc_load.json").read_text()).get("enabled_mods", [])
        if DESCRIPTOR not in enabled:
            print(f"WARNING: {DESCRIPTOR} was not enabled in the last launch "
                  f"(enabled: {enabled or 'none'}); this log does not reflect the mod")
    except (OSError, ValueError):
        pass

    counts, sources = Counter(), {}
    for raw in log.read_text(encoding="utf-8", errors="replace").splitlines():
        m = PREFIX.match(raw)
        msg = raw[m.end():] if m else raw
        if not show_all and not (MOD_ID.search(msg) or any(f in msg for f in mod_files)):
            continue
        counts[msg] += 1
        sources.setdefault(msg, m.group(1) if m else "")
    if not counts:
        print("no mod-related lines in error.log")
        return 0
    print(f"{len(counts)} distinct mod-related line(s):\n")
    for msg, n in counts.most_common():
        print(f"{'x' + str(n):>5}  {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
