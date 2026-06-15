#!/usr/bin/env python3
"""Generate a blimp.schema - a large airship floating in the sky, moored
above the Empire State Building's antenna mast (its real-world intended
purpose). Centered on X=0,Y=0,Z=0; offset afterward to position it."""

ENVELOPE = "white_concrete"
STRIPE = "red_concrete"
FIN = "red_concrete"

# (x_start, x_end, radius)
SEGMENTS = [
    (-25, -21, 3),
    (-20, -16, 6),
    (-15, -11, 7),
    (-10, -6,  8),
    (-5,  -1,  8),
    (0,   4,   8),
    (5,   9,   8),
    (10,  14,  7),
    (15,  19,  6),
    (20,  24,  3),
]

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
lines.append("# BLIMP - large airship moored above the Empire State Building")
lines.append("# Length 50, max diameter 17, oriented along X")
lines.append("# ============================================================")

section("ENVELOPE - tapered octagonal hull")
for xs, xe, r in SEGMENTS:
    # Outer hull
    pos((xs, -r, -r), (xe, r, r))
    lines.append(f"//set {ENVELOPE}")
    lines.append("")

    # Chamfer the 4 corners to round the cross-section
    c = max(1, r // 2)
    if c < r:
        for ysign in (1, -1):
            for zsign in (1, -1):
                if ysign > 0:
                    y1, y2 = r - c + 1, r
                else:
                    y1, y2 = -r, -(r - c + 1)
                if zsign > 0:
                    z1, z2 = r - c + 1, r
                else:
                    z1, z2 = -r, -(r - c + 1)
                pos((xs, y1, z1), (xe, y2, z2))
                lines.append("//set air")
                lines.append("")

    # Hollow interior for the larger segments
    if r >= 6:
        ir = r - 2
        pos((xs, -ir, -ir), (xe, ir, ir))
        lines.append("//set air")
        lines.append("")

# Longitudinal racing stripe
section("RACING STRIPE")
pos((-25, -8, -1), (24, 8, 1))
lines.append(f"//replace {ENVELOPE} {STRIPE}")


# ------------------------------------------------------------
# TAIL FINS (cross pattern at the rear)
# ------------------------------------------------------------
section("TAIL FINS")
pos((-25, 4, -1), (-20, 7, 1))
lines.append(f"//set {FIN}")
lines.append("")
pos((-25, -7, -1), (-20, -4, 1))
lines.append(f"//set {FIN}")
lines.append("")
pos((-25, -1, 4), (-20, 1, 7))
lines.append(f"//set {FIN}")
lines.append("")
pos((-25, -1, -7), (-20, 1, -4))
lines.append(f"//set {FIN}")


# ------------------------------------------------------------
# NOSE LIGHT
# ------------------------------------------------------------
section("NOSE LIGHT")
lines.append("/setblock 25 0 0 sea_lantern")


# ------------------------------------------------------------
# GONDOLA (hanging cabin under the hull)
# ------------------------------------------------------------
section("GONDOLA")
pos((-5, -12, -2), (5, -9, 2))
lines.append("//set oak_planks")
lines.append("")

pos((-4, -11, -1), (4, -10, 1))
lines.append("//set air")
lines.append("")

pos((-4, -11, 2), (4, -11, 2))
lines.append("//set glass_pane")
lines.append("")
pos((-4, -11, -2), (4, -11, -2))
lines.append("//set glass_pane")
lines.append("")

# Support chains connecting gondola to hull
for x, z in [(-5, -2), (5, -2), (-5, 2), (5, 2)]:
    lines.append(f"/setblock {x} -8 {z} chain")


with open("blimp.schema", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote blimp.schema")
