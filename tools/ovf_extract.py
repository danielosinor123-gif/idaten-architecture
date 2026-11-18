"""OVF 2.0 reader for mumax3 output.

Supports both section types emitted by mumax3 3.12:
  * '# Begin: Data Binary 4'  -> 4-byte marker prefix, then float32 data
  * '# Begin: Data Text'      -> ASCII whitespace-separated floats

The data ordering is y-fastest, then x, then z, with 'valuedim' consecutive
components per mesh point (mumax3 convention). This is verified empirically
against the CPW launch mask in the structural probe.

Validated against real mumax3 3.12 output in Downloads/gdsii_run/ovf_samples/.
"""
import re
import numpy as np

_DATA_MARK = re.compile(rb"# Begin: Data (Binary \d+|Text)\n")
_END_MARK = re.compile(rb"# End: Data (Binary \d+|Text)")


def _hdr(raw: bytes) -> dict:
    end = raw.find(b"# End: Header")
    hdr = raw[:end].decode("latin-1")
    out = {}
    for line in hdr.splitlines():
        line = line.strip()
        if line.startswith("#"):
            line = line[1:].strip()
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if k in ("xnodes", "ynodes", "znodes", "valuedim", "valueunits", "Segment count"):
            try:
                out[k] = int(v)
            except ValueError:
                out[k] = v
        elif k in ("xmin", "xmax", "ymin", "ymax", "zmin", "zmax",
                   "xbase", "ybase", "zbase", "xstepsize", "ystepsize", "zstepsize"):
            out[k] = float(v)
        else:
            out[k] = v
    return out


def read_ovf(path, order="xyz"):
    """Return (header, field ndarray shaped (nz, ny, nx, valuedim), marker).

    order='xyz'  -> mumax3 native: x fastest, components consecutive.
    order='yxz'  -> alternative: y fastest (used only to test the convention).
    """
    raw = open(path, "rb").read()
    m = _DATA_MARK.search(raw)
    if not m:
        raise ValueError(f"{path}: no OVF data section")
    kind = m.group(1).decode()
    start = m.end()
    em = _END_MARK.search(raw, start)
    if not em:
        raise ValueError(f"{path}: no OVF end marker")
    payload = raw[start:em.start()]
    hdr = _hdr(raw)

    nx, ny, nz = hdr.get("xnodes", 0), hdr.get("ynodes", 0), hdr.get("znodes", 1)
    vd = hdr.get("valuedim", 1)
    ncell = nx * ny * nz

    marker = float("nan")
    if kind.startswith("Binary"):
        vals = np.frombuffer(payload, dtype="<f4", count=len(payload) // 4)
        marker = float(vals[0])
        vals = vals[1:]
        if vals.size != ncell * vd:
            raise ValueError(f"{path}: {vals.size} values != {ncell}x{vd}")
        if order == "xyz":
            arr = vals.reshape((nz, ny, nx, vd))
        else:
            arr = vals.reshape((nz, nx, ny, vd)).transpose(0, 2, 1, 3)
    else:
        txt = payload.decode("latin-1")
        vals = np.fromstring(txt, sep=" ") if hasattr(np, "fromstring") else None
        if vals is None or vals.size != ncell * vd:
            vals = np.array(txt.split(), dtype=np.float64)
        if vals.size != ncell * vd:
            raise ValueError(f"{path}: {vals.size} values != {ncell}x{vd}")
        if order == "xyz":
            arr = vals.reshape((nz, ny, nx, vd))
        else:
            arr = vals.reshape((nz, nx, ny, vd)).transpose(0, 2, 1, 3)
    return hdr, arr, marker


def grid_axes(path, order="xyz"):
    """Return (x_um, y_um, field(nz,ny,nx,vd), header) with x/y in micrometres."""
    hdr, arr, _ = read_ovf(path, order=order)
    nx, ny = hdr["xnodes"], hdr["ynodes"]
    x0 = hdr.get("xbase", hdr["xmin"] + hdr["xstepsize"] / 2)
    y0 = hdr.get("ybase", hdr["ymin"] + hdr["ystepsize"] / 2)
    x = (x0 + hdr["xstepsize"] * np.arange(nx)) * 1e6
    y = (y0 + hdr["ystepsize"] * np.arange(ny)) * 1e6
    return x, y, arr, hdr


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        for order in ("xyz", "yxz"):
            try:
                x, y, f, hdr = grid_axes(p, order=order)
            except Exception as e:
                print(p, order, "ERR", e)
                continue
            g0 = np.abs(np.diff(f[0, :, :, 0], axis=0)).mean()
            g1 = np.abs(np.diff(f[0, :, :, 0], axis=1)).mean()
            print(f"{p} order={order} shape={f.shape} mean|d|slow={g0:.4g} fast={g1:.4g}")
