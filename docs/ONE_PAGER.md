# Idaten Ce100 — one page

*(Deep-tech summary. Full detail: `docs/CREDIBILITY_PLAN.md`, `docs/PRIOR_ART.md`, `docs/KILL_CRITERIA.md`, `PROVENANCE.md`.)*

---

## The idea in one sentence

A **magnonic bus** carries a wave whose amplitude and phase pattern encode a
computation; the wave **writes the answer into a standard foundry MRAM array**;
the answer is **read once, after the workload ends** — so the compute path never
pays for an electrical conversion between operations.

## Why the three state objects are the point

| | Code | Configuration | Result |
|---|---|---|---|
| `P₀` | fabricated geometry | — | — |
| `C_k` | — | runtime switch states | — |
| `M_k` | — | — | **persistent magnetic memory** |

Prior magnonic computing conflates configuration and result (spin-wave cellular
automata) or reads the result out after every operation (magnonic ANNs,
4f-style spatial computing). This architecture separates all three. **That
separation is the claim; the physics is a known primitive we are reusing.**

## Why now — four facts from the last 24 months

1. **Coherent magnons in patterned hematite thin films** — α ≈ 10⁻⁵, stripline-driven.
   arXiv:2610.37205, 27 Oct 2026. *The enabling result for the low-loss bus.*
2. **Hematite's GHz branch measured** — α = 1.1×10⁻⁵, v_g 10–23 km/s, ℓ = 1.1 cm at 30 mT.
   *Phys. Rev. Materials* **7**, 054407 (2023).
3. **SOT-MRAM is manufacturable on 300 mm with CMOS-compatible processes**, switching down to **300 ps**.
   IMEC. *Our result medium is a process that already exists.*
4. **GF 22FDX eMRAM in production since 2018**; Auto Grade 1 eMRAM announced March 2026.
   **GlobalFoundries is a Silicon Catalyst strategic partner.**

## The one metric everything depends on

```
W = cells switched per wave event ÷ energy of that wave event
```

From published numbers only (E): a 1.70 GHz wave on a 40.96 µm bus transits in
**3.26 ns**; the drive-power term is **41 fJ per event**; the bus holds **205**
cells at a = 200 nm → **0.20 fJ per written cell**, against an assumed
5–20 pJ/bit for a foundry MRAM write. **That four-to-five-orders-of-magnitude
gap is a naive bound, not a result** — it assumes the whole 205-cell event is
written correctly and ignores transducer, driver and circuit overhead. It is an
assumption until measured. The valuable quantity is not this ratio but `W`:
cells switched per wave event. This is the project's headline metric, measured
with error bars in Phase 0, and it is the first thing we will report, win or
lose.

## What we have today

- A **reproducible spine**: the 2023 *Nature Communications* precedent re-run
  from the authors' own mumax³ decks (vendored, CC-BY-4.0, fetched in 1.27 MB
  via HTTP range requests instead of 1.66 GiB), plus their published
  phase-diagram arrays as independent ground truth.
- A **withdrawn claim**, publicly: a prior internal decay-length figure
  (70/55/148 µm) that no well-conditioned fit supports (r² = 0.001–0.004) has
  been withdrawn and is re-measured from scratch.
- **Two GDS artifacts**, deliberately labelled differently: a **PDK-backed
  open-flow layout** and a **concept mask** (no PDK exists for hematite or
  LiNbO₃ patterning).
- **A chemistry analogue** claimed as what it is: a linear Green's-function /
  Poisson operator with a stated error bound against an independent direct
  solve — **not** "spin waves emulate DFT".
- A **full §9 energy ledger** with measured write-power anchors (36 nW /
  3.4 nW), not projected fJ/MAC figures.

## The plan

| Phase | Months | Deliverable | Gate |
|---|---|---|---|
| **0** | 0–6 | reproduce the precedent; measure `W` and `E_wave`; publish prior art, kill criteria and this ledger | K1–K4 — **one GPU, one month** |
| **1** | 6–18 | bus-material shoot-out (YIG / hematite / LiNbO₃); testable landscape whose measured `H(k)` is used to re-derive the analogue error band | K5–K8 |
| **2** | 18–30 | 1 mm² test vehicle in a 22/28 nm MPW: bus module + MRAM array, so that **current-assisted and magnon-assisted writes are compared on the same array in the same run** | K9–K10 |
| **3** | 30–48 | lead product: an **always-on edge magnonic spectral classifier**, measured against a matched digital baseline | K11 |

**Lead product:** an edge RF/spectrum classifier, *not* the general execution
processor. Same cell, same bus IP, one small die, a real buyer today. The
execution processor is the scale-up.

## The ask

- **A foundry relationship** — specifically: a discussion about writing a
  qualified eMRAM/SOT-MRAM array with a wave instead of a current. We need the
  answer, not the silicon.
- **A materials partner** for the bus film (hematite or LiNbO₃ on sapphire),
  and a magnetoelastic-strain measurement capability.
- **A hardware lead and a foundry liaison** — the two roles the project does
  not yet have.
- **One MPW shuttle slot**, with a named date.

## What would make us stop

Two gates end the project: **K1** — the wave-assisted write threshold does not
drop by at least 50 % at our geometry — and **K10** — the result pattern cannot
be read once with a BER ≤ 10⁻⁶ at acceptable energy. Both are answerable on
cheap hardware long before any commercial commitment. Seven other gates have
fallbacks (e.g. hematite → YIG; strain reset → foundry SOT reset; compute →
sensor). Full table: `docs/KILL_CRITERIA.md`.
