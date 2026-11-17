"""Generate the Idaten magnonic **concept mask** (GDSII) with gdstk.

    python tools/generate_concept_mask.py --out gds/idaten_concept_mask

WHAT THIS IS
    A 5 mm x 5 mm die layout that encodes the magnonic execution topology:
    a bus waveguide, an array of switchable nanomagnets at pitch `a`, CPW
    launch / detect structures, and optical alignment marks.

WHAT THIS IS NOT
    This is NOT a manufacturable mask set. No PDK exists for patterning
    hematite (alpha-Fe2O3) or LiNbO3, so every layer here is a *design intent*
    layer with stated dimensions, not a foundry-legal layer. It must never be
    presented alongside the SKY130 open-flow GDS without that distinction.

The layer numbers follow the magnonic layer map carried over from the previous
chip's mask plan (MgGPU_tapeout/mask/mask_layers.csv) so the concept is
traceable, but the GDS is written from scratch here.
"""
from __future__ import annotations

import argparse
import json
import os

import gdstk

# ---------------------------------------------------------------- layer map
# gdstk 1.x takes layers as (layer_number, datatype) tuples.
# key: (datatype, purpose, material/process assumption)
LAYERS = {
    10: (0, "MG_WG",     "YIG or hematite bus waveguide core"),
    11: (0, "MG_PHASE",  "phase shifter / tuning region"),
    12: (0, "MG_NL",     "non-linear pinning-site array (the weight landscape)"),
    13: (0, "MG_SOT",    "spin-orbit / spin-torque transducer"),
    14: (0, "MG_MTJ",    "switchable nanomagnet cell (the M_k write target)"),
    15: (0, "MG_RAIL",   "configuration rail (C_k distribution)"),
    20: (0, "CPW",       "coplanar waveguide, launch and detect"),
    30: (0, "ALIGN",     "optical alignment marks"),
    40: (0, "DIE",       "die outline / scribe"),
    50: (0, "LABEL",     "non-fab annotation"),
}

# ---------------------------------------------------------------- geometry
DIE = 5000.0          # um, 5 mm x 5 mm test die
CELL = 5.0            # um
BUS_W = 2.0           # um bus waveguide width
BUS_Y = 2500.0        # um bus centreline
ARRAY_X0 = 1200.0     # um start of the nanomagnet array
ARRAY_X1 = 3800.0
ARRAY_PITCH = 0.2     # um = 200 nm, matching the published precedent
ARRAY_N = int((ARRAY_X1 - ARRAY_X0) / ARRAY_PITCH) + 1
CELL_L = 0.1          # um = 100 nm long nanomagnet
CELL_W = 0.02         # um = 20 nm wide nanomagnet
GUIDE_L = 3.0         # um long guide between array rows
GUIDE_W = 0.05        # um = 50 nm guide width

CPW_W = 2.1          # um centre conductor width (published CPW w_L = 2.1 um)
CPW_GAP = 1.8         # um gap to ground
CPW_LEN = 800.0       # um


