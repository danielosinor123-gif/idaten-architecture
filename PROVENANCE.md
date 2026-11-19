# PROVENANCE.md — Idaten Ce100

**Every quantitative claim in this repository carries one of four evidence tags.**
Anything untagged is a description of intent, not a result.

| Tag | Meaning | What it requires |
|---|---|---|
| **(L)** | Literature | A citable published source, named in `references` below |
| **(S)** | Simulated | Produced by code in this repo, with the run command and tool version recorded |
| **(E)** | Engineering estimate | A calculation from stated assumptions; assumptions are written down next to the number |
| **(A)** | Predicted | An architectural hypothesis. No supporting measurement exists yet |

---

## 0. Claims this repository explicitly does **not** make

Per the source architecture paper (Idaten Ce100, rev. 16 Nov 2026, §10), the
following are prohibited as established facts anywhere in this repo:

- "zero resistance"
- "absolute zero idle power"
- "free computation"
- "instant switching"
- "world's most efficient" (or any global-superlative efficiency claim)

Additional self-imposed constraints:

- **Chemistry.** Notebook 03 demonstrates *analogue-operator equivalence* for a
  linear Green's-function / Poisson operator. It does **not** claim that spin
  waves emulate Schrödinger or Kohn–Sham operators, and does **not** claim to
  "solve DFT". PySCF is used only as an **independent** quantum-chemistry
  cross-check of the same geometry (SCF energy); it is not an input to the
  analogue and is not compared to the analogue density.
- **No fabricated-device claims.** Nothing here reports a fabricated, measured,
  or packaged device. Every device-level statement is (A) or (E).
- **Two different GDS files, two different labels.** See §5.

---

## 1. Architecture spine

The authoritative document is *Idaten Ce100: Pattern-Coded Magnonic Execution,
Persistent Magnetic Results, and Dynamic Rails* (rev. 16 Nov 2026). It defines
four distinct state objects, and the whole architecture hinges on keeping them
conceptually separate:

| Symbol | Name | Mutable by | Read by |
|---|---|---|---|
| `P₀` | Fabricated transistor/switch topology | not at runtime | — (fixed) |
| `C_k` | Execution configuration (switch states) | input coding, per step | control logic |
| `Ψ_k` | Live wavefield | physics | wave bus |
| `M_k` | Persistent magnetic result pattern | write stage | **final readout only** |

`C_k` (configuration) and `M_k` (result) must not be conflated. A result pattern
is read once, after the individual workload completes — not per operation.

### Capability ladder and gates

R0→R6 capability ladder, Gate 0→8 acceptance gates, per the source paper.
**Gate 0 freezes the workload and the result-pattern alphabet before any device
optimization.** Notebook 02 specifies the target `M` first; Stage B of
notebook 01 is scored against that frozen target, not against whatever the
device happened to produce.

---

## 2. (S) — Simulated results

### 2.1 Toolchain

| Component | Version | Host |
|---|---|---|
| mumax³ | 3.12 | WSL2, CUDA 12.0, NVIDIA GeForce MX130 (2 GB VRAM) |
| mumax⁺ | 1.2.2 | WSL2 (antiferromagnetic Néel vector, magnetoelastic coupling) |
| KLayout | 0.30.13 | Windows + WSL |
| gdstk | 1.0.2 | Windows |
| PySCF | 2.15.0 | Windows (win_amd64 wheel) |
| PyTorch / NumPy / SciPy | see `requirements.txt` | Windows |

WSL invocations on the development machine are driven by shell scripts (quoting is never
mangled by the Windows shell). The reproducible Python/tool pieces used by this repository
are committed under `tools/` (`archive_lab2.py`, `probe_antenna.py`, `run_notebooks.py`
and the decks under `tools/decks/`). The Windows-side supervisor that resumed the archive
against WSL restarts is a local driver, not part of the reproducible artifact set, and is
not required to reproduce the committed results.

### 2.2 The 2023 published precedent — reproduced

