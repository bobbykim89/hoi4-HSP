# Habsburg Spain (HSP) — HOI4 mod

Alt-history focus tree for Republican Spain (tag `SPR`; nationalist Spain is `SPA`) restoring a Habsburg monarchy. Every new identifier — focus, idea, decision, flag, variable, modifier, loc key — starts with `HSP_`. Events use the namespaces `HSP_spain_events` and `HSP_spain_news`.

## Where things are

- `common/national_focus/HSP_spain.txt` is the mod's own tree, `HSP_spanish_focus`. SPR gets it on the 1936 start, replacing vanilla's `spanish_focus`; the 1939 start keeps vanilla. Branches start at `\t# <name> path` / `\t# army` headers; map them with `grep -n '^\t#' common/national_focus/HSP_spain.txt`. Each focus is preceded by a `## <Korean name>` comment; keep that.
- **Three roots at the start, one per path.** Each path's civil war keeps the player on the HSP tree; nothing hands Spain to vanilla's tree any more.
  - `HSP_assemble_emergency_council`: the monarchy. It cancels the election, so there is no civil war.
  - `HSP_defend_the_republic`: the Republic. The election starts a 180-day fascist plot (`HSP_fascist_plot_mission`), dealt with by decisions or by civil war, then Democracy, Communism or Anarchism.
  - `HSP_national_movement`: the Fascists. The election starts a 180-day countdown (`HSP_nationalist_plot_mission`) to the uprising, then Nationalist or Falange.
  - If no root is taken before the 16 Feb 1936 election, `lar_spain.1` picks one: option a the Republic, b the Fascists, c the monarchy.
- The civil wars are `start_civil_war` calls in `common/scripted_effects/HSP_scripted_effects.txt` (`HSP_start_fascist_uprising`, `HSP_start_nationalist_uprising`, `HSP_start_anarchist_revolution`), not vanilla's `lar_spain.2`. Their outcomes are set in `on_civil_war_end` (`common/on_actions/HSP_on_actions.txt`). Pass `keep_all_characters = yes`: by default the game hands the rebels a share of Spain's characters.
- At game start, `common/on_actions/HSP_on_actions.txt` strips SPR's vanilla spirits down to 전국 파업 plus 구식 군대 and unlocks division templates.
- `common/national_focus/HSP_regional.txt` is a small development tree for the regions the democracy path releases.
- `docs/ROADMAP.md`: what is built, deferred ideas and the art and text still needed. Update it when a phase or deferred item lands.
- Localisation: `localisation/{english,korean}/hsp_*_l_{english,korean}.yml`. The two languages have the same files, the same keys in the same order, and the same `# <branch> focus` comments, which mirror the tree.

## Vanilla overrides

A mod file with the same path as a vanilla file **replaces the vanilla file entirely**. These files do that: `events/LAR_Spain.txt`, `common/scripted_effects/00_scripted_effects.txt`, `common/countries/cosmetic.txt`, `common/characters/SPR.txt`, `common/ideas/_manpower.txt` (anarchists keep volunteers only after `HSP_ana_all_must_bear_the_torch`). When editing them, keep the vanilla content intact; put new content in `HSP_`-named files where possible. To see what the mod changed: `diff "$HOI4_GAME_DIR/<path>" <path>`.

All overrides are rebased on game 1.19 (`descriptor.mod` says `1.19.*`): each is the vanilla 1.19 file plus a small, deliberate mod diff. When the game updates, re-copy the new vanilla file and re-apply that diff rather than editing the old copy. The mod does **not** override vanilla `spain.txt`.

## Localisation rules

- The mod ships **English and Korean**. Every key you add goes into both files: Korean is the author's original voice; English is a faithful translation in vanilla's register (Title Case names; `_DEF` names take "the"). The validator flags a key that exists in only one language.
- Files are UTF-8 **with BOM**, first line `l_english:` / `l_korean:`, entries `  KEY:0 "text"` (two-space indent). Script `.txt` files are UTF-8 without BOM. All files use LF.
- A focus needs `ID` and `ID_desc` (`""` is an acceptable placeholder). An event needs its title, desc and every option `name`.
- Inside text: `[ROOT.GetNameDef]`-style scopes, `§Y…§!` colours, `\n` newlines.

## Reference material

Before using an effect, trigger or modifier, confirm it exists in the installed game rather than writing it from memory:

- Docs: `$HOI4_GAME_DIR/documentation/{effects,triggers,modifiers,loc_objects}_documentation.md`. Each entry is a `## name` heading, so search with `grep -n -A15 '^## add_ideas$'`.
- Real usage: `grep -rn 'effect_name' "$HOI4_GAME_DIR/common" "$HOI4_GAME_DIR/events"`. Vanilla focus trees are the best templates.
- Sprites (`GFX_goal_*`, `GFX_idea_*`, `GFX_report_event_*`): defined in `$HOI4_GAME_DIR/interface/*.gfx`.

`HOI4_GAME_DIR` is set in `.claude/settings.local.json`.

## Verifying changes

- **`tools/validate_mod.py`** checks brace balance, loc file format, focus/event/sprite references, duplicate IDs, missing loc keys, overlapping focus positions (including icons one column apart on a row; leave two), and focuses placed relative to a focus defined later in the file (the game stacks those near the tree origin). A hook runs it after every edit and reports only issues the edit introduced. Run `python3 tools/validate_mod.py` for the whole mod before calling work done: the bar is **0 new issues**. Pre-existing issues live in `tools/known_issues.txt`; when you fix one, run `--write-baseline` to drop it.
- **CWTools** (VS Code extension) checks scopes and effect/trigger validity more deeply than the validator. Read its diagnostics for files you edited when the diagnostics tool is available.
- **In game** is the only real test. The user plays; afterwards the `check-errors` skill reads `error.log`.

## Known problems (don't fix unprompted; ask first)

- Event text for `HSP_spain_events.6` onwards and `HSP_spain_news.2` onwards is a functional draft the author is reviewing; ask the author before rewriting story text. Most focus `_desc` keys are `""` placeholders. The one remaining known issue is a vanilla sprite bug in `events/LAR_Spain.txt`.
- Some focus IDs contain typos (`HSP_convoy_escord_focus`). Renaming an ID breaks save games and references, so leave IDs as they are.

## Git

Short lowercase commit messages (`add new focus for ...`, `fix ...`). Use one branch per feature or branch of the tree.
