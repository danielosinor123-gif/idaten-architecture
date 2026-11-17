# CREDIBILITY PLAN — how this work gets taken seriously by three very different audiences

**Purpose.** Three audiences will evaluate this project, and each one gates on a
different question. This document states, for each audience: what they will
actually check, what in this repository currently fails that check, what has to
change, and by when. It also names the **one metric** that the entire economic
case depends on, so that the work can be killed cheaply if the metric fails.

**Evidence tags.** `(L)` literature · `(S)` simulated here · `(E)` engineering
estimate · `(A)` predicted/architectural hypothesis.

---

## 0. Executive summary — the three gates

| Audience | Their one question | Current state | The fix |
|---|---|---|---|
| **Spintronics professors** | *"Is the physics right, and what is genuinely new?"* | **~70% there.** Physics reproduces a 2023 *Nature Communications* result; one honest negative result is documented. Missing: prior-art differentiation, a staged experiment list, the hematite-specific gap statement | `docs/PRIOR_ART.md`, this document §3–§4, `docs/KILL_CRITERIA.md` |
| **Foundries (IMEC-class)** | *"Can you make this on 300 mm, in my process, above my logic?"* | **~20% there.** The concept mask is honest but irrelevant to them: no process exists for the material it draws | **Move the result medium `M_k` into a foundry MRAM free-layer array.** See §4 — this is the single highest-leverage change in the project |
| **Deep-tech accelerators (Silicon Catalyst-class)** | *"What do you measure, by when, and what kills the project?"* | **~25% there.** Good artifacts, no product, no dates, no kill criteria | §5 roadmap, §6 kill criteria, and a lead product that is not the general "execution processor" |

### The single highest-leverage architectural change

> **The persistent magnetic result pattern `M_k` should be a standard foundry
> MRAM free-layer array — not a bespoke nanomagnet array on a magnonic die.**

Why this matters, concretely:

1. The switching element in the published precedent (Baumgaertl & Grundler 2023)
   is a **100 nm × 20 nm Ni₈₁Fe₁₉ rectangle** (L) — that is *already* an MRAM
   free-layer geometry and material. The result medium is not exotic; it is
   what a foundry already makes.
2. Foundry SOT-MRAM is **demonstrated manufacturable on 300 mm Si with
   CMOS-compatible processes**, with single-device switching speeds down to
   **300 ps** (L, IMEC). Reset and readout — the two operations the Idaten
   design was inventing from scratch — therefore come **for free, from a
   qualified process**.
3. That removes the **piezomagnetic strain-reset hypothesis** from the
   critical path. It becomes an optimisation, not a load-bearing assumption.
   This is the single biggest reduction in technical risk available to the
   project.
4. It converts the magnonic part from "a chip that must be invented" into "a
   **bus module** that writes an existing memory array" — which is a
   3D-stacking problem, and 3D stacking (wafer-to-wafer hybrid bonding,
   backside vias) is exactly where foundries are investing.
5. It gives the accelerator audience a **binary milestone**: "does a
   magnon-assisted write beat a current-assisted write on the same array?"

---

## 1. Why now — the 24-month window (all L)

