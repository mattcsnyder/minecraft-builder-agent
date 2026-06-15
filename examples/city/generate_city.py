#!/usr/bin/env python3
"""Generate city.schema - Phase 1 of a city district just north of the glass
dome's north opening. A 3x3 grid of 40x40 plots separated by 12-wide roads,
mixing reusable skyscraper and house templates. Houses are furnished using
the Refurbished Furniture mod (refurbished_furniture:*). Built in local
coordinates with local Z <= 0 (north) and offset afterward so local (0,0)
sits just north of the dome's north wall."""

PLOT = 40
ROAD = 12
STEP = PLOT + ROAD  # 52

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


def freplace(p1, p2, old, new):
    pos(p1, p2)
    lines.append(f"//replace {old} {new}")
    lines.append("")


def sblock(x, y, z, block):
    lines.append(f"/setblock {x} {y} {z} {block}")


# ------------------------------------------------------------
# SKYSCRAPER TEMPLATE
# ------------------------------------------------------------
def skyscraper(px, pz, total_h, facade, glass, mullion):
    """32x32 footprint at (px,pz)-(px+31,pz+31). Tier1 0-30, tier2 (22x22,
    centered) 30-total_h, then antenna+beacon."""
    size1 = 32
    y0, y1 = 64, 64 + 30
    x0, x1 = px, px + size1 - 1
    z0, z1 = pz, pz + size1 - 1

    section(f"SKYSCRAPER @ ({px},{pz}) tier1")
    fset((x0, y0, z0), (x1, y1, z1), facade)
    fset((x0 + 1, y0 + 1, z0 + 1), (x1 - 1, y1 - 1, z1 - 1), "air")
    for cx, cz in [(x0, z0), (x0, z1), (x1, z0), (x1, z1)]:
        fset((cx, y0, cz), (cx, y1, cz), mullion)
    _windows(x0, x1, z0, z1, y0 + 2, y1 - 1, glass, mullion)
    for fy in range(y0 + 8, y1, 8):
        fset((x0 + 1, fy, z0 + 1), (x1 - 1, fy, z1 - 1), mullion)

    # Tier 2 - 22x22 centered
    size2 = 22
    off = (size1 - size2) // 2
    x0b, x1b = px + off, px + off + size2 - 1
    z0b, z1b = pz + off, pz + off + size2 - 1
    y0b, y1b = y1, 64 + total_h

    section(f"SKYSCRAPER @ ({px},{pz}) tier2")
    fset((x0b, y0b, z0b), (x1b, y1b, z1b), facade)
    fset((x0b + 1, y0b + 1, z0b + 1), (x1b - 1, y1b - 1, z1b - 1), "air")
    for cx, cz in [(x0b, z0b), (x0b, z1b), (x1b, z0b), (x1b, z1b)]:
        fset((cx, y0b, cz), (cx, y1b, cz), mullion)
    _windows(x0b, x1b, z0b, z1b, y0b + 2, y1b - 1, glass, mullion)
    for fy in range(y0b + 8, y1b, 8):
        fset((x0b + 1, fy, z0b + 1), (x1b - 1, fy, z1b - 1), mullion)

    # Antenna + beacon
    section(f"SKYSCRAPER @ ({px},{pz}) antenna")
    cx_ant = (x0b + x1b) // 2
    cz_ant = (z0b + z1b) // 2
    top = 64 + total_h
    pos((cx_ant, top, cz_ant), (cx_ant, top + 14, cz_ant))
    lines.append("//set lightning_rod[facing=up]")
    lines.append("")
    sblock(cx_ant, top + 15, cz_ant, "sea_lantern")


def _windows(x0, x1, z0, z1, by0, by1, glass, mullion):
    """Glass window bands with mullions every 4 blocks on all 4 faces."""
    fset((x0 + 1, by0, z0), (x1 - 1, by1, z0), glass)
    fset((x0 + 1, by0, z1), (x1 - 1, by1, z1), glass)
    fset((x0, by0, z0 + 1), (x0, by1, z1 - 1), glass)
    fset((x1, by0, z0 + 1), (x1, by1, z1 - 1), glass)
    for x in range(x0 + 1, x1, 4):
        fset((x, by0, z0), (x, by1, z0), mullion)
        fset((x, by0, z1), (x, by1, z1), mullion)
    for z in range(z0 + 1, z1, 4):
        fset((x0, by0, z), (x0, by1, z), mullion)
        fset((x1, by0, z), (x1, by1, z), mullion)


