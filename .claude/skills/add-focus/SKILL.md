---
name: add-focus
description: Add or rework a national focus in the Habsburg Spain tree end to end — focus block, placement, rewards, linked ideas/events/decisions, English and Korean localisation. Use when the user asks for a new focus or branch, or to change a focus's rewards, prerequisites or position.
---

# Add a focus

1. **Pin the design.** Settle these in chat: the id (`HSP_` + English snake_case), the name and description (the user writes Korean; you translate to English), the branch, prerequisites, mutually exclusive focuses, cost, the `completion_reward`, `available` and `bypass` conditions, and `ai_will_do`. Propose defaults from the neighbouring focuses and ask only about what you can't infer. Done when every item has a value the user agreed to or didn't contest.

2. **Find the branch.** `grep -n '^\t#' common/national_focus/HSP_spain.txt` maps the tree's branches. Read two or three neighbouring focuses and copy their shape: field order, `search_filters`, `ai_will_do`, and the `## <Korean name>` comment above each focus.

3. **Place it.** Use `relative_position_id` + `x`/`y` like its neighbours. The validator resolves positions and flags any two focuses on the same tile.

4. **Write the rewards.** Check every effect, trigger and modifier name against `$HOI4_GAME_DIR/documentation/` (`grep -n -A15 '^## name$'`) or a vanilla usage. Pick an icon that exists in `$HOI4_GAME_DIR/interface/*.gfx` (`GFX_goal_*`, `GFX_focus_*`).

5. **Add supporting content** in the mod's own files:
   - ideas → `common/ideas/habsburg_spain.txt`
   - events → `events/hsp_events.txt`, next free `HSP_spain_events.N`
   - decisions → `common/decisions/HSP_decisions.txt`
   - modifiers → `common/dynamic_modifiers/`, `common/opinion_modifiers/`
   Each one also needs its loc keys in the matching `hsp_*_l_english.yml` and `hsp_*_l_korean.yml`.

6. **Localise.** Add `HSP_x:0 "…"` and `HSP_x_desc:0 "…"` to both `localisation/korean/hsp_focus_l_korean.yml` (Korean) and `localisation/english/hsp_focus_l_english.yml` (English), at the same position under the branch's `# … focus` comment.

7. **Verify.** `python3 tools/validate_mod.py` must report 0 new issues. If the diagnostics tool is available, check CWTools diagnostics for every file you edited and fix what they flag.

8. **Hand off.** Summarise the focus: where it sits, what it requires, what it grants. Then give the in-game test: enable the mod, play as `SPR`, console `Focus.IgnorePrerequisites` / `Focus.AutoComplete` to reach it, `loc_check_focuses`, then the `check-errors` skill.
