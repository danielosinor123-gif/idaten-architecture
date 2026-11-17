'''Build the committed lab-archive summary from the raw archiver output.

    python tools/build_lab_summary.py [--raw data/lab/_summary_raw.json]

Writes:
  data/lab/_summary.json   the filtered per-deck archive records (S)
  data/lab/profiles.csv    one flat row per deck, for quick reading

The raw archiver output (`_summary_raw.json`) is produced by
`tools/archive_lab2.py` in the mumax3 work directory. The bulk `.npz`
snapshot archives stay out of git (see .gitignore); only the metadata and the
fit metrics are committed, because those are the evidence.

Decks belonging to the PREVIOUS chip are filtered out here: they are not part
of this project's evidence.
'''
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAB = os.path.join(ROOT, "data", "lab")

# Decks that are NOT part of the Idaten evidence base are simply not kept:
# the committed summary lists only the material series below. This keeps the
# prior programme's diagnostics out of the public repository without naming
# them here.
KEEP_PREFIX = ("YIG_", "BiYIG_", "Co25Fe75_", "GdFeCoP_", "NiFe_")


def main(raw_path=None):
    raw_path = raw_path
    if not raw_path:
        raw_path = os.environ.get("LAB_RAW_SUMMARY", "")
    if not raw_path or not os.path.exists(raw_path):
        print("raw archive summary not found.")
        print("Point --raw at the archiver output (_summary.json from tools/archive_lab2.py).")
        print("The raw file is kept outside the repository because it can contain")
        print("prior-project deck text; only the filtered summary is committed.")
        return 1

    with open(raw_path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    keep, dropped = {}, []
    for name, rec in raw.items():
        if not name.startswith(KEEP_PREFIX):
            dropped.append(name)
            continue
        keep[name] = rec

    out_json = os.path.join(LAB, "_summary.json")
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(keep, fh, indent=1, sort_keys=True)

    rows = []
    for name, rec in sorted(keep.items()):
        met = rec.get("metrics", {})
        deck = rec.get("deck", {})
        rows.append({
            "deck": name,
            "snapshots": rec.get("snapshots", 0),
            "bad_files": len(rec.get("bad_files", []) or []),
            "Msat_A_per_m": deck.get("Msat", ""),
            "Aex_J_per_m": deck.get("Aex", ""),
            "alpha": deck.get("alpha", ""),
            "f0_Hz": deck.get("f0_Hz", ""),
            "B_ext": deck.get("B_ext", ""),
            "ell_rms_x10_45_um": met.get("ell_rms_x10_45_um", ""),
            "r2_rms_x10_45": met.get("r2_rms_x10_45", ""),
            "r2_rms_x5_45": met.get("r2_rms_x5_45", ""),
            "r2_rms_x15_45": met.get("r2_rms_x15_45", ""),
            "r2_rms_localpeak_x10_45": met.get("r2_rms_localpeak_x10_45", ""),
            "r2_peak_x10_45": met.get("r2_peak_x10_45", ""),
            "contrast_peak_to_valley": met.get("contrast_peak_to_valley", ""),
            "node_x_um": met.get("node_x_um", ""),
            "antinode_x_um": met.get("antinode_x_um", ""),
            "dt_snapshot_ns": met.get("dt_snapshot_ns", ""),
            "t_first_ns": met.get("t_first_ns", ""),
            "t_last_ns": met.get("t_last_ns", ""),
            "archive_MB": rec.get("archive_MB", ""),
            "seconds": rec.get("seconds", ""),
        })

    out_csv = os.path.join(LAB, "profiles.csv")
    with open(out_csv, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["deck"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    total_snap = sum(r["snapshots"] for r in rows)
    print(f"kept {len(rows)} deck(s), {total_snap} snapshots")
    if dropped:
        print(f"dropped {len(dropped)} non-Idaten deck(s): {', '.join(sorted(dropped))}")
    print(f"wrote {os.path.relpath(out_json, ROOT)}")
    print(f"wrote {os.path.relpath(out_csv, ROOT)}")

    # Report the fit quality gate (K4) inline.
    r2s = [float(r["r2_rms_x10_45"]) for r in rows
           if r["r2_rms_x10_45"] not in ("", None)
           and str(r["r2_rms_x10_45"]) not in ("inf", "-inf", "nan")]
    if r2s:
        print(f"\nK4 fit-quality check on r2_rms_x10_45: "
              f"min={min(r2s):.6f} max={max(r2s):.6f} "
              f"(gate requires >= 0.8 on a stated window)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
