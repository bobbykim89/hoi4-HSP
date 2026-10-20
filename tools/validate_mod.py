#!/usr/bin/env python3
"""Static checks for the Habsburg Spain HOI4 mod.

Catches the mistakes that otherwise only show up in-game or in error.log:
unbalanced braces, malformed localisation files, references to focuses /
events / sprites that don't exist, duplicate IDs, and content with no
localisation key.

Usage:
  python3 tools/validate_mod.py              # check the whole mod
  python3 tools/validate_mod.py FILE...      # report only issues in FILE(s)
  python3 tools/validate_mod.py --hook       # Claude Code PostToolUse hook mode
  python3 tools/validate_mod.py --write-baseline   # accept current issues as known

Issues listed in tools/known_issues.txt are pre-existing: they are marked
[known] in a full run and ignored by the hook, so it only reports what an
edit newly broke. Fix them over time and re-run --write-baseline.

Vanilla game files are read from $HOI4_GAME_DIR (indexed once, cached in
tools/.cache/). Vanilla files that the mod overrides (same relative path)
are excluded, since the game never loads them.
"""
import json
import os
import re
import sys
from pathlib import Path

MOD_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GAME_DIR = "/mnt/games1/SteamLibrary/steamapps/common/Hearts of Iron IV"
LANGS = ("english", "korean")  # every language the mod ships must cover every key
CACHE_FILE = MOD_ROOT / "tools" / ".cache" / "vanilla_index.json"
CACHE_VERSION = 3
BASELINE_FILE = MOD_ROOT / "tools" / "known_issues.txt"

EVENT_TYPES = ("country_event", "news_event", "state_event",
               "unit_leader_event", "operative_leader_event")
FOCUS_REF_KEYS = ("has_completed_focus", "complete_national_focus",
                  "unlock_national_focus", "uncomplete_national_focus")
LOC_LINE = re.compile(r'^\s*([\w.\-\']+):\d*\s*"(.*)"\s*(#.*)?$')


class Issue:
    def __init__(self, path, line, msg):
        self.path, self.line, self.msg = path, line, msg

    def __str__(self):
        return f"{self.path}:{self.line}: {self.msg}"

    @property
    def signature(self):  # line-independent, so edits elsewhere don't break the baseline
        return f"{self.path} | {self.msg}"


def load_baseline():
    try:
        lines = BASELINE_FILE.read_text(encoding="utf-8").splitlines()
    except OSError:
        return set()
    return {l for l in lines if l.strip() and not l.startswith("#")}


# --------------------------------------------------------------------------
# Paradox script parsing

class Node:
    __slots__ = ("key", "op", "value", "line")

    def __init__(self, key, op, value, line):
        self.key, self.op, self.value, self.line = key, op, value, line

    @property
    def is_block(self):
        return isinstance(self.value, list)

    def children(self, key=None):
        if not self.is_block:
            return []
        return [n for n in self.value if key is None or n.key == key]

    def get(self, key):
        for n in self.children(key):
            return n
        return None

    def walk(self):
        yield self
        if self.is_block:
            for c in self.value:
                yield from c.walk()


TOKEN = re.compile(r'"(?:[^"\\\n]|\\.)*"|[{}]|[<>!?]?=|[<>]|#[^\n]*|[^\s{}=<>!?"#]+|\n|\S')


def tokenize(text):
    line = 1
    for m in TOKEN.finditer(text):
        tok = m.group()
        if tok == "\n":
            line += 1
        elif not tok.startswith("#"):
            yield tok, line