| Fact | Source | Why it matters to this project |
|---|---|---|
| **Coherent magnons demonstrated in lithographically patterned hematite thin films**; effective damping ~10⁻⁵; driven by a stripline antenna; power-dependent frequency blue shift and nonlinear response; patterned hematite "establishes a platform for exploring coherent and nonlinear antiferromagnetic magnon dynamics" | arXiv:2610.37205, submitted 27 Oct 2026 (WMI Munich; Althammer, Geprägs, Yu group) | **This is the enabling result for the hematite leg.** Until Oct 2026, coherent magnons in patterned hematite *thin films* had not been shown. The paper also states the central obstacle plainly: *"controlled studies of coherent magnons in thin films remain challenging due to strain sensitivity and spatial inhomogeneity"* — which is a direct threat to the strain-reset hypothesis (see §3.3) |
| Hematite GHz branch measured: α = 1.1×10⁻⁵, v_g = 10–23 km/s, decay length ℓ = 1.1 cm at 30 mT | Hamdi, Posva & Grundler, *Phys. Rev. Materials* **7**, 054407 (2023) | The low-loss bus that makes long operators physically possible |
| **IMEC demonstrates manufacturability of SOT-MRAM on 300 mm Si wafers**; switching down to 300 ps; CMOS-compatible processes; first full-scale SOT-MRAM module integration on 300 mm (2018) | IMEC press/research articles; *IEEE Spectrum* | The result medium `M_k` can be a process IMEC already runs |
| IMEC has integrated **thin-film LiNbO₃ / LiTaO₃ on silicon photonics** (world first, via micro-transfer printing) | IMEC press release | The paper's alternative magnetoelectric substrate is not fantasy — a foundry already does high-quality piezo-oxide integration |
| **GF 22FDX eMRAM in production since 2018**, PDK available, 2–32 Mb macros; **FDX+AutoPro150 Auto Grade 1 eMRAM announced 9 March 2026**, PDK via GF Connect | GF press releases | A *qualified* non-volatile magnetic memory that a magnonic front-end could write into |
| **GlobalFoundries is a Silicon Catalyst strategic partner**; program is a 24-month customised acceleration with semiconductor + design-services + foundry in-kind partners (Noel Technologies, Intrinsix); Silicon Catalyst Japan now running | siliconcatalyst.com | The accelerator-to-foundry chain is already built; the project has to show up with the right artifacts |
| Modern foundry 3D-integration thermal budget ≈ **400 °C** above active circuitry | CEA-Leti 400 °C CMOS programme | The hard constraint that decides whether YIG (high-temperature crystallisation) is viable at all (§4.3) |

**What this window does *not* contain:** a demonstration that a magnon can
write a foundry MRAM bit at lower energy than the current-assisted write. That
gap **is** the project. It is stated as such everywhere in this repository.

---

## 2. The one metric the whole project rests on

### 2.1 Definition

```
write amplification  W  =  N_cells_switched_per_wave_event
                          ───────────────────────────────
                             E_wave_per_event
```

The economic case is: **W must be large enough that `E_wave / N_cells` beats
the energy of the equivalent digital operation, plus one final read-out
amortised over the workload.** Nothing else matters. If W is small, the
architecture is a curiosity; if W is large, it is a platform.

### 2.2 What the published numbers imply (E)

Using only (L) values from Baumgaertl & Grundler 2023 and the authors' own
mumax³ deck:

| Quantity | Value | Source / derivation |
|---|---|---|
| Drive frequency `f` | 1.70 GHz | (L) published |
| Wavevector `k₁` | 0.85 rad/µm (λ = 7.4 µm) | (L) published |
| Group velocity `v_g = ω/k` | **12.6 km/s** | (E) 2π·1.70e9 / 0.85e6 |
| Bus length | 40.96 µm | (S) read from the authors' `.mx3` deck |
| Transit time | **3.26 ns** | (E) 40.96 µm / 12.6 km/s |
| Cells on that bus at `a` = 200 nm | **205** | (E) 40960 nm / 200 nm |
| Power into precession, k₁ mode | **36 nW** | (L) published |
| Microwave drive power at the CPW | **P_C1 = 12.6 µW**, P_C2 = 58.4 µW | (L) published |
| **Energy per wave event, precession term only** | **117 fJ** | (E) 36 nW × 3.26 ns |
| **Energy per wave event, drive-power term** | **41 pJ** | (E) 12.6 µW × 3.26 ns |
| **Implied energy per written cell (drive-power term, 205 cells, 100 % correct)** | **0.20 pJ/cell** | (E) 41 pJ / 205 |
| Comparison: SOT-MRAM write energy | **5–20 pJ/bit (assumption, to be replaced by a cited foundry figure)** | (E) pending |

**Reading this honestly.** The prize looks enormous — 25–100× on the
drive-power term — which is exactly why it must be treated as a hypothesis
rather than a result. The calculation assumes **all** of:

- one wave event switches **all 205** cells (no threshold spread, no error);
- 36 nW / 12.6 µW are the **total** bus power, not per-device;
- the CPW driver, the write-pulse shaping and the magnetic material losses are
  **free**;
- the result is read **once** per workload, not once per operation.

Any one of those failing changes the conclusion. Note also the **latency**
picture: a 3.26 ns wave transit is ~3–10 modern CMOS clock cycles, so this
architecture is **latency-competitive per stage and dense per operation** — it
wins on area and energy per operation, not on latency. It must never be
marketed as "instant".

