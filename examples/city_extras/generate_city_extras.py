#!/usr/bin/env python3
"""Generate city_extras.schema - additive Phase 2 for the city district:
furnished office interiors inside each skyscraper, extra house decor
(home office, ceiling fans/lights, stepping-stone paths, doorbells,
post boxes, plates), plus many more streetlights and facade/roof accent
lighting. Uses the SAME local grid/coords as generate_city.py and is
offset the same way (dx=-55, dy=0, dz=-85) so it overlays exactly."""

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


# ------------------------------------------------------------
# SKYSCRAPER OFFICE INTERIORS
# ------------------------------------------------------------
OFFICE_WOODS = ["dark_oak", "oak", "spruce", "birch", "jungle"]

SKYSCRAPERS = {
    (0, 0): 120,
    (2, 0): 150,
    (1, 1): 180,
    (0, 2): 110,
    (2, 2): 140,
}

HOUSES = {
    (1, 0): ("oak", "red"),
    (0, 1): ("birch", "light_blue"),
    (2, 1): ("cherry", "pink"),
    (1, 2): ("spruce", "green"),
}


def furnish_floor(ix0, ix1, iz0, iz1, y, wood, ground=False):
    cx = (ix0 + ix1) // 2
    cz = (iz0 + iz1) // 2
    # Desk + chair + computer cluster near one corner
    sblock(ix0 + 1, y, iz0 + 1, f"{RF}:{wood}_desk")
    sblock(ix0 + 1, y, iz0 + 2, f"{RF}:{wood}_chair")
    sblock(ix0 + 1, y + 1, iz0 + 1, f"{RF}:computer")
    # Second desk cluster on the opposite side
    sblock(ix1 - 1, y, iz1 - 1, f"{RF}:{wood}_desk")
    sblock(ix1 - 1, y, iz1 - 2, f"{RF}:{wood}_chair")
    sblock(ix1 - 1, y + 1, iz1 - 1, f"{RF}:computer")
    # Storage cabinet
    sblock(ix0 + 1, y, iz1 - 1, f"{RF}:{wood}_storage_cabinet")
    # Ceiling light + lamp
    sblock(cx, y + 2, cz, f"{RF}:light_ceiling_light")
    sblock(ix1 - 1, y, iz0 + 1, f"{RF}:white_lamp")
    if ground:
        sblock(cx + 1, y, iz0 + 1, f"{RF}:recycle_bin")
        sblock(cx, y, iz1 - 1, f"{RF}:{wood}_storage_cabinet")


def skyscraper_interior(px, pz, total_h, wood):
    size1 = 32
    x0, x1 = px, px + size1 - 1
    z0, z1 = pz, pz + size1 - 1
    y1 = 64 + 30  # = 94, top of tier1

    section(f"SKYSCRAPER @ ({px},{pz}) tier1 offices")
    for y, ground in [(65, True), (73, False), (81, False), (89, False)]:
        furnish_floor(x0 + 1, x1 - 1, z0 + 1, z1 - 1, y, wood, ground)

    size2 = 22
    off = (size1 - size2) // 2
    x0b, x1b = px + off, px + off + size2 - 1
    z0b, z1b = pz + off, pz + off + size2 - 1
    y1b = 64 + total_h

    section(f"SKYSCRAPER @ ({px},{pz}) tier2 offices + penthouse")
    furnish_floor(x0b + 1, x1b - 1, z0b + 1, z1b - 1, y1, wood)
    furnish_floor(x0b + 1, x1b - 1, z0b + 1, z1b - 1, y1 + 8, wood)
    furnish_floor(x0b + 1, x1b - 1, z0b + 1, z1b - 1, y1b - 1, wood)

    # Roof-ring corner accent lights on the exposed tier1 roof
    section(f"SKYSCRAPER @ ({px},{pz}) roof ring lighting")
    for cx, cz in [(x0, z0), (x0, z1), (x1, z0), (x1, z1)]:
        sblock(cx, y1 + 1, cz, "sea_lantern")

    # Ground-level entrance lights, south face
    sblock(x0 + 1, 65, z0, "sea_lantern")
    sblock(x1 - 1, 65, z0, "sea_lantern")


