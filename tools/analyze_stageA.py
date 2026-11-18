"""Stage A (Kaggle T4 run) analysis of the pulled artifacts.

Inputs (committed under data/stageA_kaggle/):
  stageA/deck.out/table.txt   -- t, mx, my, mz (global averages), 2402 rows, 0..12 ns
  stageA/deck.out/mStart.ovf  -- magnetisation after the published minimize/relax init
  stageA/deck.out/Finish.ovf  -- magnetisation after run(12 ns) with the sinc drive

Deck geometry (read from data/zenodo_baumgaertl/SupplementFig6__Sat_S1.0__14mT.mx3):
  mesh 8192 x 32 x 1 @ 5 nm  -> x in [0, 40.96 um], y in [0, 160 nm]
  51 NiFe nanomagnets, 100 x 20 nm, pitch 200 nm, row y in [20, 40] nm,
  x centre of magnet i = -5000 + 200*i nm  (negative x clipped by the mesh)
  YIG bus y in [0, 20] nm (mesh-clipped); region 252 = y > 20 nm (NiFe params).
  Bias Bn = -14 mT; drive = CPW32_40um.ovf + sinc pulse, driv = 40 uT,
  toff = 3 ns, fdel = 40*pi*GHz  ->  flat drive band 0..20 GHz; run 12 ns.

Outputs (printed + written to data/stageA_kaggle/stageA_summary.json):
  1. table.txt time span, sampling, and FFT of mx(t), my(t) over t >= toff:
     top spectral peaks vs the published anchors (L): k1 = 1.70 GHz,
     MAMR dips 9.25 / 10.75 / 11.75 GHz, drive band edge 20 GHz.
  2. per-magnet mz in mStart vs Finish: which of the visible magnets flipped.
  3. bus response: mx envelope stats in the bus row.
All numbers measured here are (S).
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ovf_extract import read_ovf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SA = os.path.join(ROOT, "data", "stageA_kaggle", "stageA", "deck.out")
OUT_JSON = os.path.join(ROOT, "data", "stageA_kaggle", "stageA_summary.json")

CELL = 5e-9          # m
NX, NY, NZ = 8192, 32, 1
MAG_Y0, MAG_Y1 = 20e-9, 40e-9     # magnet row (region 252 lower part)
MAG_X0 = -5000e-9                 # magnet 0 centre (nm -> m)
PITCH = 200e-9
MAG_W = 100e-9
TOFF = 3e-9
PUBLISHED = {  # (L) Baumgaertl & Grundler 2023
    "k1_GHz": 1.70, "MAMR_dips_GHz": [9.25, 10.75, 11.75], "drive_band_edge_GHz": 20.0,
}


def load_table():
    p = os.path.join(SA, "table.txt")
    rows = []
    with open(p) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            rows.append([float(v) for v in line.split()])
    a = np.array(rows)
    return a[:, 0], a[:, 1], a[:, 2], a[:, 3]


def spectrum(t, x, t_from, f_max_ghz=25.0):
    """FFT of x(t) sampled non-uniformly -> interpolate on uniform grid, then rfft."""
    sel = t >= t_from
    tt, xx = t[sel], x[sel]
    if len(tt) < 16:
        return np.array([]), np.array([])
    dt = float(np.median(np.diff(tt)))
    n = int(round((tt[-1] - tt[0]) / dt)) + 1
    tu = tt[0] + dt * np.arange(n)
    xu = np.interp(tu, tt, xx)
    xu = xu - xu.mean()
    w = np.hanning(n)
    F = np.abs(np.fft.rfft(xu * w))
    f = np.fft.rfftfreq(n, dt)
    keep = f <= f_max_ghz * 1e9
    return f[keep], F[keep]


def top_peaks(f, F, k=8, f_min_ghz=0.5):
    order = np.argsort(F)[::-1]
    peaks = []
    for i in order:
        if f[i] < f_min_ghz * 1e9:
            continue
        if any(abs(f[i] - fp) < 0.15e9 for fp, _ in peaks):
            continue
        peaks.append((float(f[i] / 1e9), float(F[i])))
        if len(peaks) >= k:
            break
    peaks.sort()
    return peaks


def load_field(name):
    hdr, arr, mk = read_ovf(os.path.join(SA, name), order="yxz")  # (nz, ny, nx, vd)
    return hdr, arr[0]  # (ny, nx, vd)


def magnet_stats(hdr, m_start, m_finish):
    """Per-magnet mean mz in start vs finish, over each magnet's rect."""
    xstep = hdr["xstepsize"]
    ystep = hdr["ystepsize"]
    x0 = hdr.get("xbase", hdr["xmin"] + xstep / 2)
    y0 = hdr.get("ybase", hdr["ymin"] + ystep / 2)
    y_lo = int(np.searchsorted(y0 + ystep * np.arange(NY), MAG_Y0))
    y_hi = int(np.searchsorted(y0 + ystep * np.arange(NY), MAG_Y1))
    y_lo, y_hi = max(0, y_lo), min(NY, y_hi)
    out = []
    for i in range(51):
        xc = MAG_X0 + i * PITCH
        if xc + MAG_W / 2 <= 0 or xc - MAG_W / 2 >= (hdr["xmax"]):
            continue  # fully outside the mesh
        xa = max(xc - MAG_W / 2, 0.0)
        xb = min(xc + MAG_W / 2, hdr["xmax"])
        i0 = int(np.searchsorted(x0 + xstep * np.arange(NX), xa))
        i1 = int(np.searchsorted(x0 + xstep * np.arange(NX), xb))
        i0, i1 = max(0, i0), min(NX, i1)
        if i1 - i0 < 1 or y_hi - y_lo < 1:
            continue
        blk_s = m_start[y_lo:y_hi, i0:i1, 2]
        blk_f = m_finish[y_lo:y_hi, i0:i1, 2]
        out.append({
            "i": i,
            "x_center_nm": round((xc) * 1e9, 1),
            "mz_start": round(float(blk_s.mean()), 5),
            "mz_finish": round(float(blk_f.mean()), 5),
            "dmz": round(float(blk_f.mean() - blk_s.mean()), 5),
            "switched": bool(blk_s.mean() * blk_f.mean() < 0
                             or abs(float(blk_f.mean() - blk_s.mean())) > 1.0),
        })
    return out