**Therefore:** `W` is the repo's headline metric, and it is measured, with
error bars, in Stage A/B of notebook 01 and carried into the PPA ledger in
notebook 05.

### 2.3 The hematite variant (A / E)

Hematite's ℓ = 1.1 cm (L) allows a much longer bus, and a 1 cm guide at
`a` = 200 nm holds ~50 000 cells — but at v_g ≈ 15 km/s (E, midpoint of the
published 10–23 km/s) the transit is ~0.67 µs (E). So hematite trades
**latency for parallel width**, roughly 200× more cells per event at ~200×
the transit time. Which side wins is an open quantitative question and is
exactly what Stage C of notebook 01 must answer rather than assert.

---

## 3. Gate 1 — spintronics professors

### 3.1 What they check, in order

1. **Prior art.** In the first ten minutes they will ask "what has been done?"
   See `docs/PRIOR_ART.md`.
2. **Physics correctness.** Units, dispersion, damping, mode numbers, and
   whether the proposed device is dimensionally sane.
3. **Novelty.** "Waves perform linear algebra" has been true since the 1970s
   optical 4f correlator. The novelty must be located elsewhere and stated in
   one sentence.
4. **Falsifiability.** A named experiment that would kill each claim.

### 3.2 What this repository currently gets wrong in their eyes

| Their objection | Current state | Action |
|---|---|---|
| "You claim spin waves emulate DFT" | Already handled — notebook 03 claims only analogue-operator equivalence | Keep. The prohibition is written into `PROVENANCE.md` §0 |
| "Your decay-length fit has r² = 0.003 and you call it a measurement" | Already handled — the prior 70/55/148 µm figure is **withdrawn**, recorded as a failed re-derivation, and re-measured with a stated method | Keep. This is an asset, not a liability: it shows the author can kill their own number |
| "A GDS for a material nobody can pattern is not physics" | The concept mask is correctly labelled *concept mask, no PDK* | Keep the label. **Add** a second, MRAM-coupled concept mask whose result array references a foundry-standard bitcell (see §4.2) |
| "You have no prior-art table" | Missing | `docs/PRIOR_ART.md` — written, see that file |
| "What is the physics that hematite buys you over YIG?" | Stated incompletely | §3.3 below |

### 3.3 The hematite-vs-YIG statement, stated properly (the part professors will interrogate)

**What hematite buys (L):**

- Lower damping: α = 1.1×10⁻⁵ (hematite, GHz branch) vs ~2.7×10⁻⁵ (best YIG)
  → ~2.5× longer propagation distance.
- ℓ = 1.1 cm at 30 mT → a centimetre-scale bus, i.e. ~50 000 cells at
  `a` = 200 nm in one guide (E).
- **Antiferromagnetic order**: no net magnetisation, so the operating point is
  not set by a static bias field and the device is insensitive to external
  fields below the Néel temperature (T_N ≈ 955 K).

**What hematite costs (L, and this is the honest half):**

- **No net magnetic moment** → no inductive or electrical readout of the Néel
  state. The demonstration must use XMLD-PEEM (as in the published
  hematite-Néel imaging work) or a companion ferromagnetic layer. This is a
  real cost, not a footnote.
- **Strain sensitivity and spatial inhomogeneity** are named by the Oct 2026
  microdisk paper as *the* obstacle to coherent-magnon work in thin films.
  This directly undermines the piezomagnetic **strain-reset** hypothesis:
  if strain controls the magnonic response, the strain used to reset the state
  will perturb the very bus that carries the wave.
  **Resolution taken here:** the strain-reset idea is demoted from *load-bearing
  hypothesis* to *optional optimisation*, because the foundry MRAM path
  (§4) supplies a qualified reset mechanism instead.
- Thin-film growth is strain-sensitive and not yet a foundry process (E).

**The sentence for the novelty claim:**

> Prior magnonic computing uses waves as the *computation* and reads the result
> out per operation. Idaten separates three state objects — code in the
> fabricated geometry `P₀`, runtime configuration `C_k`, and a **persistent
> result `M_k` written into a non-volatile magnetic memory and read once, after
> the workload ends** — and the wave's job is to *write memory*, not to be the
> memory.

