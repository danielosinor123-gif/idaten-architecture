"""Profile notebook 02 code cells to find the cell that timed out.

Executes the code cells of tools/nb02_ai.py in order, timing each, and stops
after the DIGITAL-baseline cell (the one that hit the 1800 s timeout).
"""
import importlib.util
import os
import sys
import time

os.environ.setdefault("MPLBACKEND", "Agg")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

spec = importlib.util.spec_from_file_location("nb02", os.path.join(HERE, "nb02_ai.py"))
nb02 = importlib.util.module_from_spec(spec)
t0 = time.time()
spec.loader.exec_module(nb02)          # defines CELLS (and rewrites the .ipynb)
print(f"module load + notebook build: {time.time() - t0:.1f}s", flush=True)

ns = {"__name__": "__main__"}
for i, (kind, src) in enumerate(nb02.CELLS):
    if kind != "code":
        continue
    t0 = time.time()
    print(f"--- cell {i} start ---", flush=True)
    exec(compile(src, f"<cell {i}>", "exec"), ns)
    dt = time.time() - t0
    print(f"--- cell {i} done in {dt:.1f}s ---", flush=True)
    if "DIGITAL baseline accuracy" in src:
        print("reached the timing-out cell; stopping", flush=True)
        break
