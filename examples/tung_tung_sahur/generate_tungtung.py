#!/usr/bin/env python3
"""Generate tung_tung_sahur.schema - a large, highly detailed voxel statue
of the "Tung Tung Tung Sahur" meme character: a tall cylindrical wooden
drum creature (kentongan) with rope-bound segments, big staring eyes,
an open toothy mouth, articulated arms, bare feet with toes, and a
two-part baseball bat (pentungan) gripped in its hand."""

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
lines.append("# TUNG TUNG TUNG SAHUR - large detailed wooden drum creature")
lines.append("# Body: radius 9, height 48 (Y68-115). Total ~57 blocks tall.")
lines.append("# ============================================================")

section("PLAZA / PLATFORM")
pos((-11, 63, -11), (11, 63, 11))
lines.append("//set stone_bricks")
lines.append("")
for x1, x2, z1, z2 in [(-11, -9, -11, -9), (-11, -9, 9, 11), (9, 11, -11, -9), (9, 11, 9, 11)]:
    pos((x1, 63, z1), (x2, 63, z2))
    lines.append("//set air")
    lines.append("")
pos((-7, 63, -7), (7, 63, 7))
lines.append("//set andesite")
lines.append("")
for x1, x2, z1, z2 in [(-7, -6, -7, -6), (-7, -6, 6, 7), (6, 7, -7, -6), (6, 7, 6, 7)]:
    pos((x1, 63, z1), (x2, 63, z2))
    lines.append("//set stone_bricks")
    lines.append("")


section("LEGS / FEET BASE")
pos((-5, 64, -5), (5, 67, 5))
lines.append("//set oak_log[axis=y]")
lines.append("")
for x, z in [(-5, -5), (-5, 5), (5, -5), (5, 5)]:
    pos((x, 64, z), (x, 67, z))
    lines.append("//set air")
    lines.append("")

section("TOES")
for x in (-3, -1, 1, 3):
    lines.append(f"/setblock {x} 64 6 oak_planks")
    lines.append(f"/setblock {x} 65 6 white_concrete")


section("BODY - main drum cylinder")
pos((-9, 68, -9), (9, 115, 9))
lines.append("//set oak_log[axis=y]")

section("DRUM SEGMENT BANDS")
for y, material in [(76, "stripped_oak_log[axis=y]"),
                     (84, "black_wool"),
                     (92, "stripped_oak_log[axis=y]"),
                     (100, "black_wool"),
                     (108, "stripped_oak_log[axis=y]")]:
    pos((-9, y, -9), (9, y, 9))
    lines.append(f"//set {material}")
    lines.append("")

section("TOP CAP")
pos((-9, 115, -9), (9, 115, 9))
lines.append("//set stripped_oak_log[axis=y]")


section("FACE - eyes, eyebrows, mouth")
# Left eye
pos((-6, 96, 9), (-3, 99, 9))
lines.append("//set white_concrete")
lines.append("")
pos((-4, 96, 9), (-3, 97, 9))
lines.append("//set black_concrete")
lines.append("")
lines.append("/setblock -3 98 9 white_wool")
lines.append("")
# Right eye
pos((3, 96, 9), (6, 99, 9))
lines.append("//set white_concrete")
lines.append("")
pos((3, 96, 9), (4, 97, 9))
lines.append("//set black_concrete")
lines.append("")
lines.append("/setblock 4 98 9 white_wool")
lines.append("")
# Eyebrows
pos((-6, 100, 9), (-3, 100, 9))
lines.append("//set black_concrete")
lines.append("")
pos((3, 100, 9), (6, 100, 9))
lines.append("//set black_concrete")
lines.append("")
# Mouth recess
pos((-5, 86, 8), (5, 90, 8))
lines.append("//set black_concrete")
lines.append("")
# Mouth outer rim
pos((-5, 85, 9), (5, 91, 9))
lines.append("//set black_concrete")
lines.append("")
# Teeth
pos((-5, 90, 9), (5, 90, 9))
lines.append("//set white_concrete")
lines.append("")
pos((-5, 86, 9), (5, 86, 9))
lines.append("//set white_concrete")
lines.append("")
# Tongue
pos((-2, 85, 9), (2, 85, 9))
lines.append("//set red_concrete")


section("BODY CHAMFER (round the cylinder)")
for x1, x2, z1, z2 in [(-9, -7, -9, -7), (-9, -7, 7, 9), (7, 9, -9, -7), (7, 9, 7, 9)]:
    pos((x1, 68, z1), (x2, 115, z2))
    lines.append("//set air")
    lines.append("")


section("EAR STUDS")
pos((-3, 116, 0), (-3, 118, 0))
lines.append("//set oak_log[axis=y]")
lines.append("")
pos((3, 116, 0), (3, 118, 0))
lines.append("//set oak_log[axis=y]")
lines.append("")
lines.append("/setblock -3 119 0 quartz_block")
lines.append("/setblock 3 119 0 quartz_block")


section("ARMS")
# Right arm (holding bat) - shoulder, forearm, hand
pos((9, 104, -1), (14, 106, 1))
lines.append("//set oak_log[axis=x]")
lines.append("")
pos((13, 75, -1), (15, 104, 1))
lines.append("//set oak_log[axis=y]")
lines.append("")
pos((12, 73, -2), (16, 75, 2))
lines.append("//set oak_planks")
lines.append("")
# Left arm - resting stub with hand
pos((-13, 104, -1), (-9, 106, 1))
lines.append("//set oak_log[axis=x]")
lines.append("")
pos((-15, 103, -2), (-13, 107, 2))
lines.append("//set oak_planks")


section("BASEBALL BAT (pentungan)")
pos((15, 64, 0), (15, 78, 0))
lines.append("//set stripped_spruce_log[axis=y]")
lines.append("")
pos((15, 64, 0), (15, 67, 0))
lines.append("//set black_wool")
lines.append("")
pos((14, 78, 0), (15, 100, 1))
lines.append("//set spruce_log[axis=y]")
lines.append("")
pos((14, 101, 0), (15, 101, 1))
lines.append("//set stripped_spruce_log[axis=y]")


section("STREETLAMP (bus stop detail)")
pos((24, 64, -9), (24, 72, -9))
lines.append("//set cobblestone_wall")
lines.append("")
pos((22, 72, -9), (24, 72, -9))
lines.append("//set oak_fence")
lines.append("")
lines.append("/setblock 22 71 -9 lantern")
lines.append("/setblock 23 70 -9 dark_oak_planks")


with open("tung_tung_sahur.schema", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote tung_tung_sahur.schema")
