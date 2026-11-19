"""Stage C figure: per-material probe RMS decay + dominant frequency.

Reads data/stageC_kaggle/stageC_summary.json and writes
figures/stageC_material_shootout.png.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(ROOT, "data", "stageC_kaggle")
OUT = os.path.join(ROOT, "figures", "stageC_material_shootout.png")

with open(os.path.join(SC, "stageC_summary.json")) as fh:
    S = json.load(fh)

PROBE_X_UM = [10.0 + 10.0 * p for p in range(8)]
ORDER = ["YIG", "BiYIG", "CoFe", "GdFeCoP", "NiFe"]
mats = [m for m in ORDER if m in S["materials"]]

fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), dpi=200)
ax = axes[0]
for m in mats:
    r = S["materials"][m]["probe_rms"]
    ax.semilogy(PROBE_X_UM, r, "o-", label=f"{m}  f_dom={S['materials'][m]['f_dom_probe0_GHz']:.2f} GHz")
ax.set_xlabel("probe x (um)")
ax.set_ylabel("band-passed |mz| RMS at probe")
ax.set_title("Stage C (S): wave amplitude along the 100 um bare bus, 4 ns run")
ax.grid(True, which="both", alpha=0.3)
ax.legend(fontsize=8)

ax = axes[1]
fd = [S["materials"][m]["f_dom_probe0_GHz"] for m in mats]
le = [S["materials"][m]["l_env_um"] for m in mats]
xpos = np.arange(len(mats))
ax.bar(xpos - 0.2, fd, width=0.4, label="f_dom (GHz)")
ax.axhline(1.70, color="gray", ls="--", lw=1, label="drive 1.70 GHz (L)")
ax.set_xticks(xpos)
ax.set_xticklabels(mats, fontsize=8)
ax.set_ylabel("f_dom (GHz)")
ax.set_title("dominant frequency per bus material (S)")
ax.legend(fontsize=8)
ax.grid(True, axis="y", alpha=0.3)

fig.tight_layout()
fig.savefig(OUT)
print("wrote", OUT)
print("l_env_um:", {m: S["materials"][m]["l_env_um"] for m in mats})
print("v_g_xcorr:", {m: S["materials"][m]["v_g_xcorr_m_s"] for m in mats})