for i, (key, total_h) in enumerate(SKYSCRAPERS.items()):
    col, row = key
    px = col * STEP
    pz = -(row * STEP) - PLOT + 1
    wood = OFFICE_WOODS[i % len(OFFICE_WOODS)]
    skyscraper_interior(px, pz, total_h, wood)


# ------------------------------------------------------------
# HOUSE EXTRA DECOR
# ------------------------------------------------------------
def house_extras(px, pz, wood, color):
    hx0, hx1 = px + 4, px + 23
    hz0, hz1 = pz + 4, pz + 17
    mx = (hx0 + hx1) // 2
    midz = (hz0 + hz1) // 2

    section(f"HOUSE @ ({px},{pz}) [{wood}/{color}] extra decor")
    # Home office nook in the living room (free corner)
    sblock(hx1 - 1, 65, hz0 + 2, f"{RF}:{wood}_desk")
    sblock(hx1 - 2, 65, hz0 + 2, f"{RF}:{wood}_chair")
    sblock(hx1 - 1, 66, hz0 + 2, f"{RF}:computer")
    # Ceiling fan + light in living room
    sblock(hx0 + 2, 67, hz0 + 2, f"{RF}:{wood}_light_ceiling_fan")
    # Plate on the kitchen table
    sblock(mx + 1, 66, midz + 2, f"{RF}:plate")
    # Storage cabinet in the bedroom free corner
    sblock(hx1 - 1, 69, hz0 + 2, f"{RF}:{wood}_storage_cabinet")
    # Ceiling lights upstairs
    sblock(hx0 + 2, 71, hz0 + 2, f"{RF}:{wood}_light_ceiling_fan")
    sblock(hx0 + 2, 71, midz + 2, f"{RF}:light_ceiling_light")
    # Doorbell + door mat at the entrance
    sblock(mx + 1, 66, hz0, f"{RF}:doorbell")
    sblock(mx, 65, pz + 3, f"{RF}:door_mat")
    # Post box next to the mailbox
    sblock(hx1 - 2, 65, hz1 + 1, f"{RF}:post_box")
    # Stepping-stone path from the gate to the front door
    for z in (pz + 1, pz + 2):
        sblock(mx, 65, z, f"{RF}:stone_stepping_stones")
    # Lanterns along the front hedge for yard lighting
    sblock(px + 8, 66, pz, "lantern")
    sblock(px + 23, 66, pz, "lantern")


for key, (wood, color) in HOUSES.items():
    col, row = key
    px = col * STEP
    pz = -(row * STEP) - PLOT + 1
    house_extras(px, pz, wood, color)


# ------------------------------------------------------------
# EXTRA STREETLIGHTS ALONG ROAD CORRIDORS
# ------------------------------------------------------------
section("ADDITIONAL STREETLIGHTS - VERTICAL ROAD CORRIDORS")
GRID_TOP_Z = 4
GRID_BOTTOM_Z = -(3 * STEP) + 4  # -152
for road_x in (PLOT + ROAD // 2, 2 * STEP + PLOT + ROAD // 2):  # 46, 98
    z = GRID_TOP_Z
    while z >= GRID_BOTTOM_Z:
        for lx in (road_x - (ROAD // 2 + 1), road_x + (ROAD // 2 + 1)):
            fset((lx, 64, z), (lx, 67, z), "cobblestone_wall")
            sblock(lx, 68, z, "lantern")
        z -= 13

section("ADDITIONAL STREETLIGHTS - HORIZONTAL ROAD CORRIDORS")
GRID_LEFT_X = -4
GRID_RIGHT_X = 3 * STEP - ROAD + 3  # 147
for road_z in (-(PLOT + ROAD // 2), -(2 * STEP + PLOT + ROAD // 2)):  # -46, -98
    x = GRID_LEFT_X
    while x <= GRID_RIGHT_X:
        for lz in (road_z - (ROAD // 2 + 1), road_z + (ROAD // 2 + 1)):
            fset((x, 64, lz), (x, 67, lz), "cobblestone_wall")
            sblock(x, 68, lz, "lantern")
        x += 13

section("CONNECTOR PLAZA LIGHTING")
for x in (40, 104):
    for z in (0, 10):
        fset((x, 63, z), (x, 67, z), "cobblestone_wall")
        sblock(x, 68, z, "sea_lantern")


with open("city_extras.schema", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote city_extras.schema")
