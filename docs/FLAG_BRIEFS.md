# Flag briefs

Background for generating the mod's flags with an image AI. Each brief has the story behind the flag and some motif ideas. Paste the shared style block first, then the flag's brief.

## Files and sizes

Every flag is three 32-bit RGBA TGA files with the same name:

| Folder | Size |
|---|---|
| `gfx/flags/` | 82×52 |
| `gfx/flags/medium/` | 41×26 |
| `gfx/flags/small/` | 10×7 |

Generate a large source image at about 1.58:1 (1640×1040 is ideal; 3:2 also works), save it as PNG rather than JPG, and Claude crops, resizes and converts it into the three TGAs.

For each ideology the game first looks for a flag named `<tag>_<ideology>.tga` (for example `HSP_kingdom_of_spain_communism.tga`) and falls back to `<tag>.tga`. Ideology flags are optional.

## Flags to make

| File name | Country | Current state |
|---|---|---|
| `SPR_POR_commonwealth` | United Kingdom of Iberia | hand-made, to redo |
| `HSP_habsburg_empire` | Habsburg Empire | hand-made, to redo |
| `HSP_franco_spanish_commonwealth` | Franco-Spanish Commonwealth | copy of Kingdom of Spain |
| `HSP_latin_union` | Latin Union | copy of vanilla Gran Colombia |
| `HSP_iberian_socialist_republic` | Iberian Socialist Republic | copy of vanilla communist Spain |
| `HSP_spanish_peoples_republic` | Spanish People's Republic | copy of vanilla democratic Spain |
| `HSP_latin_union_communism` | Latin Socialist Union | none yet (falls back to the Latin Union) |
| `HSP_viceroyalty_nueva_espana` | Viceroyalty of New Spain | Carlist Cross of Burgundy |
| `HSP_viceroyalty_nueva_granada` | Viceroyalty of New Granada | Carlist Cross of Burgundy |
| `HSP_viceroyalty_rio_de_la_plata` | Viceroyalty of the Río de la Plata | Carlist Cross of Burgundy |
| `HSP_viceroyalty_peru` | Viceroyalty of Peru | Carlist Cross of Burgundy |

Also made: `CAT_aragon_democratic` (Aragonese Republic), the democratic version of vanilla's `CAT_aragon`; vanilla only has `CAT_aragon_neutrality` (Crown of Aragon).

## Shared style block

> A national flag for an alternate-history 1936–1945 strategy game. Flat colours, bold simple shapes, no text or lettering, no fabric texture, no shading or 3D, no border, filling the whole frame at a 1.58:1 ratio. It must stay recognisable when shrunk to 82×52 pixels. Use the style of real 1930s vexillology and heraldry.

## United Kingdom of Iberia (`SPR_POR_commonwealth`)

In 1936 Spain cancels its election and restores the monarchy, crowning Otto von Habsburg king. He offers Portugal a union of the two crowns that recalls the Iberian Union of 1580–1640, when the Spanish Habsburgs ruled both kingdoms and "the oceans of the world." Portugal accepts and the two crowns are one again. It's a Catholic seafaring monarchy.

Motifs: the Spanish Habsburg arms, the Portuguese shield with its five quinas and border of castles, the armillary sphere, the Cross of Burgundy. Spain's red and gold could be paired with the blue and white of the Portuguese monarchy's flag.

## Habsburg Empire (`HSP_habsburg_empire`)

With Otto von Habsburg on the Spanish throne, Spain gathers the old Habsburg crowns one by one: Hungary, Austria, Austria-Hungary, the Holy Roman Empire, and Habsburg-ruled kingdoms in Poland, Bulgaria, Sweden/Scandinavia and Italy. In "The Empire Resurrected" it turns down both Britain and Germany, founds its own Habsburg Hegemonic League and declares a new Reconquista. It's a universal Catholic empire reborn.

Motifs: the black and gold Habsburg colours, the double-headed imperial eagle, the Spanish Habsburgs' Cross of Burgundy, an imperial crown.

The map colour is grey (128, 128, 128) and can change to match the new flag.

## Franco-Spanish Commonwealth (`HSP_franco_spanish_commonwealth`)

