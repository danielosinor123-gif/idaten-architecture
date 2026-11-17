"""Inspect the published phase-diagram arrays from Zenodo."""
import os, sys
import numpy as np

d = sys.argv[1]
for f in sorted(os.listdir(d)):
    if not f.endswith(".npy"):
        continue
    a = np.load(os.path.join(d, f), allow_pickle=True)
    print("=" * 72)
    print(f, "->", type(a), a.dtype, a.shape)
    if a.dtype == object:
        obj = a.item() if a.shape == () else a
        print("  object payload:", type(obj))
        if isinstance(obj, dict):
            for k, v in obj.items():
                arr = np.asarray(v)
                print(f"   {k!r}: shape={arr.shape} dtype={arr.dtype}")
                print("      ", np.array2string(arr.ravel()[:12], precision=6))
        else:
            print("  ", repr(obj)[:400])
    else:
        flat = a.ravel()
        print("  min", flat.min(), "max", flat.max())
        print("  ", np.array2string(flat[:24], precision=6))
        if a.ndim == 1 and a.size > 24:
            print("  ...", np.array2string(flat[-12:], precision=6))
