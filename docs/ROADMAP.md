# HSP roadmap

Status as of 2026-10-16. The full design is the author's plan; this file records what is built, what comes next, and what was deferred.

## Built: Phase 1 (foundation and monarchy)

- **The mod's own tree.** `HSP_spanish_focus` (`common/national_focus/HSP_spain.txt`) replaces vanilla's Spain tree on the 1936 start.
- **Starting choice.** The emergency council leads to the monarchy and cancels the 1936 election. 역사적 스페인 (Historical Spain) hands off to vanilla's tree.
- **Shared branches.** The economy and military branches are open to every path.
- **Choosing the king.** An event crowns Otto (Habsburg) or Alfonso XIII (Borbón); Karl Pius is the fallback.
- **Habsburg route:**
  - Portugal and Brazil
  - royal guard cavalry
  - the crowns of Hungary and Austria, as imperial dominions
  - Austria-Hungary, which needs all its former lands held
  - the Holy Roman Empire, with vanilla's requirements
  - Habsburg kingdoms: Poland, Bulgaria, Sweden and Scandinavia
  - Italy, the Papal States, and the renaming of Leningrad and Stalingrad
- **Borbón route:**
  - royal legitimacy and royal guard
  - French royalists → the French crown, by acceptance or royalist civil war → the Franco-Spanish union
  - Louisiana and Quebec
  - capital to Paris, Belgian border forts
- **Both houses:**
  - the Pan-Hispanic Federation and the four viceroyalties, with integration
  - Allies and Axis branches with house-specific claims
  - war planning and the Crusade Against Communism
- **AI.** Every focus and decision has an AI weight.

## Next: Phase 2, the Republican path

Replaces the 역사적 스페인 hand-off root for republicans. Taken from the author's design:

- **Common to all three sub-paths.** The fascist civil war can be avoided, but the fascist partisans must be dealt with.
  - Once the election happens, a civil-war countdown of 180 days starts. Use a mission, like vanilla's `SPR_military_plot_*`.
  - **Focus 1:** unlocks "Maintain order in [state]" decisions for the northern states, the historical Nationalist territories. Troops must be present; each costs 15 PP and gives +5% stability, −3% fascism and +35 days on the countdown.
  - **Focus 2:** unlocks "Negotiate with the unions": 50 PP for 30 days of +1.5% stability, −0.1 fascism per week, and −10% consumer goods.
  - **Focus 3:** unlocks "Eliminate the fascists", available at 75%+ stability and fascism below 5%. The Falange and Nationalist generals and political advisors retire.
  - After the fascists are dealt with (or after a civil war against them), choose Democracy, Communism or Anarchism.
- **Democracy.** Extends vanilla's republican route. It has strong economy and factory buffs and few military ones.
  - Communist generals retire.
  - It can join the Allies.
  - It can form the **Latin Sphere** faction. Decisions invite Latin American countries for 25 PP each: MEX GUA HON ELS NIC COS CUB JAM COL VEN ECU PRU BOL PAR CHL ARG URG.
  - The focus "Hispanic Unity" renames the country to the Latin Union and unlocks decisions to annex faction members with cores (50 PP each).
- **Communism.** Close to vanilla's Stalinist path.
  - It can trigger a communist revolution in Portugal and unite with it, taking all of Portugal's cores.
  - A focus switches the government to communism once communism has 40%+ support.
  - Republican generals retire.
- **Anarchism.** Like vanilla's anarchist Spain, with buffs, and it requires a civil war.
  - A focus gives a compliance buff and enables the occupation law 해방된 노동자들 (`liberate_workers_occupation`). Vanilla only shows that law to communist governments, so it needs a mod condition.
  - The anarchist revolution starts after the focus "Masters of Our Own Fate", and a normal civil war follows.
  - Republican generals retire.

## Next: Phase 3, the Fascist path

Requires a civil war. It has two sub-routes.

- **Common:**
  - Republican and communist generals retire.
  - **Focus 1:** unlocks a decision to cause civil unrest in the northern states: +0.1 fascism and −1% stability weekly for 30 days.
  - **Focus 2:** unlocks a per-state decision to win that state over: −5% stability and +3% fascism each, 30 days. The state joins your side when the civil war starts.
  - The civil war starts when the countdown ends, or when stability is at 0 and fascism is over 60%.
- **Nationalist:** the low-return path, close to vanilla's Nationalist Spain.
- **Falange:** the high-return path, close to vanilla's Falange path.

## Deferred and future ideas

- **The Viceroyalty of Louisiana as a separate subject country.** Today it's only Spanish states with cores (`HSP_form_viceroyalty_of_louisiana`). The future version releases a dynamic subject country, like the Latin American viceroyalties.
- **Borbón expansion.** Its late game is thinner than the Habsburg route's (8 house focuses against 22). Ideas:
  - integrating the French colonies after the Franco-Spanish union
  - restoring the Bourbon kingdoms in Italy (Two Sicilies, Parma) by decision
  - a Bourbon "family compact" faction, the counterpart to the Habsburg Hegemonic League
- **AI tuning beyond the base weights.** For example, steering the Borbón AI between the Allies and the Axis by world situation, and AI strategies for the federation and the crown events. This needs an observer run to judge.
- **Observer run.** Let an AI Spain play to 1945 and read `error.log` with the `check-errors` skill.

## Content the author needs to supply

- **Event text review.** Every event now has a functional draft in both languages (2026-10-16). The author reviews and rewrites the Korean; keep the English as a faithful translation.
- **Focus descriptions.** Most `_desc` keys are still the `""` placeholder.
- **Flags.** These currently use placeholders:
  - the four viceroyalties (`HSP_viceroyalty_*`, copied from vanilla's Carlist Cross of Burgundy)
  - `HSP_franco_spanish_commonwealth` (a copy of `HSP_kingdom_of_spain`)
- **Portrait.** Archduke Felix (king of Bulgaria) uses Archduke Joseph Ferdinand's portrait.
