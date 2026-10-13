---
name: check-errors
description: Triage the HOI4 error.log after a test run and fix what the mod caused. Use when the user has just played or launched the game, reports something broken in-game, or mentions error.log.
---

# Check errors

1. Run `python3 tools/mod_errors.py`. If it prints a WARNING that the mod was not enabled or the log predates the latest edit, stop: tell the user to enable "Habsburg Spain" in the launcher (descriptor `mod/habsburg_spain.mod`) and/or relaunch, then rerun this skill. A stale log says nothing about the current files.

2. For each distinct line, open the referenced `file:line` and classify it:
   - **mod-caused**: in a file the mod ships, or about an `HSP_` identifier;
   - **vanilla-caused**: in a vanilla file (it still matched the filter by mentioning a mod ID).
   Lines quoting vanilla line numbers in files the mod overrides (e.g. `events/LAR_Spain.txt:2740` when the mod's file is 219 lines) mean the log came from a run without the mod; go back to step 1.

3. Fix the mod-caused lines that have a clear cause. Look up the correct syntax in `$HOI4_GAME_DIR/documentation/*_documentation.md` or a vanilla usage before changing anything. When a cause is ambiguous, or the fix would change gameplay rather than correct a mistake, give the user your hypothesis and the options instead of picking one.

4. Run `python3 tools/validate_mod.py`. It must report 0 new issues.

**Done when** every distinct line from step 1 is fixed, explained as not mod-caused, or handed to the user as a decision. Finish with a list of what to retest in game. Useful console commands: `event <id> SPR`, `Focus.AutoComplete`, `Focus.IgnorePrerequisites`, `loc_check_focuses`, `loc_check_events`, `tag SPR`.
