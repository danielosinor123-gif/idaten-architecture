# openflow/ — SKY130 / OpenROAD Flow Scripts layout (pending)

This directory is reserved for the **PDK-backed open-flow** artifact: the
physical instantiation of `P₀` (fixed switch/transistor topology) and the
`C_k` configuration switches, on the open SkyWater 130 nm PDK through
OpenROAD Flow Scripts (ORFS).

**Status: not present in this checkout.** It must not be described as
complete. The open-flow run has been obstructed by disk pressure in the WSL
development VM; the VHDX cleanup freed ≈ 25 GB of logical space, but the
file itself cannot be shrunk safely on this machine (`wsl --manage …
--set-sparse` reports sparse support is disabled due to potential data
corruption; it was **not** forced). The ORFS build tree under `/root/orfs`
and the OpenROAD source under `/root/openroad-src` are retained.

When the run completes, `gds/idaten_sky130/` will hold the final DEF/GDS and
this README will be replaced with the run manifest. The artifact will be
labelled **PDK-backed open-flow layout** and will never be presented as the
magnonic die, which has no PDK.

Reproduction outline:

```bash
cd /root/orfs                       # OpenROAD Flow Scripts
./flow.sh -design idaten_sky130     # 22 nm SkyWater 130 nm PDK
```

and then copy `build/.../6_final.gds` into `../gds/idaten_sky130/` with a
manifest recording the ORFS commit, PDK revision, tool versions, and the
checks that passed.
