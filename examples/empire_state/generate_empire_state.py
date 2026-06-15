#!/usr/bin/env python3
"""Generate empire_state.schema at ~0.5 scale, matching the real ESB setback
sequence (floors 5/21/25/30/72/81/85/86 + mast/antenna), with banded windows,
steel mullions, and an open glass-floored atrium running through every tier."""

FACADE = "70%smooth_quartz,30%white_concrete"
MULLION = "light_gray_concrete"
TRIM = "black_concrete"
GLASS = "black_stained_glass"

# name, half-width (X), half-depth (Z), yfloor, yroof, floor material
TIERS = [
    dict(name="T1", hw=32, hd=14, yfloor=64,  yroof=78,  floor="smooth_quartz",     trim=True),
    dict(name="T2", hw=27, hd=12, yfloor=78,  yroof=106, floor="light_gray_concrete"),
    dict(name="T3", hw=24, hd=10, yfloor=106, yroof=113, floor="light_gray_concrete"),
    dict(name="T4", hw=20, hd=9,  yfloor=113, yroof=122, floor="light_gray_concrete"),
    dict(name="T5", hw=16, hd=7,  yfloor=122, yroof=199, floor="light_gray_concrete"),
    dict(name="T6", hw=14, hd=6,  yfloor=199, yroof=215, floor="light_gray_concrete"),
    dict(name="T7", hw=11, hd=5,  yfloor=215, yroof=222, floor="light_gray_concrete"),
    dict(name="T8", hw=9,  hd=4,  yfloor=222, yroof=224, floor="light_gray_concrete"),
]

# Observation deck (real floor 86) - open-air with railing
DECK = dict(name="T9", hw=8, hd=3, yfloor=224, yroof=227, floor="smooth_quartz")

# Mast / antenna (tapering, real floors 87-102 + pinnacle)
MAST_LOWER = dict(hw=5, hd=2, yfloor=227, yroof=242)
MAST_UPPER = dict(hw=2, hd=1, yfloor=242, yroof=256)
ANTENNA_TOP = 256
ANTENNA_PINNACLE = 287
BEACON_Y = 288

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
lines.append("# EMPIRE STATE BUILDING v3 - realistic-scale recreation")
lines.append("# ~0.5 scale (1 block ~= 2m). 9 setback tiers matching real")
lines.append("# floors 5/21/25/30/72/81/85/86, plus tapering mast & antenna.")
lines.append("# Footprint: 65x29 at base, ~225 blocks tall (Y64-Y288)")
lines.append("# ============================================================")

# Overall clear + plaza, sized to the largest tier (T1)
section("1. CLEAR BUILD AREA")
pos((-34, 63, -16), (34, 290, 16))
lines.append("//set air")

section("2. PLAZA")
pos((-34, 63, -16), (34, 63, 16))
lines.append("//set light_gray_concrete")


