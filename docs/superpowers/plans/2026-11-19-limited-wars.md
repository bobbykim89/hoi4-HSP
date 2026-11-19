# Limited Wars and Cleaner Reunification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thai-style limited wars for the rest of Morocco and the French Basque Country on the democracy federal split, and a reunification that cores only what the puppets own.

**Architecture:** Two start decisions (one per region) and one shared timed mission, in the existing `HSP_federal_claims_cat`. Shared bookkeeping lives in scripted effects/triggers. Outcomes are decisions, not events. Reunification drops `HSP_claim_conquered_regions`; `HSP_reunite_regional_puppet` already cores every state a puppet owns.

**Tech Stack:** HOI4 1.19 Paradox script; `tools/validate_mod.py`; CWTools diagnostics.

**Spec:** `docs/superpowers/specs/2026-11-19-limited-wars-design.md`

## Global Constraints

- Every new identifier starts with `HSP_` (CLAUDE.md).
- Every loc key goes into both `localisation/english/hsp_decisions_l_english.yml` and `localisation/korean/hsp_decisions_l_korean.yml`, same order; files stay UTF-8 with BOM, LF.
- Confirm each effect/trigger in `$HOI4_GAME_DIR/documentation/*_documentation.md` before use. Do not use `$PARAM$` scripted-trigger arguments (vanilla 1.19 scripted triggers never use them).
- Mission timeout: **120 days**. Ceasefire penalty: **-0.05 stability, -0.05 war support**.
- Target rule: the country controls a state that is a core of the region's tag (`MOR` / `NAV`) and is **not** its own core; not ROOT, not ROOT's subject, not the region tag.
- Closed while ROOT is allied with the target, at war with it, has a non-aggression pact with it, or another limited war runs. A target already fought for a region can't be fought again for it.
- Bar: `python3 tools/validate_mod.py` reports **0 new issues**.

## Review Focus

1. **The target capitulates to someone else mid-war** (France to Germany in 1940). Expect the mission to cancel and the limited war state to clear, not hang. Task 2 step 4 checks the cancel trigger covers `has_capitulated` on the target.
2. **Spain is already at war with the target's faction** (e.g. democratic Spain in the Allies vs Germany). Expect the Basque decision to be unavailable (`has_war_with`), not to declare a second war. Task 2 available block.
3. **The puppet takes the state, not Spain.** Expect the win to count. Mission `available` accepts a controller that is ROOT or ROOT's subject.
4. **Peace must not end unrelated wars.** Only countries recorded at the start (target, its overlord, faction members, guarantors) are white-peaced, and only if still at war with ROOT.
5. **Reunification while a limited war is running.** Expect the mission to cancel (puppet gone) and the state to clear. Cancel trigger includes `var:HSP_limited_war_puppet = { exists = no }`.

---

### Task 1: Reunification cleanup

**Files:**
- Modify: `common/national_focus/HSP_spain.txt` (focuses `HSP_reunite_spain` ~1605, `HSP_guarantee_of_local_autonomy` ~1655)
- Modify: `common/scripted_effects/HSP_scripted_effects.txt:493-527` (delete `HSP_claim_conquered_regions` and its comment)
- Modify: `localisation/{english,korean}/hsp_focus_l_{english,korean}.yml:108`

- [ ] **Step 1:** In `HSP_reunite_spain` replace `HSP_claim_conquered_regions = yes` with nothing and wrap the annex loop's tooltip: add `custom_effect_tooltip = HSP_reunite_spain_tt` before the `every_country` loop and put the loop in `hidden_effect`. Change the comment above the focus to `# Yugoslavia-style: Spain cores only the states the puppets own when they are annexed`.
- [ ] **Step 2:** In `HSP_guarantee_of_local_autonomy` remove `HSP_claim_conquered_regions = yes` (only the `swap_ideas` stays).
- [ ] **Step 3:** Delete the `HSP_claim_conquered_regions` scripted effect. Replace loc key `HSP_claim_conquered_regions_tt` (line 108, both files) with:
  - EN `HSP_reunite_spain_tt:0 "Galicia, the Basque Country, Catalonia and Morocco are §Yannexed§!. Every state they own becomes our §Ycore§!; their claims on land they do not own are §Rlost§!."`
  - KO `HSP_reunite_spain_tt:0 "갈리시아, 바스크, 카탈루냐, 모로코를 §Y합병§!합니다. 이들이 소유한 모든 주는 우리의 §Y코어§!가 되며, 소유하지 못한 땅에 대한 영유권은 §R사라집니다§!."`
