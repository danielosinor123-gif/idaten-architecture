"""Stage D hematite (alpha-Fe2O3) AF bus arm (Kaggle T4, mumax+ 1.2.2) analysis.

Inputs (pulled to data/hematite_kaggle/hematite_full/):
  table.csv    comma-separated, header line starts with '#':
               t, nx_avg, ny_avg, nz_avg, Mx_avg, My_avg, Mz_avg,
               p0_nz..p7_nz, p0_ny..p7_ny, max_intracell_angle, e_total
               (8 x-probe region-averaged Neel-vector components, every 20 ps)
  neel_end.npz neel (3,nz,ny,nx), full (3,nz,ny,nx), t  at end of run
  run_meta.json  args, material inputs (L), probe_x_um, t_end, wall_s

Deck geometry (tools/decks/idaten_hematite_mumaxplus.py):
  100 um x 8 um x 100 nm hematite bus, 100 nm cells (1000 x 80 x 1),
  z-RF stripe launch at x ~ 1 um, 1.70 GHz / 1 mT burst 0.5..3 ns,
  fixed dt = 0.2 ps, run 8 ns. Drive frequency 1.70 GHz is (L) deck input.

Measured here (S):
  f_dom      dominant frequency of probe n_z ring-down (FFT, t in last 60%)
  probe_rms  band-passed (0.5..4 GHz) RMS of n_z per probe
  l_env_um   envelope decay length from ln(probe_rms) vs probe x
  v_g        group velocity from cross-correlation lags between adjacent
             probes (spacing from run_meta probe_x_um)
  max_intracell_angle_max  AFM order integrity check (should stay << 90 deg)
Comparisons printed against (E) v_g = gamma*sqrt(2*H_E*A_T) ~ 24 km/s and
(L) 10..23 km/s (Hamdi, Posva & Grundler, PRM 7, 054407 (2023)).

Output: data/hematite_kaggle/hematite_summary.json
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HD = os.path.join(ROOT, "data", "hematite_kaggle")
FULL = os.path.join(HD, "hematite_full")
OUT_JSON = os.path.join(HD, "hematite_summary.json")

DRIVE_F0_GHZ = 1.70          # (L) deck drive frequency
GAMMA = 1.760859644e11       # rad/s/T (L)
H_E_T = 1040.0               # (L) arXiv:2610.08030
A_T = 9.153e-18              # T m^2 (L) arXiv:2212.11887 (mu0 A = 9.153e-6 T um^2)
VG_PRED_M_S = GAMMA * np.sqrt(2.0 * H_E_T * A_T)   # (E) ~ 24 km/s


def load_table(path):
    with open(path) as fh:
        header = fh.readline().lstrip("# ").strip().split(",")
        rows = [[float(v) for v in line.split(",")]
                for line in fh if line.strip()]
    return header, np.array(rows)


def fft_dom(t, y, f_lo=0.05e9, f_hi=24e9):
    dt = float(np.median(np.diff(t)))
    n = len(t)
    yu = y - y.mean()
    F = np.abs(np.fft.rfft(yu * np.hanning(n)))
    f = np.fft.rfftfreq(n, dt)
    keep = (f >= f_lo) & (f <= min(f_hi, 0.95 / (2 * dt)))
    i = int(np.argmax(F[keep]))
    return float(f[keep][i])


def bandpass(t, y, f_lo, f_hi):
    dt = float(np.median(np.diff(t)))
    n = len(t)
    yu = y - y.mean()
    F = np.fft.rfft(yu)
    f = np.fft.rfftfreq(n, dt)
    F[(f < f_lo) | (f > min(f_hi, 0.95 / (2 * dt)))] = 0
    return np.fft.irfft(F, n)


def analyze(run_dir):
    header, tab = load_table(os.path.join(run_dir, "table.csv"))
    col = {name: i for i, name in enumerate(header)}
    t = tab[:, col["t"]]
    nprobe = sum(1 for name in header if name.startswith("p") and name.endswith("_nz"))
    pnz = tab[:, [col["p{}_nz".format(p)] for p in range(nprobe)]]
    pny = tab[:, [col["p{}_ny".format(p)] for p in range(nprobe)]]
    nzg = tab[:, col["nz_avg"]]
    angle = tab[:, col["max_intracell_angle"]]
    e_tot = tab[:, col["e_total"]]

    meta_path = os.path.join(run_dir, "run_meta.json")
    meta = {}
    if os.path.isfile(meta_path):
        with open(meta_path) as fh:
            meta = json.load(fh)
    probe_x_um = meta.get("probe_x_um") or [12.5 + 12.5 * p for p in range(nprobe)]
    x = np.array(probe_x_um) * 1e-6
    f0 = float(meta.get("args", {}).get("f0", DRIVE_F0_GHZ * 1e9))   # Hz
    # qFM gap estimate (E): f_gap = gamma*sqrt(2*H_E*mu0*H_a)/2pi, H_a = 1 Oe
    f_gap = GAMMA * np.sqrt(2.0 * H_E_T * 4.0e-7 * np.pi * 79.58) / (2 * np.pi)

    res = {"run_dir": run_dir, "table_rows": int(len(t)),
           "t_span_ns": float((t[-1] - t[0]) * 1e9),
           "nprobe": nprobe, "probe_x_um": probe_x_um,
           "drive_f0_GHz_L": f0 / 1e9,
           "qfm_gap_E_GHz": round(float(f_gap) / 1e9, 3),
           "v_g_pred_E_m_s": round(float(VG_PRED_M_S), 1),
           "v_g_lit_L_m_s": "10000-23000 (Hamdi PRM 7, 054407 2023)"}

    # dominant frequency in the ring-down (last 60% of the run, burst ended 3 ns)
    sel = t >= max(3.0e-9, t[0] + 0.4 * (t[-1] - t[0]))
    if sel.sum() > 32:
        res["f_dom_probe0_nz_GHz"] = round(fft_dom(t[sel], pnz[sel, 0]) / 1e9, 4)
        res["f_dom_probe_last_nz_GHz"] = round(fft_dom(t[sel], pnz[sel, -1]) / 1e9, 4)
        res["f_dom_global_nz_GHz"] = round(fft_dom(t[sel], nzg[sel]) / 1e9, 4)

    # band-passed RMS per probe around the drive band -> envelope decay length
    bp = np.array([bandpass(t, pnz[:, p], 0.5 * f0, 1.5 * f0)
                   for p in range(nprobe)]).T
    rms = np.sqrt((bp ** 2).mean(axis=0))
    res["probe_rms_nz"] = [round(float(v), 8) for v in rms]
    good = rms > 0.05 * rms[0] if rms[0] > 0 else np.zeros(nprobe, bool)
    if good.sum() >= 3 and rms[good].min() > 0:
        B = np.vstack([x[good], np.ones(int(good.sum()))]).T
        m, _ = np.linalg.lstsq(B, np.log(rms[good]), rcond=None)[0]
        res["l_env_um"] = round(float(-1.0 / m) * 1e6, 2) if m < 0 else None
        res["l_env_fit_nprobes"] = int(good.sum())
    else:
        res["l_env_um"] = None
        res["l_env_fit_nprobes"] = int(good.sum())

    # group velocity from cross-correlation lags between adjacent probes,
    # computed on the ring-down segment (propagating packet, not the burst)
    dt = float(np.median(np.diff(t)))
    seg = t >= 3.0e-9
    if seg.sum() < 32:
        seg = np.ones(len(t), bool)
    bps = np.array([bandpass(t[seg], pnz[seg, p], 0.5 * f0, 1.5 * f0)
                    for p in range(nprobe)]).T
    lags, vgs = [], []
    for p in range(nprobe - 1):
        a, b = bps[:, p], bps[:, p + 1]
        if np.std(a) < 1e-12 or np.std(b) < 1e-12:
            continue
        c = np.correlate(b - b.mean(), a - a.mean(), mode="full")
        lag = int(np.argmax(c) - (len(a) - 1))
        lags.append(lag)
        dx = x[p + 1] - x[p]
        if lag != 0:
            vgs.append(float(np.sign(lag) * dx / (abs(lag) * dt)))
    res["xcorr_lag_samples"] = lags[:16] + (["..."] if len(lags) > 16 else [])
    res["probe_spacing_um"] = round(float(np.median(np.diff(x))) * 1e6, 3)
    if vgs:
        res["v_g_xcorr_m_s"] = round(float(np.median(vgs)), 1)
        res["v_g_xcorr_spread_m_s"] = round(float(np.std(vgs)), 1)
        res["v_g_pairs"] = len(vgs)
    else:
        res["v_g_xcorr_m_s"] = None
        res["v_g_xcorr_spread_m_s"] = None
        res["v_g_pairs"] = 0
    res["v_g_note"] = ("cross-correlation lag medians on the ring-down; spread "
                       "comparable to median means v_g is not resolved at this SNR")

    # arrival time of the wave-packet envelope per probe -> v_g from x(t_arr)
    t_arr = []
    for p in range(nprobe):
        e = np.sqrt(np.convolve(pnz[seg, p] ** 2, np.ones(25) / 25, mode="same"))
        if e.std() > 1e-9:
            t_arr.append((p, float(t[seg][int(np.argmax(e))])))
    if len(t_arr) >= 8:
        xa = np.array([x[p] for p, _ in t_arr])
        ta = np.array([tt for _, tt in t_arr])
        B = np.vstack([ta, np.ones(len(ta))]).T
        m, _ = np.linalg.lstsq(B, xa, rcond=None)[0]
        res["v_g_arrival_m_s"] = round(float(1.0 / m), 1) if m > 0 else None
        res["arrival_fit_nprobes"] = len(ta)

    # 2D FFT dispersion on the ring-down: P(k, w) ridge w(k), fit
    # w^2 = c0 + c2 k^2; predicted (E): c0 = gamma^2*2*H_E*mu0*H_a,
    # c2 = gamma^2*2*H_E*A_T -> v_g at the drive frequency
    if nprobe >= 32 and int(seg.sum()) >= 64:
        dxp = float(np.median(np.diff(x)))
        sig = pnz[seg, :] - pnz[seg, :].mean(axis=0)
        P = np.abs(np.fft.fft2(sig))[:, :int(seg.sum()) // 2 + 1]
        kk = 2 * np.pi * np.fft.fftfreq(nprobe, dxp)
        ww = 2 * np.pi * np.fft.rfftfreq(int(seg.sum()), dt)
        ridge_k, ridge_w = [], []
        pmax = P[:, 1:].max()
        for i in range(1, nprobe // 2):
            col = P[i, 1:]
            j = int(np.argmax(col))
            if col[j] > 0.1 * pmax:
                ridge_k.append(kk[i])
                ridge_w.append(ww[j + 1])
        if len(ridge_k) >= 6:
            rk = np.array(ridge_k)
            rw = np.array(ridge_w)
            keep = (rw > 0.3 * 2 * np.pi * f0) & (rw < 1.8 * 2 * np.pi * f0)
            if int(keep.sum()) >= 5:
                rk, rw = rk[keep], rw[keep]
                B = np.vstack([np.ones(len(rk)), rk ** 2]).T
                c0, c2 = np.linalg.lstsq(B, rw ** 2, rcond=None)[0]
                c2_pred = GAMMA ** 2 * 2.0 * H_E_T * A_T
                df = {"n_points": int(len(rk)),
                      "f_gap_fit_GHz": round(float(np.sqrt(max(c0, 0.0))) / (2 * np.pi) / 1e9, 3),
                      "f_gap_pred_E_GHz": round(float(f_gap) / 1e9, 3),
                      "c2_over_pred": round(float(c2 / c2_pred), 3),
                      "k_points_per_m": [round(float(v), 1) for v in rk],
                      "f_points_GHz": [round(float(v) / (2 * np.pi) / 1e9, 3) for v in rw]}
                w0 = 2 * np.pi * f0
                if w0 ** 2 > c0 and c2 > 0:
                    k0 = np.sqrt((w0 ** 2 - c0) / c2)
                    df["v_g_at_f0_m_s"] = round(float(c2 * k0 / w0), 1)
                    df["lambda_at_f0_um"] = round(float(2 * np.pi / k0) * 1e6, 3)
                res["disp_fit"] = df

    # AFM order integrity: intracell angle 180 deg = perfect AFM; report both
    # the max deviation from 180 and the minimum angle (local order collapse)
    res["intracell_angle_min_deg"] = round(float(np.nanmin(angle)) * 180.0 / np.pi, 3)
    res["intracell_angle_max_deg"] = round(float(np.nanmax(angle)) * 180.0 / np.pi, 3)
    if np.isfinite(e_tot).any():
        res["e_total_first_last"] = [float(e_tot[np.isfinite(e_tot)][0]),
                                      float(e_tot[np.isfinite(e_tot)][-1])]

    # spatial envelope from neel_end.npz if present
    npz_path = os.path.join(run_dir, "neel_end.npz")
    if os.path.isfile(npz_path):
        z = np.load(npz_path)
        neel = z["neel"]                      # (3, nz, ny, nx)
        nzv = neel[2, 0]                      # (ny, nx)
        env = np.sqrt((nzv ** 2).mean(axis=0))  # per x cell
        xs = (np.arange(neel.shape[3]) + 0.5) * 100e-9
        m = (xs >= 10e-6) & (xs <= 95e-6)
        if m.sum() > 10 and env[m].min() > 0:
            B = np.vstack([xs[m], np.ones(int(m.sum()))]).T
            s, _ = np.linalg.lstsq(B, np.log(env[m]), rcond=None)[0]
            res["l_env_field_um"] = round(float(-1.0 / s) * 1e6, 2) if s < 0 else None
        res["env_field_peak_x_um"] = round(float(xs[int(np.argmax(env))]) * 1e6, 2)
        res["t_end_ns"] = float(z["t"]) * 1e9

    os.makedirs(HD, exist_ok=True)
    return res


def main():
    import glob
    if len(sys.argv) > 1:
        runs = [sys.argv[1]]
    else:
        runs = sorted(d for d in glob.glob(os.path.join(HD, "hematite_*"))
                      if os.path.isfile(os.path.join(d, "table.csv")))
    if not runs:
        print("no hematite_* run dirs under", HD)
        sys.exit(2)
    out = {"deck": "tools/decks/idaten_hematite_mumaxplus.py",
           "solver": "mumaxplus 1.2.2 PyPI wheel on Kaggle T4 (sm_75, CUDA 13 JIT of sm_52 PTX)",
           "v_g_pred_E_m_s": round(float(VG_PRED_M_S), 1),
           "v_g_lit_L_m_s": "10000-23000 (Hamdi PRM 7, 054407 2023)",
           "runs": {}}
    for d in runs:
        r = analyze(d)
        out["runs"][os.path.basename(d)] = r
        print(json.dumps(r, indent=2))
    with open(OUT_JSON, "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote", OUT_JSON)


if __name__ == "__main__":
    main()
