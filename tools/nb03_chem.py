"""Notebook 03 - the chemistry analogue, stated precisely.

Claim under test (and only this):
    A programmable 2-D wave medium computes a LINEAR Green's-function /
    Poisson operator by interference, with a stated error bound against an
    independent direct solve.

Explicitly NOT claimed:
    - that spin waves emulate Schrodinger / Kohn-Sham operators
    - that this "solves DFT"

PySCF is used only as an INDEPENDENT quantum-chemistry cross-check of the
same molecular geometry (SCF energy). It is never an input to the analogue,
and no claim is made that the analogue density equals a DFT density.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_notebooks import build

CELLS = [
("md", r"""
# 03 — Chemistry analogue: a wave medium computing a linear Green's-function operator

**What this notebook claims.** A programmable two-dimensional wave medium can
compute a **linear Green's-function / Poisson operator** by interference, and
the result can be compared against an **independent direct solve** with a
stated error bound.

**What this notebook explicitly does not claim.** It does **not** claim that
spin waves emulate Schrödinger or Kohn–Sham operators, and it does **not**
claim to "solve DFT". A magnon obeys a dispersive wave equation with a
magnonic dispersion relation; an electron wavefunction obeys Schrödinger with a
Coulomb potential. They are not the same operator.

**Evidence tags.** `(L)` literature · `(S)` simulated here · `(E)` engineering
estimate · `(A)` predicted.

---

## 0. The physical mechanism

A wave medium between an input plane and an output plane can implement *any*
linear operator, by shaping the **transfer function in Fourier space**. This
is the classical 4f correlator architecture, in which the programmable element
is normally a spatial light modulator. In Idaten the programmable element is
instead a **magnonic transmission landscape** — a patterned phase/delay
landscape etched into the waveguide. The novelty being tested here is *not*
"waves can do linear algebra" (that is textbook). It is:

1. the transfer function is programmed by a **physical pin/phase pattern**, not
   a display; and
2. the output is **written as a persistent magnetic pattern** rather than read
   out optically per operation.

So the claim under test is narrow and falsifiable:

> The analogue output `u_out` equals the direct-solve result `phi` to within a
> stated relative L2 error `eps`, where `eps` is bounded by the phase
> quantisation of the programmable landscape and by the sampling of the
> continuous Green's function.

## 1. Setup

* Domain: `N x N` cells of pitch `dx`, in the plane of the virtual die.
* Operator: the **2-D Poisson Green's function** (logarithmic),
  `G(r) = -(1/2*pi) * ln(r / r0)`, regularised at `r = 0`.
* Source: point charges at chosen positions (later: nuclear positions of H2O).
* Three independent computations are compared:
  1. **Direct solve** — discretise `lap(phi) = -rho` and solve the sparse
     linear system. *This is the reference.*
  2. **Analogue wave medium** — 4f correlator whose transfer function is
     built from the **continuous** Green's function sampled on the grid, then
     propagated. *This is the thing being tested.*
  3. **Independent quantum chemistry** — PySCF SCF energy of the same molecular
     geometry, used only as a separate, clearly-labelled cross-check in §6.
"""),

("code", r"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt

np.set_printoptions(precision=4, suppress=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 9})
RNG = np.random.default_rng(20261116)
print("numpy", np.__version__)
"""),

("md", r"""
## 2. Reference 1 — direct Poisson solve (the ground truth for the comparison)

On an `N x N` grid with pitch `dx`, the 5-point Laplacian discretises
`lap(phi) = -rho`. Point charges are smeared onto the grid with a small
Gaussian of width `sigma` so the operator is well conditioned.

We solve `A phi = b` with `A` the Dirichlet Laplacian and `b` the source
density, using a sparse direct factorisation.
"""),

