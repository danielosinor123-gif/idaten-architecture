"""Build the repository notebooks from cell specs (so they are regenerable).

    python tools/build_notebooks.py

Each notebook is defined as a list of ("md" | "code", source) cells. The
built .ipynb files are the committed artifacts; this script is the source of
truth so that a notebook can be regenerated rather than hand-edited in JSON.
"""
from __future__ import annotations

import os
import sys

import nbformat as nbf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(ROOT, "notebooks")


def build(name, cells, kernel="python3"):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell(src) if kind == "md" else nbf.v4.new_code_cell(src)
        for kind, src in cells
    ]
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": kernel},
        "language_info": {"name": "python", "version": "3.13"},
    }
    os.makedirs(NB_DIR, exist_ok=True)
    path = os.path.join(NB_DIR, name)
    with open(path, "w", encoding="utf-8") as fh:
        nbf.write(nb, fh)
    print(f"wrote {path}  ({len(nb.cells)} cells)")
    return path


if __name__ == "__main__":
    print("This module defines the notebook builders; run the specific builder.")