def parse_script(text, rel, issues):
    """Parse into a root Node. Brace errors are appended to issues."""
    root = Node(None, None, [], 0)
    stack = [root]
    toks = list(tokenize(text.lstrip("﻿")))
    i = 0
    ops = {"=", "<", ">", "<=", ">=", "!=", "?="}
    while i < len(toks):
        tok, line = toks[i]
        cur = stack[-1].value
        if tok == "}":
            if len(stack) == 1:
                issues.append(Issue(rel, line, "unmatched '}' (extra closing brace)"))
            else:
                stack.pop()
            i += 1
            continue
        if tok == "{":  # anonymous block, e.g. inside a list
            n = Node(None, None, [], line)
            cur.append(n)
            stack.append(n)
            i += 1
            continue
        if i + 1 < len(toks) and toks[i + 1][0] in ops:
            op = toks[i + 1][0]
            if i + 2 >= len(toks):
                issues.append(Issue(rel, line, f"'{tok} {op}' has no value"))
                break
            val, vline = toks[i + 2]
            if val == "{":
                n = Node(tok.strip('"'), op, [], line)
                cur.append(n)
                stack.append(n)
            elif val == "}" or val in ops:
                issues.append(Issue(rel, line, f"'{tok} {op}' is followed by '{val}' instead of a value"))
                i += 2
                continue
            else:
                cur.append(Node(tok.strip('"'), op, val.strip('"'), line))
            i += 3
            continue
        cur.append(Node(None, None, tok.strip('"'), line))  # bare list value
        i += 1
    for n in stack[1:]:
        issues.append(Issue(rel, n.line, f"'{n.key or '{'}' block opened here is never closed"))
    return root


# --------------------------------------------------------------------------
# Vanilla index (regex-based superset, cached)

def game_dir():
    d = Path(os.environ.get("HOI4_GAME_DIR", DEFAULT_GAME_DIR))
    return d if (d / "common").is_dir() else None


def mod_relpaths():
    return {p.relative_to(MOD_ROOT).as_posix() for p in MOD_ROOT.rglob("*")
            if p.is_file() and ".git" not in p.parts and "tools" not in p.parts}


def build_vanilla_index(gdir, overridden):
    def files(sub, pattern):
        base = gdir / sub
        for p in base.rglob(pattern):
            if p.relative_to(gdir).as_posix() not in overridden:
                yield p

    def read(p):
        return p.read_text(encoding="utf-8-sig", errors="replace")

    id_re = re.compile(r'^\s*id\s*=\s*"?([\w.\-]+)', re.M)
    focuses, events, gfx = set(), set(), set()
    loc = {lang: set() for lang in LANGS}
    for p in files("common/national_focus", "*.txt"):
        focuses.update(id_re.findall(read(p)))
    for p in files("events", "*.txt"):
        events.update(id_re.findall(read(p)))
    for lang in LANGS:
        for p in files(f"localisation/{lang}", "*.yml"):
            for line in read(p).splitlines():
                m = LOC_LINE.match(line)
                if m:
                    loc[lang].add(m.group(1))
    gfx_re = re.compile(r'name\s*=\s*"?(GFX_[\w\-]+)', re.I)
    for sub in ("interface", "gfx", "dlc"):
        for p in files(sub, "*.gfx"):
            gfx.update(gfx_re.findall(read(p)))
    return {"focuses": sorted(focuses), "events": sorted(events),
            "gfx": sorted(gfx), **{f"loc_{l}": sorted(k) for l, k in loc.items()}}


def vanilla_index(overridden):
    gdir = game_dir()
    if gdir is None:
        return None
    rev_file = gdir / "hoi4_rev.txt"
    stamp = rev_file.read_text().strip() if rev_file.exists() else ""
    key = {"v": CACHE_VERSION, "game": str(gdir), "rev": stamp,
           "overridden": sorted(overridden)}
    try:
        cached = json.loads(CACHE_FILE.read_text())
        if cached.get("key") == key:
            return {k: set(v) for k, v in cached["index"].items()}
    except (OSError, ValueError):
        pass
    index = build_vanilla_index(gdir, set(overridden))
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps({"key": key, "index": index}))
    return {k: set(v) for k, v in index.items()}


# --------------------------------------------------------------------------
# Mod checks

def check_loc_file(path, rel, issues, loc_defs):
    """loc_defs: {lang: {key: "file:line"}}, filled in as files are read."""
    raw = path.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        issues.append(Issue(rel, 1, "localisation file must start with a UTF-8 BOM"))
    text = raw.decode("utf-8-sig", errors="replace")
    lang = path.parent.name
    expect_suffix = f"_l_{lang}.yml"
    if not path.name.endswith(expect_suffix):
        issues.append(Issue(rel, 1, f"filename must end with '{expect_suffix}'"))
    header_seen = False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if not header_seen:
            if s != f"l_{lang}:":
                issues.append(Issue(rel, n, f"first line must be 'l_{lang}:' (got '{s[:40]}')"))
            header_seen = True
            continue
        m = LOC_LINE.match(line)
        if not m:
            issues.append(Issue(rel, n, "malformed localisation line (expected  key:0 \"text\")"))
            continue
        if "\t" in line[:len(line) - len(line.lstrip())]:
            issues.append(Issue(rel, n, "indent with spaces, not tabs"))
        key = m.group(1)
        body = m.group(2)
        if re.search(r'(?<!\\)"', body):
            issues.append(Issue(rel, n, f"'{key}' text contains an unescaped '\"'"))
        defs = loc_defs.setdefault(lang, {})
        if key in defs:
            issues.append(Issue(rel, n, f"duplicate localisation key '{key}' (also {defs[key]})"))
        else:
            defs[key] = f"{rel}:{n}"


