#!/usr/bin/env python3
"""Generate dome.schema - a massive glass enclosure surrounding the castle,
wizard's tower, Empire State Building, and blimp, with large N/S/E/W
openings and a shallow stepped glass pyramid roof."""

CX, CZ = 17, 35     # center of the enclosure (over the combined footprint)
R = 110             # cylinder radius - covers the ~100-block footprint
                     # half-diagonal AND the blimp's ~84-block offset
CYL_Y0, CYL_Y1 = 63, 312

GLASS = "glass"
RIB = "light_gray_concrete"

# (radius, y1, y2) for the stepped pyramid roof above the cylinder
CAP_BANDS = [
    (110, 312, 313),
    (82,  314, 315),
    (55,  316, 317),
    (27,  318, 318),
]
APEX_Y = 319

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

def ring(r, y1, y2, material):
    # North wall (Z = CZ - r)
    pos((CX - r, y1, CZ - r), (CX + r, y2, CZ - r))
    lines.append(f"//set {material}")
    lines.append("")
    # South wall (Z = CZ + r)
    pos((CX - r, y1, CZ + r), (CX + r, y2, CZ + r))
    lines.append(f"//set {material}")
    lines.append("")
    # East wall (X = CX + r)
    pos((CX + r, y1, CZ - r), (CX + r, y2, CZ + r))
    lines.append(f"//set {material}")
    lines.append("")
    # West wall (X = CX - r)
    pos((CX - r, y1, CZ - r), (CX - r, y2, CZ + r))
    lines.append(f"//set {material}")
    lines.append("")

lines.append("# ============================================================")
lines.append("# GLASS DOME ENCLOSURE")
lines.append(f"# Cylinder radius {R}, centered ({CX},{CZ}), Y{CYL_Y0}-{CYL_Y1}")
lines.append(f"# Stepped glass pyramid roof up to Y{APEX_Y}")
lines.append("# Encloses castle, wizard's tower, Empire State Building, blimp")
lines.append("# ============================================================")

section("CYLINDER WALLS")
ring(R, CYL_Y0, CYL_Y1, GLASS)

section("CORNER RIBS")
for x, z in [(CX - R, CZ - R), (CX - R, CZ + R), (CX + R, CZ - R), (CX + R, CZ + R)]:
    pos((x, CYL_Y0, z), (x, CYL_Y1, z))
    lines.append(f"//set {RIB}")
    lines.append("")

section("HORIZONTAL TRIM RINGS")
for trim_y in (150, 250):
    ring(R, trim_y, trim_y, RIB)

section("STEPPED GLASS ROOF")
for r, y1, y2 in CAP_BANDS:
    ring(r, y1, y2, GLASS)

lines.append(f"/setblock {CX} {APEX_Y} {CZ} glass")

section("CARDINAL OPENINGS")
# North (Z = CZ - R)
pos((CX - 30, 70, CZ - R), (CX + 30, 290, CZ - R))
lines.append("//set air")
lines.append("")
# South (Z = CZ + R)
pos((CX - 30, 70, CZ + R), (CX + 30, 290, CZ + R))
lines.append("//set air")
lines.append("")
# East (X = CX + R)
pos((CX + R, 70, CZ - 30), (CX + R, 290, CZ + 30))
lines.append("//set air")
lines.append("")
# West (X = CX - R)
pos((CX - R, 70, CZ - 30), (CX - R, 290, CZ + 30))
lines.append("//set air")


with open("dome.schema", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote dome.schema")
