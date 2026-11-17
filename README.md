# Habsburg Spain

An alternate-history focus tree for Hearts of Iron IV. Republican Spain in 1936 can restore a Habsburg monarchy and rebuild an empire, or take one of several other roads through the decade.

- **Game version:** 1.19
- **Mod version:** 0.1.0, in development
- **Languages:** English and Korean

## What it adds

The 1936 start gives Republican Spain a new focus tree of about 330 focuses, with three roots:

- **The Monarchy.** An emergency council cancels the February election and avoids the civil war, then crowns a king.
  - **Habsburg** (Otto von Habsburg): union with Portugal, the crowns of Hungary and Austria, Austria-Hungary, the Holy Roman Empire, and Habsburg kings for Poland, Bulgaria and Scandinavia.
  - **Borbón** (Alfonso XIII): the French crown, a Franco-Spanish union ruled from Paris, and the French colonial empire.
  - **Either house:** the Pan-Hispanic Federation and the four American viceroyalties.
- **The Republic.** Hold off a fascist plot, then choose:
  - **Democracy:** a federal Spain or a Latin Union.
  - **Communism:** an Iberian Socialist Union.
  - **Anarchism:** a revolution of the communes.
- **The Fascists.** Prepare the uprising, win the civil war, then choose:
  - **Nationalist:** Franco's state, with a crowned puppet king or a military dictatorship.
  - **Falange:** a Hispanic Empire.

Shared economy and army branches are open to every path. The regions released on the federal path get a small development tree of their own.

The 1939 start is unchanged.

## Compatibility

The mod replaces these vanilla files completely, so it will conflict with other mods that change them:

- `events/LAR_Spain.txt`
- `common/scripted_effects/00_scripted_effects.txt`
- `common/countries/cosmetic.txt`
- `common/characters/SPR.txt`
- `common/ideas/_manpower.txt`

## Installing

1. Copy or clone this folder into the game's mod folder: `Documents/Paradox Interactive/Hearts of Iron IV/mod/` on Windows, `~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/` on Linux.
2. Next to the folder, put a copy of `descriptor.mod` named `habsburg_spain.mod`, and add the line `path="mod/<folder name>"` to it.
3. Enable the mod in the launcher.

## For contributors

- `docs/ROADMAP.md` lists what is built, what is planned and the art and text still needed.
- `docs/FLAG_BRIEFS.md` has the background for generating flags.
- `python3 tools/validate_mod.py` checks braces, localisation, references and focus layout. The bar is zero new issues.
