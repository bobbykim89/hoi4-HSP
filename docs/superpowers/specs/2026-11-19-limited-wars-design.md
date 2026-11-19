# Limited wars for Morocco and the French Basque Country, and a cleaner reunification

Democracy path, federal split (`HSP_moroccan_autonomy`, `HSP_basque_autonomy`, `HSP_reunite_spain`,
`HSP_guarantee_of_local_autonomy`).

## Why

- The federal split releases Morocco and the Basque Country as puppets but leaves half of each homeland
  in foreign hands. A Thai-style limited war (vanilla `SIA_start_limited_war_indochina`) lets the player
  fight for it without being dragged into a world war.
- `HSP_reunite_spain` and `HSP_guarantee_of_local_autonomy` show the same conditional tooltip
  (`HSP_claim_conquered_regions_tt`) that never says whether it applies. Each focus should do one clear thing.

## Goals

- A limited war decision for each region while its puppet exists: Morocco (states 461, 462) and the
  French Basque Country (806).
- A win within the time limit ends the war and hands the land to the puppet.
- A loss gives the player a choice: a white peace for nothing, or carry on as a full war.
- Reunification follows Yugoslavia's split route: Spain gains cores only on what its puppets **own**
  (not just occupy) when they are annexed. Claims on anything else are lost.

## Non-goals

- No limited war for Galicia's Portuguese claims or Aragon's Sardinia and Sicily claims.
- No new story events. Decisions only.
- No change to Spain's faction membership during the war (vanilla makes Siam leave its faction).

## Approaches

1. **Decisions all the way through (chosen).** A decision declares the war and starts a timed mission.
   A win makes peace automatically. A timeout unlocks two decisions. No AI reply to wait for, no story text.
2. Vanilla Siam's event chain (`siam.10`–`siam.18`). Closer to vanilla, but 6–8 new events, and the
   defender can refuse peace even after losing, which goes against "the player gets the ceasefire".
3. A plain wargoal and a normal peace conference. Simplest, but no time limit and no automatic hand-over
   to the puppet.

## Design

### Who can be targeted

One rule, which also keeps Italy out: **the target is the country that controls the land, and only
if that land is not one of its own cores.**

- Morocco: 461 and 462 are Moroccan cores, not French. France (or Vichy, after `france.3`) can be
  targeted from the start.
- French Basque Country: 806 is a French core, so France itself is never a target. After the fall of
  France, `france.3` gives Germany control of it (France still owns it), and Germany becomes a target.
- Sardinia and Sicily are Italian cores, so there is never a war for them (they also have no decision).

Also closed while Spain is allied with the target, already at war with it, or has a non-aggression
pact with it, and while another limited war is running. A target that has already been fought for a
region can't be fought again for it (as in vanilla), so a lost war against France can be tried again
against Vichy.

### Start (decision, one per region)

- Visible after the region's autonomy focus while its puppet (`MOR` / `NAV`) is Spain's subject.
- Records the target, the states it controls in that region, and the countries that will fight on
  its side (its overlord, faction members, guarantors), then declares war and starts the mission.

### The mission (120 days, like vanilla)

- **Win:** every recorded state is controlled by Spain or one of its subjects. Spain makes white peace
  with the target and the countries recorded on its side, and the recorded states are transferred to
  the puppet. If the land still belonged to someone else on paper (806 owned by Free France), that
  owner loses it.
- **Timeout:** two decisions appear.
  - *Ceasefire:* white peace with the same countries, nothing gained, a small stability and war
    support penalty.
  - *Full war:* the war continues as a normal war; the limited war state is cleared.
- **Cancelled** (the same as vanilla): Spain capitulates or the target disappears or is beaten by
  someone else. The limited war state is cleared.

### Reunification

- `HSP_reunite_spain`: annexes the puppets (existing `HSP_reunite_regional_puppet`, which already cores
  every state they own) and adds Reunification Strain. A custom tooltip says it plainly: every state our
  puppets own becomes our core; claims on land they don't own are lost.
- `HSP_guarantee_of_local_autonomy`: only swaps Reunification Strain for Local Autonomy.
- `HSP_claim_conquered_regions` and its tooltip key are removed. The limited war decisions disappear
  with the puppets, and so does `HSP_federal_claims_cat` (already hidden after reunification).

## Left to the builder

- The decision category's name, icon and priority; the decision icons; AI weights.
- The exact stability and war support penalty for the ceasefire (small: about -5% each).
- How the mission's highlight shows the states still to take.
- Korean and English text: draft both; the author reviews the Korean.
- Update `docs/ROADMAP.md`.