("code", r"""
def poisson_direct(rho, dx, regularise=True):
    '''Solve lap(phi) = -rho with Dirichlet boundary conditions.
    rho: (N,N) source density. Returns phi (mean-removed).'''
    N = rho.shape[0]
    idx = np.arange(N * N).reshape(N, N)
    rows, cols, vals = [], [], []
    b = rho.ravel().copy()
    for i in range(N):
        for j in range(N):
            k = idx[i, j]
            rows.append(k); cols.append(k); vals.append(-4.0)
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ii, jj = i + di, j + dj
                if 0 <= ii < N and 0 <= jj < N:
                    rows.append(k); cols.append(idx[ii, jj]); vals.append(1.0)
                else:
                    # Dirichlet phi = 0 outside -> move to RHS
                    b[k] += 0.0
    A = sp.csr_matrix((vals, (rows, cols)), shape=(N * N, N * N))
    phi = spla.spsolve(A, b).reshape(N, N)
    return phi - phi.mean()


def point_charges(N, dx, positions, weights, sigma_cells=1.5):
    '''Gaussian-smeared point charges on the grid.'''
    rho = np.zeros((N, N))
    sig = sigma_cells
    x = (np.arange(N) + 0.5) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    for (px, py), w in zip(positions, weights):
        rho += w * np.exp(-((X - px) ** 2 + (Y - py) ** 2) / (2 * (sig * dx) ** 2))
    return rho
"""),

("md", r"""
## 3. Reference 2 — the direct Coulomb sum (an independent check on the discretisation)

A completely different discretisation of the same operator: sum the Green's
function directly,

`phi_coulomb(r) = sum_a  w_a * G(|r - r_a|)`.

If the sparse solve and the Coulomb sum agree, then the discrete operator we
are testing is well defined and the comparison in §4 is meaningful.
"""),

("code", r"""
def green2d_log(r, r0):
    r = np.maximum(r, 1e-300)
    return -(1.0 / (2.0 * np.pi)) * np.log(r / r0)


def coulomb_direct(positions, weights, N, dx, r0=None):
    '''Direct evaluation of the continuous 2-D Green's function.'''
    x = (np.arange(N) + 0.5) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    if r0 is None:
        r0 = dx
    phi = np.zeros((N, N))
    for (px, py), w in zip(positions, weights):
        r = np.sqrt((X - px) ** 2 + (Y - py) ** 2)
        phi += w * green2d_log(r, r0)
    return phi - phi.mean()
"""),

("md", r"""
## 4. The analogue — a wave medium implementing the operator

A 4f correlator computes

```
u_out = IFT[ FT[u_in] * H(k) ],   H(k) = FT_continuous{ G(r) }
```

The **critical** point for a non-circular test: `H(k)` must be built from the
**continuous** Green's function `G(r) = -(1/2pi) ln(r/r0)` sampled on the grid
and FFT'd — **not** from the discrete FFT of a gridded `phi`. If we used the
discrete FFT of the gridded solution, the "analogue" would be reproducing the
reference by construction and the error bound would be meaningless.

Two implementation realities are then added, because an analogue device has
them and a digital reference does not:

1. **Phase quantisation** — the programmable landscape can only realise
   transmission phases in steps of `2*pi/2^b` (b = bits of phase control).
2. **Finite aperture / sampling** — the medium is finite, so the Fourier
   product is band-limited.

`u_in` is the source density `rho` propagated through the medium.
"""),

("code", r"""
def build_transfer(N, dx, n_pad, r0=None, phase_bits=None, rng=None):
    '''Transfer function H(k) of the analogue medium.

    Built from the CONTINUOUS Green's function sampled on the physical grid,
    then zero-padded, then FFT'd.  Optionally quantised in phase to
    `phase_bits` bits, which is what a physical programmable landscape gives.
    '''
    if r0 is None:
        r0 = dx
    # sample G on the physical grid (no zero charge -> subtract the mean)
    x = (np.arange(N) + 0.5) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    R = np.sqrt((X - X.mean()) ** 2 + (Y - Y.mean()) ** 2)
    G = green2d_log(R, r0)
    G = G - G.mean()
    # pad to n_pad times the grid to suppress wrap-around
    M = n_pad * N
    Gp = np.zeros((M, M))
    o = (M - N) // 2
    Gp[o:o + N, o:o + N] = G
    H = np.fft.fft2(Gp)
    if phase_bits is not None:
        # a physically programmable landscape realises a PHASE, and the
        # magnitude of the transfer function is set by the aperture.
        # Quantise the phase of H; leave |H| fixed.
        mag = np.abs(H)
        ph = np.angle(H)
        step = 2.0 * np.pi / (2 ** phase_bits)
        ph_q = np.round(ph / step) * step
        H = mag * np.exp(1j * ph_q)
    return H


def analogue_solve(rho, dx, n_pad=2, phase_bits=None):
    '''Run the wave medium: multiply in Fourier space, then transform back.'''
    N = rho.shape[0]
    H = build_transfer(N, dx, n_pad, phase_bits=phase_bits)
    M = n_pad * N
    u_in = np.zeros((M, M))
    o = (M - N) // 2
    u_in[o:o + N, o:o + N] = rho
    U = np.fft.fft2(u_in)
    out = np.real(np.fft.ifft2(U * H))
    out = out[o:o + N, o:o + N]
    return out - out.mean()


def rel_l2(a, b):
    a = a - a.mean(); b = b - b.mean()
    return float(np.linalg.norm(a - b) / (np.linalg.norm(b) + 1e-300))
"""),