- [ ] **Step 4:** Run `grep -rn HSP_claim_conquered_regions common localisation` → no output. Run `python3 tools/validate_mod.py` → 0 new issues.
- [ ] **Step 5:** Commit `simplify reunification: core only what the puppets own`.

### Task 2: Limited war decisions and mission

**Files:**
- Modify: `common/scripted_effects/HSP_scripted_effects.txt` (append)
- Modify: `common/scripted_triggers/HSP_scripted_triggers.txt` (append)
- Modify: `common/decisions/HSP_decisions.txt` (`HSP_federal_claims_cat`, ~3016)
- Modify: `localisation/{english,korean}/hsp_decisions_l_{english,korean}.yml` (after `HSP_cede_state_to_region_desc`, line 140)

**Interfaces (all on SPR / ROOT):**
- Variables: `HSP_limited_war_target` (country), `HSP_limited_war_puppet` (country). Arrays: `HSP_limited_war_states` (states), `HSP_limited_war_enemies` (countries), `HSP_limited_war_tried_MOR`, `HSP_limited_war_tried_NAV` (countries). Flag: `HSP_limited_war_timed_out_flag`.
- Trigger `HSP_can_start_limited_war` (country scope, FROM = target): not allied, not at war, no NAP, not guaranteed by ROOT, no `HSP_limited_war_target` variable on ROOT. Wrapped in `custom_trigger_tooltip = { tooltip = HSP_no_limited_war_running_tt ... }` for the variable part only.
- Effect `HSP_limited_war_start` (ROOT scope, FROM = target, with `HSP_limited_war_puppet` and `HSP_limited_war_states` already set by the caller): records enemies (target; its overlord; `every_allied_country` of the target if in a faction; every country with `has_guaranteed = FROM`), sets `HSP_limited_war_target = FROM`, `declare_war_on = { target = FROM type = annex_everything }`, `activate_mission = HSP_limited_war_mission`. Shows `custom_effect_tooltip = HSP_limited_war_start_tt`.
- Effect `HSP_limited_war_peace_out` (ROOT): for each in `HSP_limited_war_enemies` that `has_war_with = ROOT`: `ROOT = { white_peace = { tag = PREV } }`, and the same for each `every_subject_country` of ROOT still at war with it.
- Effect `HSP_limited_war_clear` (ROOT, hidden): clears both variables, `HSP_limited_war_states`, `HSP_limited_war_enemies`, `HSP_limited_war_timed_out_flag`. Keeps the `tried` arrays.

- [ ] **Step 1: Start decisions** `HSP_limited_war_morocco` and `HSP_limited_war_basque` in `HSP_federal_claims_cat`:
  - `allowed = { original_tag = SPR }`; `visible`: `MOR` (resp. `NAV`) exists and `is_subject_of = ROOT`.
  - Targeted: `target_trigger = { FROM = { NOT = { tag = ROOT } NOT = { is_subject_of = ROOT } NOT = { original_tag = MOR } any_controlled_state = { is_core_of = MOR NOT = { is_core_of = PREV } } NOT = { is_in_array = { ROOT.HSP_limited_war_tried_MOR = THIS } } } }` (NAV variant analogous). `available = { FROM = { HSP_can_start_limited_war = yes } }`. `highlight_states` = the states that would be recorded. `cost = 25`, `fire_only_once = no`.
  - `complete_effect`: set `HSP_limited_war_puppet` to `MOR`/`NAV`; `clear_array`; `every_state = { limit = { is_core_of = MOR is_controlled_by = FROM NOT = { is_core_of = FROM } } add_to_array = { ROOT.HSP_limited_war_states = THIS } }`; `add_to_array = { HSP_limited_war_tried_MOR = FROM }`; `HSP_limited_war_start = yes`.
  - `ai_will_do = { base = 5 }`, `factor = 0` when the target `is_major = yes` and has a stronger army (`fighting_army_strength_ratio` < 0.6).