def build_tier(tier):
    name = tier['name']
    hw, hd = tier['hw'], tier['hd']
    yfloor, yroof = tier['yfloor'], tier['yroof']
    xmin, xmax, zmin, zmax = -hw, hw, -hd, hd
    height = yroof - yfloor

    section(f"{name} ({xmax - xmin + 1}x{zmax - zmin + 1}, Y{yfloor}-{yroof})")

    # Solid shell
    pos((xmin, yfloor, zmin), (xmax, yroof, zmax))
    lines.append(f"//set {FACADE}")
    lines.append("")

    # Hollow interior
    pos((xmin + 1, yfloor + 1, zmin + 1), (xmax - 1, yroof - 1, zmax - 1))
    for part in FACADE.split(','):
        lines.append(f"//replace {part.split('%')[1]} air")
    lines.append("")

    # Granite-style base trim (T1 only) - perimeter ring at ground level
    if tier.get('trim'):
        pos((xmin, yfloor, zmin), (xmax, yfloor, zmax))
        for part in FACADE.split(','):
            lines.append(f"//replace {part.split('%')[1]} {TRIM}")
        lines.append("")

    # Floor
    pos((xmin + 1, yfloor, zmin + 1), (xmax - 1, yfloor, zmax - 1))
    lines.append(f"//set {tier['floor']}")
    lines.append("")

    # Open glass atrium (5x5 shaft through every floor)
    if hw - 1 >= 2 and hd - 1 >= 2:
        pos((-2, yfloor, -2), (2, yfloor, 2))
        lines.append("//set glass")
        lines.append("")

    # Corner pillars (steel verticals)
    for cx, cz in [(xmin, zmin), (xmin, zmax), (xmax, zmin), (xmax, zmax)]:
        pos((cx, yfloor, cz), (cx, yroof, cz))
        lines.append(f"//set {MULLION}")
        lines.append("")

    if height >= 5:
        # Window band with steel mullions every 4 blocks
        band_y1, band_y2 = yfloor + 2, yroof - 1

        pos((xmin + 1, band_y1, zmin), (xmax - 1, band_y2, zmin))
        lines.append(f"//set {GLASS}")
        lines.append("")
        pos((xmin + 1, band_y1, zmax), (xmax - 1, band_y2, zmax))
        lines.append(f"//set {GLASS}")
        lines.append("")
        pos((xmin, band_y1, zmin + 1), (xmin, band_y2, zmax - 1))
        lines.append(f"//set {GLASS}")
        lines.append("")
        pos((xmax, band_y1, zmin + 1), (xmax, band_y2, zmax - 1))
        lines.append(f"//set {GLASS}")
        lines.append("")

        for x in range(xmin + 1, xmax, 4):
            pos((x, band_y1, zmin), (x, band_y2, zmin))
            lines.append(f"//set {MULLION}")
            lines.append("")
            pos((x, band_y1, zmax), (x, band_y2, zmax))
            lines.append(f"//set {MULLION}")
            lines.append("")

        for z in range(zmin + 1, zmax, 4):
            pos((xmin, band_y1, z), (xmin, band_y2, z))
            lines.append(f"//set {MULLION}")
            lines.append("")
            pos((xmax, band_y1, z), (xmax, band_y2, z))
            lines.append(f"//set {MULLION}")
            lines.append("")
    else:
        # Short tier (T8) - glaze the whole wall between corner pillars
        pos((xmin + 1, yfloor + 1, zmin), (xmax - 1, yroof - 1, zmin))
        lines.append(f"//set {GLASS}")
        lines.append("")
        pos((xmin + 1, yfloor + 1, zmax), (xmax - 1, yroof - 1, zmax))
        lines.append(f"//set {GLASS}")
        lines.append("")
        pos((xmin, yfloor + 1, zmin + 1), (xmin, yroof - 1, zmax - 1))
        lines.append(f"//set {GLASS}")
        lines.append("")
        pos((xmax, yfloor + 1, zmin + 1), (xmax, yroof - 1, zmax - 1))
        lines.append(f"//set {GLASS}")
        lines.append("")


for tier in TIERS:
    build_tier(tier)


# ------------------------------------------------------------
# T9 - 86TH FLOOR OBSERVATION DECK (open-air w/ railing)
# ------------------------------------------------------------
hw, hd = DECK['hw'], DECK['hd']
yfloor, yroof = DECK['yfloor'], DECK['yroof']
xmin, xmax, zmin, zmax = -hw, hw, -hd, hd

section(f"T9 - OBSERVATION DECK ({xmax - xmin + 1}x{zmax - zmin + 1}, Y{yfloor}-{yroof})")

# Deck floor
pos((xmin, yfloor, zmin), (xmax, yfloor, zmax))
lines.append(f"//set {DECK['floor']}")
lines.append("")

# Open glass atrium continues up to the deck
pos((-2, yfloor, -2), (2, yfloor, 2))
lines.append("//set glass")
lines.append("")

# Solid roof (mast foundation)
pos((xmin, yroof, zmin), (xmax, yroof, zmax))
lines.append(f"//set {FACADE}")
lines.append("")

