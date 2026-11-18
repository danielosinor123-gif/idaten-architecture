'''Fetch the MNIST IDX files into ``data/mnist/`` (cached, no dependencies beyond urllib).

    python tools/fetch_mnist.py

The four files are ~11.6 MB compressed. They are the standard MNIST training /
test set distributed under the MNIST licence (CC BY-SA 3.0, see
http://yann.lecun.com/exdb/mnist/).

If the network is unavailable, notebook 02 falls back to
``sklearn.datasets.load_digits`` (8x8, ~1800 samples) and says so in its output.
'''
import gzip
import os
import shutil
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "mnist")

BASE = "https://storage.googleapis.com/cvdf-datasets/mnist/"
FILES = {
    "train-images-idx3-ubyte.gz": "train-images-idx3-ubyte",
    "train-labels-idx1-ubyte.gz": "train-labels-idx1-ubyte",
    "t10k-images-idx3-ubyte.gz": "t10k-images-idx3-ubyte",
    "t10k-labels-idx1-ubyte.gz": "t10k-labels-idx1-ubyte",
}


def fetch(force=False):
    os.makedirs(OUT, exist_ok=True)
    ok = []
    for gz, raw in FILES.items():
        dest = os.path.join(OUT, raw)
        if os.path.exists(dest) and not force:
            ok.append(raw)
            continue
        url = BASE + gz
        try:
            print(f"  downloading {gz} ...", flush=True)
            with urllib.request.urlopen(url, timeout=60) as r:
                data = r.read()
            with gzip.GzipFile(fileobj=__import__("io").BytesIO(data)) as g:
                plain = g.read()
            with open(dest, "wb") as fh:
                fh.write(plain)
            ok.append(raw)
        except Exception as e:
            print(f"  FAILED {gz}: {type(e).__name__}: {e}")
    return ok


def load(split="train"):
    '''Return (images uint8 (N,28,28), labels uint8 (N,)).'''
    if split == "train":
        img_p = os.path.join(OUT, "train-images-idx3-ubyte")
        lbl_p = os.path.join(OUT, "train-labels-idx1-ubyte")
    else:
        img_p = os.path.join(OUT, "t10k-images-idx3-ubyte")
        lbl_p = os.path.join(OUT, "t10k-labels-idx1-ubyte")
    if not (os.path.exists(img_p) and os.path.exists(lbl_p)):
        raise FileNotFoundError("MNIST not present; run tools/fetch_mnist.py")

    with open(img_p, "rb") as fh:
        magic, n, r, c = __import__("struct").unpack(">IIII", fh.read(16))
        assert magic == 2051, f"bad magic {magic}"
        imgs = __import__("numpy").frombuffer(fh.read(), dtype="uint8").reshape(n, r, c)
    with open(lbl_p, "rb") as fh:
        magic, n = __import__("struct").unpack(">II", fh.read(8))
        assert magic == 2049, f"bad magic {magic}"
        lbls = __import__("numpy").frombuffer(fh.read(), dtype="uint8")
    return imgs, lbls


if __name__ == "__main__":
    got = fetch()
    print(f"{len(got)}/4 MNIST files present in {OUT}")
    if len(got) == 4:
        x, y = load("train")
        print("train:", x.shape, y.shape, "classes:", sorted(set(y.tolist())))
