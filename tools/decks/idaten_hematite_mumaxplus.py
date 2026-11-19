#!/usr/bin/env python3
"""Idaten Ce100 - hematite (alpha-Fe2O3) AF bus arm, mumax+ 1.2.2 Python API.

Stage D (the "hematite question" of CREDIBILITY_PLAN Phase 1.1): the same
bare-bus propagation experiment as Stage C (100 um x 8 um bus, CPW-style
launch at x ~ 1 um, 1.70 GHz / 1 mT burst 0.5-3 ns, probes along x), but the
bus is an antiferromagnet, so the wave variable is the Neel vector n, and
the solver must be mumax+ (Antiferromagnet class), not mumax3.

mumax+ 1.2.2 is the PyPI wheel `mumaxplus==1.2.2` (GPL-3.0-only), tag
v1.2.2 = commit d16d8875 on github.com/mumax/plus. Run it anywhere with a
CUDA GPU:  python idaten_hematite_mumaxplus.py --nx 1000 --ny 80 ...

Parameter mapping (derived from the v1.2.2 source, src/physics/afmexchange.cu):
  intracell AFM exchange field  H_site = 4*|afmex_cell| / (latcon^2 * Ms)
  intercell AFM exchange field  H_grad = |afmex_nn| * k^2 / Ms
  two-sublattice linear theory then gives the acoustic branch
      omega^2 = 2 * gamma^2 * H_site * |afmex_nn| * k^2 / Ms   (low k)
  Matching to the measured hematite qFM dispersion (arXiv:2212.11887,
  Eq. 5: omega^2 = gamma^2 * 2*H_E*(H_a + A*k^2), mu0*A = 9.153e-6 T*um^2)
  with H_site = H_E gives:
      |afmex_cell| = H_E * Ms * latcon^2 / 4
      |afmex_nn|   = A_T * Ms          (A_T = mu0*A/mu0 in T*m^2)
  Predicted group velocity (E): v_g = gamma*sqrt(2*H_E*A_T) ~ 24 km/s,
  vs measured (L) 10-23 km/s (Hamdi, Posva & Grundler, PRM 7, 054407 2023).

Material inputs, all tagged (L) - they are inputs, not results:
  Ms_sub  = 9.0e5 A/m   sublattice magnetisation: 5 uB per Fe3+, 6 Fe per
                        sublattice per hexagonal cell (a=5.035 A, c=13.75 A)
  alpha   = 1.1e-5      Hamdi PRM 7, 054407 (2023)
  H_E     = 1040 T      exchange field, fixed value used in arXiv:2610.08030
  latcon  = 0.5e-9 m    ~ hematite in-plane lattice constant a = 5.035 A
  mu0*A   = 9.153e-6 T*um^2,  exchange stiffness length l_e = 0.955 A
                        (arXiv:2212.11887)
  H_a     = 1 Oe = 79.58 A/m  easy-plane anisotropy above T_M = 262 K
                        (Hamdi PRM 7, 054407, 2023)
  bias    = 30 mT along x (Hamdi's measurement field); Neel vector along y
  DMI     = 0 in this first arm (hematite's weak-FM canting via DMI is
                        neglected; H_D ~ 1 T vs H_E = 1040 T - documented
                        deviation, see PROVENANCE)

Measured here (S, by tools/analyze_hematite.py on the outputs):
  table.csv  t, global <n>, global <M>, 8 x-probe <n_z>, <n_y> every 20 ps
  neel_end.npz  full Neel-vector field at the end of the run
  -> dominant frequency, probe amplitude decay length, group velocity
"""
import argparse
import json
import os
import time

import numpy as np


def setp(holder, name, value):
    """Set a mumax+ parameter robustly (property-assignment or .set())."""
    p = getattr(holder, name)
    try:
        p.set(value)
        return
    except Exception:
        pass
    setattr(holder, name, value)


def sub(afm, which):
    """afm.sub1 is a property in the wheel returning a Ferromagnet wrapper.

    Wrapper objects carry `_impl`; bound C++ methods do not. Never call a
    wrapper blindly: FieldQuantity/ScalarQuantity define __call__ (they
    evaluate), so `callable()` is true for them too - check `_impl` first.
    """
    a = getattr(afm, which)
    if hasattr(a, "_impl"):
        return a
    return a() if callable(a) else a