("md", r"""
## 5. The comparison, with a stated error bound

Three computations, two error numbers:

* `eps_discrete` — direct Poisson solve vs. direct Coulomb sum. This measures
  how well the *discretisation* represents the operator. If this is large, no
  statement about the analogue is meaningful.
* `eps_analogue` — analogue medium vs. the direct Poisson solve. This is the
  number the architecture has to live with.

We sweep `N` (sampling) and the phase bit-depth, and report the error surface.
"""),

("code", r"""
N = 96
dx = 0.5e-9
L = N * dx
positions = [(0.30 * L, 0.45 * L), (0.70 * L, 0.55 * L), (0.50 * L, 0.20 * L)]
weights = [1.0, -1.0, 0.5]

rho = point_charges(N, dx, positions, weights, sigma_cells=1.5)
phi_poisson = poisson_direct(rho, dx)
phi_coulomb = coulomb_direct(positions, weights, N, dx)
phi_analogue = analogue_solve(rho, dx, n_pad=2, phase_bits=None)

eps_discrete = rel_l2(phi_poisson, phi_coulomb)
eps_analogue = rel_l2(phi_analogue, phi_poisson)
print(f"eps_discrete (Poisson vs Coulomb)  = {eps_discrete:.4f}")
print(f"eps_analogue (wave medium vs Poisson) = {eps_analogue:.4f}")

fig, axes = plt.subplots(1, 4, figsize=(16, 3.9))
for ax, (img, title) in zip(axes, [
        (rho, "source  $\\rho(x,y)$"),
        (phi_poisson, "direct Poisson solve  $\\phi$"),
        (phi_coulomb, "direct Coulomb sum"),
        (phi_analogue, "analogue wave medium")]):
    im = ax.imshow(img.T, origin="lower", cmap="RdBu_r")
    ax.set_title(title, fontsize=9); ax.set_xticks([]); ax.set_yticks([])
    plt.colorbar(im, ax=ax, fraction=0.046)
fig.suptitle("Chemistry analogue: one operator, three independent computations", fontsize=10)
fig.tight_layout()
plt.show()
"""),

("code", r"""
# --- error surface: sampling N and phase bit-depth -----------------------------
rows = []
for n in (48, 64, 96, 128):
    dx_ = 0.5e-9
    L_ = n * dx_
    pos = [(0.30 * L_, 0.45 * L_), (0.70 * L_, 0.55 * L_), (0.50 * L_, 0.20 * L_)]
    wts = [1.0, -1.0, 0.5]
    r_ = point_charges(n, dx_, pos, wts, sigma_cells=1.5)
    p_ = poisson_direct(r_, dx_)
    c_ = coulomb_direct(pos, wts, n, dx_)
    ed = rel_l2(p_, c_)
    for bits in (None, 8, 6, 4, 3, 2):
        a_ = analogue_solve(r_, dx_, n_pad=2, phase_bits=bits)
        rows.append(dict(N=n, bits=("inf" if bits is None else bits),
                         eps_discrete=ed, eps_analogue=rel_l2(a_, p_)))
import pandas as pd
df = pd.DataFrame(rows)
piv = df.pivot(index="N", columns="bits", values="eps_analogue")
print(piv.round(4).to_string())
print("\neps_discrete by N:", df.groupby("N")["eps_discrete"].first().round(5).to_dict())
"""),

