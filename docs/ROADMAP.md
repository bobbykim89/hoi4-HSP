# HSP roadmap

Status as of 2026-10-20. The full design is the author's plan; this file records what is built, what comes next, and what was deferred.

## Built: Phase 1 (foundation and monarchy)

- **The mod's own tree.** `HSP_spanish_focus` (`common/national_focus/HSP_spain.txt`) replaces vanilla's Spain tree on the 1936 start.
- **Starting choice.** The emergency council leads to the monarchy and cancels the 1936 election. (역사적 스페인, the Phase 1 hand-off to vanilla's tree, was replaced by the Republican and Fascist roots.)
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
  - the French colonial empire: compliance, cores on Algeria, investment in West Africa and Indochina, colonial industry (investment only; colonies are not released as subjects)
- **Both houses:**
  - the Pan-Hispanic Federation and the four viceroyalties, with integration
  - Allies and Axis branches with house-specific claims
  - war planning and the Crusade Against Communism
- **AI.** Every focus and decision has an AI weight.

## Built: Phase 2 (the Republican path)

- **Root:** 공화국 수호 (`HSP_defend_the_republic`). The election starts a 180-day fascist plot.
- **Dealing with the plot:** decisions to maintain order state by state, negotiate with the unions and eliminate the fascists. If the plot runs out, the unpacified Nationalist states rise in a civil war.
- **Democracy** (about 50 focuses):
  - an economy spine with a three-level spirit
  - domestic reforms
  - the Allies (with their research group) or the Latin Sphere (customs union, research group, mutual defence, annexation into the Latin Union)
  - the federal split (Galicia, the Basque Country, Catalonia and Morocco as puppets with their own development tree, then reunified or freed into an Iberian Defense Council)
  - a Popular Front line that can turn communist and join the Comintern
  - late-game war
- **Communism** (about 40 focuses): Stalinist or independent lines; Portuguese and French revolutions; the Iberian Socialist Union; exporting the revolution to Latin America.
- **Anarchism** (about 45 focuses), on vanilla's CNT-FAI layout:
  - the Anarchist Society, a single dynamic spirit fed by focuses
  - the revolution at Masters of Our Own Fate, in which the Republic revolts
  - volunteers only, and no puppets, factions or collaboration governments
  - the councils and theorists unlocked by focus
  - Portuguese anarchism, uprisings abroad and commune integration
  - World Revolution

## Built: Phase 3 (the Fascist path)

- **Root:** 국민 운동 (`HSP_national_movement`). The 역사적 스페인 hand-off to vanilla's tree is gone. The election starts a 180-day countdown to the uprising, which can also come early at 0% stability with fascism above 60%.
- **Before the uprising:** decisions to incite unrest and to win over states one by one.
- **The uprising:**
  - The player is the Nationalists under Franco and keeps the states won over, plus Spanish Morocco and the Canaries; the Republic revolts with the rest.
  - Winning adds 내전으로부터 회복 (−10% output, stability, construction and recruitable population).
- **Nationalist** (32 focuses), close to vanilla's Francoist route:
  - no new cores
  - the recovery spirit removed early
  - a crowned puppet king (Alfonso XIII or Jaime IV, with a stability spirit) or a military dictatorship
  - +5% recruitable population in total (2 + 2 + 1)
- **Falange** (30 focuses), close to vanilla's Falange route:
  - José Antonio as leader
  - the recovery spirit removed late
  - Portugal (cores and a war goal)
  - the Aragonese possessions, North Africa and Nueva España (claims, war goals, and decisions to core occupied states)
  - submission demands to Spanish-speaking Latin America, then the Hispanic Empire
  - the Axis

## Deferred and future ideas

- **The Viceroyalty of Louisiana as a separate subject country.** Today it's only Spanish states with cores (`HSP_form_viceroyalty_of_louisiana`). The future version releases a dynamic subject country, like the Latin American viceroyalties.
- **Borbón expansion.** Its late game is still thinner than the Habsburg route's (13 house focuses against 22). Remaining ideas:
  - releasing colonies (Indochina, Syria-Lebanon, Madagascar) as Spanish subjects
  - restoring the Bourbon kingdoms in Italy (Two Sicilies, Parma) by decision
  - a Bourbon "family compact" faction, the counterpart to the Habsburg Hegemonic League
- **AI tuning beyond the base weights.** For example, steering the Borbón AI between the Allies and the Axis by world situation, and AI strategies for the federation and the crown events. This needs an observer run to judge.
- **Observer run.** Let an AI Spain play to 1945 and read `error.log` with the `check-errors` skill.

## Content the author needs to supply

- **Event text review.** Every event now has a functional draft in both languages, including the Republican and Fascist events and news added in Phases 2 and 3. The author reviews and rewrites the Korean; keep the English as a faithful translation.
- **Focus descriptions.** Most `_desc` keys are still the `""` placeholder.
- **Flags.** These currently use placeholders:
  - `HSP_latin_union` (a copy of vanilla's Gran Colombia flag)
  - `HSP_iberian_socialist_republic` (a copy of vanilla's communist Spain flag)
  - the four viceroyalties (`HSP_viceroyalty_*`, copied from vanilla's Carlist Cross of Burgundy)
  - `HSP_franco_spanish_commonwealth` (a copy of `HSP_kingdom_of_spain`)
- **Portrait.** Archduke Felix (king of Bulgaria) uses Archduke Joseph Ferdinand's portrait.