def quant(obj, name):
    """Quantity accessors (afm.neel_vector etc.): property -> FieldQuantity.

    FieldQuantity is callable (calling it evaluates to an ndarray), which
    broke the naive `a() if callable(a)` version - return the wrapper and
    let the caller use .eval()/.average().
    """
    a = getattr(obj, name)
    if hasattr(a, "_impl"):
        return a
    return a() if callable(a) else a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nx", type=int, default=1000)
    ap.add_argument("--ny", type=int, default=80)
    ap.add_argument("--cell", type=float, default=100e-9, help="dx=dy [m]")
    ap.add_argument("--thick", type=float, default=100e-9, help="dz [m]")
    ap.add_argument("--t-run", type=float, default=8e-9, help="total sim time [s]")
    ap.add_argument("--t-settle", type=float, default=100e-12)
    ap.add_argument("--f0", type=float, default=1.70e9, help="drive frequency [Hz]")
    ap.add_argument("--b-amp", type=float, default=1e-3, help="drive amplitude [T]")
    ap.add_argument("--table-dt", type=float, default=20e-12)
    ap.add_argument("--dt", type=float, default=2e-13,
                    help="FIXED solver timestep [s]; fixed-dt mode makes "
                         "timesolver.run(dur) land exactly on t+dur (the "
                         "adaptive stepper can otherwise swallow a whole "
                         "run() call near equilibrium)")
    ap.add_argument("--nprobe", type=int, default=8)
    ap.add_argument("--out", type=str, default="hematite.out")
    ap.add_argument("--max-s", type=float, default=10.5 * 3600)
    args = ap.parse_args()

    t_start = time.time()

    def log(msg):
        print("[{}] {}".format(time.strftime("%H:%M:%S"), msg), flush=True)

    from mumaxplus import World, Grid, Antiferromagnet

    nx, ny, nz = args.nx, args.ny, 1
    dx = dy = args.cell
    dz = args.thick

    # ---- material inputs (L), see module docstring ----
    MS_SUB = 9.0e5            # A/m
    ALPHA = 1.1e-5            # Hamdi PRM 7, 054407 (2023)
    H_E = 1040.0              # T
    LATCON = 0.5e-9           # m
    MU0A = 9.153e-6 * 1e-12   # T m^2 = 9.153e-6 T um^2 (arXiv:2212.11887)
    A_T = MU0A               # dispersion coefficient in T m^2
    H_A = 79.58               # A/m (1 Oe), easy-plane above T_M
    B_BIAS = 30e-3            # T along x

    AFMEX_CELL = -H_E * MS_SUB * LATCON ** 2 / 4.0   # J/m, gives H_site = H_E
    AFMEX_NN = -A_T * MS_SUB                        # J/m, gives v_g = gamma*sqrt(2 H_E A_T)

    world = World(cellsize=(dx, dy, dz))
    # fixed timestep: with adaptive stepping, run(dur) near equilibrium can
    # advance only one clamped step (stoptime - timestep < 0 once the
    # adaptive dt explodes at zero torque), which breaks output pacing
    world.timesolver.adaptive_timestep = False
    grid = Grid((nx, ny, nz))
    afm = Antiferromagnet(world, grid, name="hematite_bus")
    s1 = sub(afm, "sub1")
    s2 = sub(afm, "sub2")

    # net magnetisation ~ Ms * H/H_E ~ 1e-5 Ms -> demag negligible (E);
    # disable for speed, documented in PROVENANCE
    try:
        afm.enable_demag = False   # sets both sublattices
    except Exception:
        pass
    for s in (s1, s2):
        setp(s, "msat", MS_SUB)
        setp(s, "alpha", ALPHA)
        setp(s, "ku1", -0.5 * MS_SUB * H_A)   # easy plane, anisU = z
        setp(s, "anisU", (0.0, 0.0, 1.0))
        # static bias on BOTH sublattices (afm.bias_magnetic_field returns
        # sub1's Parameter object; .set() on it would only bias sub1)
        setp(s, "bias_magnetic_field", (B_BIAS, 0.0, 0.0))
    setp(afm, "afmex_cell", AFMEX_CELL)
    setp(afm, "afmex_nn", AFMEX_NN)
    setp(afm, "latcon", LATCON)

    m1 = np.zeros((3, nz, ny, nx))
    m1[1] = 1.0     # Neel vector in-plane along y; bias along x (spin-flop)
    m2 = -m1
    s1.magnetization.set(m1)
    s2.magnetization.set(m2)

    try:
        afm.minimize(1e-6, 10)
    except TypeError:
        afm.minimize()
    world.timesolver.timestep = args.dt   # minimize may leave dt elsewhere
    world.timesolver.run(args.t_settle)
    t0 = world.timesolver.time
    log("settled: t={:.3e} s, fixed dt={:.3e} s".format(t0, world.timesolver.timestep))

    # ---- drive: localised out-of-plane RF stripe at x ~ 1 um ----
    xs = (np.arange(nx) + 0.5) * dx
    launch = np.exp(-((xs - 1.0e-6) / 0.7e-6) ** 2)
    mask = np.zeros((3, nz, ny, nx))
    mask[2] = launch[None, None, :]
    state = {"t0": t0}

    def rf(t):
        dt = t - state["t0"]
        w = np.tanh((dt - 0.5e-9) / 0.1e-9) - np.tanh((dt - 3.0e-9) / 0.1e-9)
        return np.array([0.0, 0.0, args.b_amp * np.sin(2 * np.pi * args.f0 * dt) * w])

    # Zeeman RF couples to BOTH sublattices - add the time term to each
    for s in (s1, s2):
        s.bias_magnetic_field.add_time_term(rf, mask)

    # ---- probes: nprobe equal x-slices of the bus ----
    pw = nx // args.nprobe          # probe width in cells
    probe_x0 = [p * pw for p in range(args.nprobe)]
    probe_x_um = [(x0 + 0.5 * pw) * dx * 1e6 for x0 in probe_x0]

    os.makedirs(args.out, exist_ok=True)
    csv_path = os.path.join(args.out, "table.csv")
    header = (["t"] + ["n{}_avg".format(c) for c in "xyz"]
              + ["M{}_avg".format(c) for c in "xyz"]
              + ["p{}_nz".format(p) for p in range(args.nprobe)]
              + ["p{}_ny".format(p) for p in range(args.nprobe)]
              + ["max_intracell_angle", "e_total"])
    fh = open(csv_path, "w")
    fh.write("# " + ",".join(header) + "\n")

    nv_q = quant(afm, "neel_vector")
    fm_q = quant(afm, "full_magnetization")

    def record():
        t = world.timesolver.time
        nv = nv_q.eval()                # (3, nz, ny, nx)
        fm = fm_q.eval()
        nvz = nv[2, 0]                  # (ny, nx)
        nvy = nv[1, 0]
        pnz = [float(nvz[:, x0:x0 + pw].mean()) for x0 in probe_x0]
        pny = [float(nvy[:, x0:x0 + pw].mean()) for x0 in probe_x0]
        row = ([t] + list(nv_q.average()) + list(fm_q.average())
               + pnz + pny)
        try:
            row.append(float(quant(afm, "max_intracell_angle").eval()))
        except Exception:
            row.append(float("nan"))
        try:
            row.append(float(quant(afm, "total_energy").eval()))
        except Exception:
            row.append(float("nan"))
        fh.write(",".join("{:.10e}".format(v) for v in row) + "\n")
        fh.flush()
        return t

    record()
    last_hb = time.time()
    # pace by explicit target times; fixed dt makes run(dur) land on t+dur.
    # Guard the final chunk: in FP32, stoptime - time_ can round to exactly 0
    # when the remaining duration is below ~ulp(t) ~ 5e-16 s at t ~ 8 ns,
    # which makes TimeSolver::step() throw "timestep <= 0".
    n_rec = int(np.ceil(args.t_run / args.table_dt))
    for i in range(1, n_rec + 1):
        target = min(i * args.table_dt, args.t_run)
        t = world.timesolver.time
        if target - t > max(1e-15, 1e-3 * args.dt):
            try:
                world.timesolver.run(target - t)
            except RuntimeError as e:
                if "timestep" in str(e):
                    log("final-step guard tripped at t={:.6e}: {}".format(t, e))
                else:
                    raise
        t = record()
        if time.time() - t_start > args.max_s:
            log("session budget reached at t={:.3e} s".format(t))
            break
        if time.time() - last_hb > 60:
            last_hb = time.time()
            log("sim t={:.3f} / {:.1f} ns ({:.1f}%), dt={:.2e} s, wall {:.0f} s".format(
                t * 1e9, args.t_run * 1e9, 100.0 * t / args.t_run,
                world.timesolver.timestep, time.time() - t_start))
    fh.close()

    np.savez(os.path.join(args.out, "neel_end.npz"),
             neel=nv_q.eval(), full=fm_q.eval(), t=t)
    meta = dict(args=vars(args), ms_sub=MS_SUB, alpha=ALPHA, h_e=H_E,
                latcon=LATCON, mu0A_T_um2=9.153e-6, afmex_cell=AFMEX_CELL,
                afmex_nn=AFMEX_NN, b_bias=B_BIAS, probe_x_um=probe_x_um,
                t_end=float(t), wall_s=time.time() - t_start,
                mumaxplus="1.2.2-wheel")
    with open(os.path.join(args.out, "run_meta.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
    log("DONE t={:.3f} ns, wall {:.0f} s -> {}".format(t * 1e9, time.time() - t_start, args.out))


if __name__ == "__main__":
    main()