def main():
    t, mx, my, mz = load_table()
    print(f"table.txt: {len(t)} rows, t = {t[0]:.3e} .. {t[-1]:.3e} s "
          f"({(t[-1]-t[0])*1e9:.3f} ns), dt median = {np.median(np.diff(t))*1e12:.3f} ps")
    print(f"global m: mz start {mz[0]:.6f} -> end {mz[-1]:.6f}; "
          f"mx range [{mx.min():.5f}, {mx.max():.5f}]; my range [{my.min():.5f}, {my.max():.5f}]")

    peaks_x = top_peaks(*spectrum(t, mx, TOFF))
    peaks_y = top_peaks(*spectrum(t, my, TOFF))
    print("\nFFT of global mx(t), t >= 3 ns (top peaks, GHz, amplitude):")
    for f, a in peaks_x:
        print(f"  {f:7.3f} GHz   {a:10.4g}")
    print("FFT of global my(t), t >= 3 ns:")
    for f, a in peaks_y:
        print(f"  {f:7.3f} GHz   {a:10.4g}")
    print(f"published anchors (L): k1 = {PUBLISHED['k1_GHz']} GHz; "
          f"MAMR dips = {PUBLISHED['MAMR_dips_GHz']} GHz; drive band edge = {PUBLISHED['drive_band_edge_GHz']} GHz")

    hdr_s, m_start = load_field("mStart.ovf")
    hdr_f, m_finish = load_field("Finish.ovf")
    print(f"\nOVF: mesh {hdr_s['xnodes']}x{hdr_s['ynodes']}x{hdr_s['znodes']}, "
          f"valuedim {hdr_s['valuedim']}, x [{hdr_s['xmin']:.3e}, {hdr_s['xmax']:.3e}] m, "
          f"y [{hdr_s['ymin']:.3e}, {hdr_s['ymax']:.3e}] m")

    mags = magnet_stats(hdr_s, m_start, m_finish)
    n_sw = sum(1 for m in mags if m["switched"])
    print(f"\nvisible nanomagnets in mesh: {len(mags)}; switched (mz sign flip or |dmz|>1): {n_sw}")
    for m in mags:
        flag = " <-- SWITCHED" if m["switched"] else ""
        print(f"  i={m['i']:2d} x={m['x_center_nm']:8.1f} nm  "
              f"mz {m['mz_start']:+.5f} -> {m['mz_finish']:+.5f}  dmz {m['dmz']:+.5f}{flag}")

    # bus-row (y < 20 nm) mean |mx| change as a wave-response sanity check
    ystep = hdr_s["ystepsize"]
    y0 = hdr_s.get("ybase", hdr_s["ymin"] + ystep / 2)
    y_bus = int(np.searchsorted(y0 + ystep * np.arange(NY), 20e-9))
    bus_dm = np.abs(m_finish[:y_bus, :, :] - m_start[:y_bus, :, :]).mean(axis=(0, 2))
    x_um = (hdr_s.get("xbase", hdr_s["xmin"] + hdr_s["xstepsize"] / 2)
            + hdr_s["xstepsize"] * np.arange(NX)) * 1e6
    print(f"\nbus row (y<20 nm): mean |dm| vs x, sampled every 2 um:")
    for k in range(0, NX, 400):
        print(f"  x={x_um[k]:7.2f} um   <|dm|>={bus_dm[k]:.5f}")

    summary = {
        "table_rows": int(len(t)),
        "t_span_ns": float((t[-1] - t[0]) * 1e9),
        "dt_median_ps": float(np.median(np.diff(t)) * 1e12),
        "global_mz_start": float(mz[0]), "global_mz_end": float(mz[-1]),
        "fft_mx_peaks_GHz": [round(f, 4) for f, _ in peaks_x],
        "fft_my_peaks_GHz": [round(f, 4) for f, _ in peaks_y],
        "published_anchors_L": PUBLISHED,
        "visible_magnets": len(mags),
        "switched_magnets": n_sw,
        "magnets": mags,
    }
    with open(OUT_JSON, "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"\nwrote {OUT_JSON}")


if __name__ == "__main__":
    main()