That is defensible, it is different from spin-wave cellular automata (where
state and computation are the same array), and it survives contact with prior
art.

### 3.4 What professors will reward immediately

- The reproduction of Baumgaertl & Grundler 2023 from the authors' own decks.
- The withdrawn decay-length claim, with r² stated.
- A **disproof experiment per claim** (`docs/KILL_CRITERIA.md`).
- Exact units and a stated fit method.
- **A paper that can fail.** Most magnonic-computing proposals are not
  falsifiable; this one will be.

---

## 4. Gate 2 — foundries (IMEC-class)

### 4.1 What they check

1. Which process, which layer, which thermal budget?
2. Die area, mask count, cost of the first shuttle?
3. What breaks first — yield, variability, stress, contamination?
4. Can it be made on 300 mm with their existing tools?
5. Does it help *their* roadmap — more MRAM, more 3D integration, more sensors?

### 4.2 The architectural change that makes this legible

**Today (weak):** a 5 mm × 5 mm die with a bus and 13 000 bespoke nanomagnets
on a material with no process. Honest, but a foundry has nothing to do with it.

**After the change (strong):**

| Block | Material / process | Who owns it | Status |
|---|---|---|---|
| **Bus module** — magnonic waveguide, transducers, tuning landscape | YIG-on-sapphire, hematite-on-sapphire, or thin-film LiNbO₃ | us / a materials partner | **No PDK exists.** This is the only genuinely new process |
| **Result array `M_k`** — 100 × 20 nm free-layer elements | Foundry SOT-MRAM / eMRAM bitcell | **the foundry** | **Qualified process already exists** (IMEC 300 mm, 300 ps; GF 22FDX eMRAM in production) |
| **Control `P₀` / `C_k`** — digital configuration | Standard CMOS logic | the foundry | Qualified |
| **Read-out** | Foundry MRAM sense amplifier | the foundry | Qualified |
| **Reset** | Foundry SOT reset (≈ 300 ps) | the foundry | Qualified |

**The ask becomes concrete and small:** *we do not need a new memory process;
we need to write your memory array with a wave instead of a current.*

That is a question a foundry can answer, and possibly fund.

### 4.3 The thermal-budget wall (E)

Modern foundry 3D integration tops out around **400 °C** above the active
circuitry (L, CEA-Leti 400 °C programme). YIG requires a high-temperature
crystallisation anneal, typically in the 700–900 °C range (E, process
literature). Therefore:

- **YIG cannot be integrated above foundry logic** (E). It must be a separate
  die, wafer-bonded, or the anneal must move to a front-end/companion-wafer
  step.
- This is precisely why the **bus-module split** (§4.2) is the right
  structure: it makes the thermal problem a *packaging* problem rather than a
  *process-integration* problem, and packaging is a solved foundry capability.

### 4.4 The first tapeout (the thing they will actually read)

**Test vehicle, 1 mm², MPW shuttle:**

| Item | Specification |
|---|---|
| Block A — magnonic bus | 100–500 µm bus, CPW launch/detect, tuning landscape. Material chosen by the Phase-1 experiment (§7), not by preference |
| Block B — MRAM-coupled write | An array of foundry MRAM free-layer elements alongside the bus, with a local write-current line, so the **current-assisted vs. magnon-assisted write can be compared on the same array in the same run** |
| Block C — control | A small configuration register driving local element selection (`C_k`) |
| Block D — reference | Standalone MRAM bits with standard write, for calibration |
| Measurement | Write current/energy per bit vs. applied RF field and vs. wave amplitude; error rate vs. write amplitude; pattern fidelity of the written array |

**The comparison in Block B is the experiment of the paper**: same array, same
bits, one written by current only, one written with the wave present. That is
a single, cheap, unambiguous measurement a foundry can run on its own probe
equipment.

---

## 5. Gate 3 — deep-tech accelerators (Silicon Catalyst-class)

### 5.1 What they check

1. **Team** — who is the PI, who is the hardware lead, is there a foundry liaison?
2. **Why now** — what changed in the last 24 months? (§1 answers this.)
3. **First tapeout** — area, masks, cost, date, and *what is measured*.
4. **Kill criteria** — what would make you stop? (`docs/KILL_CRITERIA.md`)
5. **Market** — who buys this, and what do they pay today?
6. **IP** — what is patentable and what is already claimed? (`docs/PRIOR_ART.md`)

