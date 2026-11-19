import json
import numpy as np

D = r"C:\Users\OSINOR~1\Downloads\idaten-architecture\data\hematite_kaggle\hematite_full"
with open(D + r"\table.csv") as fh:
    header = fh.readline().lstrip("# ").strip().split(",")
    rows = [[float(v) for v in ln.split(",")] for ln in fh if ln.strip()]
tab = np.array(rows)
col = {n: i for i, n in enumerate(header)}
t = tab[:, col["t"]]
print("rows", len(t), "t range ns:", t[0] * 1e9, t[-1] * 1e9, "dt ps:", np.median(np.diff(t)) * 1e12)

pnz = tab[:, [col["p%d_nz" % p] for p in range(8)]]
pny = tab[:, [col["p%d_ny" % p] for p in range(8)]]
nzg = tab[:, col["nz_avg"]]
nyg = tab[:, col["ny_avg"]]
nxg = tab[:, col["nx_avg"]]
M = tab[:, [col["Mx_avg"], col["My_avg"], col["Mz_avg"]]]
ang = tab[:, col["max_intracell_angle"]]

def fft_dom(t, y, f_lo=0.05e9, f_hi=10e9):
    dt = float(np.median(np.diff(t)))
    n = len(t)
    yu = y - y.mean()
    F = np.abs(np.fft.rfft(yu * np.hanning(n)))
    f = np.fft.rfftfreq(n, dt)
    keep = (f >= f_lo) & (f <= f_hi)
    i = int(np.argmax(F[keep]))
    return f[keep][i] / 1e9, F[keep][i]

# full-window and ring-down spectra
for name, sig in [("p0_nz", pnz[:, 0]), ("p3_nz", pnz[:, 3]), ("p7_nz", pnz[:, 7]),
                  ("p0_ny", pny[:, 0]), ("p7_ny", pny[:, 7]),
                  ("global_nz", nzg), ("global_ny", nyg), ("global_nx", nxg)]:
    f_all, a_all = fft_dom(t, sig)
    sel = t >= 3.0e-9
    f_rd, a_rd = fft_dom(t[sel], sig[sel])
    print("%-10s full: %6.3f GHz (A=%.3g)   ringdown[3ns..]: %6.3f GHz (A=%.3g)  std=%.3g" %
          (name, f_all, a_all, f_rd, a_rd, np.std(sig)))

# amplitude envelope in time for p0 and p7 (10 ps RMS windows)
w = 50  # 50 samples = 1 ns
for p in (0, 3, 7):
    env = np.sqrt(np.convolve(pnz[:, p] ** 2, np.ones(w) / w, mode="same"))
    print("p%d_nz env@0.5,1.5,2.5,3.5,5,7ns:" % p,
          [round(float(env[int(tt / 20e-12)]), 5) for tt in (0.5e-9, 1.5e-9, 2.5e-9, 3.5e-9, 5e-9, 7e-9)])

print("angle deg: min %.2f max %.2f  (180-perfect AFM; dev-from-180 max %.2f)" %
      (np.nanmin(ang) * 180 / np.pi, np.nanmax(ang) * 180 / np.pi, 180 - np.nanmin(ang) * 180 / np.pi))
print("M avg (net magnetisation):", M.mean(axis=0), " |M| ~", np.linalg.norm(M.mean(axis=0)))
print("global n: nx %.4f ny %.4f nz %.4f" % (nxg.mean(), nyg.mean(), nzg.mean()))

# neel_end field: n_z pattern along x (mean over y), and where is power?
z = np.load(D + r"\neel_end.npz")
neel = z["neel"]
nzv = neel[2, 0]  # (ny, nx)
nxy = neel[1, 0]
env_z = np.sqrt((nzv ** 2).mean(axis=0))
env_y = np.sqrt((nxy ** 2).mean(axis=0))
xs = (np.arange(neel.shape[3]) + 0.5) * 100e-9 * 1e6
print("end-field env_z every 10 um:", [round(float(env_z[i]), 4) for i in range(0, 1000, 100)])
print("end-field env_y every 10 um:", [round(float(env_y[i]), 4) for i in range(0, 1000, 100)])
# spatial FFT of end field n_z to get wavelength
seg = nzv.mean(axis=0) - nzv.mean()
F = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
k = np.fft.rfftfreq(len(seg), 100e-9)
i = int(np.argmax(F[1:])) + 1
print("end n_z dominant k = %.3e 1/m -> lambda = %.2f um -> at 1.7 GHz v=%.0f m/s" %
      (k[i], 2 * np.pi / k[i] * 1e6, k[i] * 1.7e9 / (2 * np.pi) * 2 * np.pi * 1.0))
# simpler: lambda * f
lam = 2 * np.pi / k[i]
print("lambda = %.2f um, f_dom 1.26 GHz -> v = %.0f m/s ; f 1.7 GHz -> v = %.0f m/s" %
      (lam * 1e6, lam * 1.26e9, lam * 1.7e9))

with open(D + r"\run_meta.json") as fh:
    print(json.dumps(json.load(fh), indent=1)[:800])