# ------------------------------------------------------------
# HOUSE TEMPLATE (Refurbished Furniture interiors)
# ------------------------------------------------------------
def house(px, pz, wood, color, appliance):
    """20x14 house in the front-left of a 32x32 plot at (px,pz), with a
    yard behind furnished with hedges, mailbox, and a trampoline."""
    RF = "refurbished_furniture"
    hx0, hx1 = px + 4, px + 23  # 20 wide (X)
    hz0, hz1 = pz + 4, pz + 17  # 14 deep (Z)
    mx = (hx0 + hx1) // 2

    section(f"HOUSE @ ({px},{pz}) [{wood}/{color}] shell")
    # Shell (2 floors, 8 tall)
    fset((hx0, 64, hz0), (hx1, 71, hz1), f"{wood}_planks")
    # Hollow floor 1 + floor 2
    fset((hx0 + 1, 65, hz0 + 1), (hx1 - 1, 67, hz1 - 1), "air")
    fset((hx0 + 1, 68, hz0 + 1), (hx1 - 1, 68, hz1 - 1), f"{wood}_planks")
    fset((hx0 + 1, 69, hz0 + 1), (hx1 - 1, 71, hz1 - 1), "air")
    # Roof
    fset((hx0, 72, hz0), (hx1, 72, hz1), f"{wood}_planks")
    # Corner logs
    for cx, cz in [(hx0, hz0), (hx0, hz1), (hx1, hz0), (hx1, hz1)]:
        fset((cx, 64, cz), (cx, 71, cz), f"{wood}_log")

    section(f"HOUSE @ ({px},{pz}) windows + door")
    # Windows on front (south, z=hz0) and back (north, z=hz1)
    for x in (hx0 + 2, hx1 - 2):
        fset((x, 65, hz0), (x, 66, hz0), "glass_pane")
        fset((x, 69, hz0), (x, 70, hz0), "glass_pane")
        fset((x, 65, hz1), (x, 66, hz1), "glass_pane")
        fset((x, 69, hz1), (x, 70, hz1), "glass_pane")
    # Front door
    fset((mx, 65, hz0), (mx, 66, hz0), "air")
    sblock(mx, 65, hz0, f"{wood}_door[facing=south,half=lower]")
    sblock(mx, 66, hz0, f"{wood}_door[facing=south,half=upper]")

    section(f"HOUSE @ ({px},{pz}) interior divider + stairs")
    # Divider wall splitting floor1 into living room (south) / kitchen (north)
    midz = (hz0 + hz1) // 2
    fset((hx0 + 1, 65, midz), (hx1 - 1, 67, midz), f"{wood}_planks")
    fset((hx0 + 1, 65, midz), (hx0 + 2, 66, midz), "air")  # doorway
    # Same divider on floor 2: bedroom (south) / bathroom (north)
    fset((hx0 + 1, 69, midz), (hx1 - 1, 71, midz), f"{wood}_planks")
    fset((hx0 + 1, 69, midz), (hx0 + 2, 70, midz), "air")  # doorway
    # Ladder between floors in NE corner
    sblock(hx1 - 1, 65, hz1 - 1, f"ladder[facing=south]")
    sblock(hx1 - 1, 66, hz1 - 1, f"ladder[facing=south]")
    sblock(hx1 - 1, 67, hz1 - 1, f"ladder[facing=south]")
    fset((hx1 - 1, 68, hz1 - 1), (hx1 - 1, 68, hz1 - 1), "air")
    sblock(hx1 - 1, 69, hz1 - 1, f"ladder[facing=south]")

    section(f"HOUSE @ ({px},{pz}) living room + kitchen furniture")
    # Living room (south half, floor1)
    sblock(hx0 + 1, 65, hz0 + 1, f"{RF}:{color}_sofa")
    sblock(hx0 + 1, 65, hz0 + 2, f"{RF}:{color}_sofa")
    sblock(mx + 1, 65, hz0 + 1, f"{RF}:{wood}_table")
    sblock(mx + 1, 65, hz0 + 2, f"{RF}:television")
    sblock(hx1 - 1, 65, hz0 + 1, f"{RF}:{color}_lamp")
    # Kitchen (north half, floor1)
    fset((hx0 + 1, 65, midz + 1), (hx1 - 1, 65, midz + 1), f"{RF}:{wood}_kitchen_cabinetry")
    sblock(hx0 + 1, 65, midz + 2, f"{RF}:{wood}_kitchen_sink")
    sblock(hx0 + 2, 65, midz + 2, f"{RF}:{appliance}_stove")
    sblock(hx0 + 3, 65, midz + 2, f"{RF}:{appliance}_fridge")
    sblock(mx + 1, 65, midz + 2, f"{RF}:{wood}_table")
    sblock(mx, 65, midz + 2, f"{RF}:{wood}_chair")
    sblock(mx + 2, 65, midz + 2, f"{RF}:{wood}_chair")

    section(f"HOUSE @ ({px},{pz}) bedroom + bathroom furniture")
    # Bedroom (south half, floor2)
    sblock(hx0 + 1, 69, hz0 + 1, f"{color}_bed[part=foot,facing=east]")
    sblock(hx0 + 2, 69, hz0 + 1, f"{color}_bed[part=head,facing=east]")
    sblock(hx0 + 1, 69, hz0 + 2, f"{RF}:{wood}_drawer")
    sblock(hx1 - 1, 69, hz0 + 1, f"{RF}:{color}_lamp")
    # Bathroom (north half, floor2)
    sblock(hx0 + 1, 69, midz + 1, f"{RF}:{color}_toilet")
    sblock(hx0 + 1, 69, midz + 2, f"{RF}:{color}_basin")
    fset((hx1 - 3, 69, midz + 1), (hx1 - 1, 69, midz + 2), f"{RF}:{color}_bath")

    section(f"HOUSE @ ({px},{pz}) yard")
    # Backyard hedge border around the plot
    fset((px, 64, pz), (px + 31, 64, pz + 31), "grass_block")
    fset((px, 65, pz), (px + 31, 65, pz), f"{RF}:{wood}_hedge")
    fset((px, 65, pz + 31), (px + 31, 65, pz + 31), f"{RF}:{wood}_hedge")
    fset((px, 65, pz), (px, 65, pz + 31), f"{RF}:{wood}_hedge")
    fset((px + 31, 65, pz), (px + 31, 65, pz + 31), f"{RF}:{wood}_hedge")
    # Gate at the front path
    sblock(mx, 65, pz, f"{RF}:{wood}_lattice_fence_gate[facing=south]")
    # Trampoline + mailbox in the backyard
    sblock(px + 8, 65, pz + 25, f"{RF}:{color}_trampoline")
    sblock(hx1 - 1, 65, hz1 + 1, f"{RF}:{wood}_mail_box")


