# KILL CRITERIA — the gates that end this project if they fail

**Philosophy.** A gate is not a milestone. A milestone is something you finish;
a gate is something that can **end** the project. Every gate below has:

1. a **binary** pass condition (no "reasonable progress"),
2. a **measurement method** that exists today,
3. a **threshold** stated as a number,
4. a **deadline**,
5. a **consequence**, including the fallback if there is one.

The gates are ordered **cheapest-falsification first**, so that the project
spends as little as possible before it can die.

**Evidence tags.** `(L)` literature · `(S)` simulated here · `(E)` engineering
estimate · `(A)` hypothesis under test.

---

## Gate block A — physics and economics (simulated; 0–6 months; no hardware spend)

### K0 — Toolchain and archive integrity
- **Measure:** `data/lab_archive/_summary.json` lists every deck with its
  snapshot count and fit metrics; the mumax³ version is pinned.
- **Pass:** ≥ 10 decks and ≥ 4 000 snapshots archived, with every deck's fit
  metrics including r².
- **Fail →** no deletion of raw snapshots; re-run the archiver.
- **Status:** in progress (8 decks archived at time of writing).

### K1 — The write primitive is real at our geometry
- **Measure:** the in-plane field required to reverse a 100 × 20 nm Ni₈₁Fe₁₉
  element **with a propagating magnon present** vs. **with no wave**.
- **Pass:** reduction ≥ 50 % of the published effect (i.e. threshold ≤ 23 mT,
  against the published 33.4 → 12.9 mT (L)).
- **Fail →** **the thesis fails.** Wave-assisted writing is not a usable effect
  at our geometry; stop.
- **Cost:** one mumax³ run + the authors' deck. Days, not months.

### K2 — Write economics
- **Measure:** energy per **correctly** written cell, `E_cell = E_wave / N_cells`,
  with the error rate of the written pattern measured, not assumed.
- **Pass:** `E_cell ≤ 1 pJ` at a write error rate ≤ 10⁻³.
- **Fail →** no advantage over foundry MRAM write (5–20 pJ/bit, (E), to be
  replaced by a cited figure). **Fallback:** pivot the project to a
  **read-only** magnonic sensor, which does not need the write economics.
- **Depends on:** K1.

### K3 — Parallelism
- **Measure:** cells switched per wave event, `N_cells`.
- **Pass:** `N_cells ≥ 64` (i.e. `W ≥ 64 / 41 pJ ≈ 1.6 cells/pJ`).
- **Fail →** the architecture degenerates into a serial chain and the density
  argument disappears. **Fallback:** a serial magnonic interconnect, which is
  a much smaller and much more crowded field.
- **Depends on:** K1.

### K4 — The decay length is measurable and stated
- **Measure:** log-linear fit of the time-averaged envelope over a stated x
  window, **with r² reported**.
- **Pass:** r² ≥ 0.8 on a stated window for a stated material.
- **Fail →** the quantity is **not reportable** and must not appear in any
  table. (This gate exists because the prior internal 70/55/148 µm figure had
  r² = 0.001–0.004 and was withdrawn — see `PROVENANCE.md` §2.3.)
- **Cost:** minutes, from the existing archive.

---

## Gate block B — materials and process (6–18 months)

### K5 — Bus material integration
- **Measure:** total thermal budget of the bus-material integration, and the
  measured α, v_g and ℓ of the fabricated film.
- **Pass:** total thermal budget ≤ 450 °C (matching the modern 3D-integration
  ceiling, L: CEA-Leti 400 °C programme) **or** the bus is planned as a
  separate die that is wafer-bonded (making the thermal budget a packaging
  question, not an integration question).
- **Fail →** the YIG route is dead; restrict to hematite / thin-film LiNbO₃ and
  accept the thin-film risk. **Fallback:** separate bus die.

### K6 — Hematite-specific: is the low-loss branch usable in a patterned thin film?
- **Measure:** coherent magnon resonance and a thresholded write in a
  **patterned thin film**, with the measured α compared against the
  single-crystal 1.1×10⁻⁵ (L).
- **Pass:** demonstrable coherent magnons and a thresholded write in thin film.
- **Fail →** **hematite is dropped entirely** and the project continues on YIG
  with a 2.5× shorter propagation distance. This gate exists because the
  Oct 2026 microdisk paper (L) names strain sensitivity and spatial
  inhomogeneity as the central obstacle for coherent magnons in thin films.
