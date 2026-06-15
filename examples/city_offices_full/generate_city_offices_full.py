#!/usr/bin/env python3
"""Generate city_offices_full.schema - office interiors for every floor of
every skyscraper, with varied per-floor layouts for a "completely full but
realistic" open-plan office feel:

  - "dense"  : wall-to-wall desk/computer + chair rows, with a carpeted
               walkway row left between each pair (less crowded than a
               pure grid)
  - "pods"   : clusters of 4 desks arranged so two face-to-face pairs sit
               back-to-back (a common open-plan "bench" pod), with
               carpeted walkways between pods
  - "lounge" : a sparse floor - central meeting table + chairs, sofas,
               lamps, potted plants, mostly open carpeted floor

Each floor is carpeted first (theme color per tower), then furniture is
placed on top - carpet shows through in the walkways/open areas. Floors
cycle through lounge -> dense -> pods (-> dense for tier1's 4th floor) so
no two adjacent floors look identical. TVs are re-placed on the south wall
of every floor. Uses the SAME local grid/coords as generate_city.py,
offset the same way (dx=-55, dy=0, dz=-85)."""

PLOT = 40
ROAD = 12
STEP = PLOT + ROAD  # 52
RF = "refurbished_furniture"

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


def fset(p1, p2, mat):
    pos(p1, p2)
    lines.append(f"//set {mat}")
    lines.append("")


def sblock(x, y, z, block):
    lines.append(f"/setblock {x} {y} {z} {block}")


OFFICE_WOODS = ["dark_oak", "oak", "spruce", "birch", "jungle"]
CARPETS = ["gray_carpet", "light_gray_carpet", "green_carpet", "white_carpet", "lime_carpet"]
SOFA_COLORS = ["black", "white", "lime", "light_gray", "green"]

SKYSCRAPERS = {
    (0, 0): 120,
    (2, 0): 150,
    (1, 1): 180,
    (0, 2): 110,
    (2, 2): 140,
}


# ------------------------------------------------------------
# LAYOUTS
# ------------------------------------------------------------
def layout_dense(ix0, ix1, iz0, iz1, y, wood):
    """Desk+computer row, chair row, then a 2-row carpeted walkway."""
    z = iz0 + 1
    while z + 1 <= iz1 - 1:
        fset((ix0 + 1, y, z), (ix1 - 1, y, z), f"{RF}:{wood}_desk")
        fset((ix0 + 1, y + 1, z), (ix1 - 1, y + 1, z), f"{RF}:computer")
        fset((ix0 + 1, y, z + 1), (ix1 - 1, y, z + 1), f"{RF}:{wood}_chair[facing=north]")
        z += 4


def layout_pods(ix0, ix1, iz0, iz1, y, wood):
    """4-desk back-to-back pods (two facing pairs) on an 8-block grid,
    leaving carpeted walkways between pods."""
    px = ix0 + 1
    while px + 3 <= ix1 - 1:
        pz = iz0 + 1
        while pz + 3 <= iz1 - 1:
            fset((px, y, pz), (px + 3, y, pz), f"{RF}:{wood}_chair[facing=south]")
            fset((px, y, pz + 1), (px + 3, y, pz + 1), f"{RF}:{wood}_desk")
            fset((px, y + 1, pz + 1), (px + 3, y + 1, pz + 1), f"{RF}:computer")
            fset((px, y, pz + 2), (px + 3, y, pz + 2), f"{RF}:{wood}_desk")
            fset((px, y + 1, pz + 2), (px + 3, y + 1, pz + 2), f"{RF}:computer")
            fset((px, y, pz + 3), (px + 3, y, pz + 3), f"{RF}:{wood}_chair[facing=north]")
            pz += 8
        px += 8


def layout_lounge(ix0, ix1, iz0, iz1, y, wood, color):
    """Sparse breakout floor: central meeting table + chairs, sofas,
    lamps, potted plants, mostly open carpet."""
    cx = (ix0 + ix1) // 2
    cz = (iz0 + iz1) // 2

    sblock(cx, y, cz, f"{RF}:{wood}_table")
    for dx, dz, face in [(1, 0, "west"), (-1, 0, "east"), (0, 1, "north"), (0, -1, "south")]:
        sblock(cx + dx, y, cz + dz, f"{RF}:{wood}_chair[facing={face}]")

    sblock(ix0 + 1, y, iz0 + 1, f"{RF}:{color}_sofa")
    sblock(ix0 + 2, y, iz0 + 1, f"{RF}:{color}_sofa")
    sblock(ix1 - 1, y, iz1 - 1, f"{RF}:{color}_sofa")
    sblock(ix1 - 2, y, iz1 - 1, f"{RF}:{color}_sofa")

    sblock(ix1 - 1, y, iz0 + 1, f"{RF}:{color}_lamp[powered=true]")
    sblock(ix0 + 1, y, iz1 - 1, f"{RF}:{color}_lamp[powered=true]")

    for cxp, czp in [(ix0 + 1, iz0 + 1), (ix1 - 1, iz0 + 1), (ix0 + 1, iz1 - 1), (ix1 - 1, iz1 - 1)]:
        sblock(cxp, y + 1, czp, "potted_fern")


