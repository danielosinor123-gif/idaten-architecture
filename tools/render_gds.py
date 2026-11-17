"""Inspect and render the Idaten concept mask with KLayout.

    python tools/render_gds.py --gds gds/idaten_concept_mask/idaten_concept_mask.gds \
                               --out figures

Produces:
  * a layer census (shape counts, bounding boxes) printed to stdout and JSON
  * three figures: full die, CPW launch zoom, and the nanometre-scale
    nanomagnet array zoom
"""
from __future__ import annotations

import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
import numpy as np

import klayout.db as db

LAYER_COLORS = {
    10: "#4C78A8",  # MG_WG
    11: "#F58518",  # MG_PHASE
    12: "#54A24B",  # MG_NL
    13: "#E45756",  # MG_SOT
    14: "#B279A2",  # MG_MTJ
    15: "#9D755D",  # MG_RAIL
    20: "#79706E",  # CPW
    30: "#000000",  # ALIGN
    40: "#DDDDDD",  # DIE
    50: "#7A7A7A",  # LABEL
}
LAYER_NAMES = {
    10: "MG_WG bus", 11: "MG_PHASE", 12: "MG_NL pinning", 13: "MG_SOT transducer",
    14: "MG_MTJ nanomagnet", 15: "MG_RAIL config", 20: "CPW",
    30: "ALIGN", 40: "DIE", 50: "LABEL",
}


def load_shapes(path):
    ly = db.Layout()
    ly.read(path)
    dbu = ly.dbu            # database unit in micrometres (e.g. 0.001 = 1 nm)
    out = {}
    top = ly.top_cell()
    for li in ly.layer_indices():
        info = ly.get_info(li)
        polys = []
        for it in top.begin_shapes_rec(li):
            sh = it.shape()
            if sh.is_polygon() or sh.is_box() or sh.is_path():
                pts = sh.polygon.each_point_hull()
                polys.append([(p.x * dbu, p.y * dbu) for p in pts])
            elif sh.is_text():
                t = sh.text
                polys.append([(t.x * dbu, t.y * dbu), (t.x * dbu, t.y * dbu)])
        out[(info.layer, info.datatype)] = polys
    return ly, out


def census(ly, shapes):
    rows = []
    for (lnum, dt), polys in sorted(shapes.items()):
        if not polys:
            continue
        xs = [p[0] for poly in polys for p in poly]
        ys = [p[1] for poly in polys for p in poly]
        rows.append({
            "layer": lnum, "datatype": dt, "name": LAYER_NAMES.get(lnum, "?"),
            "shapes": len(polys),
            "bbox_um": [min(xs), min(ys), max(xs), max(ys)],
            "size_um": [max(xs) - min(xs), max(ys) - min(ys)],
        })
    return rows


def draw(ax, shapes, layers, xlim=None, ylim=None, lw_scale=1.0):
    """Draw layers in the given order (first = bottom)."""
    z = 1
    for lnum in layers:
        for (l, dt), polys in shapes.items():
            if l != lnum or not polys:
                continue
            for poly in polys:
                ax.add_patch(MplPolygon(poly, closed=True,
                                        facecolor=LAYER_COLORS.get(l, "none"),
                                        edgecolor=LAYER_COLORS.get(l, "none"),
                                        linewidth=lw_scale, zorder=z))
        z += 1
    ax.set_xlim(*(xlim or (0, 5000)))
    ax.set_ylim(*(ylim or (0, 5000)))
    ax.set_aspect("equal")
    ax.ticklabel_format(style="plain", useOffset=False)
    ax.set_xlabel("x (um)")
    ax.set_ylabel("y (um)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gds", default="gds/idaten_concept_mask/idaten_concept_mask.gds")
    ap.add_argument("--out", default="figures")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    ly, shapes = load_shapes(args.gds)
    rows = census(ly, shapes)
    print(f"{'layer':>6} {'dt':>3}  {'name':<20} {'shapes':>7}  bbox size (um)")
    for r in rows:
        print(f"{r['layer']:>6} {r['datatype']:>3}  {r['name']:<20} {r['shapes']:>7}  "
              f"{r['size_um'][0]:.3f} x {r['size_um'][1]:.3f}")
    with open(os.path.join(args.out, "concept_mask_census.json"), "w") as fh:
        json.dump({"gds": os.path.basename(args.gds), "dbu_um": ly.dbu, "layers": rows}, fh, indent=2)

    # ---- Fig 1: full die.  DIE is drawn first as a filled backdrop.
    fig, ax = plt.subplots(figsize=(9, 9))
    draw(ax, shapes, [40, 20, 10, 15, 13, 14, 12, 11, 30])
    ax.set_title("Idaten Ce100 magnonic concept mask — full 5 mm x 5 mm die\n"
                 "CONCEPT MASK: no PDK exists for hematite / LiNbO3 patterning",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, "concept_mask_full_die.png"), dpi=170)
    plt.close(fig)

    # ---- Fig 2: CPW launch + transducer zoom
    fig, ax = plt.subplots(figsize=(10, 6))
    draw(ax, shapes, [10, 11, 13, 20], xlim=(700, 1100), ylim=(2350, 2650))
    ax.set_title("Concept mask: edge launch — CPW centre conductor (2.1 um) + "
                 "spin-torque transducer\n"
                 "the wave enters the bus from the die edge", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, "concept_mask_launch_zoom.png"), dpi=190)
    plt.close(fig)

    # ---- Fig 3: nanometre-scale nanomagnet array zoom
    fig, ax = plt.subplots(figsize=(10, 4))
    draw(ax, shapes, [10, 12, 14], xlim=(1200.00, 1200.60), ylim=(2499.94, 2500.06))
    ax.set_title("Concept mask: nanomagnet array at nanometre scale — "
                 "100 nm x 20 nm elements on a = 200 nm pitch\n"
                 "these cells are the M_k (persistent result) write targets",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, "concept_mask_array_zoom_nm.png"), dpi=200)
    plt.close(fig)

    print("\nwrote figures to", args.out)


if __name__ == "__main__":
    main()
