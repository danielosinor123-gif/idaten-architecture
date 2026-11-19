# openflow/ — SKY130 / OpenROAD Flow Scripts layout (COMPLETE)

This directory documents the **PDK-backed open-flow** artifact: the physical
instantiation of `P₀` (fixed switch/transistor topology) and the `C_k`
configuration switches, on the open SkyWater 130 nm PDK through OpenROAD Flow
Scripts (ORFS).

**Status: run complete (2026-11-19).** The final GDS/DEF/Verilog/SPEF, the
design sources, the stage reports, and the full run manifest are in
`gds/idaten_sky130/` (see `gds/idaten_sky130/RUN_MANIFEST.md`). Layout figure:
`figures/idaten_sky130_layout.png`. Headline flow results (S): FLOW_EXIT=0,
DRC 0 violations, antenna 0 violations, WNS/TNS 0.00 ns (Fmax 140.87 MHz vs
10 ns constraint), design area 14,420 um² at 32% utilization.

The artifact is labelled **PDK-backed open-flow layout** and is never
presented as the magnonic die, which has no PDK — that artifact is
`gds/idaten_concept_mask/` ("concept mask, no PDK exists for hematite/LiNbO₃
patterning").

## Toolchain used (all free/open, $0)

- ORFS master (codeload tarball), platform `sky130hd` (sky130A PDK bundled).
- OpenROAD built from source locally (`/root/openroad-src`, BUILD_EXIT=0,
  headless GUI patches marked `IDATEN_GUI_PATCH*`).
- Yosys 0.71 from conda-forge (TCL enabled; ORFS scripts are Tcl).
- KLayout 0.30.12 (conda env).

## Reproduce

```bash
cd /root/orfs_run/idaten   # any empty work dir
env OPENROAD_EXE=/root/eda/orfs-tools/bin/openroad \
    OPENSTA_EXE=/root/eda/orfs-tools/bin/sta \
    YOSYS_EXE=/root/eda/envy/bin/yosys \
    KLAYOUT_CMD=/root/eda/envk/bin/klayout \
    PYTHON_EXE=/usr/bin/python3 \
    LD_LIBRARY_PATH=/root/eda/build-env/lib:/root/eda/ortools-cpp/lib:/root/eda/envy/lib \
  make -f /root/orfs/flow/Makefile \
    DESIGN_CONFIG=/root/orfs/flow/designs/sky130hd/idaten_sky130/config.mk
```

(The earlier `./flow.sh -design ...` entry point is a per-stage helper in this
ORFS revision; the Makefile with `DESIGN_CONFIG` is the supported entry.)
