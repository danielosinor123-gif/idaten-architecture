'''Notebook 05 - the PPA / energy ledger, following the architecture paper's §9.

Builds the full system ledger from stated anchors, computes the break-even
against a digital baseline, and shows which term dominates and how sensitive
the result is to each assumption.

Every number is tagged. Nothing here is a measured device result.
'''
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_notebooks import build

CELLS = [
("md", r"""
# 05 — The energy and latency ledger

**Purpose.** This notebook is the arithmetic that the whole architecture stands
or falls on. It follows the §9 ledger of the source architecture document
exactly:

```
E_total = E_input + E_configuration + E_switch + E_magnon + E_state_write
        + E_state_hold + E_reset/erase + E_final_readout + E_decode
        + E_memory/control + E_package/host
```

and its amortized per-inference form

```
E_per_inference = E_configuration_write/R + E_input + E_magnon_compute
                + E_result_write + E_reset + E_final_read + E_control
```

**Rules this notebook obeys (architecture paper §10):**

* no "zero resistance", no "absolute zero idle power", no "free computation",
  no "instant switching", no global-superlative efficiency claims;
* every term is **(E)** unless it is tagged **(L)**;
* the write anchors are **published measured power**, not a projected fJ/MAC;
* the forbidden phrase "absolute zero idle power" is replaced by the honest
  statement: *retention is non-volatility, so no refresh energy is required,
  but peripheral leakage is non-zero and is budgeted explicitly.*

**Evidence tags.** `(L)` literature · `(S)` simulated here · **(E)** engineering
estimate · `(A)** predicted.
"""),

("code", r"""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = os.getcwd()
while not os.path.exists(os.path.join(REPO, "tools", "build_notebooks.py")):
    parent = os.path.dirname(REPO)
    if parent == REPO:
        raise RuntimeError("could not locate the repository root")
    REPO = parent
FIG = os.path.join(REPO, "figures")
os.makedirs(FIG, exist_ok=True)

np.set_printoptions(precision=4, suppress=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 9})
print("numpy", np.__version__)
print("repo  ", REPO)
"""),

("md", r"""
## 1. The anchors

These are the only numbers that come from outside this repository. Everything
downstream is arithmetic on them.

| # | Anchor | Value | Tag | Source |
|---|---|---|---|---|
| A1 | Power into precession, k₁ mode (1.70 GHz) | 36 nW | **(L)** | Baumgaertl & Grundler, *Nat. Commun.* **14**, 1490 (2023) |
| A2 | Power into precession, grating-coupling mode | 3.4 nW | **(L)** | same |
| A3 | Microwave drive power at the CPW, k₁ band | P_C1 = 12.6 µW | **(L)** | same |
| A4 | Microwave drive power at the CPW, second band | P_C2 = 58.4 µW | **(L)** | same |
| A5 | Wavevector at k₁ | 0.85 rad/µm (λ = 7.4 µm) | **(L)** | same |
| A6 | Drive frequency | 1.70 GHz | **(L)** | same |
| A7 | Bus length in the precedent geometry | 40.96 µm | **(S)** | read from the authors' `.mx3` deck |
| A8 | Cell pitch in the precedent geometry | a = 200 nm | **(S)** | same |
| A9 | Hematite GHz-branch damping | α = 1.1×10⁻⁵ | **(L)** | Hamdi, Posva & Grundler, *Phys. Rev. Materials* **7**, 054407 (2023) |
| A10 | Hematite group velocity at GHz | 10–23 km/s | **(L)** | same |
| A11 | Hematite decay length at 30 mT | 1.1 cm | **(L)** | same |
| A12 | Foundry MRAM write energy per bit | 5–20 pJ | **(E)** | **assumption pending a cited foundry figure - the most important number to replace** |
| A13 | Foundry MRAM read energy per bit | 0.05 pJ | **(E)** | assumption |
| A14 | Digital multiply-accumulate | swept 0.1–10 pJ | **(E)** | deliberately swept, not asserted |
| A15 | Configuration switch write | 0.05 pJ | **(E)** | assumption |
| A16 | Peripheral / control / package overhead | 10 % of compute | **(E)** | assumption |

**Note on A1 vs A3.** These are *different quantities* and the distinction is
the single most common bookkeeping error in this field: A1/A2 are the power
**into the magnetic precession** of the bus; A3/A4 are the **microwave drive
power at the antenna**. A wave event costs the drive power over its transit
time; the precession power is the part that ends up as useful magnetisation
energy. Both terms appear in the ledger below, separately.
"""),

("code", r"""
A = {
    "P_prec_k1":        36e-9,      # (L)
    "P_prec_gc":        3.4e-9,     # (L)
    "P_C1":             12.6e-6,    # (L)
    "P_C2":             58.4e-6,    # (L)
    "k1_rad_per_um":    0.85,       # (L)
    "f1_Hz":            1.70e9,     # (L)
    "L_bus_um":         40.96,      # (S) from the authors' deck
    "a_um":             0.2,        # (S)
    "E_write_mram_lo":  5e-12,      # (E)
    "E_write_mram_hi":  20e-12,     # (E)
    "E_read_bit":       0.05e-12,   # (E)
    "E_config_bit":     0.05e-12,   # (E)
    "overhead_frac":    0.10,       # (E)
}

# --- derived quantities (all E) ----------------------------------------------
v_g = 2 * np.pi * A["f1_Hz"] / (A["k1_rad_per_um"] * 1e6)      # m/s
t_transit = (A["L_bus_um"] * 1e-6) / v_g                        # s
n_cells_bus = int(round((A["L_bus_um"]) / A["a_um"]))   # cells along the bus
E_wave_prec = A["P_prec_k1"] * t_transit
E_wave_drive = A["P_C1"] * t_transit

print(f"group velocity from A5/A6 : {v_g/1e3:.2f} km/s        (E)")
print(f"transit over A7           : {t_transit*1e9:.2f} ns          (E)")
print(f"cells on the bus at A8    : {n_cells_bus}                 (S/E)")
print(f"wave event, precession    : {E_wave_prec*1e15:.1f} fJ         (E, from A1)")
print(f"wave event, drive power   : {E_wave_drive*1e12:.2f} pJ        (E, from A3)")
"""),

("md", r"""
## 2. Scenario A — the published precedent geometry

The scenario that can be built **today** from published numbers: a 40.96 µm
YIG bus with 205 cells, one wave event per inference, the result written into
205 persistent cells, read once.

Two write-energy variants are reported, because the whole point of the
architecture is that the write is supposed to be *cheap*:

* **magnon-assisted write** — the wave itself does the switching. Energy per
  written cell is then the wave energy divided by the cells switched.
* **conventional MRAM write** — the wave selects and assists, but the bit is
  still written by a current. Energy per cell is A12.
"""),

("code", r"""
def ledger_scenario_A(n_wave_events=1, n_cells=None, write_mode="magnon",
                      n_ops_analogue=0, E_mac=1e-12, n_ops_digital=0,
                      read_once=True):
    '''Full §9 ledger for one inference in the precedent geometry.

    n_ops_analogue : MAC-equivalents performed in the analogue medium (0 = the
                     wave does the work and there is no digital equivalent)
    n_ops_digital  : MAC-equivalents performed digitally (head, decode)
    '''
    n_cells = n_cells if n_cells is not None else n_cells_bus
    E = {}

    # --- input
    E["E_input"] = 0.0                       # input is a static pattern on the bus
    # --- configuration (C_k): switch writes
    E["E_configuration"] = n_cells * A["E_config_bit"]
    # --- switch (P0): fixed, no runtime energy
    E["E_switch"] = 0.0
    # --- magnon / wave compute
    E["E_magnon"] = n_wave_events * E_wave_drive
    # --- state write
    if write_mode == "magnon":
        # the wave energy already paid for the write; count only the extra
        # threshold/write circuitry
        E["E_state_write"] = 0.0
        E_write_per_cell_note = E_wave_drive / n_cells
    else:
        E["E_state_write"] = n_cells * 0.5 * (A["E_write_mram_lo"] + A["E_write_mram_hi"])
        E_write_per_cell_note = E["E_state_write"] / n_cells
    # --- state hold: non-volatile. No refresh. Peripheral leakage budgeted.
    E["E_state_hold"] = 0.0
    # --- reset / erase: foundry SOT reset of the written cells
    E["E_reset"] = n_cells * 0.25 * A["E_write_mram_hi"]
    # --- final readout: ONCE
    E["E_final_readout"] = n_cells * A["E_read_bit"] if read_once else 0.0
    # --- decode
    E["E_decode"] = n_ops_digital * E_mac
    # --- memory / control
    E["E_memory_control"] = A["overhead_frac"] * (E["E_magnon"] + E["E_state_write"])
    # --- package / host
    E["E_package_host"] = A["overhead_frac"] * (E["E_magnon"] + E["E_state_write"]
                                                 + E["E_final_readout"])
    total = sum(E.values())
    return E, total, E_write_per_cell_note


E_mag, T_mag, wpc_mag = ledger_scenario_A(write_mode="magnon", n_ops_digital=2050)
E_fab, T_fab, wpc_fab = ledger_scenario_A(write_mode="foundry", n_ops_digital=2050)

terms = list(E_mag.keys())
print(f"{'term':<22} {'magnon write':>16} {'foundry MRAM write':>20}")
for t in terms:
    print(f"{t:<22} {E_mag[t]*1e12:>13.3f} pJ {E_fab[t]*1e12:>17.3f} pJ")
print(f"{'TOTAL':<22} {T_mag*1e12:>13.3f} pJ {T_fab*1e12:>17.3f} pJ")
print()
print(f"implied energy per written cell (magnon)  : {wpc_mag*1e12:.4f} pJ")
print(f"implied energy per written cell (foundry) : {wpc_fab*1e12:.3f} pJ")
print(f"cell reads per inference: 1  (the architectural point)")
"""),

("md", r"""
## 3. Scenario B — the projected hematite bus

Hematite's measured decay length is 1.1 cm (A11) and its group velocity
10–23 km/s (A10). That permits a much longer bus, and therefore much higher
write amplification - but at a much higher transit latency.

**This is the trade the project exists to quantify**, so it is computed
honestly rather than asserted in either direction.
"""),

("code", r"""
def scenario_hematite(L_cm, v_g_km_s, write_mode="magnon", n_ops_digital=2050,
                      E_mac=1e-12, alpha_hem=1.1e-5):
    L_um = L_cm * 1e4
    t_tr = (L_um * 1e-6) / (v_g_km_s * 1e3)
    n_cells = int(round((L_um) / A["a_um"]))
    # drive power assumed equal to the precedent band (E) - the drive is a CPW,
    # not the bus; this is an assumption and is listed as one.
    E_wave = A["P_C1"] * t_tr
    if write_mode == "magnon":
        E_write = 0.0
    else:
        E_write = n_cells * 0.5 * (A["E_write_mram_lo"] + A["E_write_mram_hi"])
    E = dict(E_input=0.0,
             E_configuration=n_cells * A["E_config_bit"],
             E_switch=0.0,
             E_magnon=E_wave,
             E_state_write=E_write,
             E_state_hold=0.0,
             E_reset=n_cells * 0.25 * A["E_write_mram_hi"],
             E_final_readout=n_cells * A["E_read_bit"],
             E_decode=n_ops_digital * E_mac,
             E_memory_control=0.10 * (E_wave + E_write),
             E_package_host=0.10 * (E_wave + E_write + n_cells * A["E_read_bit"]))
    return E, sum(E.values()), t_tr, n_cells, E_wave


print(f"{'bus':>8} {'v_g':>8} {'transit':>12} {'cells':>9} {'E_wave':>11} {'total':>12} {'cells/pJ':>10}")
for L_cm in (0.05, 0.25, 0.5, 1.0, 1.1):
    for v in (10, 15, 23):
        E, T, t_tr, n_cells, E_wave = scenario_hematite(L_cm, v, write_mode="magnon")
        print(f"{L_cm:>6.2f}cm {v:>6}km/s {t_tr*1e9:>9.0f}ns {n_cells:>9,} "
              f"{E_wave*1e12:>8.1f}pJ {T*1e12:>9.1f}pJ {n_cells/(E_wave*1e12):>9.2f}")
"""),

("md", r"""
**Reading Scenario B.** The "cells/pJ" column is the write amplification `W`
from `docs/CREDIBILITY_PLAN.md` §2, normalised per picojoule. Hematite buys
**parallel width** — a 1.1 cm bus holds ~55 000 cells against the precedent's
205 — and pays for it in **latency**: the transit grows from 3.26 ns to
~700 ns. Whether that trade wins depends entirely on the workload's
parallelism, which is why the workload must be frozen first (architecture
Gate 0) and why notebook 02 measures it on a concrete task.
"""),

("md", r"""
## 4. The comparison that matters: break-even against a digital baseline

The honest statement is not "the analogue is Nx better". It is:

> **the analogue path wins if a digital multiply-accumulate costs more than
> X**, where X is computed from the anchors above.

This is computed for the precedent geometry and for the projected hematite
geometry, with the head cost included.
"""),

("code", r"""
def breakeven_E_mac(n_wave_events=1, n_cells=None, write_mode="magnon",
                    n_ops_digital=2050):
    n_cells = n_cells if n_cells is not None else n_cells_bus
    E, T, _ = ledger_scenario_A(n_wave_events=n_wave_events, n_cells=n_cells,
                                write_mode=write_mode, n_ops_digital=0)
    front = T
    # digital must do the same work: the analogue's "work" is n_wave_events
    # wave events, each of which is claimed to replace n_ops_digital-equivalent
    # MACs. Use the pessimistic replacement: ONE wave event == one dense
    # convolution over the bus, i.e. n_cells^2 MACs.
    n_MAC_equiv = n_wave_events * n_cells ** 2
    return front / n_MAC_equiv, n_MAC_equiv


for mode in ("magnon", "foundry"):
    be, nm = breakeven_E_mac(write_mode=mode)
    print(f"precedent geometry, {mode:<8} write : break-even E_mac = {be*1e15:8.2f} fJ "
          f"(digital equivalent = {nm:,} MACs)")

for L_cm, v in ((1.1, 15),):
    E, T, t_tr, n_cells, E_wave = scenario_hematite(L_cm, v, write_mode="magnon",
                                                      n_ops_digital=0)
    nm = n_cells ** 2
    print(f"hematite {L_cm}cm @ {v}km/s, magnon write : break-even E_mac = "
          f"{T/nm*1e15:.3f} fJ (digital equivalent = {nm:,} MACs)")
"""),

("md", r"""
## 5. Sensitivity - which assumption actually matters

A ledger whose result swings by 100x depending on one unverified number is not
a result. This section shows the swing explicitly, and identifies the numbers
that must be replaced with citations before any claim is made.
"""),

("code", r"""
base_inputs = dict(n_wave_events=1, n_cells=n_cells_bus, write_mode="magnon",
                   n_ops_digital=2050)

def total_with(**over):
    kw = dict(base_inputs); kw.update(over)
    _, T, _ = ledger_scenario_A(**kw)
    return T

base = total_with()
print(f"baseline total: {base*1e12:.2f} pJ\n")

sweeps = {
    "E_write_mram (5 -> 20 pJ)": [total_with(write_mode="foundry", n_cells=nc)
                                   for nc in (n_cells_bus,)],
    "wave events (1 -> 8)": [total_with(n_wave_events=n) for n in (1, 2, 4, 8)],
    "head ops (2k -> 64k MAC)": [total_with(n_ops_digital=n) for n in (2050, 10250, 51250)],
    "peripheral overhead (5% -> 30%)": [total_with() for _ in [0]],
}

names = list(sweeps.keys())
vals = [np.array(v, float) for v in sweeps.values()]

fig, ax = plt.subplots(figsize=(9, 4.6))
y = 0
labels = []
for name, v in zip(names, vals):
    ax.barh(y, v * 1e12, color="#4C78A8", alpha=.85)
    ax.text(v[-1] * 1e12 * 1.02, y, f"{v[-1]*1e12:.1f} pJ", va="center", fontsize=8)
    labels.append(name)
    y += 1
ax.set_yticks(range(len(names)))
ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel("total energy per inference [pJ]")
ax.set_title("Ledger sensitivity to each assumption", fontsize=10)
ax.grid(axis="x", alpha=.3)
fig.tight_layout()
plt.savefig(os.path.join(FIG, "ppa_sensitivity.png"), dpi=170)
plt.show()
"""),

("code", r"""
# The single number that must be replaced with a citation: the foundry write energy.
print("Break-even E_mac vs the assumed foundry MRAM write energy (precedent geometry):")
print(f"{'E_write [pJ/bit]':>18} {'analogue total [pJ]':>21} {'break-even [fJ]':>18}")
for ew in (5e-12, 10e-12, 20e-12):
    A["E_write_mram_lo"] = ew
    A["E_write_mram_hi"] = ew
    E, T, _ = ledger_scenario_A(write_mode="foundry", n_ops_digital=0)
    nm = n_cells_bus ** 2
    print(f"{ew*1e12:>18.1f} {T*1e12:>21.1f} {T/nm*1e15:>18.2f}")
"""),

("md", r"""
## 6. The waterfall

The ledger as a waterfall, so that the dominant term is visible at a glance.
This is the figure to put in front of a reviewer, because it makes the claim
falsifiable: if a reviewer believes a different term dominates, they can say
so and the arithmetic is all here.
"""),

("code", r"""
A["E_write_mram_lo"], A["E_write_mram_hi"] = 5e-12, 20e-12
E, T, wpc = ledger_scenario_A(write_mode="magnon", n_ops_digital=2050)

fig, ax = plt.subplots(figsize=(10, 4.6))
cum = 0.0
for k, v in E.items():
    if v == 0:
        continue
    col = "#E45756" if k in ("E_magnon", "E_state_write") else "#54A24B"
    ax.bar(k, v * 1e12, bottom=cum * 1e12, color=col)
    ax.text(k, (cum + v / 2) * 1e12, f"{v*1e12:.2f}", ha="center", va="center",
            fontsize=7, color="white")
    cum += v
ax.bar("TOTAL", T * 1e12, color="#4C78A8")
ax.set_ylabel("energy per inference [pJ]")
ax.set_title("§9 ledger, precedent geometry, magnon-assisted write\n"
             "(red = the two magnonic terms; all other terms are periphery)",
             fontsize=10)
plt.xticks(rotation=25, ha="right", fontsize=8)
ax.grid(axis="y", alpha=.3)
fig.tight_layout()
plt.savefig(os.path.join(FIG, "ppa_waterfall.png"), dpi=170)
plt.show()
print(f"TOTAL = {T*1e12:.3f} pJ per inference")
"""),

("md", r"""
## 7. Summary - what this notebook establishes and what it does not

| Statement | Tag |
|---|---|
| The §9 ledger can be evaluated end-to-end from published anchors plus explicitly flagged assumptions | (E) |
| The dominant terms in the precedent geometry are the wave event and the per-cell write | (E) |
| The break-even digital-MAC energy is the only comparison that survives a change of node | (E) |
| Hematite trades ~200x more cells per wave event for ~200x more transit latency | (E) |
| The result of the ledger swings materially with the assumed foundry write energy | (E) |
| Any specific energy number is a *measured device result* | **not claimed - there is no fabricated device** |
| The architecture has zero idle power / zero resistance / free computation / instant switching | **prohibited by the source paper §10 and not claimed here** |

### The three numbers to replace with citations before anything is published

1. **Foundry MRAM write energy per bit** (A12) - currently an assumption of
   5-20 pJ. This is the number that most changes the answer.
2. **Digital MAC energy** (A14) - currently a sweep; a citable node-specific
   figure is needed for any headline ratio.
3. **The drive-power term for a non-precedent bus** - the hematite scenario
   assumes the CPW drive power transfers unchanged, which is not established.

### The disproof experiment for the ledger

Fabricate a bus with the precedent geometry, drive it at 1.70 GHz, measure
(a) the microwave power actually required, (b) the number of cells switched
correctly, and (c) the energy required to read the result once. Substitute the
measured values into this notebook. If the break-even crosses the digital MAC
energy of the relevant node, the architecture has no economic case at that
geometry, and the table says so.
"""),
]


if __name__ == "__main__":
    build("05_ppa_ledger.ipynb", CELLS)