### 5.2 The lead product should not be the general "execution processor"

**Recommendation (A, strategic):** lead with an **always-on edge magnonic
spectral classifier** — an RF/microwave front-end whose signal path is a
magnonic waveguide feeding a small array of thresholded read-outs, for
wake-word detection, spectrum sensing and anomaly detection.

Why this product first:

- It needs **only** the bus and a small read array → one small die → a
  first shuttle in a standard MPW is plausible.
- Ultra-low damping matters for preserving spectral detail, so the *physics
  advantage is real and load-bearing* rather than decorative.
- The market is legible: edge wake-up and spectrum sensing have buyers today.
- It shares **the same core IP and the same cell** as the execution processor,
  so it is not a detour — it is the small, fundable instance of the large
  thesis.

**The general execution processor remains the research thesis and the
scale-up**, not the first product. Claiming the general processor first is the
single most common way deep-tech pitches die: it has no first customer and no
first tapeout.

### 5.3 What to send them

- This document, `docs/PRIOR_ART.md`, `docs/KILL_CRITERIA.md`.
- The repository, with a green CI and one-command reproduction.
- A **one-page summary** (`docs/ONE_PAGER.md`) — accelerators read that first
  and rarely read past it.
- A named tapeout slot and a named foundry contact.

---

## 6. Kill criteria (the accelerators' and professors' favourite section)

Full table in `docs/KILL_CRITERIA.md`. The five that matter most:

| # | Gate | Measured quantity | Kill threshold | Consequence if failed |
|---|---|---|---|---|
| K1 | Physics | Field needed to reverse a nanomagnet with a wave present vs. absent | < 50 % of the published reduction (33.4 → 12.9 mT, i.e. < 23 mT) | Wave-assisted writing is not a real effect at our geometry → thesis fails |
| K2 | Economics | Energy per correctly written cell | > 1 pJ | No advantage over foundry MRAM write (5–20 pJ) |
| K3 | Parallelism | Cells switched per wave event | < 64 | Architecture degenerates to a serial chain; no density advantage |
| K4 | Process | Total thermal budget of the bus material | > 450 °C | YIG route dead; restrict to hematite / LiNbO₃ and accept the thin-film risk |
| K5 | Read-out | Error rate of the result pattern after one workload | BER > 10⁻⁶ | Not a memory — the persistence claim fails |

---

## 7. Milestone roadmap

### Phase 0 — credibility spine (0–6 months) — *no new hardware required*

| # | Deliverable | Evidence tag on completion |
|---|---|---|
| 0.1 | Reproduce Baumgaertl & Grundler 2023 from their own deck on our GPU: k₁, λ, H_C1/H_C2 shifts, MAMR dips | (S) |
| 0.2 | Measure `W` (write amplification) and `E_wave` directly, with error bars | (S) |
| 0.3 | Full §9 energy ledger with both power anchors and the foundry comparison | (S)/(E) |
| 0.4 | `docs/PRIOR_ART.md`, `docs/KILL_CRITERIA.md`, `docs/ONE_PAGER.md` | — |
| 0.5 | Repository public, green CI, one-command reproduction | — |

**Gate:** K1 and K2 must pass on simulated data before any hardware spend.

### Phase 1 — the enabling physics (6–18 months)

| # | Deliverable | Kill criterion |
|---|---|---|
| 1.1 | Bus-material shoot-out: YIG vs hematite vs thin-film LiNbO₃, same geometry, measured ℓ, v_g, α | K4 |
| 1.2 | **Hematite-specific:** demonstrate thresholded write into a patterned thin-film hematite array, and measure the strain-reset hypothesis honestly (including whether strain perturbs the bus) | strain-reset deemed unusable → foundry reset path becomes primary (§4.2) |
| 1.3 | Measured transfer function `H(k)` of a fabricated programmable landscape, vs. the design, vs. the phase-quantisation error model in notebook 03 | measured `H(k)` outside predicted band → notebook 03's error model is wrong |

### Phase 2 — foundry shuttle (18–30 months)

