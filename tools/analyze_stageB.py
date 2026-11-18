'''Analyse the Stage B mumax3 output into a small committed summary.

    wsl -d Ubuntu-24.04 -u root -- bash -lc "python3 /mnt/c/Users/OSINOR~1/Downloads/idaten-architecture/tools/analyze_stageB.py /root/mumax/idaten_stageB.out /mnt/c/Users/OSINOR~1/Downloads/idaten-architecture"

Produces, in the repo:

  data/lab/stageB_summary.json     small metrics (S)
  data/lab/stageB_elements.csv     per-result-element mean amplitude (S)
  figures/01_stageB_pattern.png    the pattern at the result array (S)

IMPORTANT: this reads a spatial / time series of the transverse component. It
does NOT measure magnetisation reversal, a threshold, or switching error rate.
The honest outputs are: pattern contrast across the 64 coarse-grained NiFe
elements, and the bus envelope decay fit with r2. Nothing else is claimed.
'''
import glob
import json
import math
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ovf_extract import read_ovf

REPO = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
FIG = os.path.join(REPO, "figures")
DATA = os.path.join(REPO, "data", "lab")
os.makedirs(FIG, exist_ok=True)
os.makedirs(DATA, exist_ok=True)

SNAPS = sorted(glob.glob(os.path.join(OUT, "*.ovf")))
print("snapshots found:", len(SNAPS), "in", OUT)


def time_of(hdr, fallback):
    d = hdr.get("Desc") or hdr.get("desc") or ""
    m = re.search(r"time[:=]\s*([0-9.eE+-]+)\s*s?", d, re.IGNORECASE)
    if m:
        return float(m.group(1))
    return float(fallback)


rows = []
times = []
E_list = []
P_list = []
M_list = []
x_um = y_um = None
for i, p in enumerate(SNAPS):
    hdr, arr, _ = read_ovf(p, order="yxz")
    m = arr[0, :, :, 0].astype(np.float64)     # (ny, nx)
    if x_um is None:
        x_um = (hdr.get("xbase", 0) + hdr["xstepsize"] * np.arange(hdr["xnodes"])) * 1e6
        y_um = (hdr.get("ybase", 0) + hdr["ystepsize"] * np.arange(hdr["ynodes"])) * 1e6
    t = time_of(hdr, i)
    times.append(t)
    E_list.append(np.sqrt((m ** 2).mean(axis=0)))
    P_list.append(np.abs(m).max(axis=0))
    M_list.append(m)

E_t = np.asarray(E_list)
P_t = np.asarray(P_list)
order = np.argsort(times)
times = [times[i] for i in order]
E_t, P_t = E_t[order], P_t[order]
M_list = [M_list[i] for i in order]

# --- bus envelope decay fit (time-averaged), several windows ---------------
def fit_ell(x, E, lo, hi):
    sel = (x >= lo) & (x <= hi)
    xs, es = x[sel], E[sel]
    ok = es > 1e-12
    xs, es = xs[ok], es[ok]
    if len(xs) < 8:
        return {"ell_um": None, "r2": None, "n": int(ok.sum())}
    A = np.vstack([xs, np.ones_like(xs)]).T
    coef, *_ = np.linalg.lstsq(A, np.log(es), rcond=None)
    pred = A @ coef
    ssr = float(((np.log(es) - pred) ** 2).sum())
    sst = float(((np.log(es) - np.log(es).mean()) ** 2).sum())
    r2 = 1.0 - ssr / sst if sst > 0 else float("nan")
    ell = (-1.0 / coef[0]) if coef[0] < 0 else None
    return {"ell_um": (float(ell) if ell else None), "r2": float(r2),
            "n": int(ok.sum())}

E_mean = E_t.mean(axis=0)
fit_windows = {f"{lo}-{hi}": fit_ell(x_um, E_mean, lo, hi)
               for lo, hi in ((5, 45), (10, 45), (10, 50), (15, 45), (5, 90), (10, 95))}

# --- result array: 64 elements, 100 nm x 50 nm, pitch 200 nm, x = 60..72.6 um
last_n = min(10, len(M_list))
stack_last = np.stack(M_list[-last_n:], axis=0)   # (T, ny, nx)
amp_map = np.abs(stack_last).mean(axis=0)          # mean |m_y|, time-averaged

elem = []
for i in range(64):
    xc = 60.0 + i * 0.2
    xsel = (x_um >= xc - 0.05) & (x_um < xc + 0.05)
    ysel = (np.abs(y_um - 2.0) <= 0.025)
    if not xsel.any() or not ysel.any():
        continue
    elem.append({"index": i, "x_um": xc,
                 "amp": float(amp_map[np.ix_(ysel, xsel)].mean())})

amps = np.array([e["amp"] for e in elem])
contrast = float((amps.max() - amps.min()) / (amps.max() + amps.min())) if amps.size else None
n_above_half_max = int((amps > 0.5 * amps.max()).sum()) if amps.size else 0

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.2))
    ax = axes[0]
    ax.plot([e["x_um"] for e in elem], [e["amp"] for e in elem], "o-", color="#4C78A8")
    ax.set_xlabel("result element x position [µm]")
    ax.set_ylabel("time-averaged |m_y|")
    ax.set_title("Stage B: pattern across the 64 result elements", fontsize=10)
    ax.grid(alpha=.3)
    ax = axes[1]
    ax.plot(x_um, E_mean, color="#4C78A8")
    ax.set_yscale("log")
    ax.set_xlabel("x [µm]")
    ax.set_ylabel("bus envelope E(x) = rms |m_y|")
    ax.set_title("Stage B: time-averaged bus envelope", fontsize=10)
    ax.grid(alpha=.3, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "01_stageB_pattern.png"), dpi=170)
    plt.close(fig)
except Exception as e:
    print("matplotlib unavailable; skipping figure:", type(e).__name__, e)

summary = {
    "tag": "(S)",
    "snapshots": int(E_t.shape[0]),
    "t_first_ns": float(times[0] * 1e9),
    "t_last_ns": float(times[-1] * 1e9),
    "bus_decay_fits": fit_windows,
    "result_array_elements": len(elem),
    "result_array_contrast_over_elements": contrast,
    "n_elements_above_half_max": n_above_half_max,
    "note": ("Spatial pattern only. No switching threshold, reversal probability, "
             "or write-error rate is measured. Compare against the frozen target M, "
             "not against whatever this run produced."),
}

with open(os.path.join(DATA, "stageB_summary.json"), "w", encoding="utf-8") as fh:
    json.dump(summary, fh, indent=2)
with open(os.path.join(DATA, "stageB_elements.csv"), "w", encoding="utf-8") as fh:
    fh.write("index,x_um,amp\n")
    for e in elem:
        fh.write(f"{e['index']},{e['x_um']:.3f},{e['amp']:.8g}\n")

print(json.dumps(summary, indent=2))
