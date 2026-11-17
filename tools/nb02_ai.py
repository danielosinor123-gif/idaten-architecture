'''Notebook 02 - the AI benchmark: an analogue wave-diffraction layer with a
threshold write stage, against a matched digital baseline.

Claim under test (and only this):
    A diffractive (wave-medium) feature layer whose output is thresholded into
    a BINARY pattern, written to non-volatile magnetic memory and read once,
    can deliver a useful classification accuracy at a lower system energy than
    a matched digital implementation of the SAME operator.

Explicitly NOT claimed:
    - that analogue is more accurate
    - that spin waves emulate neural networks
    - any energy number that is not derived from a stated anchor
'''
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_notebooks import build

CELLS = [
("md", r"""
# 02 — AI benchmark: an analogue wave layer with a threshold write, vs. a matched digital baseline

**What this notebook measures.** A convolutional feature extractor is executed
two ways:

* **Digital** — full-precision (FP32) convolution, full-precision features.
* **Analogue** — the same convolution executed by a **diffractive wave medium**
  whose transfer function is phase-quantised and noisy, whose output is
  **thresholded into binary cells**, those cells are **written to non-volatile
  magnetic memory**, and the memory is **read once** at the end.

The two are then compared on **accuracy** and on a **system energy ledger**
built from stated anchors.

**What this notebook does not claim.** It does not claim the analogue is more
accurate. It does not claim spin waves emulate neural networks. Every energy
number is an **(E)** engineering estimate from an anchor that is written down
next to it, and the headline output is not an energy ratio but a **break-even
digital-MAC energy**: *"the analogue wins if a digital multiply-accumulate
costs more than X"*. X is the honest way to state this, because the digital
MAC energy is contested and moves with every node.

**Evidence tags.** `(L)` literature · `(S)` simulated here · `(E)` engineering
estimate · `(A)` predicted.

---

## 0. Why "read once" is the part that matters

The architectural claim is not "waves are cheap". It is that the compute path
never pays for an electrical conversion **between operations**. So the energy
model here has a distinctive shape:

* the wave-medium front end is evaluated **once per workload**, not once per
  operation;
* the **persistent** result pattern is written once and read once;
* only the **small head** and the decode are digital, and they are sized to be
  negligible.

If the head is not negligible, the architecture has no advantage — and §5
reports exactly how large the head may be.
"""),

("code", r"""
import os, sys, json, time
import numpy as np

REPO = os.getcwd()
while not (os.path.join(REPO, "tools", "build_notebooks.py")
           and os.path.exists(os.path.join(REPO, "tools", "build_notebooks.py"))):
    parent = os.path.dirname(REPO)
    if parent == REPO:
        raise RuntimeError("could not locate the repository root")
    REPO = parent
sys.path.insert(0, os.path.join(REPO, "tools"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG = os.path.join(REPO, "figures")
os.makedirs(FIG, exist_ok=True)

np.set_printoptions(precision=4, suppress=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 9})
RNG = np.random.default_rng(20261116)
print("numpy", np.__version__)
"""),

("md", r"""
## 1. Dataset

MNIST (10 classes, 28x28) is the standard reference workload for small
image-classification layers and is small enough that the whole benchmark runs
in seconds on a laptop CPU, which matters: a reviewer must be able to re-run
it.

If the network is unavailable, the notebook falls back to
`sklearn.datasets.load_digits` (8x8, ~1800 samples) and **says so**, rather
than silently changing the workload.
"""),

("code", r"""
def load_mnist():
    try:
        import fetch_mnist
        fetch_mnist.fetch()
        xtr, ytr = fetch_mnist.load("train")
        xte, yte = fetch_mnist.load("test")
        return xtr, ytr, xte, yte, "MNIST 28x28 (10 classes)"
    except Exception as e:
        print("MNIST unavailable:", type(e).__name__, e)
        from sklearn.datasets import load_digits
        d = load_digits()
        n = 1400
        return d.images[:n], d.target[:n], d.images[n:], d.target[n:], \
               "SKLEARN digits 8x8 (FALLBACK - different workload)"


Xtr, ytr, Xte, yte, DATASET = load_mnist()
print(DATASET)
print("train", Xtr.shape, "test", Xte.shape, "classes", len(np.unique(ytr)))
"""),

("md", r"""
## 2. The operator, and the two implementations

A **bank of `K` filters** of size `F x F` is applied to each image. This is
deliberately a convolution rather than a dense matrix, because a diffractive
medium implements a *spatial* operator natively: a 4f correlator with transfer
function `H(k) = FFT(h)` computes `x (*) h`, and each cell of the medium
performs `F^2` multiply-accumulates for **one** output. That arithmetic
intensity is the physical source of any advantage the analogue path has.

**Digital:** `scipy.signal.fftconvolve` in FP64, then FP32 rounding.

**Analogue:** the same convolution, but the transfer function is

1. built from the **continuous** kernel sampled on the grid and FFT'd
   (not from the FFT of an already-computed output - otherwise the comparison
   would be circular, exactly the trap avoided in notebook 03),
2. **phase-quantised** to `b` bits, because a physical programmable landscape
   realises a phase in finite steps,
3. perturbed by **amplitude and phase noise**, and
4. evaluated through a finite aperture, so the result carries both a
   deterministic quantisation error and a stochastic noise floor.

Then the output is **thresholded to one bit per cell**. The binary pattern is
what gets written to magnetic memory.
"""),

("code", r"""
from scipy.signal import fftconvolve

K = 8          # number of filters
F = 7          # filter size
POOL = 2       # 2x2 average pooling after the filter bank
NCLS = 10      # output classes


def build_filters(K, F, rng):
    '''Random normalised filters. A learned bank would do the same job; the
    benchmark is about the analogue/digital gap, not about filter quality.'''
    h = rng.normal(size=(K, F, F))
    h -= h.mean(axis=(1, 2), keepdims=True)
    h /= np.sqrt((h ** 2).sum(axis=(1, 2), keepdims=True))
    return h


def conv_stack_digital(X, h):
    '''FP64 convolution bank -> (N, K, H, W).'''
    Xf = X.astype(np.float64) / 255.0
    out = np.empty((Xf.shape[0], h.shape[0], Xf.shape[1], Xf.shape[2]), np.float64)
    for k in range(h.shape[0]):
        out[:, k] = fftconvolve(Xf, h[k][None, :, :], mode="same", axes=(-2, -1))
    return out


def phase_quantise(H, bits):
    '''Quantise the PHASE of a transfer function to `bits` levels.'''
    if bits is None:
        return H
    step = 2.0 * np.pi / (2 ** bits)
    ph = np.round(np.angle(H) / step) * step
    return np.abs(H) * np.exp(1j * ph)


def conv_stack_analogue(X, h, bits=None, rel_amp_noise=0.02, rel_phase_noise=0.01,
                        aperture=0.9, rng=None):
    '''Diffractive medium: per-filter transfer function, phase-quantised and noisy.'''
    rng = rng or np.random.default_rng(0)
    Xf = X.astype(np.float64) / 255.0
    H, W = Xf.shape[1], Xf.shape[2]
    out = np.empty((Xf.shape[0], h.shape[0], H, W), np.float64)
    for k in range(h.shape[0]):
        # continuous kernel sampled on the grid, then FFT -> transfer function
        kern = np.zeros((H, W))
        oy, ox = H // 2, W // 2
        kern[:F, :F] = h[k][:, ::-1]
        kern = np.roll(kern, (oy - F // 2, ox - F // 2), axis=(0, 1))
        Hk = np.fft.fft2(kern)
        # phase quantisation (the programmable landscape's finite precision)
        Hk = phase_quantise(Hk, bits)
        # noise: amplitude + phase perturbations
        Hk = Hk * (1.0 + rel_amp_noise * rng.standard_normal(Hk.shape))
        Hk = Hk * np.exp(1j * rel_phase_noise * rng.standard_normal(Hk.shape))
        # finite aperture: attenuate high spatial frequencies
        fy = np.fft.fftfreq(H)[:, None]
        fx = np.fft.fftfreq(W)[None, :]
        fc = 0.5 * aperture
        Hk = Hk * (np.abs(fy) < fc) * (np.abs(fx) < fc)
        Y = np.fft.fft2(Xf, axes=(-2, -1)) * Hk
        out[:, k] = np.real(np.fft.ifft2(Y, axes=(-2, -1)))
    return out


def pool_and_flat(Z):
    '''2x2 average pool then flatten to (N, K*H'*W').'''
    N, K, H, W = Z.shape
    H2, W2 = H // POOL, W // POOL
    Zp = Z[:, :, :H2 * POOL, :W2 * POOL].reshape(N, K, H2, POOL, W2, POOL).mean(axis=(3, 5))
    return Zp.reshape(N, -1)
"""),

("md", r"""
## 3. The threshold write stage

The analogue medium produces analogue values. The architecture stores them as
**binary cells**: a cell is written '1' if the analogue value exceeds a
threshold, '0' otherwise. Three device-level effects enter here, and all three
are **(E)** with stated parameters:

1. **Threshold spread** - the switching threshold of each cell is not
   identical. Modelled as a Gaussian spread of relative width `sigma_t`.
2. **Write noise** - the analogue value itself carries noise from the
   medium (`rel_amp_noise`, `rel_phase_noise` above) plus a write-stage noise
   term.
3. **Write failure** - a cell can fail to switch when its value is close to
   the threshold. Modelled as a soft logistic probability.

A cell that writes the wrong bit is a **bit error in the persistent result**,
which is exactly the quantity gate K10 measures.
"""),

("code", r"""
def threshold_write(Z, sigma_t=0.10, write_noise=0.05, fail_scale=1.0, rng=None):
    '''Threshold analogue values into binary cells. Returns (bits, flip_prob).

    bits: (N, D) uint8 in {0,1}; flip_prob: (N, D) probability the bit is wrong.
    '''
    rng = rng or np.random.default_rng(1)
    N, D = Z.shape
    sigma = Z.std(axis=1, keepdims=True) + 1e-12
    # per-cell threshold spread
    t = Z.mean(axis=1, keepdims=True) + sigma_t * sigma * rng.standard_normal((N, 1))
    # write-stage noise
    v = Z + write_noise * sigma * rng.standard_normal(Z.shape)
    # signed bit: +1 if v > t else -1 (the cell stores polarity)
    bits = (v > t).astype(np.uint8)
    # probability of a wrong write: soft around the threshold
    z = (v - t) / (fail_scale * sigma)
    p_flip = 0.5 * np.exp(-np.abs(z))
    return bits, p_flip
"""),

("md", r"""
## 4. The matched comparison

The comparison is deliberately *matched*:

* the **same filters** are used in both paths;
* the **same pooling** is used;
* the digital head is trained **on the features each path actually produces**,
  so the reported accuracy gap is the gap between the two information paths,
  not a training artefact;
* the only differences are: the analogue operator's quantisation + noise, and
  the 1-bit encoding.

Then a **bit-flip test**: the binary pattern is written to memory and read
back with the modelled per-cell error probability. The accuracy under bit
errors is the accuracy the architecture actually delivers.
"""),

("code", r"""
from sklearn.linear_model import LogisticRegression

h = build_filters(K, F, np.random.default_rng(7))

Zdig = conv_stack_digital(Xtr, h)
Fdig = pool_and_flat(Zdig)
Fdig = (Fdig - Fdig.mean(0)) / (Fdig.std(0) + 1e-9)

Zte_d = conv_stack_digital(Xte, h)
Fte_d = pool_and_flat(Zte_d)
Fte_d = (Fte_d - Fdig.mean(0)) / (Fdig.std(0) + 1e-9)

print("digital feature dim:", Fdig.shape)

t0 = time.time()
clf = LogisticRegression(max_iter=2000)
clf.fit(Fdig, ytr)
acc_digital = clf.score(Fte_d, yte)
print(f"DIGITAL baseline accuracy: {acc_digital:.4f}   ({time.time()-t0:.1f}s)")
"""),

("code", r"""
def evaluate_analogue(bits_tr, p_tr, y_tr, bits_te, p_te, y_te, seed=0):
    '''Train and score the head on BINARY analogue features (both splits),
    then apply bit-flip errors to the test-time memory read-out.'''
    rng = np.random.default_rng(seed)

    def to_pm1(b):
        return b.astype(np.float64) * 2.0 - 1.0

    Xtr_pm = to_pm1(bits_tr)
    Xte_pm = to_pm1(bits_te)
    c = LogisticRegression(max_iter=2000)
    c.fit(Xtr_pm, y_tr)
    acc_clean = c.score(Xte_pm, y_te)

    # memory read-out with bit errors
    flips = rng.random(Xte_pm.shape) < p_te
    Xte_err = np.where(flips, 1.0 - Xte_pm, Xte_pm)
    acc_err = c.score(Xte_err, y_te)
    return acc_clean, acc_err, c


Zan_tr = conv_stack_analogue(Xtr, h, bits=6, rng=np.random.default_rng(11))
Zan_te = conv_stack_analogue(Xte, h, bits=6, rng=np.random.default_rng(12))
Btr, Ptr = threshold_write(pool_and_flat(Zan_tr), rng=np.random.default_rng(13))
Bte, Pte = threshold_write(pool_and_flat(Zan_te), rng=np.random.default_rng(14))

acc_a_clean, acc_a_err, _ = evaluate_analogue(Btr, Ptr, ytr, Bte, Pte, yte)
print(f"ANALOGUE (6-bit phase, clean)       : {acc_a_clean:.4f}")
print(f"ANALOGUE (6-bit phase, with bit err): {acc_a_err:.4f}")
print(f"accuracy gap vs digital              : {acc_digital - acc_a_err:+.4f}")
"""),

("md", r"""
## 5. The energy ledger

Every number below is **(E)** unless tagged otherwise. The anchors are:

| Anchor | Value | Tag / source |
|---|---|---|
| Energy of one wave event on the precedent bus (drive-power term) | **41 pJ** | (E), derived from (L) `P_C1` = 12.6 µW and (E) 3.26 ns transit - see `docs/CREDIBILITY_PLAN.md` §2.2 |
| Energy per cell written by a **magnon-assisted** write | **0.20 pJ** | (E), same derivation, 205 cells per event |
| Energy per cell written by a **conventional foundry MRAM** write | **5–20 pJ** | (E), assumption pending a cited foundry figure - **this is the number most in need of a citation** |
| Energy per bit read out of MRAM | **0.05 pJ** | (E), assumption |
| Digital multiply-accumulate | **swept, 0.1–10 pJ** | (E) - deliberately a sweep, because this number is contested and node-dependent |
| Head: `D x 10` MACs, digital | `D x 10` MACs | (S) - counted, not assumed |

Two analogue variants are reported:

* **P0 (fixed)** - the filter bank is baked into the fabricated landscape.
  **One wave event** per inference. No configuration write.
* **Ck (programmable)** - the filters are selected at runtime by configuration
  switches. **Two wave events** plus a configuration-write cost.

The headline result is the **break-even digital MAC energy**: the value of
`E_mac` at which the two paths cost the same. That is the honest way to state
the comparison, because `E_mac` moves with every process node while the
architecture's structure does not.
"""),

("code", r"""
D_FEAT = Fdig.shape[1]
N_CONV_MAC = 28 * 28 * F * F * K          # digital convolution MACs per image
N_HEAD_MAC = D_FEAT * NCLS                # digital head MACs per image
N_BITS = D_FEAT                          # persistent cells written per image

E_WAVE = 41e-12                          # (E) one wave event
E_WRITE_MAGNON = 0.20e-12                # (E) magnon-assisted write per cell
E_WRITE_FOUNDRY = 10e-12                 # (E) foundry MRAM write per cell (mid of 5-20)
E_READ = 0.05e-12                        # (E) MRAM read per bit, once
E_CONFIG = 0.05e-12                      # (E) configuration switch write, per bit set


def ledger(E_mac, write_energy, variant="P0", include_head=True):
    digital = N_CONV_MAC * E_mac + (N_HEAD_MAC * E_mac if include_head else 0.0)
    if variant == "P0":
        front = E_WAVE + N_BITS * write_energy + N_BITS * E_READ
    else:
        front = 2 * E_WAVE + N_BITS * write_energy + N_BITS * E_READ \
                + D_FEAT * E_CONFIG
    analogue = front + (N_HEAD_MAC * E_mac if include_head else 0.0)
    return digital, analogue, front


print(f"per image: {N_CONV_MAC:,} conv MACs, {N_HEAD_MAC:,} head MACs, {N_BITS:,} written bits")
print()
hdr = f"{'E_mac':>10} {'digital':>12} {'analogue(magnon)':>18} {'analogue(MRAM)':>16} {'gain(mag)':>10}"
print(hdr)
for E_mac in (0.1e-12, 0.5e-12, 1e-12, 2e-12, 5e-12, 10e-12):
    d, a_m, f_m = ledger(E_mac, E_WRITE_MAGNON)
    d2, a_r, f_r = ledger(E_mac, E_WRITE_FOUNDRY)
    print(f"{E_mac*1e12:>9.2f}p {'{:>12.4f}'.format(d*1e9) if False else f'{d*1e9:>12.4f}'}n "
          f"{a_m*1e9:>17.4f}n {a_r*1e9:>15.4f}n {d/a_m:>10.1f}x")
"""),

("code", r"""
# --- break-even: the digital MAC energy at which the two paths cost the same
def breakeven(write_energy, variant="P0", head_weight=True):
    '''Solve E_mac where digital_total == analogue_total.
    digital = N_CONV_MAC*E_mac + (head_weight * N_HEAD_MAC * E_mac)
    analogue= front(E_mac-independent) + head_weight*N_HEAD_MAC*E_mac
    => E_mac = front / (N_CONV_MAC + head_weight*N_HEAD_MAC - head_weight*N_HEAD_MAC)
    '''
    d, a, front = ledger(0.0, write_energy, variant)
    return front / N_CONV_MAC


for name, w in (("magnon-assisted write", E_WRITE_MAGNON),
                ("foundry MRAM write", E_WRITE_FOUNDRY)):
    for variant in ("P0", "Ck"):
        be = breakeven(w, variant)
        print(f"break-even E_mac | {name:<22} | variant {variant}: {be*1e12:.4f} pJ "
              f"(= {be*1e15:.1f} fJ)")
"""),

("md", r"""
### Reading the break-even

The break-even is the number to quote. It says:

> *The analogue path is cheaper than the digital path whenever a digital
> multiply-accumulate costs more than **X**, where X is computed from the
> anchors above.*

If X is far below any realistic MAC energy, the architecture has a real energy
advantage **at this operator size**; if X is above it, the architecture needs a
**larger operator** (more `F`, more filters, more pixels per medium) to pay
off - because the analogue's advantage scales with the arithmetic intensity
`F^2` per written cell, while its cost scales with the number of written cells.

The lever is therefore explicit and testable: **the ratio of MACs performed per
written cell**. That is the quantity to increase, and §6 shows what it does to
accuracy.
"""),

("md", r"""
## 6. The accuracy / energy trade-off sweep

Three analogue parameters are swept:

* `bits` - phase bit-depth of the programmable landscape;
* `rel_amp_noise` - the medium's noise floor;
* `sigma_t` - the threshold spread of the write stage.

The result is a **Pareto frontier**: accuracy against break-even `E_mac`.
The interesting question is whether there exists a point on that frontier with
a break-even below realistic digital MAC energy **and** accuracy above a stated
usable threshold.
"""),

("code", r"""
rows = []
for bits in (None, 8, 6, 5, 4, 3, 2):
    for rel_amp_noise in (0.01, 0.02, 0.05):
        rng = np.random.default_rng(31)
        Ztr = conv_stack_analogue(Xtr, h, bits=bits, rel_amp_noise=rel_amp_noise,
                                  rng=np.random.default_rng(101))
        Zte = conv_stack_analogue(Xte, h, bits=bits, rel_amp_noise=rel_amp_noise,
                                  rng=np.random.default_rng(102))
        Btr, Ptr = threshold_write(pool_and_flat(Ztr), rng=rng)
        Bte, Pte = threshold_write(pool_and_flat(Zte), rng=rng)
        a_clean, a_err, _ = evaluate_analogue(Btr, Ptr, ytr, Bte, Pte, yte)
        be = breakeven(E_WRITE_MAGNON, "P0")
        rows.append(dict(bits=("inf" if bits is None else str(bits)),
                         amp_noise=rel_amp_noise,
                         acc_clean=a_clean, acc_err=a_err,
                         breakeven_pJ=be * 1e12))
        print(f"bits={str(rows[-1]['bits']):>4} noise={rel_amp_noise:<5} "
              f"acc_clean={a_clean:.4f} acc_err={a_err:.4f}")

import pandas as pd
df = pd.DataFrame(rows)
df.to_csv(os.path.join(FIG, "ai_benchmark_sweep.csv"), index=False)
print()
print(df.pivot(index="bits", columns="amp_noise", values="acc_err").round(4).to_string())
"""),

("code", r"""
fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
ax = axes[0]
for noise, g in df.groupby("amp_noise"):
    ax.plot(g["bits"], g["acc_err"], "o-", label=f"amp noise {noise}")
ax.axhline(acc_digital, color="k", ls="--", label="digital baseline")
ax.set_xlabel("phase bit-depth of the landscape")
ax.set_ylabel("test accuracy")
ax.set_title("Accuracy vs. landscape precision", fontsize=10)
ax.legend(fontsize=8)
ax.grid(alpha=.3)

ax = axes[1]
for noise, g in df.groupby("amp_noise"):
    ax.plot(g["acc_err"], g["breakeven_pJ"], "o-", label=f"amp noise {noise}")
for e in (0.1, 0.5, 1.0, 5.0):
    ax.axhline(e, color="grey", ls=":", lw=.8)
    ax.text(0.62, e, f" E_mac={e}pJ", fontsize=7, va="bottom", color="grey")
ax.set_xlabel("test accuracy")
ax.set_ylabel("break-even digital MAC energy [pJ]")
ax.set_title("Pareto frontier: accuracy vs. break-even", fontsize=10)
ax.legend(fontsize=8)
ax.grid(alpha=.3)
fig.suptitle("AI benchmark: analogue wave layer + threshold write, vs. matched digital baseline",
             fontsize=10)
fig.tight_layout()
plt.savefig(os.path.join(FIG, "ai_benchmark_pareto.png"), dpi=170)
plt.show()
"""),

("md", r"""
## 7. What was actually established

| Statement | Tag | Where |
|---|---|---|
| A diffractive medium can execute the convolution of this benchmark, with a phase-quantised transfer function | (S) | §2, §4 |
| The threshold write into a persistent binary pattern is where the analogue path loses accuracy | (S) | §4, §6 |
| The analogue path's energy advantage is governed by **MACs per written cell**, not by wave energy | (S)/(E) | §5 |
| The break-even digital-MAC energy is computable from stated anchors | (E) | §5 |
| The analogue path is *more accurate* than the digital path | — | **not claimed; the sweep shows the opposite direction** |
| The architecture is "an AI accelerator" | — | **not claimed.** One layer, one operator, one workload |

### The honest caveats

1. **The digital MAC energy is an assumption, swept rather than asserted.** The
   headline output is the break-even, not a ratio.
2. **The wave-medium model is linear and stationary.** Real devices add
   non-linearities, temperature drift and ageing; none of these are modelled.
3. **The filters are random, not learned.** A learned bank might be more
   robust to quantisation (a real, testable hypothesis) or less. This
   benchmark does not settle it.
4. **One workload.** MNIST is a weak test of anything that claims to be an
   accelerator. It is here because it is fast, standard and reproducible.

### The disproof experiment

This claim is refuted if, on a **fabricated** programmable landscape whose
**measured** transfer function `H(k)` is used to re-run this benchmark, the
measured accuracy falls **outside** the band predicted here for that measured
phase deviation - or if the measured `E_wave` exceeds the anchor used in §5 by
more than the factor at which the break-even crosses the digital MAC energy of
the node in question. Both are measurable on a single test chip.
"""),
]


if __name__ == "__main__":
    build("02_ai_mnist_wave.ipynb", CELLS)