In this branch the Bourbon Alfonso XIII is crowned instead. He backs the French royalists and wins the French crown, either peacefully or through a royalist civil war. The two Bourbon kingdoms merge, the capital moves to Paris, and the realm takes over France's colonial empire, Louisiana and Quebec.

Motifs: gold fleurs-de-lis on royal blue alongside Spain's red and gold, and the Bourbon arms. The map colour is gold.

## Latin Union (`HSP_latin_union`)

The Spanish Republic survives and stays democratic. It founds the Latin Sphere, an alliance and customs union with the Latin American republics, then merges the members into one Latin Union. It's a republican, transatlantic, pan-Hispanic federation, so no crowns.

Motifs: the Second Republic's red, yellow and purple tricolour, a star or sun for each member, the Atlantic joining the two sides. The map colour is red.

## Iberian Socialist Republic (`HSP_iberian_socialist_republic`)

The Republic turns communist, sparks a revolution in Portugal and absorbs it into a single socialist state covering the whole peninsula.

Motifs: a red field, a star or hammer and sickle, the Republic's purple, an emblem of the peninsula. The map colour is dark red.

## Spanish People's Republic (`HSP_spanish_peoples_republic`)

The democratic Republic's popular front of socialists, communists and left republicans wins power by the ballot and turns the Republic socialist (`HSP_peoples_republic`). It is the Second Republic gone red, not Moscow's Spain: it must look clearly different from the communist path, which keeps vanilla's communist flag.

Motifs: keep the Second Republic's red, yellow and purple tricolour as the base; one red five-pointed star, edged in gold, centred on the yellow band. No hammer and sickle, no coat of arms (a crest turns to mud at 82×52). The map colour is a wine red.

## Latin Socialist Union (`HSP_latin_union_communism`)

The Latin Union (see above) under a socialist government: the same transatlantic union of the Spanish Republic and the Latin American republics, now socialist. The game uses this flag for the Latin Union whenever its government is communist.

Motifs: a red field; a wavy blue band edged in white running across the middle, the Atlantic that joins the two sides; in the upper hoist, a ring of five small gold stars, one per founding nation. It must stay distinct from the Iberian Socialist Republic (red field with a peninsula emblem), so the Atlantic band is the key element. The map colour stays the Latin Union's red.

## Aragonese Republic (`CAT_aragon_democratic`)

On the democratic Republic's federal path, Spain grants Catalonia autonomy as a self-governing republic within the federation, and hands it every Spanish land of the old Crown of Aragon: Catalonia, Aragón, Valencia and the Balearic Islands. It also claims the Crown's old Mediterranean kingdoms, Sardinia and Sicily. It takes vanilla's name for this, the Aragonese Republic. It's a democratic republic, so no crown. Spain can later reunite the federation or set it free.

Motifs: the red and gold stripes of the Senyera (the Crown of Aragon's bars), shared by Catalonia, Aragón, Valencia and the Balearics; a republican star or a plain shield of the four bars; a hint of the Republic's purple. Vanilla's Crown of Aragon flag uses the crowned Aragonese arms on the stripes, and the Catalan independence flag has a white star on blue, so the new flag should be distinct from both. The map colour is dark red (166, 68, 72).

## Viceroyalties (`HSP_viceroyalty_*`)

A restored Spanish monarchy, under either house, rebuilds the colonial-era viceroyalties as loyal subject kingdoms in the Americas. The Cross of Burgundy (the old Spanish imperial flag) works as the shared base. Give each one its own local element and its map colour.

- **New Spain** (`HSP_viceroyalty_nueva_espana`): Mexico, Central America, Cuba and the Dominican Republic. Map colour green (104, 152, 83). Motif idea: the eagle on a cactus.
- **New Granada** (`HSP_viceroyalty_nueva_granada`): Colombia, Venezuela, Ecuador and Panama. Map colour gold (222, 187, 91).
- **Río de la Plata** (`HSP_viceroyalty_rio_de_la_plata`): Argentina, Uruguay, Paraguay and Bolivia. Map colour light blue (145, 157, 236). Motif idea: the Sun of May.
- **Peru** (`HSP_viceroyalty_peru`): centred on Peru. Map colour pale lavender (196, 189, 204). Motif idea: an Inca sun or a vicuña.