def build() -> gdstk.Library:
    lib = gdstk.Library("IDATEN_CONCEPT_MASK", unit=1e-6, precision=1e-9)
    top = lib.new_cell("IDATEN")

    def L(key):
        dt, _, _ = LAYERS[key]
        return (key, dt)

    def rect(x0, y0, x1, y1, key):
        # gdstk.rectangle(corner1, corner2) - CORNERS, not deltas
        p = gdstk.rectangle((x0, y0), (x1, y1),
                            layer=L(key)[0], datatype=L(key)[1])
        top.add(p)

    def label(x, y, s, size, key):
        # gdstk.text() returns a list of polygons
        for p in gdstk.text(s, size, (x, y),
                            layer=L(key)[0], datatype=L(key)[1]):
            top.add(p)

    # ---- die outline
    rect(0, 0, DIE, DIE, 40)

    # ---- bus waveguide along x at y = BUS_Y
    rect(0, BUS_Y - BUS_W / 2, DIE, BUS_Y + BUS_W / 2, 10)

    # ---- phase shifter / tuning region (marked band over the bus)
    rect(ARRAY_X0 - 100, BUS_Y - BUS_W / 2 - 0.3,
         ARRAY_X1 + 100, BUS_Y + BUS_W / 2 + 0.3, 11)

    # ---- configuration rails above and below the bus
    for yoff in (+40, -40):
        rect(200, BUS_Y + yoff - 1.5, ARRAY_X1 + 200, BUS_Y + yoff + 1.5, 15)

    # ---- nanomagnet array: 100 nm x 20 nm elements on a 200 nm pitch.
    #      These are the M_k write targets; their state is the persistent result.
    n_mtj = 0
    for i in range(ARRAY_N):
        x = ARRAY_X0 + i * ARRAY_PITCH
        if x + CELL_L > ARRAY_X1:
            break
        rect(x, BUS_Y - CELL_W / 2, x + CELL_L, BUS_Y + CELL_W / 2, 14)
        n_mtj += 1

    # ---- non-linear pinning landscape: rows of small scatterers that both
    #      diffract the wave and pin the written domain walls.
    #      Coarser than the nanomagnet array: 1 um pitch, 50 nm square.
    n_nl = 0
    nl_pitch = 1.0
    nl_rows = 4
    for row in range(nl_rows):
        y = BUS_Y - 6.0 + row * GUIDE_L * 0.25
        i = 0
        while True:
            x = ARRAY_X0 + i * nl_pitch
            if x + 0.05 > ARRAY_X1:
                break
            rect(x, y, x + 0.05, y + 0.05, 12)
            n_nl += 1
            i += 1

    # ---- spin-torque transducers: edge launch (left) and edge detect (right)
    for xend, direction in ((CPW_LEN, +1), (DIE - CPW_LEN, -1)):
        rect(xend, BUS_Y - CPW_W / 2, xend + direction * 80, BUS_Y + CPW_W / 2, 13)
        # CPW: centre conductor + two grounds
        rect(xend, BUS_Y - CPW_W / 2, xend + direction * CPW_LEN, BUS_Y + CPW_W / 2, 20)
        for s in (-1, +1):
            gy = BUS_Y + s * (CPW_W / 2 + CPW_GAP)
            rect(xend, gy - CPW_W, xend + direction * CPW_LEN, gy + CPW_W, 20)

    # ---- optical alignment marks (crosses) at the four corners
    for cx, cy in ((300, 300), (DIE - 300, 300),
                   (300, DIE - 300), (DIE - 300, DIE - 300)):
        rect(cx - 60, cy - 4, cx + 60, cy + 4, 30)
        rect(cx - 4, cy - 60, cx + 4, cy + 60, 30)

    # ---- annotation text (non-fabrication)
    label(60, DIE - 120, "IDATEN Ce100 CONCEPT MASK - NO PDK", 40, 50)
    label(60, DIE - 180, "hematite/LiNbO3 patterning: no process design kit exists", 22, 50)
    label(60, DIE - 220,
          f"a={int(ARRAY_PITCH*1000)}nm  cell={int(CELL_L*1000)}x{int(CELL_W*1000)}nm  N={n_mtj}",
          22, 50)

    # NOTE: Library.new_cell() already registers the cell in the library.
    # Do NOT call lib.add(top) as well - that duplicates it and makes the
    # GDS unreadable ("A cell with name ... already exists").
    return lib, n_mtj, n_nl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="gds/idaten_concept_mask")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    lib, n_mtj, n_nl = build()
    gds_path = os.path.join(args.out, "idaten_concept_mask.gds")
    lib.write_gds(gds_path)

    meta = {
        "file": os.path.basename(gds_path),
        "label": "CONCEPT MASK - no PDK exists for hematite/LiNbO3 patterning",
        "not_a_manufacturable_mask_set": True,
        "die_um": [DIE, DIE],
        "grid_um": CELL,
        "unit_m": 1e-6,
        "precision_m": 1e-9,
        "bus_width_um": BUS_W,
        "array_pitch_um": ARRAY_PITCH,
        "array_elements": n_mtj,
        "pinning_sites": n_nl,
        "cell_nm": [int(CELL_L * 1000), int(CELL_W * 1000)],
        "cpw_centre_um": CPW_W,
        "layers": {str(k): {"datatype": v[0], "purpose": v[1], "assumption": v[2]}
                   for k, v in LAYERS.items()},
    }
    with open(os.path.join(args.out, "concept_mask_meta.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    print(json.dumps(meta, indent=2))
    print(f"\nwrote {gds_path} ({os.path.getsize(gds_path)/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