# Corner pillars
for cx, cz in [(xmin, zmin), (xmin, zmax), (xmax, zmin), (xmax, zmax)]:
    pos((cx, yfloor, cz), (cx, yroof, cz))
    lines.append(f"//set {MULLION}")
    lines.append("")

# Railing ring around the open deck
pos((xmin, yfloor + 1, zmin), (xmax, yfloor + 1, zmin))
lines.append("//set iron_bars")
lines.append("")
pos((xmin, yfloor + 1, zmax), (xmax, yfloor + 1, zmax))
lines.append("//set iron_bars")
lines.append("")
pos((xmin, yfloor + 1, zmin + 1), (xmin, yfloor + 1, zmax - 1))
lines.append("//set iron_bars")
lines.append("")
pos((xmax, yfloor + 1, zmin + 1), (xmax, yfloor + 1, zmax - 1))
lines.append("//set iron_bars")


# ------------------------------------------------------------
# MAST & ANTENNA
# ------------------------------------------------------------
section("MAST & ANTENNA")

hw, hd = MAST_LOWER['hw'], MAST_LOWER['hd']
pos((-hw, MAST_LOWER['yfloor'], -hd), (hw, MAST_LOWER['yroof'], hd))
lines.append("//set 70%light_gray_concrete,30%iron_block")
lines.append("")

hw, hd = MAST_UPPER['hw'], MAST_UPPER['hd']
pos((-hw, MAST_UPPER['yfloor'], -hd), (hw, MAST_UPPER['yroof'], hd))
lines.append("//set 70%light_gray_concrete,30%iron_block")
lines.append("")

pos((0, ANTENNA_TOP, 0), (0, ANTENNA_PINNACLE, 0))
lines.append("//set lightning_rod[facing=up]")
lines.append("")

lines.append(f"/setblock 0 {BEACON_Y} 0 sea_lantern")


# ------------------------------------------------------------
# GRAND ENTRANCE (south face, T1)
# ------------------------------------------------------------
section("GRAND ENTRANCE (south face, T1)")
pos((-1, 64, 14), (1, 67, 14))
lines.append("//set air")
lines.append("")
pos((-1, 64, 14), (-1, 67, 14))
lines.append("//set black_stained_glass_pane")
lines.append("")
pos((1, 64, 14), (1, 67, 14))
lines.append("//set black_stained_glass_pane")
lines.append("")
pos((0, 66, 14), (0, 67, 14))
lines.append("//set black_stained_glass_pane")
lines.append("")
lines.append("/setblock 0 64 14 dark_oak_door[facing=south,half=lower]")
lines.append("/setblock 0 65 14 dark_oak_door[facing=south,half=upper]")
lines.append("")
pos((-2, 63, 15), (2, 63, 15))
lines.append("//set smooth_quartz_stairs[facing=north]")


# ------------------------------------------------------------
# LOBBY INTERIOR
# ------------------------------------------------------------
section("LOBBY INTERIOR")
for cx, cz in [(-20, -10), (20, -10), (-20, 10), (20, 10)]:
    pos((cx, 65, cz), (cx, 76, cz))
    lines.append("//set polished_andesite")
    lines.append("")

lines.append("/setblock -28 65 -12 lantern")
lines.append("/setblock 28 65 -12 lantern")
lines.append("/setblock -28 65 12 lantern")
lines.append("/setblock 28 65 12 lantern")


# ------------------------------------------------------------
# SETBACK TERRACE LIGHTING
# ------------------------------------------------------------
section("SETBACK TERRACE LIGHTING")
lines.append("/setblock -31 78 -13 sea_lantern")
lines.append("/setblock 31 78 -13 sea_lantern")
lines.append("/setblock -31 78 13 sea_lantern")
lines.append("/setblock 31 78 13 sea_lantern")
lines.append("")
lines.append("/setblock -15 122 -6 sea_lantern")
lines.append("/setblock 15 122 -6 sea_lantern")
lines.append("/setblock -15 122 6 sea_lantern")
lines.append("/setblock 15 122 6 sea_lantern")


with open("empire_state.schema", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote empire_state.schema")