# ------------------------------------------------------------
# ROADS / GROUND
# ------------------------------------------------------------
GRID_W = 3 * PLOT + 2 * ROAD  # 144
GRID_H = 3 * PLOT + 2 * ROAD  # 144 (north extent)

section("GROUND PLATE")
fset((-4, 63, -GRID_H - 1), (GRID_W + 3, 63, 4), "gray_concrete")

section("PLOT YARDS (default grass, houses override their own)")
for col in range(3):
    for row in range(3):
        px = col * STEP
        pz = -(row * STEP) - PLOT + 1
        fset((px, 63, pz), (px + PLOT - 1, 63, pz + PLOT - 1), "grass_block")

section("STREETLIGHTS AT ROAD INTERSECTIONS")
for col in range(4):
    for row in range(4):
        lx = col * STEP - (ROAD // 2) if col > 0 else -2
        lz = -(row * STEP) + (ROAD // 2) if row > 0 else 2
        if col == 0:
            lx = -2
        if row == 0:
            lz = 2
        fset((lx, 64, lz), (lx, 68, lz), "cobblestone_wall")
        sblock(lx, 69, lz, "lantern")

section("CONNECTOR PLAZA TO DOME NORTH OPENING")
# Local z 0..10 aligns with world Z -85..-75 after dz=-85; local x 42..102
# aligns with world X -13..47 after dx=-55 (the dome's north opening).
fset((42, 63, 0), (102, 63, 10), "gray_concrete")


# ------------------------------------------------------------
# BUILD THE 3x3 GRID
# ------------------------------------------------------------
SKYSCRAPERS = {
    (0, 0): (120, "light_gray_concrete", "light_blue_stained_glass", "white_concrete"),
    (2, 0): (150, "white_concrete", "glass", "light_gray_concrete"),
    (1, 1): (180, "light_gray_concrete", "cyan_stained_glass", "black_concrete"),
    (0, 2): (110, "smooth_quartz", "glass", "light_gray_concrete"),
    (2, 2): (140, "light_gray_concrete", "blue_stained_glass", "white_concrete"),
}

HOUSES = {
    (1, 0): ("oak", "red", "light"),
    (0, 1): ("birch", "light_blue", "dark"),
    (2, 1): ("cherry", "pink", "light"),
    (1, 2): ("spruce", "green", "dark"),
}

for col in range(3):
    for row in range(3):
        px = col * STEP
        pz = -(row * STEP) - PLOT + 1
        key = (col, row)
        if key in SKYSCRAPERS:
            total_h, facade, glass, mullion = SKYSCRAPERS[key]
            skyscraper(px, pz, total_h, facade, glass, mullion)
        elif key in HOUSES:
            wood, color, appliance = HOUSES[key]
            house(px, pz, wood, color, appliance)


with open("city.schema", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote city.schema")
