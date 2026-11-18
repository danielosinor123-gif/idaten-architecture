"""Time LogisticRegression settings on the real notebook-02 digital features."""
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

# run everything up to (not including) the cell that times out
for i, src in code_cells:
    if "DIGITAL baseline accuracy" in src:
        break
    exec(compile(src, f"<cell {i}>", "exec"), ns)

# build the digital features exactly as cell 9 does
from sklearn.linear_model import LogisticRegression
np = ns["np"]
h = ns["build_filters"](ns["K"], ns["F"], np.random.default_rng(7))
t0 = time.time()
Zdig = ns["conv_stack_digital"](ns["Xtr"], h)
Fdig = ns["pool_and_flat"](Zdig)
Fdig = (Fdig - Fdig.mean(0)) / (Fdig.std(0) + 1e-9)
Zte = ns["conv_stack_digital"](ns["Xte"], h)
Fte = ns["pool_and_flat"](Zte)
Fte = (Fte - Fdig.mean(0)) / (Fdig.std(0) + 1e-9)
print(f"features: train {Fdig.shape} test {Fte.shape}  build {time.time()-t0:.1f}s",
      flush=True)

ytr, yte = ns["ytr"], ns["yte"]
for mi, tol in [(2000, 1e-4), (500, 1e-3), (300, 1e-3), (200, 1e-3)]:
    t0 = time.time()
    clf = LogisticRegression(max_iter=mi, tol=tol)
    clf.fit(Fdig, ytr)
    dt = time.time() - t0
    acc = clf.score(Fte, yte)
    print(f"max_iter={mi} tol={tol:g}: {dt:.1f}s  n_iter_max={clf.n_iter_.max()}  "
          f"acc={acc:.4f}", flush=True)
