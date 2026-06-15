#!/usr/bin/env python3
"""Generate mario.schema - a huge floating pixel-art mural of classic Mario,
16x16 source sprite scaled 4x to 64x64 blocks, with a black outline border
drawn around every individual "pixel" for a crisp sticker/pixel-art look.
Built in the X-Y plane at a fixed Z, centered at local (0,0)-(63,63)."""

# 16x16 sprite grid, row 0 = TOP of sprite
GRID = [
    "................",
    ".......RRRRR....",
    "......RRRRRRRR..",
    "......BBBSSSB...",
    ".....BSBSSSSBS..",
    ".....BSBBSSSSBSS",
    ".....BSBBSSSSBB.",
    "......BSSSSSSSB.",
    "........SSRSS...",
    "......RRRRRRRRRR",
    ".....RRRRORRRRRO",
    "....RRROROOOROOO",
    "....SSOOOOOROOOO",
    "....SSOOOOOOOOOO",
    "......BBB...BBB.",
    ".....BBBB...BBBB",
]

COLORS = {
    "R": "red_concrete",
    "S": "terracotta",
    "B": "brown_concrete",
    "O": "blue_concrete",
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
lines.append("# GIANT MARIO PIXEL-ART MURAL")
lines.append(f"# 16x16 sprite at {SCALE}x scale = 64x64 blocks, single Z plane")
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

with open("mario.schema", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote mario.schema")
