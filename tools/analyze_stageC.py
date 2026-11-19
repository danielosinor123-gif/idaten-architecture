"""Stage C (Kaggle T4 run) analysis: per-material bus propagation metrics.

Inputs (pulled to data/stageC_kaggle/run_<mat>/deck.out/):
  table.txt   -- columns: t, mx, my, mz, then 8 probe columns of
                 region-averaged my over x cells [200+200p, 280+200p),
                 y cells [0,80)  (x = 10+10p um, 50 nm cells), every 20 ps
  mStart.ovf / Finish.ovf -- full snapshots (2000 x 160 x 1 @ 50 nm)

Deck geometry (tools/decks/idaten_stageC_template.mx3):
  100 um x 8 um bus, 64 NiFe elements at x = 60..72.6 um, CPW antenna at
  x = 0.05 um, 1.70 GHz burst 1 mT in t = 0.5..3 ns, run 4 ns.

Per material, measured here (S):
  f_dom    dominant frequency of probe my (FFT, t in [3,4] ns ring-down)
  t_arr[p] arrival time of the wave packet at probe p (max of smoothed
           |my| in t in [0.5,4] ns)  ->  v_g from linear fit x(p) vs t_arr
  l_env    envelope decay length from ln(peak |my|) vs x over the probes
Outputs data/stageC_kaggle/stageC_summary.json.
"""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ovf_extract import read_ovf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(ROOT, "data", "stageC_kaggle")
OUT_JSON = os.path.join(SC, "stageC_summary.json")

CELL = 50e-9
NX, NY = 2000, 160
NPROBE = 8
PROBE_X_UM = [10.0 + 10.0 * p for p in range(NPROBE)]   # probe centre ~ x0+2 um
DRIVE_F0_GHZ = 1.70   # (L) deck drive frequency


def load_table(path):
    rows = []
    with open(path) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            rows.append([float(v) for v in line.split()])
    return np.array(rows)


def smooth(y, w):
    k = np.ones(w) / w
    return np.convolve(y, k, mode="same")


def fft_dom(t, y, f_lo=0.2e9, f_hi=8e9):
    dt = float(np.median(np.diff(t)))
    n = len(t)
    yu = y - y.mean()
    F = np.abs(np.fft.rfft(yu * np.hanning(n)))
    f = np.fft.rfftfreq(n, dt)
    keep = (f >= f_lo) & (f <= f_hi)
    i = np.argmax(F[keep])
    return float(f[keep][i])


