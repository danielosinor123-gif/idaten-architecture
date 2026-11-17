"""Fetch the OVF / NPY members (drive files + simulation arrays) from Zenodo."""
import json, os, sys
from remotezip import RemoteZip

URL = "https://zenodo.org/records/7714181/files/Data_Reversal_of_nanomagnets_by_propagating_magnons.zip?download=1"
OUT = sys.argv[1]
WANT = (".ovf", ".npy")
os.makedirs(OUT, exist_ok=True)
man = []
with RemoteZip(URL) as z:
    for i in z.infolist():
        if i.filename.endswith("/"):
            continue
        if os.path.splitext(i.filename)[1].lower() not in WANT:
            continue
        data = z.read(i.filename)
        rel = i.filename.replace("/", "__")
        with open(os.path.join(OUT, rel), "wb") as fh:
            fh.write(data)
        man.append({"member": i.filename, "bytes": len(data), "saved_as": rel})
        print(f"  saved {rel} ({len(data)} bytes)")
with open(os.path.join(OUT, "_ovf_manifest.json"), "w") as fh:
    json.dump({"source": URL, "doi": "10.5281/zenodo.7714181",
               "licence": "CC-BY-4.0", "members": man}, fh, indent=2)
print(f"{len(man)} members saved")
