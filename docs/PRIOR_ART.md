# PRIOR ART — differentiation, stated before anyone asks

**Purpose.** A spintronics professor will ask "what has already been done?" in
the first ten minutes. A Silicon Catalyst screening committee will ask "what
can you actually own?". This document answers both, including the parts that
are unfavourable.

**Evidence tags.** `(L)` literature · `(A)` architectural claim.

---

## 1. The novelty statement

> **Not new:** waves performing linear operators; magnons reversing
> nanomagnets; non-volatile magnetic storage of results.
>
> **Claimed as new (A):** the **separation of three state objects** — code in
> the fabricated geometry `P₀`, runtime configuration `C_k`, and a **persistent
> result `M_k` written into a non-volatile magnetic memory that is read once,
> after the workload ends** — where the wave's function is to *write memory*
> rather than to *be* the memory, and where the result medium is a
> **standard foundry MRAM free-layer array**.

This is a **systems claim, not a physics claim**, and it is presented as such.
A reviewer who disagrees with the systems framing should be able to say
exactly which row of §4 defeats it.

---

## 2. The five questions and the short answers

| Question | Short answer | Where |
|---|---|---|
| "Isn't 'waves compute linear algebra' 50 years old?" | Yes — the 4f correlator. The novelty is not the operator, it is that the programme is a **fabricated magnetic landscape** and the output is **written to persistent memory and read once**. | §4.12 |
| "Isn't magnon-written memory already done?" | **Yes** — Baumgaertl & Grundler 2023 (L), Joglekar et al. 2024 (L), and a 2025 EPFL perspective (L) already occupy this space. We **build on** them; we do not claim the primitive. | §4.1–§4.4 |
| "Isn't spin-wave cellular automata the same thing?" | No: in SWCA the **state and the computation are the same array**, so `C_k` and `M_k` are conflated. The whole point of the architecture is that they are not. | §4.10 |
| "Isn't this just MRAM compute-in-memory?" | No: MRAM-CIM does the **arithmetic inside the memory**. Here the memory is only the **destination**; the operator is executed in a wave medium. | §4.11 |
| "Who else has said this exact architecture?" | **This is the most dangerous entry in the table.** A 2025 EPFL perspective (L) surveys non-volatile magnon-signal storage and in-memory computing. It must be read and cited in the first paragraph of any paper. | §4.2 |

---

## 3. Master differentiation table

`P₀` = fabricated topology · `C_k` = runtime configuration · `Ψ_k` = live wave ·
`M_k` = persistent result

| Prior-art class | Where the **code** lives | Where the **result** lives | How the result is **read** | Per-operation read-out? | Separation of code / result |
|---|---|---|---|---|---|
| Optical 4f correlator (Goodman 1976) | Spatial light modulator | detector plane | optical, every op | **yes** | no |
| Magnonic spatial analog / matrix operations (Chumak roadmap 2022) | etched waveguide geometry | detector / electrical pickup | electrical, every op | **yes** | no |
| Magnonic logic & reconfigurable interconnects (Hanze 2016 and class) | device geometry + currents | output port | electrical, every op | **yes** | no |
| Spin-wave cellular automata (Bichromatic and class) | fixed array geometry | **the same array** | electrical, every op | **yes** | **no — `C_k` ≡ `M_k`** |
| Magnon-written nanomagnets (Baumgaertl 2023; Joglekar 2024) | drive waveform | the nanomagnet | electrical / imaging | after the event, but no *workload* semantics | partial |
| Magnonic ANN / neurons (Papp 2021; all-magnonic neurons 2025) | device physics (the nonlinearity) | conventional output | electrical, every op | **yes** | no |
| MRAM / eMRAM compute-in-memory | the stored weights | the memory array | electrical, every op | **yes** | **no — the memory *is* the computer** |
| Domain-wall / MESO logic | device geometry | device state | electrical, every op | **yes** | partial |
| **Idaten (A)** | **`P₀` (fabricated geometry) + `C_k` (config switches)** | **`M_k` — a separate foundry MRAM free-layer array** | **once, after the workload ends** | **no** | **yes — three separate state objects** |

The last row is the claim. Every other row has at least one of the three
properties missing.

---

## 4. The closest prior art, itemised

### 4.1 Baumgaertl & Grundler, *Nature Communications* **14**, 1490 (2023) (L)