def analyze_material(mat, deckout):
    tab = load_table(os.path.join(deckout, "table.txt"))
    t = tab[:, 0]
    probes = tab[:, 4:4 + NPROBE]          # after t, mx, my, mz
    res = {"material": mat, "table_rows": int(len(t)),
           "t_span_ns": float((t[-1] - t[0]) * 1e9)}

    # ring-down spectrum per probe 0 and 7 (near/far)
    sel = (t >= 3.0e-9)
    res["f_dom_probe0_GHz"] = round(fft_dom(t[sel], probes[sel, 0]) / 1e9, 4)
    res["f_dom_probe7_GHz"] = round(fft_dom(t[sel], probes[sel, 7]) / 1e9, 4)

    # bandpass each probe to the drive band and use its RMS as the local
    # wave amplitude; robust against cycle-to-cycle phase noise
    dt = float(np.median(np.diff(t)))
    def bandpass(y):
        yu = y - y.mean()
        n = len(y)
        F = np.fft.rfft(yu)
        f = np.fft.rfftfreq(n, dt)
        F[(f < 0.5e9) | (f > 4.0e9)] = 0
        return np.fft.irfft(F, n)

    bp = np.array([bandpass(probes[:, p]) for p in range(NPROBE)]).T   # (nt, nprobe)
    rms = np.sqrt((bp ** 2).mean(axis=0))
    res["probe_rms"] = [round(float(v), 8) for v in rms]

    # v_g from cross-correlation lag between adjacent probes (10 um apart).
    # lag in samples -> dt -> v_g = 10 um / dt; use the median over pairs.
    x = np.array(PROBE_X_UM) * 1e-6
    lags, vgs = [], []
    for p in range(NPROBE - 1):
        a, b = bp[:, p], bp[:, p + 1]
        if np.std(a) < 1e-9 or np.std(b) < 1e-9:
            continue
        c = np.correlate(b - b.mean(), a - a.mean(), mode="full")
        lag = int(np.argmax(c) - (len(a) - 1))     # samples of b rel. to a
        lags.append(lag)
        if lag != 0:
            vgs.append(10e-6 / (abs(lag) * dt) * (1 if lag > 0 else -1))
    res["xcorr_lag_samples"] = lags
    if vgs:
        res["v_g_xcorr_m_s"] = round(float(np.median(vgs)), 1)
        res["v_g_xcorr_spread_m_s"] = round(float(np.std(vgs)), 1)
        res["v_g_pairs"] = len(vgs)
    else:
        res["v_g_xcorr_m_s"] = None
        res["v_g_xcorr_spread_m_s"] = None
        res["v_g_pairs"] = 0
    res["v_g_note"] = ("cross-correlation lag medians; spread comparable to "
                       "median means v_g is not resolved at this SNR/window")

    # decay length: ln(rms) vs x over probes with rms > 5% of probe0
    good = rms > 0.05 * rms[0]
    if good.sum() >= 3 and rms[good].min() > 0:
        B = np.vstack([x[good], np.ones(int(good.sum()))]).T
        m, c = np.linalg.lstsq(B, np.log(rms[good]), rcond=None)[0]
        res["l_env_um"] = round(float(-1.0 / m) * 1e6, 2) if m < 0 else None
        res["l_env_fit_nprobes"] = int(good.sum())
    else:
        res["l_env_um"] = None
        res["l_env_fit_nprobes"] = int(good.sum())

    # spatial envelope from Finish.ovf: RMS over y of |my| per x
    fin = os.path.join(deckout, "Finish.ovf")
    if os.path.isfile(fin):
        hdr, arr, _ = read_ovf(fin, order="xyz")   # (nz, ny, nx, vd), x-fastest
        my = arr[0, :, :, 1]
        env = np.sqrt((my ** 2).mean(axis=0))       # per x cell (axis 0 = y)
        xs = (hdr.get("xbase", hdr["xmin"] + hdr["xstepsize"] / 2)
              + hdr["xstepsize"] * np.arange(NX))
        # decay over x = 10..95 um, excluding element rows? use bus rows y<40
        myb = arr[0, :40, :, 1]
        envb = np.sqrt((myb ** 2).mean(axis=0))
        m = (xs >= 10e-6) & (xs <= 95e-6)
        if envb[m].min() > 0:
            B = np.vstack([xs[m], np.ones(m.sum())]).T
            s, _ = np.linalg.lstsq(B, np.log(envb[m]), rcond=None)[0]
            res["l_finish_bus_um"] = round(float(-1.0 / s) * 1e6, 2) if s < 0 else None
        res["env_bus_peak_x_um"] = round(float(xs[int(np.argmax(envb))]) * 1e6, 2)
    return res


def main():
    runs = sorted(glob.glob(os.path.join(SC, "run_*")))
    if not runs:
        print("no run_* dirs under", SC)
        sys.exit(2)
    out = {"deck": "tools/decks/idaten_stageC_template.mx3",
           "drive_f0_GHz_L": DRIVE_F0_GHZ, "materials": {}}
    for d in runs:
        mat = os.path.basename(d).replace("run_", "")
        deckout = os.path.join(d, "deck.out")
        if not os.path.isfile(os.path.join(deckout, "table.txt")):
            print("skip", mat, "(no table.txt)")
            continue
        r = analyze_material(mat, deckout)
        out["materials"][mat] = r
        print(json.dumps(r, indent=1))
    with open(OUT_JSON, "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote", OUT_JSON)


if __name__ == "__main__":
    main()
