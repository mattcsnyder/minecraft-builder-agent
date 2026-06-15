# Minecraft Datapack Builder

Convert a WorldEdit `.schema` file into a Minecraft Java Edition datapack (1.21.4+ compatible) and install it into a world.

## Usage
`/minecraft-datapack [schema file path]`

If no path is given, look for a `.schema` file in the current directory.

## What to do

1. **Read the schema file** — it contains WorldEdit commands (`/pos1`, `/pos2`, `//set`, `//replace`, `/setblock`).

2. **Write a Python conversion script** (or reuse one if it exists) that:
   - Parses `/pos1 x,y,z` and `/pos2 x,y,z` pairs
   - Converts `//set <block_spec>` → `fill x1 y1 z1 x2 y2 z2 <block>` using the dominant block for weighted specs like `75%stone_bricks,15%cobblestone`
   - Converts `//replace <old> <new>` → `fill x1 y1 z1 x2 y2 z2 <new> replace <old>`
   - Converts `/setblock x y z block` → `setblock x y z block` (strip the leading `/`)
   - Splits any fill region exceeding 32,768 blocks along the longest axis recursively
   - **No leading `/` on any command** — mcfunction files don't use them
   - Uses **old-style fill syntax**: `fill x1 y1 z1 x2 y2 z2 block [replace filter]` (NOT `fill from ... to ...`)

3. **Create the datapack folder structure**:
   ```
   <name>/
     pack.mcmeta          ← pack_format 71, supported_formats [1, 9999]
     data/
       <namespace>/
         function/        ← singular "function", not "functions" (1.21.4+ change)
           build.mcfunction
   ```
   Use the schema filename (without extension) as the datapack name and namespace.

4. **Find Minecraft worlds** — check these locations in order:
   - `~/Documents/curseforge/minecraft/Instances/*/saves/`
   - `~/Library/Application Support/minecraft/saves/`

5. **Ask the user which world** to install into, then copy the datapack folder into `<world>/datapacks/`.

6. **Tell the user**:
   - How many commands were generated
   - The exact `/function <namespace>:build` command to run in-game
   - To run `/reload` first if the world is already open

## Key rules
- `pack.mcmeta` must use `supported_formats: [1, 9999]` to avoid version mismatch errors
- The function directory is `function/` (singular) for Minecraft 1.21.4+
- Never add a leading `/` to commands in `.mcfunction` files
- For weighted block specs, always pick the highest-percentage block
