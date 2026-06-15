#!/usr/bin/env python3
"""Generate city_offices.schema - additive Phase 3 for the city district:
every single floor of every skyscraper (both tiers, lobby to penthouse)
gets a cubicle layout (desk + chair + computer + glass-pane divider) and a
wall-mounted TV. Uses the SAME local grid/coords as generate_city.py and is
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


def sblock(x, y, z, block):
    lines.append(f"/setblock {x} {y} {z} {block}")


OFFICE_WOODS = ["dark_oak", "oak", "spruce", "birch", "jungle"]

# (col,row) -> total_h
SKYSCRAPERS = {
    (0, 0): 120,
    (2, 0): 150,
    (1, 1): 180,
    (0, 2): 110,
    (2, 2): 140,
}


def cubicle(x, y, z, wood):
    sblock(x, y, z, f"{RF}:{wood}_desk")
    sblock(x, y, z + 1, f"{RF}:{wood}_chair")
    sblock(x, y + 1, z, f"{RF}:computer")
    sblock(x + 1, y, z, "glass_pane")


def furnish_office_floor(ix0, ix1, iz0, iz1, y, wood, num_cubicles):
    cx = (ix0 + ix1) // 2
    cz = (iz0 + iz1) // 2

    corners = [
        (ix0 + 1, iz0 + 1),
        (ix1 - 2, iz0 + 1),
        (ix0 + 1, iz1 - 2),
        (ix1 - 2, iz1 - 2),
    ]
    for cxp, czp in corners[:num_cubicles]:
        cubicle(cxp, y, czp, wood)

    # Wall-mounted TV on the south interior wall, ceiling light at center
    sblock(cx, y, iz0, f"{RF}:television")
    sblock(cx, y + 2, cz, f"{RF}:light_ceiling_light")


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


def skyscraper_offices(px, pz, total_h, wood):
    size1 = 32
    x0, x1 = px, px + size1 - 1
    z0, z1 = pz, pz + size1 - 1
    ix0, ix1 = x0 + 1, x1 - 1
    iz0, iz1 = z0 + 1, z1 - 1

    section(f"SKYSCRAPER @ ({px},{pz}) tier1 - all floors")
    for y in floor_levels_tier1():
        furnish_office_floor(ix0, ix1, iz0, iz1, y, wood, 4)

    size2 = 22
    off = (size1 - size2) // 2
    x0b, x1b = px + off, px + off + size2 - 1
    z0b, z1b = pz + off, pz + off + size2 - 1
    ix0b, ix1b = x0b + 1, x1b - 1
    iz0b, iz1b = z0b + 1, z1b - 1

    section(f"SKYSCRAPER @ ({px},{pz}) tier2 - all floors")
    for y in floor_levels_tier2(total_h):
        furnish_office_floor(ix0b, ix1b, iz0b, iz1b, y, wood, 2)


for i, (key, total_h) in enumerate(SKYSCRAPERS.items()):
    col, row = key
    px = col * STEP
    pz = -(row * STEP) - PLOT + 1
    wood = OFFICE_WOODS[i % len(OFFICE_WOODS)]
    skyscraper_offices(px, pz, total_h, wood)


with open("city_offices.schema", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote city_offices.schema")
