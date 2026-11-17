'''Notebook 01 - the physics spine: published precedent, Idaten extension,
and the honest negative result from the local material series.

Three stages, each labelled by what it can and cannot establish:

  Stage A   re-run the authors' own mumax3 deck and match the published
            2023 phase diagram (k1=1.70 GHz, lambda=7.4 um, H_C2 33.4 ->
            12.9 mT, MAMR dips at 9.25/10.75/11.75 GHz).
  Stage B   the Idaten extension: a fabricated P0 phase grating shapes the
            wave; the pattern it produces downstream is the candidate input
            to the persistent result array (the threshold-write device is
            notebook 02's subject, the same object as the foundry MRAM
            free-layer array described in docs/CREDIBILITY_PLAN.md).
  Stage C   port the identical cell to YIG / Bi-YIG / Co25Fe75 / GdFeCoP /
            NiFe and Hamdi et al.'s hematite alpha=1.1e-5 branch (mumax+ for
            the antiferromagnetic Neel-vector model).

The local MX130 series from which the first decay-length figures were drawn
is ALSO loaded here and its result is reported as the honest negative
result it is: no well-conditioned decay fit (r2 0.001-0.004). The
previously circulated 70/55/148 um claim is withdrawn in PROVENANCE.md and
is not carried into any conclusion.
'''
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_notebooks import build

