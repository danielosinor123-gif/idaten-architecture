# data/lab/ — archived local mumax³ material series (evidence)

This directory holds the **committed evidence** for the honest negative result
reported in `PROVENANCE.md` §2.3 and notebook 01 §2: the local YIG / Bi-YIG /
Co₂₅Fe₇₅ / GdFeCoP / NiFe series has **no reportable decay length**
(r² = 0.001–0.004 over x ∈ [10, 45] µm).

Contents:

| File | What |
|---|---|
| `antenna.ovf` | the CPW launch used by the series — a flared, diamond/lens-shaped launch at the x = 0.05 µm edge (see `tools/probe_antenna.py`); bounding box x ∈ [0.050, 0.500] µm, y ∈ [2.050, 6.000] µm |
| `_summary.json` | per-deck archive records: snapshot counts, bad-file lists, fit metrics, archive size, run duration, and material parameters (Msat / Aex / α / B_ext / f₀) |
| `profiles.csv` | one flat row per deck, for quick reading |

**Provenance and normalization.** The series was originally generated under a
prior, now retired, internal program. The raw archiver output contained the
originating deck headers; those headers are **not** committed, because the
prior program is out of scope for this repository. The committed
`_summary.json` is a normalization of that output that keeps only the
physics-relevant parameters and the metrics. The bulk `.npz` snapshot
archives (≈ 7.3 GB before compaction; ≈ 4400 snapshots for this series) are
gitignored and not committed; the regeneration path is
`tools/archive_lab2.py`.

Decks excluded as not part of this evidence base: the diagnostic decks from the
retired prior programme (see `tools/build_lab_summary.py` for the exact filter).
The three zero-snapshot decks (`YIG_a1e-3_2G_w2`, `YIG_a1e-3_5G`, `YIG_pma_2G`)
are retained in the summary because their absence of recoverable OVF output is
itself information.