The foundation, and the reason this project has a reproducible spine. A
propagating magnon reverses Ni₈₁Fe₁₉ nanomagnets; the switching threshold is
reduced (H_C1 16.8→2.7 mT, H_C2 33.4→12.9 mT); the mechanism is magnon-assisted
MAMR.

**Delta.** They demonstrate the **write primitive** and the **field
reduction**. We do not claim either. Our claim starts one level up: that the
primitive should be used to write a **standard foundry memory array**, inside
an architecture that keeps **code, configuration and result in three separate
places**, with the result **read once per workload**.

**This paper is vendored, not paraphrased.** The authors' own mumax³ decks and
plotting scripts are in `data/zenodo_baumgaertl/` (CC-BY-4.0), and the
published phase-diagram arrays are included as independent ground truth.

### 4.2 Nizet et al. (2025), EPFL — *Perspective on nonvolatile magnon-signal storage and in-memory computing* (L)

**The most dangerous citation in this list.** It surveys the same idea space:
storing magnon signals non-volatilely and using them for in-memory computing.

**Delta.** A *perspective* is not a demonstration — but a perspective may
already claim the architectural framing. **Action:** read it in full, cite it
in the first paragraph, and state explicitly whether the code/result separation
and the read-once semantics are already proposed there. If they are, the claim
narrows to the *foundry-MRAM-coupled implementation and the measured write
amplification*, which is still defensible but is a smaller claim. **Do not
submit without this check.**

### 4.3 Joglekar et al. (2024), *Nanoscale Horizons* **9**, 1740 (L) — "Reversing the magnetization of 50-nm-wide ferromagnets…"

Reversing the magnetization of 50-nm-wide ferromagnets with spin waves, to
encode a magnon signal in a nanomagnetic memory bit.

**Delta.** Different element geometry (50 nm wide vs. the precedent's
100 × 20 nm) and, more importantly, no code/result separation and no
workload-level read-once semantics.

**This is the closest *physical* prior art and must be cited alongside
§4.1.**

### 4.4 "Magnonic memory effect — reading and writing of magnetic bits by spin-waves: Two lattices" (L)

Reading **and** writing magnetic bits with spin waves, using two coupled
lattices.

**Delta.** Architecturally the closest match to `M_k` as a distinct medium.
**Action:** read in full; the "two lattices" separation is close to the
`Ψ_k`/`M_k` separation and must be addressed head-on. The Idaten delta is the
**third** object (`P₀`/`C_k`) and the **read-once** semantics.

### 4.5 Schulze et al. (2023), ETH Zürich — "Realization of a magnonic analog adder with frequency-multiplexed…" (L)

A **demonstrated** magnonic analog adder.

**Delta.** An adder is a digital-operation primitive read out per operation.
No persistent result, no read-once semantics, no separation of configuration
from result.

### 4.6 Papp et al., *Nature Communications* **12**, 26711 (2021) (L) — "Nanoscale neural network using non-linear spin-wave physics"

**Delta.** The network's weights live in the device physics; the output is
conventional. No persistent-result architecture.

### 4.7 "All-magnonic neurons for analog artificial neural networks" (arXiv:2509.18321, 2025) (L)

Non-linear magnon excitation as an analogue neuron.

**Delta.** As §4.6. Note the **input-output** framing: this is precisely the
per-operation read-out pattern Idaten removes.

### 4.8 "Toward magnonic logic and neuromorphic computing: controlling spin waves by spin-polarized current" (2024) (L)

A current-density distribution acting as a **diffracting medium** for spin
waves, analogous to Snell's law in optics.

**Delta — and this one matters technically.** This is the closest prior art to
the *programmable landscape* idea. Their landscape is a **current distribution**,
which is electrical, per-operation, and consumes current. Idaten's landscape is
**fabricated magnetic geometry** (`P₀`) plus **configuration switches** (`C_k`),
whose state is itself magnetic and non-volatile. **This row is where the
architecture earns its keep** — and it is also where a reviewer will press
hardest.

### 4.9 Magnonic logic and reconfigurable interconnects — Hanze et al., *J. Appl. Phys.* **120**, 023901 (2016) and the surrounding class (L)

**Delta.** Signal routing and processing; per-operation electrical read-out;
no persistent result.

### 4.10 Spin-wave cellular automata — Bichromatic et al. and the class (L)

**Delta — architectural and decisive.** In a spin-wave cellular automaton the
**state of the array is the computation**, and the next wave is generated *by
the array's own state*. In Idaten, `C_k` (what the wave is told to do) and
`M_k` (what the wave has just computed) live in **different physical places**.
This is the distinction most likely to be challenged as "you have reinvented
SWCA" — and the answer is the three-object separation, plus the fact that the
result **survives** the wave and is **read once**.

