"""Probe: confirm the train/test standardization mismatch in notebook 02.

Reproduces the digital feature build exactly (deterministic), then scores the
head under (a) the notebook's current (buggy) test-path standardization and
(b) the corrected one (train stats applied to both splits).
"""
import importlib.util
import os
import sys
import time

os.environ.setdefault("MPLBACKEND", "Agg")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

spec = importlib.util.spec_from_file_location("nb02", os.path.join(HERE, "nb02_ai.py"))
nb02 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nb02)

ns = {"__name__": "__main__"}
code_cells = [(i, s) for i, (k, s) in enumerate(nb02.CELLS) if k == "code"]
for i, src in code_cells:
    if "DIGITAL baseline accuracy" in src:
        break
    exec(compile(src, f"<cell {i}>", "exec"), ns)

from sklearn.linear_model import LogisticRegression

np = ns["np"]
h = ns["build_filters"](ns["K"], ns["F"], np.random.default_rng(7))
t0 = time.time()
Fdig = ns["pool_and_flat"](ns["conv_stack_digital"](ns["Xtr"], h))
Fte = ns["pool_and_flat"](ns["conv_stack_digital"](ns["Xte"], h))
ytr, yte = ns["ytr"], ns["yte"]
print(f"features: train {Fdig.shape} test {Fte.shape}  build {time.time()-t0:.1f}s",
      flush=True)

# exactly what the notebook does now
Fdig_buggy = (Fdig - Fdig.mean(0)) / (Fdig.std(0) + 1e-9)
Fte_buggy = (Fte - Fdig_buggy.mean(0)) / (Fdig_buggy.std(0) + 1e-9)

# corrected: train stats captured before rebinding, applied to both splits
mu, sd = Fdig.mean(0), Fdig.std(0) + 1e-9
Fdig_fix = (Fdig - mu) / sd
Fte_fix = (Fte - mu) / sd

print(f"test feature scale: raw sd={Fte.std():.4f}  "
      f"buggy-path sd={Fte_buggy.std():.4f}  fixed-path sd={Fte_fix.std():.4f}",
      flush=True)

for name, Xtr_, Xte_ in (("BUGGY (as-is) ", Fdig_buggy, Fte_buggy),
                         ("FIXED         ", Fdig_fix, Fte_fix)):
    for mi, tol in ((500, 1e-3), (2000, 1e-4)):
        t0 = time.time()
        clf = LogisticRegression(max_iter=mi, tol=tol)
        clf.fit(Xtr_, ytr)
        acc = clf.score(Xte_, yte)
        print(f"{name} max_iter={mi} tol={tol:g}: {time.time()-t0:.1f}s "
              f"n_iter={clf.n_iter_.max()} acc={acc:.4f}", flush=True)
