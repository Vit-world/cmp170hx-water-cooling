#!/usr/bin/env python3
"""Generate printable spacer test blanks: plain boxes, binary STL, millimetres, one face on Z=0.

  make_spacer_blanks.py                       # 15 x 7 mm footprint, heights 3.0 ... 6.5 mm in 0.5 mm steps
  make_spacer_blanks.py --length 12 --width 8 --heights 2,2.5,3
  make_spacer_blanks.py --plate               # additionally write ONE file with all blanks laid out in a grid

Standard library only. Output files: blank_<L>x<W>x<H>.stl (decimal point written as 'p', e.g. blank_15x7x3p5.stl).
"""
import argparse, os, struct


def fmt(v):
    s = f"{v:g}"
    return s.replace(".", "p")


def box_triangles(l, w, h):
    # 8 corners, 12 triangles (2 per face), outward normals, counter-clockwise seen from outside
    v = {(x, y, z): (x * l, y * w, z * h) for x in (0, 1) for y in (0, 1) for z in (0, 1)}
    faces = [  # (normal, four corners in CCW order seen from outside)
        ((0, 0, -1), [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)]),
        ((0, 0, 1), [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]),
        ((0, -1, 0), [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)]),
        ((0, 1, 0), [(0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)]),
        ((-1, 0, 0), [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)]),
        ((1, 0, 0), [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)]),
    ]
    tris = []
    for n, c in faces:
        a, b, c3, d = (v[k] for k in c)
        tris.append((n, a, b, c3))
        tris.append((n, a, c3, d))
    return tris


def write_stl(path, l, w, h):
    write_triangles(path, f"spacer blank {l}x{w}x{h} mm", box_triangles(l, w, h))


def write_plate(path, l, w, heights, cols=4, gap=5.0):
    """All blanks in one STL, laid out in a grid on the Z=0 plane with `gap` mm between them."""
    tris = []
    for i, h in enumerate(heights):
        dx, dy = (i % cols) * (l + gap), (i // cols) * (w + gap)
        for n, a, b, c in box_triangles(l, w, h):
            sh = lambda p: (p[0] + dx, p[1] + dy, p[2])
            tris.append((n, sh(a), sh(b), sh(c)))
    write_triangles(path, f"spacer blanks plate {len(heights)} pcs", tris)


def write_triangles(path, header, tris):
    with open(path, "wb") as f:
        f.write(header.encode().ljust(80, b"\0"))
        f.write(struct.pack("<I", len(tris)))
        for n, a, b, c in tris:
            f.write(struct.pack("<12fH", *n, *a, *b, *c, 0))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--length", type=float, default=15)
    ap.add_argument("--width", type=float, default=7)
    ap.add_argument("--heights", default="3,3.5,4,4.5,5,5.5,6,6.5", help="comma separated heights in mm")
    ap.add_argument("--out", default=".")
    ap.add_argument("--plate", action="store_true", help="also write one plate file with all blanks")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    heights = [float(x) for x in a.heights.split(",")]
    if a.plate:
        p = os.path.join(a.out, f"blanks_plate_{fmt(a.length)}x{fmt(a.width)}.stl")
        write_plate(p, a.length, a.width, heights)
        print(p)
    for h in heights:
        p = os.path.join(a.out, f"blank_{fmt(a.length)}x{fmt(a.width)}x{fmt(h)}.stl")
        write_stl(p, a.length, a.width, h)
        print(p)


if __name__ == "__main__":
    main()