def scalar_or_text(node):
    """title = key  |  title = { text = key trigger = {...} }"""
    if node is None:
        return []
    if not node.is_block:
        return [(node.value, node.line)]
    return [(t.value, t.line) for t in node.children("text") if not t.is_block]


def main(argv):
    hook = "--hook" in argv
    targets = [a for a in argv if not a.startswith("--")]
    if hook:
        try:
            payload = json.load(sys.stdin)
        except ValueError:
            return 0
        fp = (payload.get("tool_input") or {}).get("file_path") or ""
        targets = [fp]
    target_rel = set()
    for t in targets:
        p = Path(t).resolve()
        try:
            rel = p.relative_to(MOD_ROOT).as_posix()
        except ValueError:
            continue
        if p.suffix in (".txt", ".yml") and not rel.startswith(("tools/", ".claude/")):
            target_rel.add(rel)
    if (hook or targets) and not target_rel:
        return 0  # nothing we validate

    issues = []
    rels = mod_relpaths()
    vanilla = vanilla_index(rels)

    # Parse everything (the mod is small; cross-references need all of it).
    trees = {}
    for rel in sorted(rels):
        if rel.endswith(".txt") and (rel.startswith("common/") or rel.startswith("events/")):
            text = (MOD_ROOT / rel).read_text(encoding="utf-8-sig", errors="replace")
            trees[rel] = parse_script(text, rel, issues)
    loc_defs = {}
    for rel in sorted(rels):
        if rel.startswith("localisation/") and rel.endswith(".yml"):
            check_loc_file(MOD_ROOT / rel, rel, issues, loc_defs)

    # Collect definitions.
    focus_defs, event_defs, namespaces = {}, {}, set()
    focus_pos = {}  # tree id -> {focus id: (x, y, relative_position_id, rel, line)}
    needs_loc = []  # (key, rel, line, what)
    gfx_refs = []   # (sprite, rel, line)
    for rel, root in trees.items():
        if rel.startswith("common/national_focus/"):
            for tree in root.children("focus_tree"):
                tid = tree.get("id")
                tpos = focus_pos.setdefault(tid.value if tid is not None else rel, {})
                for f in tree.children("focus"):
                    fid, x, y = f.get("id"), f.get("x"), f.get("y")
                    if fid is None or x is None or y is None or fid.is_block:
                        continue
                    rp = f.get("relative_position_id")
                    try:
                        tpos[fid.value] = (int(x.value), int(y.value), rp.value if rp else None, rel, fid.line)
                    except ValueError:
                        pass  # computed position; skip layout check
            for n in root.walk():
                if n.key in ("focus", "shared_focus") and n.is_block:
                    fid = n.get("id")
                    if fid is None or fid.is_block:
                        issues.append(Issue(rel, n.line, "focus has no id"))
                        continue
                    if fid.value in focus_defs:
                        issues.append(Issue(rel, fid.line, f"duplicate focus id '{fid.value}' (also {focus_defs[fid.value]})"))
                    focus_defs[fid.value] = f"{rel}:{fid.line}"
                    text = n.get("text")
                    lk = text.value if text is not None and not text.is_block else fid.value
                    needs_loc.append((lk, rel, fid.line, "focus name"))
                    if text is None:
                        needs_loc.append((lk + "_desc", rel, fid.line, "focus description"))
                    for icon in n.children("icon"):
                        for v, ln in ([(icon.value, icon.line)] if not icon.is_block
                                      else [(c.value, c.line) for c in icon.children("value") if not c.is_block]):
                            gfx_refs.append((v, rel, ln))
        if rel.startswith("events/"):
            for n in root.children():
                if n.key == "add_namespace" and not n.is_block:
                    namespaces.add(n.value)
                if n.key in EVENT_TYPES and n.is_block:
                    eid = n.get("id")
                    if eid is None or eid.is_block:
                        issues.append(Issue(rel, n.line, "event has no id"))
                        continue
                    ns = eid.value.split(".")[0]
                    if ns not in namespaces:
                        issues.append(Issue(rel, eid.line, f"event namespace '{ns}' is not declared with add_namespace in this file"))
                    if eid.value in event_defs:
                        issues.append(Issue(rel, eid.line, f"duplicate event id '{eid.value}' (also {event_defs[eid.value]})"))
                    event_defs[eid.value] = f"{rel}:{eid.line}"
                    hidden = n.get("hidden")
                    if hidden is not None and hidden.value == "yes":
                        continue
                    for k in ("title", "desc"):
                        for node in n.children(k):
                            for v, ln in scalar_or_text(node):
                                needs_loc.append((v, rel, ln, f"event {k}"))
                    for opt in n.children("option"):
                        for nm in opt.children("name"):
                            if not nm.is_block:
                                needs_loc.append((nm.value, rel, nm.line, "event option"))
                    pic = n.get("picture")
                    if pic is not None and not pic.is_block:
                        gfx_refs.append((pic.value, rel, pic.line))
        if rel.startswith("common/ideas/"):
            for ideas in root.children("ideas"):
                for cat in ideas.children():
                    for idea in cat.children():
                        if idea.is_block and idea.key:
                            nm = idea.get("name")
                            needs_loc.append((nm.value if nm and not nm.is_block else idea.key, rel, idea.line, "idea"))
        if rel.startswith("common/decisions/"):
            what = "decision category" if "/categories/" in rel else "decision"
            for top in root.children():
                if not (top.is_block and top.key):
                    continue
                if what == "decision category":
                    needs_loc.append((top.key, rel, top.line, what))
                else:
                    for d in top.children():
                        if d.is_block and d.key:
                            needs_loc.append((d.key, rel, d.line, what))
        if rel.startswith("common/dynamic_modifiers/"):
            for top in root.children():
                if top.is_block and top.key:
                    needs_loc.append((top.key, rel, top.line, "dynamic modifier"))
        if rel.startswith("common/opinion_modifiers/"):
            for om in root.children("opinion_modifiers"):
                for m in om.children():
                    if m.is_block and m.key:
                        needs_loc.append((m.key, rel, m.line, "opinion modifier"))

    # Layout: resolve relative positions and flag focuses that sit on the same tile.
    for tpos in focus_pos.values():
        absolute = {}

        def resolve(fid, seen=()):
            if fid in absolute:
                return absolute[fid]
            x, y, rp, rel, line = tpos[fid]
            if rp:
                if rp not in tpos or rp in seen:
                    return None
                base = resolve(rp, seen + (fid,))
                if base is None:
                    return None
                x, y = x + base[0], y + base[1]
            absolute[fid] = (x, y)
            return absolute[fid]

        tiles = {}
        for fid in tpos:
            xy = resolve(fid)
            if xy is not None:
                tiles.setdefault(xy, []).append(fid)
        for (x, y), fids in tiles.items():
            for fid in fids[1:]:
                _, _, _, rel, line = tpos[fid]
                issues.append(Issue(rel, line, f"focus '{fid}' overlaps '{fids[0]}' at x={x} y={y}"))

        # Focus icons are wider than one grid step: neighbours on a row need two columns between them.
        for (x, y), fids in tiles.items():
            if (x + 1, y) in tiles:
                _, _, _, rel, line = tpos[tiles[(x + 1, y)][0]]
                issues.append(Issue(rel, line, f"focus '{tiles[(x + 1, y)][0]}' is one column from '{fids[0]}' at y={y}; the icons overlap"))

        # The game places focuses in file order: a relative_position_id pointing at a focus defined
        # further down is not resolved yet, and the focus lands near the tree origin on top of others.
        order = {fid: i for i, fid in enumerate(tpos)}
        for fid, (_, _, rp, rel, line) in tpos.items():
            if rp in order and order[rp] > order[fid]:
                issues.append(Issue(rel, line, f"focus '{fid}' is placed relative to '{rp}', which is defined later in the file"))

    known_focus = set(focus_defs) | (vanilla["focuses"] if vanilla else set())
    known_event = set(event_defs) | (vanilla["events"] if vanilla else set())
    mod_langs = [l for l in LANGS if l in loc_defs]
    known_loc = {l: set(loc_defs[l]) | (vanilla[f"loc_{l}"] if vanilla else set()) for l in mod_langs}
    known_gfx = None
    if vanilla:
        mod_gfx = set()
        for gp in MOD_ROOT.glob("interface/**/*.gfx"):
            mod_gfx.update(re.findall(r'name\s*=\s*"?(GFX_[\w\-]+)', gp.read_text(encoding="utf-8-sig", errors="replace"), re.I))
        known_gfx = vanilla["gfx"] | mod_gfx

    # Cross-references.
    for rel, root in trees.items():
        in_focus_file = rel.startswith("common/national_focus/")
        for n in root.walk():
            if in_focus_file and n.key in ("prerequisite", "mutually_exclusive") and n.is_block:
                for f in n.children("focus"):
                    if not f.is_block and f.value not in known_focus:
                        issues.append(Issue(rel, f.line, f"{n.key} references unknown focus '{f.value}'"))
            if in_focus_file and n.key == "relative_position_id" and not n.is_block:
                if n.value not in known_focus:
                    issues.append(Issue(rel, n.line, f"relative_position_id references unknown focus '{n.value}'"))
            if n.key in FOCUS_REF_KEYS and not n.is_block:
                if n.value not in known_focus and not n.value.startswith(("var:", "[")):
                    issues.append(Issue(rel, n.line, f"{n.key} references unknown focus '{n.value}'"))
            if n.key in EVENT_TYPES:
                if rel.startswith("events/") and n in root.value:
                    continue  # the event definition itself
                ref = n.value if not n.is_block else (n.get("id").value if n.get("id") and not n.get("id").is_block else None)
                if ref and "." in ref and ref not in known_event:
                    issues.append(Issue(rel, n.line, f"fires unknown event '{ref}'"))

    if vanilla is not None:
        for key, rel, line, what in needs_loc:
            missing = [l for l in mod_langs if key not in known_loc[l]]
            if missing:
                issues.append(Issue(rel, line, f"{what} '{key}' has no localisation ({', '.join(missing)})"))
        # Every key the mod defines in one language needs the other languages too.
        for lang in mod_langs:
            for key, where in loc_defs[lang].items():
                for other in mod_langs:
                    if other != lang and key not in known_loc[other]:
                        rel, line = where.rsplit(":", 1)
                        issues.append(Issue(rel, int(line), f"'{key}' has no {other} translation"))
        for sprite, rel, line in gfx_refs:
            if sprite.startswith("GFX_") and sprite not in known_gfx:
                issues.append(Issue(rel, line, f"sprite '{sprite}' is not defined in any .gfx file"))

    if "--write-baseline" in argv:
        sigs = sorted({i.signature for i in issues})
        BASELINE_FILE.write_text(
            "# Pre-existing issues accepted by `validate_mod.py --write-baseline`.\n"
            "# The hook ignores these; a full run marks them [known]. Delete lines as you fix them.\n"
            + "".join(s + "\n" for s in sigs), encoding="utf-8")
        print(f"wrote {len(sigs)} known issue(s) to {BASELINE_FILE.relative_to(MOD_ROOT)}")
        return 0

    if target_rel:
        issues = [i for i in issues if i.path in target_rel]
    issues.sort(key=lambda i: (i.path, i.line))
    known = load_baseline()
    new = [i for i in issues if i.signature not in known]

    if hook:
        if new:
            print(f"validate_mod.py: your edit introduced {len(new)} issue(s):", file=sys.stderr)
            for i in new:
                print(i, file=sys.stderr)
            return 2
        return 0

    if vanilla is None:
        print("note: game dir not found (set HOI4_GAME_DIR); skipped vanilla-dependent checks")
    for i in issues:
        print(("[known] " if i.signature in known else "") + str(i))
    scope = ", ".join(sorted(target_rel)) if target_rel else "whole mod"
    stale = known - {i.signature for i in issues} if not target_rel else set()
    print(f"{len(new)} new issue(s), {len(issues) - len(new)} known ({scope})")
    if stale:
        print(f"{len(stale)} known issue(s) no longer occur; run --write-baseline to drop them")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
