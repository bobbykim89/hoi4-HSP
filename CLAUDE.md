# Habsburg Spain (HSP) — HOI4 mod

Alt-history focus tree for Republican Spain (tag `SPR`; nationalist Spain is `SPA`) restoring a Habsburg monarchy. Every new identifier — focus, idea, decision, flag, variable, modifier, loc key — starts with `HSP_`. Events use the namespaces `HSP_spain_events` and `HSP_spain_news`.

## Where things are

- `common/national_focus/spain.txt` is a **full copy of vanilla's Spain tree** with the mod's tree appended after the `## Habsburd focus` comment (~line 13400). The mod's branches start at `\t# <name> path` / `\t# army` headers; map them with `grep -n '^\t#' common/national_focus/spain.txt`. Each mod focus is preceded by a `## <Korean name>` comment; keep that.
- Localisation: `localisation/english/hsp_*_l_english.yml`, grouped by `# <branch> focus` comments that mirror the tree.

## Vanilla overrides

A mod file with the same path as a vanilla file **replaces the vanilla file entirely**. These files do that: `common/national_focus/spain.txt`, `events/LAR_Spain.txt`, `common/scripted_effects/00_scripted_effects.txt`, `common/countries/cosmetic.txt`, `common/characters/SPR.txt`. When editing them, keep the vanilla content intact; put new content in `HSP_`-named files where possible. To see what the mod changed: `diff "$HOI4_GAME_DIR/<path>" <path>`.

The overrides were copied from game 1.14 (`descriptor.mod` says `1.14.*`), but the installed game is 1.19, so their vanilla parts are stale.

## Localisation rules

- Text is written in **Korean**, inside `l_english` files (the mod predates official Korean support).
- Files are UTF-8 **with BOM**, first line `l_english:`, entries `  KEY:0 "text"` (two-space indent). Script `.txt` files are UTF-8 without BOM. All files use LF.
- A focus needs `ID` and `ID_desc` (`""` is an acceptable placeholder). An event needs its title, desc and every option `name`.
- Inside text: `[ROOT.GetNameDef]`-style scopes, `§Y…§!` colours, `\n` newlines.

## Reference material

Before using an effect, trigger or modifier, confirm it exists in the installed game rather than writing it from memory:

- Docs: `$HOI4_GAME_DIR/documentation/{effects,triggers,modifiers,loc_objects}_documentation.md`. Each entry is a `## name` heading, so search with `grep -n -A15 '^## add_ideas$'`.
- Real usage: `grep -rn 'effect_name' "$HOI4_GAME_DIR/common" "$HOI4_GAME_DIR/events"`. Vanilla focus trees are the best templates.
- Sprites (`GFX_goal_*`, `GFX_idea_*`, `GFX_report_event_*`): defined in `$HOI4_GAME_DIR/interface/*.gfx`.

`HOI4_GAME_DIR` is set in `.claude/settings.local.json`.

## Verifying changes

- **`tools/validate_mod.py`** checks brace balance, loc file format, focus/event/sprite references, duplicate IDs and missing loc keys. A hook runs it after every edit and reports only issues the edit introduced. Run `python3 tools/validate_mod.py` for the whole mod before calling work done: the bar is **0 new issues**. Pre-existing issues live in `tools/known_issues.txt`; when you fix one, run `--write-baseline` to drop it.
- **CWTools** (VS Code extension) checks scopes and effect/trigger validity more deeply than the validator. Read its diagnostics for files you edited when the diagnostics tool is available.
- **In game** is the only real test. The user plays; afterwards the `check-errors` skill reads `error.log`.

## Known problems (don't fix unprompted; ask first)

- `events/LAR_Spain.txt` contains only `lar_spain.1`, so it deletes vanilla's other ~143 La Résistance Spain events. Vanilla focuses in `spain.txt` still fire them (they appear in `known_issues.txt`). The fix is to restore the full vanilla file and re-apply the mod's changes to `lar_spain.1`.
- The game runs in `l_korean`, but the mod only ships `l_english`, so in-game text may show raw keys. Confirm with the user before restructuring localisation.

## Git

Short lowercase commit messages (`add new focus for ...`, `fix ...`). Use one branch per feature or branch of the tree.
