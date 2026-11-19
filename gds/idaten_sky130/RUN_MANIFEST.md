# RUN_MANIFEST — `idaten_sky130` PDK-backed open-flow layout (SKY130 / ORFS)

**Label: PDK-backed open-flow layout.** This is the digital tier (`P0` fixed
topology + `C_k` config register bank + `M_k` result register) of the Idaten
Ce100, placed and routed on the open SkyWater 130 nm PDK through OpenROAD Flow
Scripts. It is **not** the magnonic die — no PDK exists for hematite/LiNbO3
patterning; that artifact is `gds/idaten_concept_mask/` ("concept mask").

## Run facts (all measured, (S))

| Item | Value |
|---|---|
| Run date | 2026-11-19, 00:45–00:59 WAT (14 min wall, single `make`, FLOW_EXIT=0) |
| Entry point | `make -f /root/orfs/flow/Makefile DESIGN_CONFIG=.../sky130hd/idaten_sky130/config.mk` |
| Design | `idaten_sky130` (see `src/`): 8-bit spectral input, 4-tap MAC pipeline, `C_k` 8-bit config reg, `M_k` 16-bit result reg |
| Platform / PDK | ORFS `sky130hd` platform; sky130A PDK files bundled in ORFS (`flow/platforms/sky130hd/{lib,lef,gds}`, tech `sky130A`) |
| ORFS | OpenROAD-flow-scripts master, codeload tarball at `/root/orfs` (no git metadata; fetched 2026-11) |
| OpenROAD | built from source at `/root/openroad-src` on 2026-11-19 (BUILD_EXIT=0), installed `/root/eda/orfs-tools/bin/openroad`; GUI patches marked `IDATEN_GUI_PATCH*` (headless build) |
| Yosys | 0.71+ (conda-forge, TCL 8.6 enabled — required by ORFS tcl scripts) at `/root/eda/envy/bin/yosys` |
| KLayout | 0.30.12 at `/root/eda/envk/bin/klayout` |
| Clock constraint | 10.0 ns (`src/constraint.sdc`) |

## Results (from `reports/`, (S))

- Final GDS `6_final.gds` (2,463,484 bytes, MD5 `ebe60559d93183e20a403abe5941e58c`), plus `6_final.def/.v/.spef`.
- Die 216.3 x 216.3 um; design area 14,420 um^2, 32% utilization (`6_finish.rpt`).
- Synthesis: 6,864 cells, chip area 13,780.7 um^2 (`synth_stat.txt`).
- Timing closed: WNS 0.00 ns, TNS 0.00 ns, worst slack 2.90 ns, Fmax 140.87 MHz (min period 7.10 ns vs 10 ns constraint).
- DRC: detailed-route final iteration **0 violations** (`[INFO DRT-0199] Number of violations = 0`; empty `5_route_drc.rpt`); antenna check 0 net / 0 pin violations.
- KLayout merge check: all LEF cells have matching GDS cells, no orphan cells.
- Power (report_design_power, tt_025C_1v80): total 1.46e-3 W (54.1% internal / 45.9% switching) at the constrained clock.

## Layout figure

`figures/idaten_sky130_layout.png` — gdstk+matplotlib render of `6_final.gds`
(layers up to metal5; top-metal fill excluded for visibility).

## Reproduce

```bash
# WSL Ubuntu-24.04, tools as above
export LD_LIBRARY_PATH=/root/eda/build-env/lib:/root/eda/ortools-cpp/lib:/root/eda/envy/lib
cd /root/orfs_run/idaten   # any empty work dir
env OPENROAD_EXE=/root/eda/orfs-tools/bin/openroad \
    OPENSTA_EXE=/root/eda/orfs-tools/bin/sta \
    YOSYS_EXE=/root/eda/envy/bin/yosys \
    KLAYOUT_CMD=/root/eda/envk/bin/klayout \
    PYTHON_EXE=/usr/bin/python3 \
  make -f /root/orfs/flow/Makefile \
    DESIGN_CONFIG=/root/orfs/flow/designs/sky130hd/idaten_sky130/config.mk
```

Design sources are mirrored in `src/`; the flow consumed the identical copies
under `/root/orfs/flow/designs/{src,sky130hd}/idaten_sky130/`.

## Honesty notes

- This layout instantiates only the digital tier. The magnonic wave-compute
  stage has no PDK and is not represented here.
- Power/area numbers are from the open PDK's tt corner reports of a tiny
  prototype (6.9k cells); they are flow outputs, not silicon measurements.
- OpenROAD was built headless (GUI disabled) — see PROVENANCE.md for the
  build patches and the 12:42 crash note.
