"""Execute every notebook in notebooks/ and report pass/fail per cell.

    python tools/run_notebooks.py [--notebook 03_chem_potential_match.ipynb]

Executed notebooks are written back in place with their outputs, so the
committed .ipynb files carry the evidence of the run, not just the code.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import traceback

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(ROOT, "notebooks")


def run_one(path):
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=1800, kernel_name="python3",
                            allow_errors=False, resources={"metadata": {"path": ROOT}})
    t0 = time.time()
    try:
        client.execute()
    except CellExecutionError as e:
        print(f"FAIL  {os.path.basename(path)}: {e}")
        # find the offending cell
        for i, c in enumerate(nb.cells):
            for o in c.get("outputs", []):
                if o.get("output_type") == "error":
                    print(f"      cell {i} ({c.cell_type}) -> {o.get('ename')}: {o.get('evalue')}")
                    for ln in (o.get("traceback") or [])[-12:]:
                        print("      " + ln.replace("\n", "\n      "))
                    break
        return False, time.time() - t0
    except Exception:
        traceback.print_exc()
        return False, time.time() - t0
    nbformat.write(nb, path)
    print(f"PASS  {os.path.basename(path)}  ({time.time()-t0:.1f}s)")
    return True, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notebook", action="append", default=None)
    args = ap.parse_args()

    names = args.notebook or sorted(
        f for f in os.listdir(NB_DIR) if f.endswith(".ipynb"))
    results = []
    for n in names:
        p = os.path.join(NB_DIR, n)
        ok, dt = run_one(p)
        results.append((n, ok, dt))

    print("\n" + "=" * 58)
    all_ok = True
    for n, ok, dt in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {n:<40} {dt:7.1f}s")
        all_ok &= ok
    print("=" * 58)
    print("ALL PASS" if all_ok else "FAILURES PRESENT")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
