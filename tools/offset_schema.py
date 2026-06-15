#!/usr/bin/env python3
import re
import sys

def offset_schema(in_path, out_path, dx, dy, dz):
    with open(in_path) as f:
        lines = f.readlines()

    out_lines = []
    for line in lines:
        stripped = line.rstrip('\n')

        m = re.match(r'(/pos[12]\s+)(-?\d+),(-?\d+),(-?\d+)', stripped)
        if m:
            prefix, x, y, z = m.groups()
            x, y, z = int(x) + dx, int(y) + dy, int(z) + dz
            out_lines.append(f"{prefix}{x},{y},{z}\n")
            continue

        m = re.match(r'(/setblock\s+)(-?\d+)\s+(-?\d+)\s+(-?\d+)(\s+.*)', stripped)
        if m:
            prefix, x, y, z, rest = m.groups()
            x, y, z = int(x) + dx, int(y) + dy, int(z) + dz
            out_lines.append(f"{prefix}{x} {y} {z}{rest}\n")
            continue

        out_lines.append(line)

    with open(out_path, 'w') as f:
        f.writelines(out_lines)

if __name__ == "__main__":
    in_path, out_path = sys.argv[1], sys.argv[2]
    dx, dy, dz = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    offset_schema(in_path, out_path, dx, dy, dz)
    print(f"Wrote offset schema to {out_path} (dx={dx}, dy={dy}, dz={dz})")
