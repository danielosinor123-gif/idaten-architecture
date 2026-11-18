# Device-element ledger

Architecture paper §10 requirement: every proposed element states what quantity
changes, what launches it, retention/reset, how the next stage detects it, the
energy and delay, and the experiment that could disprove it.

**Evidence tags.** `(L)` literature · `(S)` simulated here · `(E)` engineering
estimate · `(A)` predicted · `—` stateless.

| # | Element | Quantity that changes | Launched / written by | Retention / reset | Detected by | Energy + delay | Disproof experiment |
|---|---|---|---|---|---|---|---|
| 1 | CPW launch port | microwave field `h_rf` in the guide | RF source (external) | — (stateless) | — | `P_C1 = 12.6 µW` (L); wave transit over 40.96 µm = **3.26 ns** (E) | measure no coupled mode in the CPW band → `P_C1` not transferable to the fabricated geometry |
| 2 | YIG bus (P₀ port to `Ψ_k`) | spin-wave amplitude `A(x,t)` and phase `φ(x,t)` | CPW burst | — (stateless) | result array / antenna | `P_prec = 36 nW` (L); transit 3.26 ns; ℓ = 99 µm unpatterned, 23 µm in-circuit (L) | no propagating mode at k₁ = 1.70 GHz in the re-run of the authors' deck (K1) |
| 3 | `P₀` phase grating (fabricated `Aex` bands) | local phase velocity of `Ψ_k` | fixed geometry (not at runtime) | fixed; change only by re-fabrication | wavefield downstream | 0 runtime energy (fixed) (E) | measured landscape transfer function `H(k)` deviates from the designed grating by more than the π-step budget (K8) |
| 4 | `C_k` configuration switches (foundry eMRAM/STT/SOT bits) | switch state (route / phase step) | input coding, per step | non-volatile; reset by foundry SOT/eMRAM | wavefield / control logic | `E_config ≈ 0.05 pJ` per bit (E); write ≈ `5–20 pJ/bit` (E, foundry write anchor — pending citation) | measured switch-phase spread exceeds the π-step phase budget |
| 5 | Result element `M_k` (Ni₈₁Fe₁₉ free layer, 100 nm × 20 nm, pitch 200 nm) | magnetisation orientation (up/down) | magnon-assisted reversal | non-volatile; reset by foundry SOT (preferred) or piezomagnetic strain (optional) | MRAM sense amplifier | write ≈ 0.20 fJ/cell (E, drive-power term ÷ 205 cells); read once (E) | wave-present threshold equals wave-absent threshold (K1) — no assist, no advantage |
| 6 | Result-array sense readout (foundry MRAM) | digital word from `M_k` | read instruction at workload end | — | host | `E_read ≈ 0.05 pJ/bit` (E); delay = foundry MRAM read (L, GF 22FDX) | BER > 10⁻⁶ after one workload (K10) |
| 7 | Reset of `M_k` | magnetisation back to reference | foundry SOT write | non-volatile | — | `≈ 0.25 × E_write(SOT)` per bit (E) | reset energy destroys the amortised read-once advantage |
| 8 | Peripheral / control | digital decode + configuration sequencing | host | — | host | 10 % overhead on compute terms (E) | overhead exceeds the analogue advantage at the workload size (K11) |

## Standing prohibitions

- No claim of **zero resistance**, **absolute zero idle power**, **free
  computation**, **instant switching**, or any global-superlative energy.
- **Non-volatile retention is not zero power**: retention removes refresh, not
  peripheral leakage; leakage is budgeted explicitly in §9 ledger / notebook 05.
- The piezomagnetic strain-reset route (Q₂₂₂, Q₃₂₁ in hematite) is an
  **optional optimisation to be tested, not a load-bearing assumption**; the
  foundry MRAM path supplies reset from a qualified process.
- Nothing in this repository reports a fabricated or measured device. `P₀`
  and `C_k` switches are scoped for the SKY130 digital tier; the open-flow
  layout itself is not yet produced and is labelled pending in `openflow/README.md`.
  `M_k` is specified against foundry eMRAM/SOT-MRAM cell dimensions, not fabricated here.
- Chemistry and AI notebooks claim analogue-operator equivalence and a
  benchmark comparison, not "DFT emulation" and not "spin waves are neural
  networks".
