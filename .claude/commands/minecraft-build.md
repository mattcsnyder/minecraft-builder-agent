# Minecraft Build Generator

Take a natural language description of a Minecraft build and generate a complete `.schema` file of WorldEdit commands, then automatically convert it to a vanilla datapack.

## Usage
`/minecraft-build <description>`

Example: `/minecraft-build a small viking longhouse with a thatched roof and firepit inside`

## What to do

### Step 1 — Design the build

Read the user's description and plan the structure:
- Infer style, size, materials, and key features from the description
- Center the build on X=0, Z=0 with ground at Y=64
- Keep builds reasonably sized (under 80x80 footprint) unless the user specifies otherwise
- Think in layers: foundation → outer shell → interior → roof → details → lighting → decoration

### Step 2 — Generate the `.schema` file

Write a `.schema` file to the current directory named after the build (e.g., `viking_longhouse.schema`).

Format rules:
- Use `#` comment headers to label each section (e.g., `# FOUNDATION`, `# WALLS`, `# ROOF`)
- Use `/pos1 x,y,z` and `/pos2 x,y,z` before every `//set` or `//replace`
- `//set` fills a region: `//set stone_bricks` or weighted `//set 70%stone_bricks,20%cobblestone,10%mossy_stone_bricks`
- `//replace old new` swaps blocks in a region: `//replace stone_bricks air` (to hollow)
- `/setblock x y z block[state]` for single blocks
- Always clear the build area first with `//set air`
- Always add a foundation layer at Y=63

Good material choices by style:
- Medieval/castle: stone_bricks, cracked_stone_bricks, mossy_stone_bricks, cobblestone, oak_planks, spruce_planks
- Viking/Norse: spruce_log, spruce_planks, spruce_stairs, dark_oak_log, cobblestone, hay_block
- Modern: white_concrete, gray_concrete, glass, iron_bars, quartz_block
- Desert/Egyptian: sandstone, cut_sandstone, smooth_sandstone, sand
- Fantasy/Elven: oak_log, oak_leaves, mossy_cobblestone, grass_block, vines
- Nether/Dark: nether_bricks, blackstone, crimson_planks, soul_sand

Always include:
- Hollow interiors (use `//replace` to carve out walls)
- A doorway or entrance opening
- At least basic lighting (lantern, torch, glowstone, or sea_lantern via `/setblock`)
- Roof structure appropriate to the style

### Step 3 — Convert and install

After writing the schema file, immediately run the `/minecraft-datapack` skill on it:
- Pass the schema file path
- Let it handle world selection and installation

### Step 4 — Report back

Tell the user:
- What you built and key design decisions
- The dimensions (X width × Z depth × Y height)
- The main materials used
- The in-game command to run: `/function <name>:build`
