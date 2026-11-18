"""Wave-propagation metrics from mumax3 OVF snapshot series.

Geometry (all lab decks): grid 2000 x 160 x 1, cell 50 nm x 50 nm x 1.2 um.
  x = propagation axis, 100 um long, CPW launch at the x = 0.05 um edge
  (see PROVENANCE.md section 2.3 and tools/probe_antenna.py)
  y = transverse axis, 8 um wide.
Data ordering in mumax3 OVF: y fastest, then x, then z (components consecutive).

Outputs per snapshot:
  envelope(x) = RMS over y of |m_y|   (phase-insensitive wave amplitude)
  peak_x     = argmax envelope
  peak_amp   = max envelope
Derived:
  wave velocity  = d(peak_x)/d(t)
  decay length   = 1 / slope of ln(envelope) vs x over a fitted tail window
"""
import os
import re
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ovf_extract import read_ovf

# mumax3 grid memory layout is y-fastest -> reshape (nz, nx, ny, vd) then transpose
def load_field(path):
    hdr, arr, mk = read_ovf(path, order="yxz")   # -> (nz, ny, nx, vd)
    return hdr, arr[0, :, :, 0], mk               # -> (ny, nx)


def snapshot_series(paths):
    """paths sorted by snapshot index -> list of (index, time_s, x_um, envelope, raw)."""
    out = []
    for p in paths:
        base = os.path.basename(p)
        m = re.search(r"(\d{6})\.ovf$", base)
        idx = int(m.group(1)) if m else -1
        hdr, f, _ = load_field(p)
        t = 0.0
        d = hdr.get("Desc", "")
        mt = re.search(r"time:\s*([0-9.eE+-]+)\s*s", d)
        if mt:
            t = float(mt.group(1))
        nx = hdr["xnodes"]
        x = (hdr.get("xbase", hdr["xmin"] + hdr["xstepsize"] / 2)
             + hdr["xstepsize"] * np.arange(nx)) * 1e6
        env = np.sqrt((f ** 2).mean(axis=0))
        out.append((idx, t, x, env, f))
    out.sort(key=lambda r: r[0])
    return out


def decay_length(x_um, env, x_min_um, x_max_um, min_amp_frac=0.05):
    """Log-linear fit of ln(env) vs x over [x_min, x_max]; returns (ell_um, r2, npts)."""
    sel = (x_um >= x_min_um) & (x_um <= x_max_um)
    if sel.sum() < 10:
        return float('nan'), float('nan'), 0
    xs, es = x_um[sel], env[sel]
    good = es > 0
    if good.sum() < 10:
        return float('nan'), float('nan'), 0
    xs, es = xs[good], es[good]
    if es.max() > 0 and es.min() / es.max() < min_amp_frac:
        pass
    A = np.vstack([xs, np.ones_like(xs)]).T
    coef, *_ = np.linalg.lstsq(A, np.log(es), rcond=None)
    slope = coef[0]
    pred = A @ coef
    ss_res = float(((np.log(es) - pred) ** 2).sum())
    ss_tot = float(((np.log(es) - np.log(es).mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    ell = -1.0 / slope if slope < 0 else float('inf')
    return float(ell), r2, int(len(xs))


def wavefront(series, t_from, t_to):
    """Linear fit of peak_x vs t over a time window -> (v_m_per_s, intercept_um, n, r2)."""
    pts = [(t, x[np.argmax(e)]) for (_, t, x, e, _) in series
           if t_from <= t <= t_to]
    if len(pts) < 4:
        return float('nan'), float('nan'), 0, float('nan')
    T = np.array([p[0] for p in pts]); X = np.array([p[1] for p in pts])
    A = np.vstack([T, np.ones_like(T)]).T
    coef, *_ = np.linalg.lstsq(A, X, rcond=None)
    pred = A @ coef
    ss_res = float(((X - pred) ** 2).sum())
    ss_tot = float(((X - X.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    return float(coef[0] * 1e6), float(coef[1]), len(pts), r2   # um/s -> m/s


if __name__ == "__main__":
    d = sys.argv[1]
    paths = sorted([os.path.join(d, f) for f in os.listdir(d) if f.endswith(".ovf")])
    series = snapshot_series(paths)
    print(f"{len(series)} snapshots from {d}")
    print(f"{'idx':>4} {'t(ns)':>9} {'peak_x(um)':>11} {'peak_amp':>10} "
          f"{'env@10':>9} {'env@30':>9} {'env@50':>9} {'env@80':>9}")
    for idx, t, x, env, f in series:
        def at(xu):
            i = int(np.argmin(np.abs(x - xu)))
            return env[i]
        print(f"{idx:>4} {t*1e9:>9.4f} {x[np.argmax(env)]:>11.3f} {env.max():>10.5f} "
              f"{at(10):>9.5f} {at(30):>9.5f} {at(50):>9.5f} {at(80):>9.5f}")
