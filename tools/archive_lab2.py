"""Archive mumax3 lab output to a compact, re-analysable form (v2).

Per deck writes one .npz containing:
  t       (T,)         snapshot times [s]
  E_x     (T,nx)       RMS over y of |m_y|  -> phase-insensitive wave envelope
  P_x     (T,nx)       max over y of |m_y|  -> peak amplitude
  map_y   (T,ny2,nx2)  down-sampled |m_y| maps (row=y, col=x), float16
  x_um, y_um, metrics

Unreadable / truncated OVF files are skipped and reported.
Metrics are computed in the same pass so the archive is self-describing.
"""
import json
import os
import re
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ovf_extract import read_ovf

Y_DECIM = 8          # y down-sampling (160 -> 20)
X_DECIM = 4          # x down-sampling (2000 -> 500) for the 2-D maps only


def parse_deck(path):
    txt = open(path, "r", errors="replace").read()
    out = {"deck_text": txt}
    for key in ("Msat", "Aex", "alpha", "B_ext", "SetGridSize", "SetCellSize"):
        m = re.search(rf"^\s*{key}\s*=\s*(.+)$", txt, re.M)
        if m:
            out[key] = m.group(1).strip()
    m = re.search(r"f0\s*:=\s*([0-9.eE+-]+)", txt)
    if m:
        out["f0_Hz"] = float(m.group(1))
    return out


