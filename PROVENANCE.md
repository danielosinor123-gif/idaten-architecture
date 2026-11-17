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
  "solve DFT". PySCF is used only to supply an **independent** ground-truth
  electron density for a separate cross-check.
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