- [ ] **Step 2: Mission** `HSP_limited_war_mission` in the same category: `activation = { always = no }`, `days_mission_timeout = 120`, `is_good = no`, `fire_only_once = no`.
  - `available`: `all_of_scopes = { array = HSP_limited_war_states OR = { is_controlled_by = ROOT controller = { is_subject_of = ROOT } } }`.
  - `complete_effect`: `HSP_limited_war_peace_out = yes`; each state in `HSP_limited_war_states` → `var:HSP_limited_war_puppet = { transfer_state = PREV }`; `HSP_limited_war_clear = yes`.
  - `timeout_effect`: `set_country_flag = HSP_limited_war_timed_out_flag`.
  - `cancel_trigger`: ROOT `has_capitulated`; `var:HSP_limited_war_target` `exists = no` or `has_capitulated = yes`; `NOT = { has_war_with = var:HSP_limited_war_target }`; `var:HSP_limited_war_puppet = { exists = no }`. `cancel_effect`: `HSP_limited_war_peace_out = yes` only if the target still exists and is not capitulated, then `HSP_limited_war_clear = yes`.
  - `highlight_states`: in `HSP_limited_war_states` and not controlled by ROOT or a subject.
- [ ] **Step 3: Timeout decisions** `HSP_limited_war_ceasefire` and `HSP_limited_war_full_war`: visible/available with `has_country_flag = HSP_limited_war_timed_out_flag`, `cost = 0`. Ceasefire: `HSP_limited_war_peace_out = yes`, `add_stability = -0.05`, `add_war_support = -0.05`, `HSP_limited_war_clear = yes`. Full war: `custom_effect_tooltip = HSP_limited_war_full_war_tt`, `HSP_limited_war_clear = yes`. AI: ceasefire `base = 10`, full war `base = 1`.
- [ ] **Step 4:** Check the Review Focus items 1, 2, 3 and 5 against the code you wrote (cancel trigger, `has_war_with` in `HSP_can_start_limited_war`, the subject-controller clause, puppet `exists = no`).
- [ ] **Step 5: Loc** (both files, after line 140): name and `_desc` for the four decisions and the mission, plus `HSP_limited_war_start_tt`, `HSP_limited_war_full_war_tt`, `HSP_no_limited_war_running_tt`. Targeted names use `[FROM.GetName]`, e.g. EN `HSP_limited_war_morocco:0 "Limited War for Morocco against §Y[FROM.GetName]§!"`. The start tooltip must say: 120 days to take the highlighted states; on success, peace and the states go to the region; otherwise choose a ceasefire or full war. Korean is drafted in the register of `HSP_federal_claims_cat_desc` and flagged for the author.
- [ ] **Step 6:** `python3 tools/validate_mod.py` → 0 new issues; read CWTools diagnostics for the four edited script files if the tool is available.
- [ ] **Step 7:** Commit `add limited wars for morocco and the french basque country`.

### Task 3: Docs

**Files:** Modify `docs/ROADMAP.md:39`

- [ ] **Step 1:** Extend the federal split bullet: limited wars (Thai-style, 120 days) for French Morocco and, once a non-French power holds it, the French Basque Country; reunification cores only what the puppets own.
- [ ] **Step 2:** `python3 tools/validate_mod.py` → 0 new issues. Commit `update roadmap for limited wars` together with the spec and this plan.
- [ ] **Step 3:** Hand over the in-game test list: Morocco vs France in 1936–39; Morocco vs Vichy; Basque vs Germany after France falls; let a war time out and take each outcome; reunify with and without French Morocco owned by `MOR`.
