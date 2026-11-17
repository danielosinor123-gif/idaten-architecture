'''Print the exact geometry of a mumax3 CPW antenna mask (OVF, valuedim=3).

This is the CORRECTED structural probe. The earlier version reduced the 3-D
raster with `mask.any(axis=...)`, which collapses the wrong axes and therefore
reported a transposed orientation - a diamond-shaped launch was published as
"a stripe at the y = 0 edge, x = 2-6 um". That wrong statement survived in
README.md and PROVENANCE.md until the mask was re-rendered directly.

The rule this script enforces: read the geometry off the 2-D mask raster, never
off a reduction of a 3-D array.

    python tools/probe_antenna.py path/to/antenna.ovf

Reference geometry for the lab antenna (verified 2026-11-16):

    filled cells          662
    non-empty rows        80  (y indices 40-119)
    bounding box          x [0.050, 0.500] um,  y [2.050, 6.000] um
    spine                 1 cell (50 nm) wide at x = 0.050 um, full height
    flare                 x_max: 0.100 um at y=2.05 -> 0.500 um over
                          y ~ 3.55-4.55 -> back to the spine at y=6.00
'''
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ovf_extract import read_ovf


def main(path):
    hdr, arr, mk = read_ovf(path, order="yxz")     # (nz, ny, nx, vd)
    mag = np.linalg.norm(arr[0, :, :, :3], axis=-1)  # (ny, nx)
    ny, nx = mag.shape

    x0 = (hdr.get("xbase", 0) + hdr.get("xstepsize", 0) / 2) * 1e6
    y0 = (hdr.get("ybase", 0) + hdr.get("ystepsize", 0) / 2) * 1e6
    dx = hdr["xstepsize"] * 1e6
    dy = hdr["ystepsize"] * 1e6

    ys, xs = np.where(mag > 0.5)
    print(f"file            : {path}")
    print(f"grid (ny, nx)   : {ny} x {nx}")
    print(f"cell (dx, dy)   : {dx:.3f} x {dy:.3f} um")
    print(f"filled cells    : {len(xs)}")
    print(f"non-empty rows  : {len(set(ys.tolist()))}  "
          f"(y indices {ys.min()}..{ys.max()})")
    print(f"bbox            : x [{x0 + xs.min() * dx:.3f}, {x0 + xs.max() * dx:.3f}] um"
          f"   y [{y0 + ys.min() * dy:.3f}, {y0 + ys.max() * dy:.3f}] um")

    # Is there a continuous 1-cell spine at the low-x edge, over the rows the
    # antenna occupies? (The grid extends beyond the antenna, so the test is
    # over the occupied rows only.)
    occ_rows = np.where(mag.max(axis=1) > 0.5)[0]
    spine_cols = [c for c in range(nx) if np.all(mag[occ_rows, c] > 0.5)]
    print(f"full-height spine columns (over the {len(occ_rows)} occupied rows): "
          f"{spine_cols if spine_cols else 'none'}")

    rows = sorted(set(ys.tolist()))
    print("\nrow-by-row extent:")
    step = max(1, len(rows) // 12)
    for yi in rows[::step] + ([rows[-1]] if (len(rows) - 1) % step else []):
        r = np.where(mag[yi] > 0.5)[0]
        print(f"   yi={yi:4d} y={y0 + yi * dy:7.3f} um  n={len(r):4d}  "
              f"x=[{x0 + r.min() * dx:7.3f}, {x0 + r.max() * dx:7.3f}] um")

    # ASCII map (rows = y, top = high y), for visual confirmation
    print("\nASCII map (rows = y, top = high y; cols = x):")
    step_y = max(1, ny // 80)
    step_x = max(1, nx // 150)
    for yi in range(ny - 1, -1, -step_y):
        row = mag[yi]
        s = "".join("#" if row[xi] > 0.5 else "." for xi in range(0, nx, step_x))
        if "#" in s:
            print(f" y={y0 + yi * dy:6.3f} |{s}|")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