**Source (L):** Baumgaertl & Grundler, *Nature Communications* **14**, 1490
(2023), "Reversal of nanomagnets by propagating magnons in ferrimagnetic yttrium
iron garnet enabling nonvolatile magnon memory". DOI
[10.1038/s41467-023-37078-8](https://doi.org/10.1038/s41467-023-37078-8).
Dataset: Zenodo [10.5281/zenodo.7714181](https://doi.org/10.5281/zenodo.7714181),
CC-BY-4.0.

The authors' own MuMax³ **3.10** decks and Python plotting scripts are
included under `data/zenodo_baumgaertl/`. They were retrieved with **HTTP range
requests only** (`tools/fetch_zenodo.py`) — 151 script members totalling
**1.27 MB** instead of the 1.66 GiB container zip.

The deck `SupplementFig6__Hys_S0.0__02mT.mx3` fixes the published geometry and
material set (S — read directly from the authors' file):

| Quantity | Value in authors' deck |
|---|---|
| Grid | 8192 × 32 × 1, cell 5 nm × 5 nm × 5 nm, `SetPBC(0,0,2048)` |
| YIG bus | 40960 nm × 100 nm |
| Switching elements | 100 nm × 20 nm rectangles, pitch `a` = 200 nm |
| YIG region | `Msat` 140 kA/m, `Aex` 3.75 pJ/m, `alpha` **9×10⁻⁴** |
| Ni₈₁Fe₁₉ region | `Msat` 800 kA/m, `Aex` 13 pJ/m, `alpha` 0.01 |
| Drive file | `CPW32_40um.ovf` (3.1 MB), included in `data/zenodo_baumgaertl/` |
| Published targets to match | k₁ = 1.70 GHz, λ = 7.4 µm, k₁ = 0.85 rad/µm; GC mode λ = 195 nm; αᵢ = 9×10⁻⁴ → ℓ = 99 µm unpatterned, ℓ_d = 23 µm in-circuit; P_C1 = 12.6 µW; P_C2 = 58.4 µW; P_prec = 36 nW (k₁) / 3.4 nW (GC); H_C1 16.8→2.7 mT; H_C2 33.4→12.9 mT; ratio ΔH_C2/Δh_rf,x = 32.1; MAMR dips at 9.25 / 10.75 / 11.75 GHz |

The authors' measured phase-diagram arrays
(`Fig.1__...__PhaseDiagramN.npy`, shape 2×7×49; `SumFull1/2.npy`, 33×49 and
41×49) are included as **independent ground truth** for the switching-threshold
comparison.

### 2.3 Our own prior lab series — an honest negative result

Fourteen mumax³ decks were run locally on the MX130 for this series (grid
2000 × 160 × 1, cell 50 nm × 50 nm × 1.2 µm; CPW edge antenna; in-plane bias
20 mT; burst drive 0.5–3 ns) across YIG, Bi-YIG, Co₂₅Fe₇₅, GdFeCoP and NiFe,
at 2 / 3 / 5 / 10 GHz and several damping values. **Eleven of the fourteen
produced recoverable snapshots**; `YIG_a1e-3_2G_w2`, `YIG_a1e-3_5G` and
`YIG_pma_2G` produced no valid OVF output (for the PMA decks this is expected
by construction — `m = Uniform(0,0,1)` makes the saved transverse component
identically zero). A further seven diagnostic decks from the retired prior programme were archived
and then excluded from the committed evidence (the committed `_summary.json` is
filtered by `tools/build_lab_summary.py`).

**The CPW antenna geometry, stated correctly (S).** An earlier version of this
document described the antenna as "a stripe at the y = 0 edge, x = 2–6 µm".
**That was wrong.** The antenna mask (`antenna.ovf`, 2000 × 160 at 50 nm) was
re-probed by direct rendering of the mask raster, with the result:

| Property | Value |
|---|---|
| Filled cells | **662** |
| Non-empty rows | 80 (y indices 40–119) |
| Bounding box | **x ∈ [0.050, 0.500] µm, y ∈ [2.050, 6.000] µm** |
| Spine | a continuous 1-cell (50 nm) wide vertical strip at **x = 0.050 µm** over the occupied height (y = 2.05–6.00 µm) |
| Flare | the right-hand boundary grows from x = 0.100 µm at y = 2.05 µm to x = 0.500 µm around y ≈ 3.55–4.85 µm, then tapers back to x = 0.100 µm at y = 6.00 µm — a **diamond/lens-shaped launch**, not a 45° wedge |

So the antenna is a **compact flared (diamond-shaped) coplanar-waveguide launch hugging the x = 0.05 µm edge**, not an edge stripe at y = 0. The wave therefore propagates **along +x** from x ≳ 0.5 µm. The corrected renderer is `tools/probe_antenna.py`; it prints the row-by-row extent and the bounding box.

**The raw OVF snapshots (7.3 GB) were archived to compact `.npz` form and then
deleted to reclaim VHDX space.** The archive stores per snapshot: the RMS-over-y
envelope `E_x` and the peak amplitude `P_x` at native x-resolution (2000
points), plus 2-D `|m_y|` maps down-sampled to 500×20. Regeneration path:
`tools/archive_lab2.py`. Archive status as of the cleanup: **18 decks /
5,807 snapshots archived**; the Idaten material series within it is
**11 decks / 4,400 snapshots** (three local decks — `YIG_a1e-3_5G`,
`YIG_a1e-3_2G_w2`, `YIG_pma_2G` — produced no recoverable snapshots and are
recorded as such). The prior-chip and diagnostic decks are excluded from the
committed evidence (`data/lab/_summary.json`, filtered by
`tools/build_lab_summary.py`).

**Finding (S):** the decay length is **not** recoverable from this series with
any well-conditioned fit. Log-linear fits of the time-averaged envelope over
x ∈ [10, 45] µm return r² = **0.001–0.004** for every material and every
frequency. The spatial pattern is dominated by a transverse standing mode
(λ_y = 4 µm) and a longitudinal node at x ≈ 52 µm, and is **nearly
frequency-independent** (see the fit-method sweep used to test the prior
claim; the committed `_summary.json` carries the same fit windows).

Consequence, stated plainly: a previously circulated internal figure of
"ℓ = 70 µm @2 GHz, 55 µm @3 GHz, ~148 µm @5 GHz" for this series is **not
supported by a well-conditioned fit of the archived data** and is therefore
**not** carried forward as a result in this repository. It is recorded here as
a prior internal estimate that failed re-derivation, and the corresponding
quantity is re-measured from scratch in the Stage A/B experiments with an
explicit, stated fit method and reported with its r².

**Two further methodological findings (S)**, both reproducible:

1. mumax³ rounds a requested `run(2e-12)` up to its own internal step. On a
   50 nm cell with `Aex` = 5 pJ/m and `Msat` = 140 kA/m the realised step is
   ≈ 23 ps, so the decks advance ≈ 581 ps per snapshot, not the 50 ps the
   script implies. Any temporal demodulation at 2–3 GHz on this geometry is
   therefore under-sampled; the Stage A/B decks are written to use
   `FixDt`/`MaxDt` explicitly.
2. The archive ordering in mumax³ OVF output is **y-fastest**, then x, then z,
   with `valuedim` consecutive components per point. `tools/ovf_extract.py`
   implements this and is unit-checked against the CPW antenna mask geometry
   (the flared launch described in §2.3: 662 filled cells, x ∈ [0.050, 0.500] µm,
   y ∈ [2.050, 6.000] µm).
3. **A probe bug that produced a wrong published statement (now fixed).** The
   first structural probe reduced the 3-D antenna raster with
   `mask.any(axis=...)`, which collapses the wrong axes and therefore reported
   a transposed orientation — and that wrong orientation was carried into this
   document and the README as "a stripe at the y = 0 edge, x = 2–6 µm" until
   it was caught in this session. The fix is to render the 2-D mask raster
   directly (`tools/probe_antenna.py`) and read the geometry off the raster,
   not off a reduction of it. The lesson is recorded here deliberately: the
   error survived in two documents because the *claim* was plausible and
   nobody re-rendered the mask. Every geometry claim in this repository is now
   checked by re-rendering the file, not by re-reading the intent.

---

### 2.4 Stage B extension — executed on the local MX130

The Idaten extension deck `tools/decks/idaten_stageB.mx3` was run on the
MX130 (committed deck, 2000 × 160 × 1 cells at 50 nm, six `P₀` phase
bands, 64 NiFe result elements coarse-grained to 100 nm × 50 nm at pitch
200 nm). It completed and wrote **40 snapshots** of `m.Comp(1)`.

| Quantity measured (S) | Result |
|---|---|
| Bus envelope log-linear fit, x = 10–45 µm | **r² = 0.0024** (ell = 114 µm) |
| Same fit, x = 5–45 µm | r² = 0.0032 (ell = 111 µm) |
| Same fit, x = 10–50 µm | r² = 0.0051 (ell = 90 µm) |
| Time-averaged pattern contrast across the 64 result elements | **0.955** |
| Result elements above half the maximum amplitude | **9** |

**Gate K4 fails** for this bus. The local decay length is not reportable. The
pattern is non-uniform — evidence that a fabricated landscape can imprint a
spatially structured pattern, not evidence of switching, reversal, or a
write-error rate. Committed artefacts: `data/lab/stageB_summary.json`,
`data/lab/stageB_elements.csv`, `figures/01_stageB_pattern.png`.
Any switching claim remains tied to the published threshold values (L), not to
this simulation.

---

### 2.5 Stage A — published-deck reproduction, run on Kaggle (Tesla T4)

Stage A re-runs the authors' own deck
`SupplementFig6__Sat_S1.0__14mT.mx3` (12 ns driven transient, full
`minimize()`/`relax()` init exactly as published) to establish that the
precedent reproduces on **(S)** before any Idaten extension is attempted.

Because the local MX130 (2 GB VRAM) cannot hold the 8192-cell-long mesh, the
run was executed on a Kaggle Tesla T4 (15 GB) via the kernel
`danielvking/idaten-stage-a-mumax`; assets (deck, `CPW32_40um.ovf`, mumax³
3.12 binary, and the binary's own CUDA 11 runtime libs `libcufft.so.11` /
`libcurand.so.10`, which the T4 image does not ship) are the dataset
`danielvking/idaten-stagea-assets`. The mumax³ binary resolves those libs
through its `RUNPATH $ORIGIN/lib`; they are staged into `work/lib/` by the
kernel script.

Run facts (S — from the kernel log and `table.txt`):

| Quantity | Value |
|---|---|
| Mode | fresh — full published init (no checkpoint resume) |
| Wall time on T4 | ≈ 7.8 min for the 12 ns transient |
| Simulated span | 12.000 / 12 ns (100 %), `mumax exited rc=0` |
| `table.txt` | 2,402 rows, t = 0 → 1.2×10⁻⁸ s, columns `t, mx, my, mz` |
| `Finish.ovf` | OVF 2.0, mesh 40.96 µm × 0.16 µm (8192 × 32 × 1) |
| Outputs pulled | `data/stageA_kaggle/` (`table.txt`, `mStart.ovf`, `Finish.ovf`, runlog, kernel log) |

Two documented deviations from the authors' deck, both sampling-only:

1. **Autosave cadence 10 ps → 50 ps** for `mx_center` and `B_ext_Line`
   (reduces output volume; does not alter the dynamics — mumax³ internal
   stepping is untouched).
2. **[resume path only]** the init block is replaced by `m.LoadFile` of a
   checkpoint. The run reported here used the fresh path, so deviation 2 did
   not apply.

mumax³ empties `deck.out` at startup, so checkpoints are kept outside it
(`stageA_ckpt/`); the committed copies are byte-identical to the `deck.out`
ones and were de-duplicated before commit (MD5-verified).

**Environment note (18 Nov 2026):** the development machine suffered a hard
crash (Event 41) at 12:42 that same day, mid-build. It left a 0-byte
`dbTechLayer.cpp.o` in the OpenROAD tree, which later surfaced as undefined
`odb::dbTechLayer` symbols at link time; the corrupt object was found by
size, deleted, and recompiled. This is recorded because the failure mode
(mtime-valid, content-empty object) is invisible to a normal build log and
cost a full debug cycle — any re-run on this machine should check for
zero-byte build products first.

### 2.6 PDK-backed open-flow layout — ORFS / sky130hd run (19 Nov 2026, (S))

The digital tier (`P₀` MAC pipeline + `C_k` config register + `M_k` result
register, `gds/idaten_sky130/src/idaten_sky130.v`) was taken through the full
ORFS flow on the open sky130hd platform:

| Quantity | Value |
|---|---|
| Entry | `make -f /root/orfs/flow/Makefile DESIGN_CONFIG=.../sky130hd/idaten_sky130/config.mk` (FLOW_EXIT=0, 14 min) |
| OpenROAD | built from source 2026-11-19 (`/root/openroad-src`, BUILD_EXIT=0/INSTALL_EXIT=0), headless GUI patches `IDATEN_GUI_PATCH*` |
| Yosys | 0.71+ conda-forge, TCL 8.6 (ORFS scripts are Tcl; yowasp-yosys WASM build cannot run them) |
| KLayout | 0.30.12 |
| PDK | sky130A files bundled with ORFS (`flow/platforms/sky130hd/`) |
| Timing | constraint 10 ns; WNS 0.00, TNS 0.00, worst slack 2.90 ns, Fmax 140.87 MHz |
| DRC / antenna | 0 violations (DRT-0199), 0 net / 0 pin antenna violations |
| Area | design 14,420 µm² (32% util) in a 216.3 × 216.3 µm die; 6,864 cells |
| Outputs | `gds/idaten_sky130/6_final.{gds,def,v,spef}` (GDS MD5 `ebe60559d93183e20a403abe5941e58c`), reports in `gds/idaten_sky130/reports/`, manifest `gds/idaten_sky130/RUN_MANIFEST.md` |

Label: **PDK-backed open-flow layout** — never presented as the magnonic die
(§5).

### 2.7 Stage C — material-portfolio shoot-out, run on Kaggle (19 Nov 2026, (S))

Kernel `danielvking/idaten-stage-c-mumax` (v4; dataset
`danielvking/idaten-stagec-assets` with mumax³ 3.12 + CUDA-11 libs +
`antenna.ovf` + deck template) ran the identical bare bus
(2000×160×1 @ 50 nm = 100 µm × 8 µm, 64 NiFe result elements at x = 60 µm,
CPW antenna launch, 1.70 GHz / 1 mT burst window 0.5–3 ns, `run(4e-9)`)
once per bus material: YIG, Bi-YIG, CoFe, GdFeCoP, NiFe (parameters (L),
inputs). All five `mumax exited rc=0`; deck.out `table.txt` (t, mx, my, mz
+ 8 x-probe mz averages every 20 ps) + `mStart/Finish.ovf` pulled to
`data/stageC_kaggle/run_<mat>/deck.out/`; analysis `tools/analyze_stageC.py`
→ `data/stageC_kaggle/stageC_summary.json`; figure
`figures/stageC_material_shootout.png` (`tools/fig_stageC.py`).

Deck fixes verified locally on mumax³ 3.12 before the successful run
(`gdsii_run/smoke_stageC.sh`): `tableadd` takes one argument; the default
table already carries t/mx/my/mz; probes are `tableadd(Crop(m.Comp(2),
xc0, xc0+80, 0, 80, 0, 1))` (table stores the crop average); the
`@MATERIAL_BLOCK@` placeholder must sit on its own line or the runner's
first line (Msat) gets commented out; the burst window is anchored to
post-relax `t0 := t`.

Measured (S):

| Material | f_dom (GHz) | probe-RMS decay fit ℓ (µm, 10–80 µm) | v_g |
|---|---|---|---|
| YIG | 1.93 | ~63 (far probe still ~20 % of near) | xcorr median ≈ 21.6 km/s but lag spread ≈ median → not resolved |
| Bi-YIG | 1.93 | ~42, flat | not resolved |
| CoFe | 2.94 | ~119 | not resolved |
| GdFeCoP | 3.55 | ~266, flat | not resolved |
| NiFe | 7.68 | ~60, lowest amplitudes | not resolved |

Reading: f_dom increases with Msat; no material attenuates within the 100 µm
bus at this drive; with only ~8 cycles at ~10⁻⁴ amplitude in a 4 ns window,
group velocity is **not resolved** — longer run is the follow-up. The
hematite (α-Fe₂O₃) arm needs mumax⁺ 1.2.2 (AF Néel model) and is **not**
in this run — it is §2.8 below.

### 2.8 Stage D — hematite (α-Fe₂O₃) AF bus, mumax⁺ 1.2.2 on Kaggle (19 Nov 2026, (S))

Kernel `danielvking/idaten-hematite-mumaxplus` (v6; deck dataset
`danielvking/idaten-hematite-assets`). The solver is the PyPI wheel
`mumaxplus==1.2.2` (GPL-3.0-only), pip-installed inside the kernel
(`enable_internet: true`, FP32/SINGLE), on the T4 (sm_75 — the wheel's
embedded PTX targets sm_52 only and JITs under the T4's CUDA 13.0; the
local MX130 sm_61 cannot, so **all mumax⁺ runs go to Kaggle**; GPU sanity
check printed `GPU_SANITY_OK`). Deck
`tools/decks/idaten_hematite_mumaxplus.py`: 1000×80×1 cells @ 100 nm
(100 µm × 8 µm × 100 nm bus), **fixed solver dt = 0.2 ps**, 100 ps settle,
8 ns run, table every 20 ps, **200 probes at 0.5 µm spacing**
(x = 0.25…99.75 µm); z-stripe RF launch at x ≈ 1 µm; burst window 0.5–3 ns.

Parameter mapping (derived from the v1.2.2 source `src/physics/afmexchange.cu`):
`afmex_cell = −H_E·Ms·latcon²/4 = −5.85×10⁻¹¹ J/m`,
`afmex_nn = −A_T·Ms = −8.24×10⁻¹² J/m`, with (L) inputs
Ms_sub = 9.0×10⁵ A/m, α = 1.1×10⁻⁵ (PRM 7, 054407), H_E = 1040 T
(arXiv:2610.08030), latcon = 0.5 nm, μ₀A = 9.153×10⁻⁶ T·µm²
(arXiv:2212.11887), easy-plane H_a = 1 Oe = 79.58 A/m
(`ku1 = −0.5·Ms·H_a` — mumax⁺'s anisotropy-field kernel carries no μ₀, so
ku1 is in internal-field units, probe-verified in `anisotropy.cu`),
30 mT bias along x, Néel vector along y. Documented deviations:
**DMI = 0** and **demagnetisation disabled** ((E): net M ~ Ms·H/H_E
~ 10⁻⁵ Ms).

Predicted (E): qFM gap f_gap = γ√(2H_E·μ₀H_a)/2π ≈ **12.78 GHz**;
v_g,max = γ√(2H_E·A_T) ≈ **24.3 km/s** vs (L) 10–23 km/s (Hamdi, Posva &
Grundler, PRM 7, 054407 (2023)).

Two arms, one full 8 ns run each (deck rc=0; 268 s and 255 s wall on the T4;
a kernel running both arms back-to-back is CANCEL_ACKNOWLEDGED at ~9–10 min
total, so v6 ran the credibility-critical 15 GHz arm first; the 1.70 GHz
arm is from v5, also rc=0):

| Arm | (S) result |
|---|---|
| 1.70 GHz, 1 mT — below the (E) gap | forced/evanescent response only: dispersion-ridge points f ≈ 0.6–2.8 GHz, c₂/pred ≈ 0 — **consistent with the gap; no propagating branch below it** |
| 15 GHz, 0.1 mT (= 1 Oe = H_a, linear regime) — above the gap | launcher probe f_dom **14.23 GHz** vs 15 GHz drive; **global ring-down 12.97 GHz vs (E) gap 12.78 GHz — 1.5 % match, validating the afmex_cell ↔ H_E mapping**; end-field decay ℓ ≈ **2477 µm ≫ 100 µm bus** (no in-bus attenuation; cf. (L) ℓ = 1.1 cm at 30 mT) |

Measured (S) for both arms in `data/hematite_kaggle/hematite_summary.json`
(analysis `tools/analyze_hematite.py`; raw tables, end-field `neel_end.npz`
snapshots and the kernel log under `data/hematite_kaggle/`):

- **v_g NOT resolved.** Cross-correlation lags between adjacent probes
  (0.5 µm spacing, 198 pairs) have spread ≫ median (15 GHz arm: median
  221 m/s, spread 4.1 km/s); packet-arrival times are simultaneous
  (t ≈ 3.0 ns) at all probes — the ring-down is a **standing/global mode**,
  not a traveling packet, so no group velocity is extractable from this
  window. The 2-D FFT dispersion ridge (89 k-points) is dominated by
  standing-wave peaks (f_gap fit 16.7 GHz, c₂/pred = 0.07), not the
  propagating branch. Follow-up: longer run + windowed launch.
- **AFM-order caveat (S):** intracell angle transient min **2.33° at
  t = 0.14 ns** (local order collapse at burst onset); post-burst mean
  123°, max 169–174°. The drive pushes the AFM locally nonlinear; the
  linear-regime numbers above carry this caveat.
- **Energy:** e_total changes < 0.5 % over 8 ns in both arms
  (−6.8204×10⁻⁸ → −6.8547×10⁻⁸ J at 1.70 GHz; −6.8204×10⁻⁸ →
  −6.7947×10⁻⁸ J at 15 GHz) — no numerical runaway; the 15 GHz arm's sign
  is not cleanly dissipative (drive work during the burst), stated as-is.
- probe RMS vs x is flat-to-rising (15 GHz arm: 0.27 → 0.37) — the same
  standing-mode signature, not a 1/e decay.

Deck fixes probe-verified on the T4 before the successful runs:
FieldQuantity/ScalarQuantity wrappers are callable, so `quant()`/`sub()`
check `_impl` rather than `callable()`; fixed-timestep mode
(`timesolver.adaptive_timestep = False`, dt = 2×10⁻¹³ s) because the
adaptive stepper near equilibrium can advance only one clamped step per
`run(dur)`; an FP32 guard on the final `run()` chunk (stoptime − t rounds
to ≤ 0 at ulp(t) ≈ 5×10⁻¹⁶ s near t = 8 ns, which otherwise throws
"timestep ≤ 0"); `afm.bias_magnetic_field` returns sub1's Parameter, so
the static bias and the RF time term are set on **both** sublattices
individually.

---

## 3. (L) — Literature values used

| Quantity | Value | Source |
|---|---|---|
| Hematite GHz-branch damping | α = 1.1×10⁻⁵ | Hamdi, Posva & Grundler, *Phys. Rev. Materials* **7**, 054407 (2023) |
| Hematite group velocity | v_g = 10–23 km/s | same |
| Hematite decay length | ℓ = 1.1 cm at 30 mT | same |
| Hematite Néel temperature / Morin temperature | T_N ≈ 955 K / T_M ≈ 262 K | same |
| Hematite basal anisotropy (in-plane, at RT) | ≈ 1 Oe (easy-plane above T_M) | same |
| Hematite piezomagnetism | Q₂₂₂, Q₃₂₁ non-zero | literature (see references) |
| Best-YIG damping for comparison | αᵢ = 2.7×10⁻⁵ (YIG) vs 1.1×10⁻⁵ (hematite) | Hamdi et al. 2023 |
| mumax⁺ capabilities (AF Néel vector, magnetoelastic) | — | Moreels et al., *npj Spintronics* (2026) |
| Magnonic-compute metrics taxonomy | — | Kurebayashi et al., *Nat. Rev. Phys.* **8**, 208–225 (2026) |
| Inverse design for AI magnonics | — | Vilsmeier et al., arXiv:2607.07324 (2026) |

---

## 4. (E) — Engineering estimates and the energy ledger

The energy model follows the source paper §9 exactly:

```
E_total = E_input + E_configuration + E_switch + E_magnon + E_state_write
        + E_state_hold + E_reset/erase + E_final_readout + E_decode
        + E_memory/control + E_package/host
```

and its amortized form

```
E_per_inference = E_configuration_write/R + E_input + E_magnon_compute
                + E_result_write + E_reset + E_final_read + E_control
```

**The important upgrade over the earlier internal model:** `E_state_write` is
anchored to **published measured power** rather than to a projected fJ/MAC.
Two anchors are used, both (L):

| Anchor | Value | Condition |
|---|---|---|
| Power into precession, k₁ mode | **36 nW** | Baumgaertl & Grundler 2023 |
| Power into precession, grating-coupling mode | **3.4 nW** | Baumgaertl & Grundler 2023 |

The earlier **2.5 fJ/MAC** figure was an ArchSim projection from the previous
chip's architecture. It is **(A)** — predicted — and it is *not* used as a
measured anchor anywhere in this repository. It survives only in a clearly
labelled "Projected Silicon" section.

---

## 5. GDS files — two different things, two different labels

| File | What it is | Label used everywhere |
|---|---|---|
| `gds/idaten_sky130/` | OpenROAD Flow Scripts / SKY130 digital tier, produced by a real open-flow run | **PDK-backed open-flow layout.** A foundry-recognizable artifact: the physical instantiation of `P₀` and the `C_k` configuration switches. |
| `gds/idaten_concept_mask/` | 5 mm × 5 mm magnonic die written with `gdstk`: bus, cell array at `a` = 200 nm, CPW launch/detect, alignment marks | **Concept mask — no PDK exists for hematite or LiNbO₃ patterning.** Coordinates are dimensioned and nanometre-accurate, but this is not a manufacturable mask set. |

They are never presented as equivalent, and never in the same figure without
their labels.

---

## 6. Device-element ledger (paper §10 requirement)

Every proposed element in this repository states: what quantity changes, what
launches it, retention/reset, how the next stage detects it, energy and delay,
and the experiment that could disprove it. The table is maintained in
`notebooks/01_wave_imprinting.ipynb` (Stage B) and in `docs/device_ledger.md`.

---

## 7. References

1. K. Baumgaertl, D. Grundler, *Reversal of nanomagnets by propagating magnons
   in ferrimagnetic yttrium iron garnet enabling nonvolatile magnon memory*,
   **Nature Communications 14**, 1490 (2023).
   DOI: 10.1038/s41467-023-37078-8 · Dataset: 10.5281/zenodo.7714181 (CC-BY-4.0).
2. M. Hamdi, F. Posva, D. Grundler, *Spin wave dispersion of ultra-low damping
   hematite (α-Fe₂O₃) at GHz frequencies*, **Physical Review Materials 7**,
   054407 (2023).
3. J. Moreels et al., *mumax⁺: extensible GPU-accelerated micromagnetics and
   beyond*, **npj Spintronics** (2026).
4. S. Kurebayashi et al., *Metrics for spin-based computing*, **Nature Reviews
   Physics 8**, 208–225 (2026).
5. F. Vilsmeier, F. Bruckner, C. Abert, D. Suess, A. V. Chumak, *Perspectives on
   inverse design for AI magnonics*, arXiv:2607.07324 (2026).
6. *Idaten Ce100: Pattern-Coded Magnonic Execution, Persistent Magnetic Results,
   and Dynamic Rails*, rev. 16 Nov 2026 — the authoritative architecture
   document (internal; source of the four state objects, R0–R6 ladder,
   Gate 0–8, §9 ledger and §10 guidance).