### 4.11 MRAM / eMRAM compute-in-memory — the 22 nm eMRAM CIM line (L)

Foundry eMRAM (GF 22FDX, production since 2018) is used for analogue
compute-in-memory, and IMEC has 300 mm SOT-MRAM with 300 ps switching (L).

**Delta.** In MRAM-CIM the **memory performs the arithmetic** — the array is
both the operand store and the multiplier. In Idaten the memory is only the
**destination**: the operator is executed in a wave medium and the result is
**written** into the array. Crucially, this means the two approaches are
**complementary, not competing** — an eMRAM array is a plausible `M_k`
substrate, and a foundry that already makes eMRAM is the natural partner.

### 4.12 Optical 4f correlators — Goodman, *Introduction to Fourier Optics* (1976) (L)

The archetype. Any linear operator, implemented by interference, with the
transfer function programmed in a spatial light modulator.

**Delta.** The programme element is a **fabricated magnetic landscape**, and
the output is **written to persistent magnetic memory and read once**. The
optical correlator has neither.

### 4.13 Domain-wall and MESO logic — Tao et al., *Nature Nanotechnology* **13**, 992 (2018); Parto et al. (2018) (L)

**Delta.** These are the **comparator class**: they deliver very low energy
per operation with per-operation electrical read-out. Their published energy
figures are the baseline that Idaten's write-amplification metric
(`CREDIBILITY_PLAN.md` §2) must beat, and they are the reason the project
needs a foundry-grade result medium rather than a bespoke one.

### 4.14 Inverse design for AI magnonics — Vilsmeier et al., arXiv:2607.07324 (2026) (L)

**Delta.** A methods contribution (how to design the landscape), not an
architecture. Compatible with, and used by, this project.

---

## 5. What is explicitly **not** claimed

Stating this is worth more than any row of §3, because it is what makes the
remaining rows credible:

1. **Not** that waves can compute linear operators — 50 years old.
2. **Not** that magnons can reverse nanomagnets — demonstrated (L), §4.1, §4.3.
3. **Not** that magnetic memory is non-volatile — it is MRAM.
4. **Not** that spin waves can emulate Schrödinger / Kohn–Sham operators or
   "solve DFT" — they cannot; see `PROVENANCE.md` §0.
5. **Not** "zero resistance", "absolute zero idle power", "free computation",
   "instant switching", or any global-superlative efficiency figure.
6. **Not** a fabricated, measured or packaged device. Every device-level
   statement is (A) or (E).

---

## 6. What to own, and where the freedom actually is (IP)

Patent-landscape guidance for the accelerator application. The **device-level
physics is crowded** — magnon reversal, strain reset and SOT write are all
multi-actor areas. The freedom is in the **system architecture and the
integration**:

| Candidate claim | Crowding | Priority |
|---|---|---|
| The three-object separation (`P₀` / `C_k` / `M_k`) with read-once result semantics | low | **highest** |
| A **magnonic bus module writing a foundry MRAM array**, with the same-array current-assisted vs. magnon-assisted comparison as the measurement | low | **highest** |
| A **write-amplification design objective** (`W` = cells switched per wave event ÷ wave energy) and the method for optimising a landscape against it | low | high |
| Calibration of a **fabricated programmable landscape**: measuring `H(k)` and re-deriving the analogue error band from the *measured* transfer function (notebook 03 §disproof) | medium | high |
| The specific bus-module ↔ MRAM-array geometry, and the reset sequence | medium | high |
| Magnon-induced reversal of a free layer | **high** | low — build on, do not claim |
| Piezomagnetic strain reset of a Néel state | **high** | low — and demoted to optional (`CREDIBILITY_PLAN.md` §3.3) |

**Search terms to run before any filing:** "magnon assisted MRAM write",
"spin wave memory write", "magnonic in-memory computing nonvolatile",
"spin wave cellular automaton persistent result", "4f correlator magnetic
implementation", "hematite magnonic waveguide", "piezomagnetic Néel reset".

---

## 7. Citation hygiene

- Every quantitative claim in this repository carries a tag and a source.
- Where a bibliographic detail is not yet verified against the publisher of
  record, the row is marked *(to verify)* rather than given a confident
  volume/page number.
- The authoritative list, with the tag attached to each number, is
  `PROVENANCE.md` §7.
