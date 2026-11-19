# Contributing

This repository is a **research artifact set**: every number must carry an
evidence tag — **(L)** literature, **(S)** simulated (with the run command
and tool version), **(E)** engineering estimate with written assumptions,
**(A)** predicted hypothesis. Pull requests that add numbers without a tag,
or that use the prohibited phrases listed in the README ("zero resistance",
"absolute zero idle power", "free computation", "instant switching",
global-superlative efficiency claims), will be closed.

## How to reproduce the evidence

- Notebooks: `python tools/nb01_physics.py` … `python tools/nb05_ppa.py`
  rebuild `notebooks/*.ipynb`; `python tools/run_notebooks.py` executes them
  in place (outputs are committed as evidence).
- Simulation decks: `tools/decks/`. mumax³ decks run on any CUDA GPU
  (`mumax3 -f deck.mx3`); the hematite deck needs the PyPI wheel
  `mumaxplus==1.2.2` on an sm_75+ GPU (Kaggle T4 works — see
  `PROVENANCE.md` §2.8 for why the local sm_61 machine cannot JIT it).
- Layout: ORFS/sky130hd run, see `gds/idaten_sky130/RUN_MANIFEST.md`.
- Kaggle kernels/datasets with the full run logs are listed in
  `PROVENANCE.md` §2.5/§2.7/§2.8.

## Good first issues

- Run the Stage C bare-bus deck for a 6th material on any GPU and open a PR
  with `table.txt` + the analyzer output.
- Longer hematite run (windowed launch, 20+ ns) to try to resolve v_g —
  currently **not resolved** (standing-mode ring-down), stated in
  `PROVENANCE.md` §2.8.
- Add a DMI parameter to the hematite deck from literature (currently
  documented as DMI = 0).
- Add the padframe/IO required for a SkyWater open-MPW shuttle submission of
  `gds/idaten_sky130/`.

## Where to ask

Use GitHub **Discussions** for questions and claim challenges; use
**Issues** (template: "Challenge a claim") to dispute any (L)/(S)/(E)/(A)
number — that is the fastest way to improve this repository.
