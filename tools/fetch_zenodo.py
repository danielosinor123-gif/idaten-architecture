"""Fetch only the simulation scripts from the Baumgaertl & Grundler Zenodo record.

The record ships one 1.66 GiB zip. We use HTTP range requests (remotezip) to
pull only the *.mx3 / *.py / *.txt members, which are a few MB.

Record : 10.5281/zenodo.7714181
Paper  : Baumgaertl & Grundler, Nat Commun 14, 1490 (2023)
Licence: CC-BY-4.0
"""
import io
import os
import sys
import json

URL = "https://zenodo.org/records/7714181/files/Data_Reversal_of_nanomagnets_by_propagating_magnons.zip?download=1"
OUT = sys.argv[1] if len(sys.argv) > 1 else "zenodo_baumgaertl"

from remotezip import RemoteZip

WANT_EXT = (".mx3", ".py")
MAX_MEMBER = 40 * 1024 * 1024

os.makedirs(OUT, exist_ok=True)
manifest = []

with RemoteZip(URL) as z:
    names = z.namelist()
    print(f"members in archive: {len(names)}")
    candidates = [n for n in names
                  if not n.endswith("/")
                  and os.path.splitext(n)[1].lower() in WANT_EXT]
    print(f"simulation-script members matching {WANT_EXT}: {len(candidates)}")
    for n in candidates:
        info = z.getinfo(n)
        if info.file_size > MAX_MEMBER:
            print(f"  skip (too large {info.file_size}): {n}")
            continue
        try:
            data = z.read(n)
        except Exception as e:
            print(f"  FAIL {n}: {e}")
            continue
        rel = n.replace("/", "__")
        if not rel.lower().endswith(WANT_EXT):
            rel += ".txt"
        dest = os.path.join(OUT, rel)
        with open(dest, "wb") as fh:
            fh.write(data)
        manifest.append({"member": n, "bytes": len(data), "saved_as": rel})
        print(f"  saved {rel}  ({len(data)} bytes)")

with open(os.path.join(OUT, "_manifest.json"), "w") as fh:
    json.dump({"source": URL, "doi": "10.5281/zenodo.7714181",
               "paper": "Baumgaertl & Grundler, Nat Commun 14, 1490 (2023)",
               "licence": "CC-BY-4.0", "members": manifest}, fh, indent=2)
print(f"\n{len(manifest)} members saved to {OUT}")
