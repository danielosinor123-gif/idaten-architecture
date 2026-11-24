# Outreach and visibility plan ($0 budget)

Everything below uses free/open channels only. Status column is updated as
items land. The repo already carries the audience routing in `README.md`,
the one-pager (`docs/ONE_PAGER.md`), the disproof gates
(`docs/KILL_CRITERIA.md`), and the full evidence ledger (`PROVENANCE.md`).

## Tier 1 — make it citable and indexed (highest credibility per hour)

| # | Action | How | Status |
|---|---|---|---|
| 1 | Release tag `v0.1.0` on GitHub | `git tag v0.1.0 && gh release create v0.1.0` | done 2026-11-19 |
| 2 | `CITATION.cff` | committed at repo root → GitHub shows a "Cite this repository" button | done 2026-11-19 |
| 3 | **Zenodo DOI**: connect the GitHub repo to Zenodo (Settings → GitHub → add repository, 3 clicks, OAuth in browser). Every release then gets a free DOI — this is what makes the repo citable in papers | zenodo.org → user action | TODO (browser) |
| 4 | **arXiv preprint** of the revised paper `docs/idaten-ce100-architecture-paper-rev-2026-11-24.md` (rev 2026-11-24) + evidence summary, cross-listed `cond-mat.mes-hall` (physics) — the channel spintronics professors actually read | build PDF from the markdown (PyPI `fpdf2`/`reportlab` or pandoc if available), submit at arxiv.org (free) | TODO |
| 5 | Enable GitHub Discussions as the public Q&A door | `gh api` (done 2026-11-19) + issue templates `claims_and_repro.yml` | done 2026-11-19 |
| 6 | Make the Kaggle kernels + datasets **public** so the (S) runs are clickable evidence: `danielvking/idaten-stage-a-mumax`, `danielvking/idaten-stage-c-mumax`, `danielvking/idaten-hematite-mumaxplus`, `danielvking/idaten-hematite-mumax-af-bus` (+ asset datasets `idaten-stagea-assets`, `idaten-stagec-assets`, `idaten-hematite-assets`) | Kaggle API `update_dataset_metadata` with `is_private=false` (kagglesdk; the CLI `datasets metadata --update` accepted the file but did not flip the flag — verified via `get_dataset`) | done 2026-11-24, all 4 kernels + 3 datasets verified `is_private: False` |
| 7 | Revised paper **rev 2026-11-24** (evidence revision: new §2A, §8 gate-status note, Appendix A evidence ledger A1–A15) at `docs/idaten-ce100-architecture-paper-rev-2026-11-24.md`; rev 2026-11-16 paper kept unchanged at `docs/idaten-ce100-architecture-paper.md` | commit to `main` | done 2026-11-24 |

## Tier 2 — real silicon and real labs (free paths to "make it real")

| # | Action | Notes |
|---|---|---|
| 8 | **SkyWater open MPW shuttle**: submit the ORFS/sky130hd digital tier (`gds/idaten_sky130/6_final.gds`, DRC 0, 140.87 MHz Fmax) to a free open-PDK shuttle (efabless chipIgnite / Google-sponsored MPW runs accept open-source sky130 designs at no cost). First add the shuttle's required padframe/IO — tracked as a good-first-issue in `CONTRIBUTING.md` | Makes the *digital* tier silicon-bound. The magnonic die stays a **concept mask — no PDK exists for hematite/LiNbO₃ patterning**, and the repo says so explicitly |
| 9 | **Ask the cited groups to reproduce the kill criteria on their own GPUs** (email templates below): the 2023 Nat. Commun. group (Stage A deck is *their* deck — trivial for them), the hematite PRM group (Stage D gap match 12.97 vs 12.78 GHz (S)/(E)), IMEC-class SOT-MRAM teams ("write your MRAM array with a wave, not a current") | Reproductions by independent groups are the strongest (S) upgrade available at $0 |
| 10 | **University cleanroom collaboration** for the first fabricated device: YIG + NiFe exactly as the published precedent (standard films), hematite only when a lab with α-Fe₂O₃ growth takes it | YIG first; hematite is the follow-up |
| 11 | **Accelerator applications** (free to apply): Silicon Catalyst (semiconductor), plus imec.xpand / IC-link style programs for foundry access | Application is free; use `docs/ONE_PAGER.md` + KILL_CRITERIA |

## Tier 3 — visibility posts (time them after the arXiv ID exists)

- Hacker News "Show HN", Reddit (r/hardware, r/Physics, r/spintronics),
  LinkedIn, X, Mastodon — one post per channel, all linking the arXiv ID +
  repo + `PROVENANCE.md`. The honest negatives (0/26 switches at −14 mT (S);
  v_g not resolved (S)) are in the posts — they are the credibility signal.
- University seminar / journal-club circuit (remote talks are free): spintronics
  and magnonics groups.
- Conference abstracts: MMM–Intermag / APS March Meeting (abstract fee is the
  one non-$0 item; skip if budget stays zero — arXiv + seminars cover it).

## Email templates

### To a spintronics professor (reproduction ask)

> Subject: Reproduction request — magnon-assisted switching decks + Kaggle runs (Idaten Ce100)
>
> Dear Prof. ___,
>
> We are building a public evidence package around pattern-coded magnonic
> execution (repo: github.com/danielosinor123-gif/idaten-architecture).
> Your published result [cite paper] is our Stage A ground truth: our
> Kaggle-T4 re-run of the authors' deck gives a dominant mode of 1.89 GHz
> vs the published 1.70 GHz (simulated, (S)), and honestly 0/26 test magnets
> switched at −14 mT in our hands. The disproof gates are in
> docs/KILL_CRITERIA.md. If your group can re-run any deck on your own
> hardware, we will tag the result (S) with your group credited and link it
> from PROVENANCE.md. The hematite arm (mumax⁺) matched the qFM gap at
> 12.97 vs 12.78 GHz predicted (1.5 %, (S)/(E)).
>
> Happy to give a 20-min remote seminar.

### To a foundry / IMEC-class process team

> Subject: Small ask: write your SOT-MRAM free-layer array with a spin wave instead of a current
>
> The result medium in our architecture is a standard foundry MRAM
> free-layer array (100 nm × 20 nm NiFe in the 2023 precedent = already an
> MRAM geometry (L); SOT-MRAM on 300 mm with 300 ps switching (L)). The ask
> is not a new memory process — it is a measurement: does a patterned spin
> wave in an adjacent YIG bus reduce the write current of your array below
> the published 33.4 → 12.9 mT threshold effect (L)? Evidence + GDS of the
> digital tier (ORFS/sky130hd, DRC 0) in the repo; kill criteria attached.

### To an accelerator (Silicon Catalyst-class)

> Subject: Application — always-on edge magnonic spectral classifier
>
> One-pager: docs/ONE_PAGER.md. Lead product is an always-on edge spectral
> classifier (wake-word / spectrum sensing): bus + small MRAM read array, one
> small die. Headline metric W = cells written per wave event, 0.20 fJ/cell
> (E) vs 5–20 pJ/bit MRAM bound (L) — stated as a bound, not a result.
> Kill criteria with dates: docs/KILL_CRITERIA.md. Repo with all sims/GDS/PPA:
> github.com/danielosinor123-gif/idaten-architecture.
