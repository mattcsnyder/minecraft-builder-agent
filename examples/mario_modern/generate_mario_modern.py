#!/usr/bin/env python3
"""Generate mario_modern.schema - a "modern" style Mario pixel-art mural
(cap with M emblem, separate mustache, white gloves, blue overalls with
yellow buttons, brown shoes, leg separation). 24x24 source grid scaled 4x
to 96x96 blocks, with a black outline border drawn around every individual
"pixel" for a crisp pixel-art look. Built in the X-Y plane at a fixed Z,
local coords (0,0)-(95,95)."""

# 24x24 sprite grid built from mirrored 12-column halves (left half + its
# mirror), row 0 = TOP of sprite.
HALVES = [
    "........RRRR",  # 0  cap top
    ".......RRRRR",  # 1  cap
    "......RRRRRR",  # 2  cap brim, solid red
    "......RRRWWW",  # 3  cap emblem - white circle starts
    "......RRWWWW",  # 4  white circle widens
    "......RRWWRW",  # 5  red "M" mark inside circle
    "......RRRRRR",  # 6  cap brim bottom
    ".....HHSSSSS",  # 7  hair sideburns + forehead
    ".....HSWBSSS",  # 8  eyes (white + blue pupil)
    ".....HSSSSSS",  # 9  face / eyebrow
    "....SSHHHHHH",  # 10 mustache
    "....SSSHHHSS",  # 11 mustache / mouth
    "....SSSSSSSS",  # 12 chin / neck
    "...WRRRRRRRR",  # 13 shoulders, glove starts
    "..WWRRRRRRRR",  # 14 shirt + gloves
    "..WWRRRRRBYB",  # 15 strap + button transition
    "..WWBBBBBBBB",  # 16 overalls
    "..WWBBBBBBBB",  # 17 overalls
    "..WWBBYBBBBB",  # 18 overalls + button
    "..WWBBBBBBBB",  # 19 overalls
    "..WWBBBBBBBK",  # 20 overalls / leg gap
    "..WWBBBBBBBK",  # 21 legs / leg gap
    "..NNBBBBBBBK",  # 22 shoes start
    ".NNNNBBBBBBK",  # 23 shoes bottom
]

GRID = [h + h[::-1] for h in HALVES]

COLORS = {
    "R": "red_concrete",
    "S": "terracotta",
    "H": "brown_concrete",
    "W": "white_concrete",
    "B": "blue_concrete",
    "Y": "yellow_concrete",
    "K": "black_concrete",
    "N": "brown_terracotta",
}

OUTLINE = "black_concrete"
SCALE = 4

lines = []

def section(title):
    lines.append("")
    lines.append("")
    lines.append("# " + "-" * 60)
    lines.append(f"# {title}")
    lines.append("# " + "-" * 60)
    lines.append("")

def pos(p1, p2):
    lines.append(f"/pos1 {p1[0]},{p1[1]},{p1[2]}")
    lines.append(f"/pos2 {p2[0]},{p2[1]},{p2[2]}")

lines.append("# ============================================================")
lines.append("# MODERN MARIO PIXEL-ART MURAL")
lines.append(f"# 24x24 sprite at {SCALE}x scale = 96x96 blocks, single Z plane")
lines.append("# Cap w/ M emblem, mustache, gloves, overalls w/ buttons, shoes")
lines.append("# Each pixel: black outline border + colored 2x2 core")
lines.append("# ============================================================")

ROWS = len(GRID)
COLS = len(GRID[0])

# Pass 1: fill each pixel's full 4x4 block with its color
for r, row in enumerate(GRID):
    for c, ch in enumerate(row):
        if ch == ".":
            continue
        x0 = c * SCALE
        y0 = (ROWS - 1 - r) * SCALE  # flip so row 0 (top) is highest Y

        section(f"PIXEL ({c},{r}) = {ch}")
        pos((x0, y0, 0), (x0 + SCALE - 1, y0 + SCALE - 1, 0))
        lines.append(f"//set {COLORS[ch]}")

# Pass 2: outline only the silhouette edges (where a neighboring cell is
# empty or off-grid), so the black lines trace the character's outline
# instead of crossing every pixel.
section("SILHOUETTE OUTLINE")
for r, row in enumerate(GRID):
    for c, ch in enumerate(row):
        if ch == ".":
            continue
        x0 = c * SCALE
        y0 = (ROWS - 1 - r) * SCALE

        # up (row-1 -> higher Y)
        if r == 0 or GRID[r - 1][c] == ".":
            pos((x0, y0 + SCALE - 1, 0), (x0 + SCALE - 1, y0 + SCALE - 1, 0))
            lines.append(f"//set {OUTLINE}")
            lines.append("")
        # down (row+1 -> lower Y)
        if r == ROWS - 1 or GRID[r + 1][c] == ".":
            pos((x0, y0, 0), (x0 + SCALE - 1, y0, 0))
            lines.append(f"//set {OUTLINE}")
            lines.append("")
        # left
        if c == 0 or GRID[r][c - 1] == ".":
            pos((x0, y0, 0), (x0, y0 + SCALE - 1, 0))
            lines.append(f"//set {OUTLINE}")
            lines.append("")
        # right
        if c == COLS - 1 or GRID[r][c + 1] == ".":
            pos((x0 + SCALE - 1, y0, 0), (x0 + SCALE - 1, y0 + SCALE - 1, 0))
            lines.append(f"//set {OUTLINE}")
            lines.append("")

with open("mario_modern.schema", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote mario_modern.schema")