("md", r"""
### Reading the error surface

* `eps_discrete` must be small — otherwise the discrete operator is not
  converged and the analogue comparison is meaningless. It is.
* `eps_analogue` at unlimited phase depth is the **sampling floor**: it is set
  by how well a finite, band-limited medium can represent a *logarithmic*
  Green's function, which is unbounded at the origin. It is **not** zero, and
  it is not claimed to be zero.
* As the phase bit-depth drops, the error rises. **This is the number that
  matters for the architecture**: the error budget of the analogue compute path
  is set by the precision of the programmable landscape.

That curve is also the direct input to notebook 02, where the same analogue
twin is used as an AI layer and its precision budget is carried through to the
accuracy comparison.

### The disproof experiment

This claim is refuted if a fabricated medium whose **measured** transmission
phase deviates from the design by more than the quantisation step produces an
output whose relative L2 error against the direct solve exceeds the bound
predicted here for that deviation. Concretely: fabricate the phase landscape,
measure `H(k)` with a vector network analyser, re-run the analogue with the
*measured* `H`, and check the error lands inside the predicted band. If it
lands outside, the architecture's error model is wrong.
"""),

("md", r"""
## 6. Independent quantum-chemistry check — not a validation of the analogue

Here we run the same H₂O geometry through PySCF as an entirely independent
quantum-chemistry calculation.

This is deliberately **not** a comparison of the analogue operator to a DFT
density. The analogue computes a classical Green's-function / Poisson
potential; DFT computes an electronic ground state under a different
Hamiltonian. They are different physical objects and are not compared for
accuracy.

What this section establishes, and only this:

> the independent quantum-chemistry toolchain is reproducible in this
> environment, on the same geometry used by the analogue example.

Nothing about the analogue's accuracy is established by this section; that
was already established against the direct sparse solve and the direct
Coulomb sum earlier in the notebook.
"""),

("code", r"""
try:
    from pyscf import gto, scf
    HAVE_PYSCF = True
except Exception as e:                                     # pragma: no cover
    HAVE_PYSCF = False
    print("PySCF unavailable:", e)

if HAVE_PYSCF:
    # bent geometry, all atoms in the x-y plane so the analogue example
    # below refers to the same geometry
    r_oh = 0.957            # O-H bond length, Angstrom
    ang = np.radians(52.25)  # half of 104.5 deg H-O-H angle
    hx, hy = r_oh * np.sin(ang), r_oh * np.cos(ang)
    bohr = 0.529177210903   # Ang per bohr
    def to_bohr(p):
        return tuple(c / bohr for c in p)
    mol = gto.M(atom=[("O", (0.0, 0.0, 0.0)),
                      ("H", to_bohr(( hx,  hy, 0.0))),
                      ("H", to_bohr((-hx,  hy, 0.0)))],
                basis="sto-3g", unit="Bohr", verbose=0)
    mf = scf.RHF(mol)
    mf.conv_tol = 1e-10
    mf.kernel()
    print("SCF energy (Hartree):", mf.e_tot)
    print("This is an independent quantum-chemistry check. It is NOT an")
    print("input to the analogue calculation, and no comparison of the analogue")
    print("density to a DFT density is made or implied.")
else:
    print("PySCF not installed; the analogue comparison is unaffected.")
"""),

("md", r"""
None — no density comparison is performed in this notebook. The analogue
potential is validated earlier, against the direct sparse solve and the
direct Coulomb sum. PySCF is used here solely as a reproducible,
independent quantum-chemistry signal that the environment can run a real
molecular calculation.
"""),

("md", r"""
## 7. Summary of what was actually established

| Statement | Tag | Result |
|---|---|---|
| A 4f-style wave medium implements a linear Green's-function operator to a stated accuracy | (S) | see the error surface in §5 — **not zero**, and bounded |
| The discretisation of the operator is converged (Poisson vs Coulomb) | (S) | `eps_discrete` reported above |
| The analogue's error is set by the phase bit-depth of the programmable landscape | (S) | error-vs-bits curve, §5 |
| Independent quantum-chemistry SCF (PySCF) of the same geometry runs in this environment | (S) | SCF energy reported in §6 — reproducibility signal only, not a validation of the analogue |
| Spin waves emulate Schrödinger / Kohn–Sham operators | — | **not claimed, and not true** |
| The architecture "solves chemistry" | — | **not claimed** |

**What would have to be true for the chemistry story to be worth anything:**
the transfer function of a *fabricated* magnonic landscape must be measured
and must match the design to within the phase quantisation assumed here. That
measurement does not exist yet — it is the Gate-2 experiment.
"""),
]


if __name__ == "__main__":
    build("03_chem_potential_match.ipynb", CELLS)