def local_peak(E, win=21):
    pad = np.pad(E, win // 2, mode="edge")
    return np.array([pad[i:i + win].max() for i in range(len(E))])


def fit_ell(x, E, lo, hi):
    sel = (x >= lo) & (x <= hi)
    xs, es = x[sel], E[sel]
    good = es > 1e-12
    xs, es = xs[good], es[good]
    if len(xs) < 8:
        return float('nan'), float('nan'), 0
    A = np.vstack([xs, np.ones_like(xs)]).T
    coef, *_ = np.linalg.lstsq(A, np.log(es), rcond=None)
    pred = A @ coef
    ssr = ((np.log(es) - pred) ** 2).sum()
    sst = ((np.log(es) - np.log(es).mean()) ** 2).sum()
    r2 = 1 - ssr / sst if sst > 0 else float('nan')
    ell = -1.0 / coef[0] if coef[0] < 0 else float('inf')
    return float(ell), float(r2), int(len(xs))


def metrics_from(x, t, E, P):
    """Derive the quantities the repo cites, with explicit method + conditioning."""
    m = {}
    Ebar = E.mean(axis=0)
    Pbar = P.mean(axis=0)
    for label, prof in (("rms", Ebar), ("peak", Pbar)):
        for wname, (lo, hi) in (("x10_45", (10, 45)), ("x5_45", (5, 45)),
                                ("x15_45", (15, 45)), ("x10_50", (10, 50))):
            ell, r2, n = fit_ell(x, prof, lo, hi)
            m[f"ell_{label}_{wname}_um"] = ell
            m[f"r2_{label}_{wname}"] = r2
            m[f"n_{label}_{wname}"] = n
        ell, r2, n = fit_ell(x, local_peak(prof), 10, 45)
        m[f"ell_{label}_localpeak_x10_45_um"] = ell
        m[f"r2_{label}_localpeak_x10_45"] = r2
    # wavefront: track argmax of the smoothed envelope in time
    sm = np.array([np.convolve(e, np.ones(41) / 41, mode="same") for e in E])
    px = x[np.argmax(sm, axis=1)]
    ok = np.isfinite(t)
    if ok.sum() > 10:
        A = np.vstack([t[ok], np.ones(ok.sum())]).T
        coef, *_ = np.linalg.lstsq(A, px[ok], rcond=None)
        pred = A @ coef
        ssr = ((px[ok] - pred) ** 2).sum()
        sst = ((px[ok] - px[ok].mean()) ** 2).sum()
        m["wavefront_slope_um_per_s"] = float(coef[0])
        m["wavefront_r2"] = float(1 - ssr / sst) if sst > 0 else float('nan')
    # interference contrast of the time-averaged envelope in the active region
    sel = (x >= 8) & (x <= 95)
    seg = Ebar[sel]
    m["contrast_peak_to_valley"] = float((seg.max() - seg.min()) / (seg.max() + 1e-30))
    m["node_x_um"] = float(x[sel][int(np.argmin(seg))])
    m["antinode_x_um"] = float(x[sel][int(np.argmax(seg))])
    m["t_first_ns"] = float(t[0] * 1e9)
    m["t_last_ns"] = float(t[-1] * 1e9)
    m["dt_snapshot_ns"] = float(np.median(np.diff(t)) * 1e9) if len(t) > 1 else float('nan')
    return m


def archive_deck(deck_dir, out_npz):
    files = sorted([f for f in os.listdir(deck_dir) if f.endswith(".ovf")])
    good, bad = [], []
    for fn in files:
        try:
            hdr, arr, mk = read_ovf(os.path.join(deck_dir, fn), order="yxz")
            good.append((fn, hdr, arr))
        except Exception as e:
            bad.append((fn, str(e)[:80]))
    if not good:
        return {"snapshots": 0, "bad_files": bad, "metrics": {}}

    T = len(good)
    nx = good[0][1]["xnodes"]; ny = good[0][1]["ynodes"]
    hdr0 = good[0][1]
    x_um = ((hdr0.get("xbase", 0) + hdr0["xstepsize"] * np.arange(nx))) * 1e6
    y_um = ((hdr0.get("ybase", 0) + hdr0["ystepsize"] * np.arange(ny))) * 1e6

    E = np.zeros((T, nx), np.float32)
    P = np.zeros((T, nx), np.float32)
    M = np.zeros((T, ny // Y_DECIM, nx // X_DECIM), np.float16)
    t = np.zeros(T, np.float64)

    for i, (fn, hdr, arr) in enumerate(good):
        m = arr[0, :, :, 0].astype(np.float32)
        d = hdr.get("Desc", "")
        mt = re.search(r"time:\s*([0-9.eE+-]+)\s*s", d)
        t[i] = float(mt.group(1)) if mt else np.nan
        E[i] = np.sqrt((m.astype(np.float64) ** 2).mean(axis=0))
        P[i] = np.abs(m).max(axis=0)
        M[i] = np.abs(m[::Y_DECIM, ::X_DECIM])

    met = metrics_from(x_um, t, E, P)
    np.savez_compressed(out_npz, t=t, E_x=E, P_x=P, map_y=M,
                        x_um=x_um.astype(np.float32), y_um=y_um.astype(np.float32),
                        meta_xnodes=np.int64(nx), meta_ynodes=np.int64(ny),
                        meta_znodes=np.int64(hdr0.get("znodes", 1)),
                        meta_y_decim=np.int64(Y_DECIM), meta_x_decim=np.int64(X_DECIM))
    return {"snapshots": T, "bad_files": bad, "metrics": met,
            "archive_MB": round(os.path.getsize(out_npz) / 1e6, 2)}


if __name__ == "__main__":
    root, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    summary = {}
    for name in sorted(os.listdir(root)):
        d = os.path.join(root, name)
        if not os.path.isdir(d) or not name.endswith(".out"):
            continue
        deck = name[:-4]
        t0 = time.time()
        info = archive_deck(d, os.path.join(outdir, deck + ".npz"))
        mx3 = os.path.join(root, deck + ".mx3")
        if os.path.exists(mx3):
            info["deck"] = parse_deck(mx3)
        info["seconds"] = round(time.time() - t0, 1)
        summary[deck] = info
        mt = info.get("metrics", {})
        print(f"ARCHIVED {deck}: snaps={info['snapshots']} bad={len(info.get('bad_files', []))} "
              f"MB={info.get('archive_MB')} ell_rms[10-45]={mt.get('ell_rms_x10_45_um')} "
              f"r2={mt.get('r2_rms_x10_45')} contrast={mt.get('contrast_peak_to_valley')}", flush=True)
    with open(os.path.join(outdir, "_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print("DONE", flush=True)