- **Note:** this gate is about *whether hematite works*, not about whether the
  architecture works. It is a **scope** gate, not a **thesis** gate.

### K7 — The strain-reset hypothesis, tested honestly
- **Measure:** (a) the strain amplitude needed to reset the Néel state;
  (b) the change in the magnonic response of the bus under that strain.
- **Pass:** reset achievable at a strain whose perturbation of the bus is
  below the error budget of the write.
- **Fail →** **strain reset is dropped.** This is acceptable, because the
  foundry SOT-MRAM path supplies a qualified reset mechanism
  (`CREDIBILITY_PLAN.md` §4.2). **This gate is deliberately allowed to fail
  without killing the project.**

### K8 — The programmable landscape is calibratable
- **Measure:** the transfer function `H(k)` of a fabricated landscape, measured
  with a VNA, compared against the design and against the phase-quantisation
  error model of notebook 03.
- **Pass:** the measured `H(k)` reproduces the **measured** analogue output
  within the error band predicted from the *measured* phase deviation.
- **Fail →** notebook 03's error model is wrong and must be corrected before
  any analogue-accuracy claim is made. (This is the disproof experiment
  specified in notebook 03.)

---

## Gate block C — foundry shuttle (18–30 months)

### K9 — Same-array write comparison
- **Measure:** on **one** array, in **one** run, the write energy and error
  rate of (i) current-assisted writes and (ii) magnon-assisted writes.
- **Pass:** magnon-assisted write energy ≤ 50 % of current-assisted on the
  same array at equal error rate.
- **Fail →** the magnonic front-end adds cost rather than removing it.
  **Fallback:** the project becomes a **sensor** company, not a compute
  company — which is still a company, and still uses the same bus IP.

### K10 — The result pattern survives and reads once
- **Measure:** error rate of the written pattern after one workload, read out
  once, with the read energy included in the ledger.
- **Pass:** BER ≤ 10⁻⁶ after one workload; total read energy ≤ 20 % of the
  compute energy.
- **Fail →** **the persistence claim fails.** If the result cannot be read
  once, reliably, at acceptable energy, there is no memory and no architecture.

---

## Gate block D — product (30–48 months)

### K11 — System-level advantage against a matched baseline
- **Measure:** total system energy per inference (compute + write + reset +
  read + control + package), against a matched digital baseline running the
  same workload and the same accuracy.
- **Pass:** ≥ 5× system energy advantage at equal accuracy, **or** ≥ 10×
  latency advantage at equal energy, for the lead edge-classifier product.
- **Fail →** no product. The project stops, having published the physics.

---

## Gate ordering — cheapest falsification first

| Order | Gate | Cost to run | Weeks to answer |
|---|---|---|---|
| 1 | K4 (r² on the existing archive) | minutes | this week |
| 2 | K1 (wave-assisted threshold, simulated) | 1 GPU-day | 2–4 weeks |
| 3 | K3 (parallelism, same run as K1) | included | 2–4 weeks |
| 4 | K2 (write economics, same run as K1) | included | 2–4 weeks |
| 5 | K8 (landscape calibration) | one fabricated chip + a VNA | 4–9 months |
| 6 | K6/K7 (hematite scope) | materials partner | 6–18 months |
| 7 | K9/K10 (foundry shuttle) | one MPW shuttle | 18–30 months |

**The first four gates cost one GPU and a month.** If the architecture is
wrong, that is the price of finding out.

---

## What "killed" means in practice

Every gate above has a fallback except **K1**. The fallbacks are not
consolation prizes:

| Gate | Fallback | Is it still a company? |
|---|---|---|
| K1 fails | **none** | no |
| K2 fails | magnonic **sensor** product | yes — edge RF/spectrum sensing |
| K3 fails | serial magnonic interconnect | yes, but a crowded market |
| K5 fails | bus as a separate wafer-bonded die | yes |
| K6 fails | YIG bus | yes |
| K7 fails | foundry SOT reset | yes (this is the expected path) |
| K8 fails | correct the error model, re-claim | yes |
| K9 fails | sensor product | yes |
| K10 fails | none | no |

Two gates can kill the company: **K1** (the write primitive is not real) and
**K10** (the result cannot be read once, reliably). Both are measured on
small, cheap hardware long before any commercial commitment.