| # | Deliverable | Kill criterion |
|---|---|---|
| 2.1 | 1 mm² test vehicle (Block A–D, §4.4) in a 22/28 nm MPW | non-fab deliverable → partner foundry |
| 2.2 | Same-array comparison: current-assisted vs magnon-assisted write | K2, K3 |
| 2.3 | Error rate of the written result pattern, read once | K5 |

### Phase 3 — demonstrator (30–48 months)

Edge spectral classifier demonstrator on the Phase-2 cell, measured against a
matched digital baseline, with a full system energy ledger that includes
read-out, control, packaging and host.

---

## 8. What changes in the repository because of this document

| Change | Reason |
|---|---|
| Result medium re-specified as a foundry MRAM free-layer array | §4.2 — the highest-leverage change available |
| Concept mask gains a **second** variant: MRAM-coupled, with the result array referencing a foundry bitcell | A foundry can act on that one; they cannot act on the hematone |
| Piezomagnetic strain reset demoted from load-bearing to optional | §3.3 — strain sensitivity of hematite thin films is documented as the central obstacle |
| `W` (write amplification) promoted to a headline, measured quantity | §2 — it is the only number that decides the project |
| Stage C of notebook 01 reframed as *latency vs. parallel width* for hematite | §2.3 |
| Lead product defined as an edge spectral classifier, execution processor as scale-up | §5.2 |
| Kill criteria published as a first-class artifact | §6 |

---

## 9. References for this document

1. K. Baumgaertl, D. Grundler, *Reversal of nanomagnets by propagating magnons
   in ferrimagnetic yttrium iron garnet enabling nonvolatile magnon memory*,
   **Nature Communications 14**, 1490 (2023). DOI 10.1038/s41467-023-37078-8.
   Dataset 10.5281/zenodo.7714181 (CC-BY-4.0).
2. M. Hamdi, F. Posva, D. Grundler, *Spin wave dispersion of ultra-low damping
   hematite (α-Fe₂O₃) at GHz frequencies*, **Physical Review Materials 7**,
   054407 (2023).
3. J. Wang, K. Müller, H. Peng, J. Gückelhorn, W. Song, L. Sheng, J. Chen,
   S. Liu, D. Yu, S. Geprägs, M. Althammer, H. Yu, *Magnons in α-Fe₂O₃
   microdisks: from thermal to coherent excitation*, arXiv:2610.37205
   (27 Oct 2026). CC-BY-4.0.
4. R. Lebrun et al., *Long-distance spin-transport across the Morin phase
   transition in iron oxide*, **Nature Communications 11** (2020).
5. A. V. Chumak et al., *Advances in Magnetics Roadmap on Spin-Wave
   Computing*, **J. Appl. Phys. 132, 041001 (2022)** — the field roadmap; the
   mandatory citation for any magnonic-compute claim.
6. S. Kurebayashi et al., *Metrics for spin-based computing*, **Nature Reviews
   Physics 8**, 208–225 (2026).
7. *Spintronic memristors for computing*, **npj Spintronics** (2025).
8. IMEC: *Imec demonstrates manufacturability of state-of-the-art spin-orbit
   torque MRAM devices on 300mm Si wafers*; *Bringing SOT-MRAM technology
   closer to last-level cache memory specifications*; *Double world first:
   integrating lithium niobate and lithium tantalate modulators on silicon*.
9. GlobalFoundries: *Launches Embedded MRAM on 22FDX platform* (2016);
   *Availability of Embedded MRAM on 22FDX* (2017); *Availability of AutoPro
   150 eMRAM technology on enhanced FDX platform* (9 March 2026).
10. CEA-Leti: *400 °C CMOS breakthrough opens critical doors to 3D integration*.
11. Silicon Catalyst: program and partner pages (24-month customised
    acceleration programme; GlobalFoundries, Arm, ST, Sony, NXP, TI, onsemi,
    Soitec, Bosch, Cirrus Logic, Mayfield, Qnity, SMD Semiconductor as
    strategic partners; Noel Technologies and Intrinsix as in-kind
    semiconductor / design-service partners).
12. *Idaten Ce100: Pattern-Coded Magnonic Execution, Persistent Magnetic
    Results, and Dynamic Rails*, rev. 16 Nov 2026 (internal architecture
    document).
