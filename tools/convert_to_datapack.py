#!/usr/bin/env python3
import re
import os

MAX_FILL = 32768

def dominant_block(spec):
    """Return the highest-weight block from a weighted spec like '75%stone_bricks,15%cobblestone'."""
    if '%' not in spec:
        return spec.strip()
    best_pct, best_block = 0, spec.strip()
    for part in spec.split(','):
        m = re.match(r'(\d+)%(\S+)', part.strip())
        if m and int(m.group(1)) > best_pct:
            best_pct, best_block = int(m.group(1)), m.group(2)
    return best_block

def fill_commands(x1, y1, z1, x2, y2, z2, block, replace=None):
    """Generate /fill commands, splitting if the region exceeds MAX_FILL blocks."""
    ax, bx = min(x1, x2), max(x1, x2)
    ay, by = min(y1, y2), max(y1, y2)
    az, bz = min(z1, z2), max(z1, z2)
    dx, dy, dz = bx - ax + 1, by - ay + 1, bz - az + 1

    if dx * dy * dz <= MAX_FILL:
        suffix = f" replace {replace}" if replace else ""
        return [f"fill {ax} {ay} {az} {bx} {by} {bz} {block}{suffix}"]

    cmds = []
    # Split along the longest axis
    if dx >= dy and dx >= dz:
        chunk = max(1, MAX_FILL // (dy * dz))
        for cx in range(ax, bx + 1, chunk):
            cmds += fill_commands(cx, ay, az, min(cx + chunk - 1, bx), by, bz, block, replace)
    elif dy >= dz:
        chunk = max(1, MAX_FILL // (dx * dz))
        for cy in range(ay, by + 1, chunk):
            cmds += fill_commands(ax, cy, az, bx, min(cy + chunk - 1, by), bz, block, replace)
    else:
        chunk = max(1, MAX_FILL // (dx * dy))
        for cz in range(az, bz + 1, chunk):
            cmds += fill_commands(ax, ay, cz, bx, by, min(cz + chunk - 1, bz), block, replace)
    return cmds

def parse_schema(path):
    commands = []
    pos1 = pos2 = None

    with open(path) as f:
        lines = f.readlines()

    for raw in lines:
        line = raw.strip()
        if not line or line.startswith('#'):
            continue

        m = re.match(r'/pos1\s+(-?\d+),(\d+),(-?\d+)', line)
        if m:
            pos1 = tuple(int(x) for x in m.groups())
            continue

        m = re.match(r'/pos2\s+(-?\d+),(\d+),(-?\d+)', line)
        if m:
            pos2 = tuple(int(x) for x in m.groups())
            continue

        m = re.match(r'//set\s+(.+)', line)
        if m and pos1 and pos2:
            block = dominant_block(m.group(1))
            commands += fill_commands(*pos1, *pos2, block)
            continue

        m = re.match(r'//replace\s+(\S+)\s+(\S+)', line)
        if m and pos1 and pos2:
            old_block, new_block = m.group(1), m.group(2)
            commands += fill_commands(*pos1, *pos2, new_block, replace=old_block)
            continue

        # setblock — already vanilla
        if line.startswith('/setblock'):
            commands.append(line[1:])
            continue

    return commands

def build_datapack(commands, out_dir, namespace):
    fn_dir = os.path.join(out_dir, "data", namespace, "function")
    os.makedirs(fn_dir, exist_ok=True)

    # pack.mcmeta (pack_format 71, wide supported_formats range for 1.21.x compatibility)
    mcmeta = os.path.join(out_dir, "pack.mcmeta")
    with open(mcmeta, "w") as f:
        f.write('{\n  "pack": {\n    "pack_format": 71,\n    "supported_formats": [1, 9999],\n    "description": "%s build commands"\n  }\n}\n' % namespace)

    # build.mcfunction
    fn_path = os.path.join(fn_dir, "build.mcfunction")
    with open(fn_path, "w") as f:
        f.write("\n".join(commands) + "\n")

    print(f"Datapack written to: {out_dir}")
    print(f"Commands generated: {len(commands)}")
    print(f"\nUsage:")
    print(f"  1. Copy '{os.path.basename(out_dir)}' into your world's datapacks/ folder")
    print(f"  2. Load the world (or /reload if already open)")
    print(f"  3. Run: /function {namespace}:build")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: convert_to_datapack.py <schema_file>")
        sys.exit(1)
    schema_path = sys.argv[1]
    namespace = os.path.splitext(os.path.basename(schema_path))[0]
    out_dir = os.path.join(os.path.dirname(os.path.abspath(schema_path)), namespace)
    commands = parse_schema(schema_path)
    build_datapack(commands, out_dir, namespace)