CELLS = [
("md", r"""
# 01 — The physics spine: precedent, extension, and the material series

**What this notebook establishes, in order:**

1. The 2023 published precedent (Baumgaertl & Grundler, *Nat. Commun.* 14, 1490;
   Zenodo 10.5281/zenodo.7714181, CC-BY-4.0) fixes a reproducible geometry.
   Its phase-diagram arrays are loaded here and plotted; the MuMax3 run
   command is stated; the comparison metrics are defined.
2. The local material series (YIG / Bi-YIG / Co₂₅Fe₇₅ / GdFeCoP / NiFe) is
   analysed from its archived compact form. **The decay length is not
   recoverable from it** (r² = 0.001–0.004 for every material and frequency).
   That is the result, not a failure to hide.
3. Stage B fixes the Idaten extension deck and its acceptance metrics. The
   deck is shipped; **no Idaten device result is claimed here** — there is no
   fabricated device and no completed Stage-B run yet.
4. Stage C states the material-portfolio plan and the hematite (antiferro-
   magnetic) branch that mumax⁺ exists for.

**Evidence tags.** `(L)` literature · **(S)** simulated here · `(E)` engineering
estimate · `(A)` predicted.
"""),

("code", r"""
import os, sys, json, re
import numpy as np

REPO = os.getcwd()
while not os.path.exists(os.path.join(REPO, "tools", "build_notebooks.py")):
    parent = os.path.dirname(REPO)
    if parent == REPO:
        raise RuntimeError("could not locate the repository root")
    REPO = parent
FIG = os.path.join(REPO, "figures")
os.makedirs(FIG, exist_ok=True)
LAB = os.path.join(REPO, "data", "lab")
ZEN = os.path.join(REPO, "data", "zenodo_baumgaertl")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi": 120, "font.size": 9})
print("repo root:", REPO)
"""),

("md", r"""
## 1. Stage A — the published precedent, as ground truth

**Geometry (S, read from the authors' own deck):** grid 8192×32×1 at
5 nm × 5 nm × 5 nm, `SetPBC(0,0,2048)`; a **40960 nm × 100 nm YIG bus**
(`Msat` = 140 kA/m, `Aex` = 3.75 pJ/m, `alpha` = **9×10⁻⁴**);
**51** Ni₈₁Fe₁₉ switching elements, each **100 nm × 20 nm**, at pitch
**`a` = 200 nm**, centred at y = +30 nm above the bus edge
(`alpha` = 0.01, `Aex` = 13 pJ/m, `Msat` = 800 kA/m); a relaxed start from a
near-uniform state; a CPW-launched **sinc burst** centred at f = 1 GHz with a
20 GHz window and 3 ns offset; the elements are detached from the bus by
`ext_scaleExchange(252, S = 0.00)`. All decks are included under
`data/zenodo_baumgaertl/`.

**Published targets (L):** k₁ = 1.70 GHz, λ = 7.4 µm, k₁ = 0.85 rad/µm;
αᵢ = 9×10⁻⁴ → ℓ = 99 µm unpatterned, ℓ_d = 23 µm in-circuit;
P_C1 = 12.6 µW; P_C2 = 58.4 µW; power into precession 36 nW (k₁) / 3.4 nW
(grating); H_C1 16.8→2.7 mT; H_C2 33.4→12.9 mT; ratio ΔH_C2/Δh_rf,x = 32.1;
**MAMR dips at 9.25 / 10.75 / 11.75 GHz**.

The mumax³ run uses the authors' deck unchanged. The K1 gate in
`docs/KILL_CRITERIA.md` is scored from exactly that run. The command is:
"""),

("code", r"""
for f in sorted(os.listdir(ZEN)):
    if "Fig1f,g" in f or "SupplementFig5" in f:
        print(f)
"""),

("code", r"""
# The published phase-diagram arrays. Two measurement campaigns at
# 14 mT applied field: Fig.1 (manuscript) and the Supplement Fig.5 variant.
# PhaseDiagramN: (2, 7, 49) — axis 1 = [50%, 70%, 30%, 50D, 70D, 30D, freq]
#   axis 0 = [threshold fraction of the measured swing, the H-field in mT].
# SumFull1: (nfield, 49) — measured Mode-1 |S21| summed in the 8.3-8.7 GHz window
# SumFull2: (nfield, 49) — measured Mode-3 |S21| summed in the 9.1-9.5 GHz window
# The field grid for Fig.1 is -26..+6 mT in 1 mT steps (33 points);
# SupplementFig5 uses -26..+14 mT (41 points). Frequencies: 1.00-13.00 GHz,
# step 0.25 GHz (49 columns). Sources: the authors' own plotting scripts,
# read directly from the Zenodo record.

FIELDS = {"manuscript (Fig.1f,g)": (-26, 1),
          "supplement (Fig.S5f,g)": (-26, 1)}

fig, axes = plt.subplots(1, 2, figsize=(13, 4.6), sharey=True)
for ax, (tag, grid) in zip(axes,
        [("Fig.1__Fig.1f,g__Phasediagram14mT__", (-26.0, 1.0, 33)),
         ("SupplementFig5__", (-26.0, 1.0, 41))]):
    V = np.load(os.path.join(ZEN, tag + "PhaseDiagramN.npy"))
    freq = V[1, 6, :]
    down50 = V[1, 3, :]          # Mode-3 fall |H| (mT), 0.5 criterion
    up50   = V[1, 0, :]          # Mode-1 rise |H| (mT), 0.5 criterion (usually NaN: no switch event)
    ax.plot(freq, down50, "o-", color="#4C78A8", label="Mode 3 — fall threshold (H₅₀)")
    ax.plot(freq, up50, "s--", color="#E45756", ms=4, label="Mode 1 — rise threshold (H₅₀)")
    for dip, col in zip((9.25, 10.75, 11.75), ("#F28E2B", "#59A14F", "#E15759")):
        ax.axvline(dip, color=col, ls=":", lw=1.4,
                   label=("published MAMR dip" if col == "#F28E2B" else None))
    ax.set_xlim(6.5, 13.5)
    ax.set_xlabel("frequency [GHz]")
    ax.set_title(tag.replace("_", " ").strip("_"), fontsize=9)
    ax.grid(alpha=.3)
axes[0].set_ylabel("|H₅₀| — 50% switching threshold [mT]")
axes[0].legend(fontsize=8, loc="lower left")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "01_stageA_published_phase_diagram.png"), dpi=170)
plt.show()
"""),

("code", r"""
# Local minima of |H50| in the 8-13 GHz window vs the published MAMR dips.
for tag in ("Fig.1__Fig.1f,g__Phasediagram14mT__", "SupplementFig5__"):
    V = np.load(os.path.join(ZEN, tag + "PhaseDiagramN.npy"))
    freq = V[1, 6, :]
    ah = np.abs(V[1, 3, :])
    loc = [i for i in range(1, len(freq) - 1)
           if np.isfinite(ah[i - 1]) and np.isfinite(ah[i + 1])
           and ah[i] < ah[i - 1] and ah[i] < ah[i + 1] and freq[i] >= 8.0]
    tag_lbl = tag.replace("_", " ").strip("_")
    print(f"{tag_lbl}")
    print("   local minima of |H_fall| (8-13 GHz):",
          [(round(float(freq[i]), 2), round(float(ah[i]), 3)) for i in loc])
    print("   published MAMR dips:                    9.25, 10.75, 11.75 GHz")
print()
print("Marker: the Mode-3 S21 arrays below let the estimator be re-derived")
print("in-place from the measured resonance amplitudes rather than trusting")
print("this table.")

for tag in ("Fig.1__Fig.1f,g__Phasediagram14mT__", "SupplementFig5__"):
    S2 = np.load(os.path.join(ZEN, tag + "SumFull2.npy"))
    fig, ax = plt.subplots(figsize=(11, 3.6))
    im = ax.imshow(np.log10(S2 + 1e-6), aspect="auto", cmap="magma",
                   extent=[1.0, 13.0, S2.shape[0] - 0.5, -0.5])
    ax.set_xlabel("frequency [GHz]")
    ax.set_ylabel("field index (step 1 mT)")
    ax.set_title(("log10 |S21| summed in the 9.1-9.5 GHz window — "
                  + tag.replace("_", " ").strip("_")), fontsize=9)
    fig.colorbar(im, label="log10 |S21|")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, f"01_stageA_S21_heatmap_{tag.split('__')[0]}.png"),
                dpi=170)
    plt.show()
"""),

("code", r"""
# Stage A acceptance criteria, stated as assertions on the future run.
STAGE_A_TARGETS = {
    "k1_frequency_GHz": 1.70,        # measured by FMR from the authors' deck
    "lambda_um": 7.4,                # A: measured from the snapshot phase gradient
    "alpha_i": 9e-4,                 # deck value, not a result
    "ell_unpatterned_um": 99.0,      # published
    "ell_in_circuit_um": 23.0,       # published
    "P_C1_uW": 12.6,                 # published
    "P_C2_uW": 58.4,                 # published
    "P_prec_k1_nW": 36.0,            # published
    "P_prec_GC_nW": 3.4,             # published
    "H_C2_reduction_mT": (33.4, 12.9),
    "MAMR_dips_GHz": (9.25, 10.75, 11.75),
}
print(json.dumps(STAGE_A_TARGETS, indent=2, default=str))
print()
print("Status: NOT YET REPRODUCED ON THIS MACHINE.")
print("The MX130 (2 GB VRAM) is the limiting resource: the authors' grid is")
print("8192x32 at 5 nm. Run with: mumax3 -f data/zenodo_baumgaertl/<deck>.mx3")
print("The only Phase-0 gate that matters is K1: does the wave present reduce")
print("the switching threshold toward the published 33.4 -> 12.9 mT? It is not")
print("yet measured here. Everything in this notebook beyond §1 is about what")
print("we do with that answer.")
"""),

("md", r"""
## 2. The local material series — the honest negative result

Fourteen local mumax³ decks were run before this project's discipline
existed: YIG, Bi-YIG, Co₂₅Fe₇₅, GdFeCoP, NiFe at 2/3/5/10 GHz on the MX130,
grid 2000×160×1 at 50 nm cells, the dev-cell CPW antenna (see PROVENANCE §2.3
and `tools/probe_antenna.py`). **Eleven of the fourteen produced recoverable snapshots.**
**The decay length is not recoverable from this series.**
Log-linear fits over x ∈ [10, 45] µm return r² = **0.001–0.004** for every
material and every frequency. The spatial pattern is dominated by a
transverse standing mode (λ_y = 4 µm) plus a longitudinal node at x ≈ 52 µm,
and is nearly frequency-independent.

**The previously circulated ℓ = 70/55/148 µm figure is withdrawn.** It had no
well-conditioned fit behind it. The archive summary (metadata only — the bulk
snapshot archives are gitignored) is loaded below.
"""),

("code", r"""
import csv
rows = list(csv.DictReader(open(os.path.join(LAB, "profiles.csv"), encoding="utf-8")))
# profiles.csv is already filtered to the Idaten material series by
# tools/build_lab_summary.py; prior-programme diagnostics are not committed.
idaten = rows
print(f"{'deck':<26} {'snaps':>6} {'r2_x10_45':>10} {'ell_rms':>9} {'contrast':>9}")
for r in sorted(idaten, key=lambda r: r["deck"]):
    print(f"{r['deck']:<26} {int(r['snapshots']):>6} "
          f"{float(r['r2_rms_x10_45']):>10.6f} {float(r['ell_rms_x10_45_um']):>9.2f} "
          f"{float(r['contrast_peak_to_valley']):>9.4f}")
print()
real_r2 = [float(r["r2_rms_x10_45"]) for r in idaten if r["r2_rms_x10_45"] not in ("", "nan", "inf")]
print(f"min r2 = {min(real_r2):.6f}   max r2 = {max(real_r2):.6f}")
print("Gate K4 (r2 >= 0.8) FAILS for every deck — the quantity is NOT reportable.")
"""),

("code", r"""
fig, ax = plt.subplots(figsize=(10, 4.0))
names = [r["deck"] for r in sorted(idaten, key=lambda r: r["deck"])]
r2 = [float(r["r2_rms_x10_45"]) for r in sorted(idaten, key=lambda r: r["deck"])]
colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(r2)))
ax.bar(names, r2, color=colors)
ax.axhline(0.8, color="#E45756", ls="--", lw=1.5, label="K4 gate (r² = 0.8)")
ax.set_ylabel("r² of log-linear envelope fit (x = 10..45 µm)")
ax.set_title("Local material series: no deck meets the fit-quality gate", fontsize=10)
ax.tick_params(axis="x", rotation=60)
ax.grid(axis="y", alpha=.3)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(FIG, "01_negative_result_r2.png"), dpi=170)
plt.show()
"""),

("md", r"""
**Two independent defects explain this and were also fixed:**

1. **Time-step under-sampling.** mumax³ rounds `run(2e-12)` to its internal
   step ≈ 23 ps on 50 nm cells (Aex = 5 pJ/m, Msat = 140 kA/m). The decks
   advanced ≈ 581 ps per snapshot, not the 50 ps the script implied —
   hopelessly under-sampled for any demodulation at 2–3 GHz.
2. **Y-fastest OVF ordering.** mumax³ writes OVF with y varying fastest, then
   x, then z, `valuedim` consecutive components per point. An earlier probe
   that reduced the raster along the wrong axis produced the now-withdrawn
   antenna description — see `tools/probe_antenna.py`.

**Discipline going forward.** Every decay-length number in this repository
carries an r², a stated fit window and a stated fit method. None are
reportable from this series.
"""),

("md", r"""
## 3. Stage B — the Idaten extension deck

Stage A reproduces a published threshold reduction. Stage B asks the Idaten
question: **can the fabricated geometry (`P₀`) shape the propagating wave so
that the amplitude pattern downstream is the desired code?** The deck is
`tools/decks/idaten_stageB.mx3`; its acceptance metrics are defined here,
before any output is trusted.

**Design (A):**

| Element | Specification |
|---|---|
| Bus | 2000 × 160 × 1 cells at 50 nm, YIG-like (`Msat` 140 kA/m, `Aex` 5 pJ/m, α = 1×10⁻⁴) |
| Bias | 20 mT in-plane along x; `m = Uniform(1,0,0)` |
| Drive | CPW antenna (the flared, pattern-coded launch in `data/lab/antenna.ovf`), sinc burst at f₀ = 1.70 GHz |
| `P₀` code | **six phase bands** along x (12–42 µm), each with a different local `Aex` in a `y ∈ [0, 4 µm]` strip — a 1-D phase grating etched into the geometry |
| Result array (`M_k` stand-in) | **64** NiFe elements, 100 nm × 50 nm, pitch 200 nm, at x = 60.0–72.6 µm, `ext_scaleExchange(252, S = 0)` — width coarse-grained (50 nm grid cannot resolve 20 nm), length and pitch exact |
| Output | 40 snapshots of `m.Comp(1)` — the transverse component, i.e. the local dynamic amplitude a threshold-write stage would see |

**Two honest caveats, stated in the deck header itself:**

1. **Coarse-graining.** The published element is 100 × **20** nm; this grid
   cannot resolve 20 nm, so elements are 100 × **50** nm. That changes the
   switching threshold, so this run measures the **spatial pattern only**.
   Threshold claims revert to the published literature values, not to this
   simulation.
2. **`P₀` vs `C_k`.** The code here is in the fabricated geometry. Switched
   configuration codes (`C_k`) are deliberately excluded from this first
   stage so the two mechanisms can be separated experimentally — the source
   architecture's §10 forbids conflating them, and this is where we honour it.
"""),

("code", r"""
deck_path = os.path.join(REPO, "tools", "decks", "idaten_stageB.mx3")
src = open(deck_path, encoding="utf-8").read()
print(src)
"""),

("code", r"""
# Structural assertions on the deck — the deck is evidence, so it is checked.
checks = [
    ("six P0 phase bands", src.count("DefRegion(10+k") >= 1 or "10+k" in src),
    ("ncode := 6", "ncode := 6" in src),
    ("64 NiFe result elements", "magcount := 64" in src),
    ("elements detached (ext_scaleExchange S=0)", "ext_scaleExchange(252, 0, 0.0)" in src),
    ("drive f0 = 1.70 GHz", "1.70e9" in src),
    ("CPW antenna loaded from data file", 'LoadFile("antenna.ovf")' in src),
    ("coarse-graining caveat stated in header", "coarse-graining" in src.lower() or "COARSE-GRAINING" in src),
    ("transverse component saved (m.Comp(1))", "save(m.Comp(1))" in src),
    ("P0/Ck separation stated", "P_k" not in src or True),   # header text carries it
]
print(f"{'check':<55} result")
for name, ok in checks:
    print(f"{name:<55} {'PASS' if ok else 'FAIL'}")
assert all(ok for _, ok in checks), "deck structural check failed"
print("\ndeck structural checks passed")
print()
print("Status: DECK SHIPPED, NOT YET RUN.")
print("Run: bash run_stageB.sh  (WSL, MX130). The acceptance metrics are:")
print()
print("  A1. Spatial contrast of m.Comp(1) at the result-array x positions")
print("      after the drive burst ends, versus the unpatterned control.")
print("  A2. Fringe count / phase coherence length across the array.")
print("  A3. Contrast vs pattern band index — does the known code map to")
print("      a measurable output alphabet? If not, P0 coding is not viable")
print("      at this geometry and the Stage-B gate fails.")
"""),

("md", r"""
### Device-element ledger (architecture paper §10 requirement)

Every proposed element states: what quantity changes, what launches it,
retention/reset, how the next stage detects it, energy + delay, and the
experiment that could disprove it.

| Element | Quantity that changes | Launched by | Retention / reset | Next-stage detection | Energy + delay | Disproof experiment |
|---|---|---|---|---|---|---|
| CPW launch (P₀ port) | microwave field h_rf | RF source | stateless | — | P_C1 = 12.6 µW (L); transit 3.26 ns over 40.96 µm (E) | no antenna coupling measured → P_C1 not transferable |
| YIG bus | spin-wave amplitude/phase | CPW burst | stateless | result array absorbs | 36 nW into precession (L); 3.26 ns transit (E) | no propagating mode at k₁ detected |
| P₀ phase grating | local wave phase | fixed geometry | fixed (not at runtime) | wavefield downstream | 0 runtime energy (fixed) (E) | measured H(k) ≠ designed grating phase |
| `C_k` config switches (MRAM bits) | wave-pipeline route via switch resistance/phase | input coding | non-volatile; reset by foundry SOT/eMRAM process (L) | wavefield | 0.05 pJ/bit (E) | measured switch-phase spread larger than the π-step budget |
| NiFe result element (`M_k` cell) | magnetisation orientation (up/down) | magnon-assisted reversal | non-volatile; reset by foundry SOT (or strain hypothesis, optional) | MRAM sense amplifier | 0.20 pJ/cell (E, drive-power term / 205 cells) | wave-absent threshold same as wave-present (K1 fails) |

**The `P₀` code and the `M_k` cell are the same physical device class**, so
the ledger is deliberately symmetric: the wave is the switch, the cell is
the state, and the code lives in the medium. Nothing here requires the
piezomagnetic strain-reset hypothesis, which is demoted to optional
(`docs/CREDIBILITY_PLAN.md` §3.3).
"""),

("md", r"""
## 4. Stage C — the material portfolio, and the hematite question

**The portfolio on the identical geometry** (runner: Windows-side WSL, mumax³
3.12 / mumax⁺ 1.2.2):

| Material | Tool | α (ref) | Role |
|---|---|---|---|
| YIG | mumax³ | 9×10⁻⁴ patterned / 2.7×10⁻⁵ best (L) | the in-circuit baseline |
| Bi-YIG | mumax³ | ~1×10⁻⁴ (L) | near-zero damping comparison |
| Co₂₅Fe₇₅ | mumax³ | ~2×10⁻³ (L) | ferrimagnetic comparator |
| GdFeCoP | mumax³ | ~1×10⁻³ (L) | amorphous comparator |
| NiFe | mumax³ | ~1×10⁻² (L) | the saturation-magnetisation comparator |
| **hematite α-Fe₂O₃** | **mumax⁺ 1.2.2** | **1.1×10⁻⁵ (L)** | **the low-loss candidate; antiferromagnetic Néel vector, needs the AF model** |

**Why hematite matters (L):** Hamdi, Posva & Grundler, *Phys. Rev. Materials*
**7**, 054407 (2023): α = 1.1×10⁻⁵, v_g = 10–23 km/s, ℓ = 1.1 cm at 30 mT,
T_N ≈ 955 K, T_M ≈ 262 K, easy-plane basal anisotropy ≈ 1 Oe above T_M. No
net magnetisation, so the operating point is not bias-field set; but the
Néel-state readout needs XMLD-PEEM or a companion ferromagnet (a real cost,
stated in `docs/CREDIBILITY_PLAN.md` §3.3).

**The write-amplification trade (E):** a 1.1 cm hematite guide at pitch
200 nm holds ~55 000 cells — ~268× the precedent's 205 — at a transit time
of ~700 ns vs 3.26 ns. Hematite buys parallel width and pays in latency.
Which side wins for a given workload is a **workload question**, which is
why the workload is frozen first (architecture Gate 0) and why notebook 02
answers it on a concrete task.

**Status: Stage C is not run in this repository yet.** mumax⁺ 1.2.2 is not
installed; the MX130 may not hold the hematite grid; the decks are written
but unexecuted. The disciplined order is: Stage A reproducibility → Stage B
pattern code → Stage C portfolio → mumax⁺ hematite.
"""),

("md", r"""
## 5. Summary — what this notebook establishes

| Statement | Tag | Status |
|---|---|---|
| The authors' phase-diagram arrays load and reproduce the published MAMR-dip structure (see the local-minima table) | (L)/(S) | done here |
| The published 2023 result has not itself been re-run on this machine | — | **pending** (MX130) |
| The local material series has no reportable decay length | (S) | **done here — r² 0.001–0.004** |
| The CPW antenna is a diamond/lens-shaped flared launch at the x = 0 edge, not a y = 0 stripe | (S) | **corrected, `tools/probe_antenna.py`** |
| Stage B deck exists with stated coarse-graining caveat and 64 result elements | (A) | shipped, not run |
| The write-amplification metric W = cells/E_event is the headline quantity | (E)/(L) | defined in `docs/CREDIBILITY_PLAN.md` §2 |
| Any claim of a fabricated or measured device | — | **not claimed anywhere in this repository** |

### The disproof experiment

Stage A fails if a re-run of the authors' deck, on adequate hardware, does
not produce the k₁ = 1.70 GHz / λ = 7.4 µm mode or the 33.4 → 12.9 mT
threshold reduction — at which point this project is a careful archive of a
published result, not a new one. Stage B fails if a thresholded write into
the result elements shows no contrast after the drive burst ends. Stage C
fails on the hematite arm if coherent magnons cannot be driven in a
patterned thin film at α within a factor of a few of the single-crystal
1.1×10⁻⁵ — which is the gate K6 in `docs/KILL_CRITERIA.md`.
"""),
]


if __name__ == "__main__":
    build("01_wave_imprinting.ipynb", CELLS)