def add_ceiling_lights(ix0, ix1, iz0, iz1, y, color):
    """Dense grid of ceiling lights every 3 blocks, plus wall lamps along
    every wall, for a brightly-lit office floor."""
    x = ix0 + 1
    while x <= ix1 - 1:
        z = iz0 + 1
        while z <= iz1 - 1:
            sblock(x, y + 6, z, "glowstone")
            z += 3
        x += 3

    # Wall lamps along all four walls every 4 blocks
    x = ix0 + 1
    while x <= ix1 - 1:
        sblock(x, y, iz0, f"{RF}:{color}_lamp[powered=true]")
        sblock(x, y, iz1, f"{RF}:{color}_lamp[powered=true]")
        x += 4
    z = iz0 + 1
    while z <= iz1 - 1:
        sblock(ix0, y, z, f"{RF}:{color}_lamp[powered=true]")
        sblock(ix1, y, z, f"{RF}:{color}_lamp[powered=true]")
        z += 4


def add_power_room(ix0, ix1, iz0, iz1, y):
    """Power room in the center of the floor - always-lit furnaces flanked
    by sea lanterns and an iron-block housing, standing in for a permanently
    running generator bank."""
    cx = (ix0 + ix1) // 2
    cz = (iz0 + iz1) // 2
    fset((cx - 2, y, cz - 1), (cx + 2, y, cz + 1), "iron_block")
    for dx in (-1, 0, 1):
        sblock(cx + dx, y, cz, "furnace[facing=south,lit=true]")
    sblock(cx - 2, y + 1, cz, "sea_lantern")
    sblock(cx + 2, y + 1, cz, "sea_lantern")


def furnish_floor(ix0, ix1, iz0, iz1, y, wood, color, carpet, layout, ground=False):
    cx = (ix0 + ix1) // 2

    # Clear any previous furniture on this floor and re-carpet it
    fset((ix0 + 1, y, iz0 + 1), (ix1 - 1, y + 1, iz1 - 1), "air")
    fset((ix0 + 1, y, iz0 + 1), (ix1 - 1, y, iz1 - 1), carpet)
    fset((ix0 + 1, y + 2, iz0 + 1), (ix1 - 1, y + 2, iz1 - 1), "air")

    if layout == "dense":
        layout_dense(ix0, ix1, iz0, iz1, y, wood)
    elif layout == "pods":
        layout_pods(ix0, ix1, iz0, iz1, y, wood)
    else:
        layout_lounge(ix0, ix1, iz0, iz1, y, wood, color)

    add_ceiling_lights(ix0, ix1, iz0, iz1, y, color)

    if ground:
        add_power_room(ix0, ix1, iz0, iz1, y)

    # TV on the south interior wall
    sblock(cx, y, iz0, f"{RF}:television")


def floor_levels_tier1():
    return [65, 73, 81, 89]


def floor_levels_tier2(total_h):
    y0b = 94
    y1b = 64 + total_h
    floors = [y0b + 1]
    plate = y0b + 8
    while plate < y1b:
        floors.append(plate + 1)
        plate += 8
    return floors


LAYOUT_CYCLE = ["lounge", "dense", "pods"]


def skyscraper_full_offices(px, pz, total_h, wood, color, carpet):
    size1 = 32
    x0, x1 = px, px + size1 - 1
    z0, z1 = pz, pz + size1 - 1
    ix0, ix1 = x0 + 1, x1 - 1
    iz0, iz1 = z0 + 1, z1 - 1

    section(f"SKYSCRAPER @ ({px},{pz}) tier1 - varied floors")
    t1_floors = floor_levels_tier1()
    t1_layouts = ["lounge", "dense", "pods", "dense"]
    for i, (y, layout) in enumerate(zip(t1_floors, t1_layouts)):
        furnish_floor(ix0, ix1, iz0, iz1, y, wood, color, carpet, layout, ground=(i == 0))

    size2 = 22
    off = (size1 - size2) // 2
    x0b, x1b = px + off, px + off + size2 - 1
    z0b, z1b = pz + off, pz + off + size2 - 1
    ix0b, ix1b = x0b + 1, x1b - 1
    iz0b, iz1b = z0b + 1, z1b - 1

    section(f"SKYSCRAPER @ ({px},{pz}) tier2 - varied floors")
    for i, y in enumerate(floor_levels_tier2(total_h)):
        layout = LAYOUT_CYCLE[i % len(LAYOUT_CYCLE)]
        furnish_floor(ix0b, ix1b, iz0b, iz1b, y, wood, color, carpet, layout)


for i, (key, total_h) in enumerate(SKYSCRAPERS.items()):
    col, row = key
    px = col * STEP
    pz = -(row * STEP) - PLOT + 1
    wood = OFFICE_WOODS[i % len(OFFICE_WOODS)]
    color = SOFA_COLORS[i % len(SOFA_COLORS)]
    carpet = CARPETS[i % len(CARPETS)]
    skyscraper_full_offices(px, pz, total_h, wood, color, carpet)


with open("city_offices_full.schema", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote city_offices_full.schema")
