# Citations

External datasets and reference papers used by this repository.

## Software Heritage per-extension counts

The per-extension popularity table at `data/derived/swh_extensions_popularity.csv.gz`
counts distinct files per extension and year of first appearance in the whole
Software Heritage archive. Since 2026-09-30 it is computed from the SWH
*Aggregated Contents* dataset of the **2026-06-04** graph export
(<https://datasets.softwareheritage.org/datasets/2026-06-04-contents/>) by
`tools/build_swh_ext_year_table.py` → `tools/build_swh_ext_popularity.py`
(see `docs/SWH_EXTENSIONS_DECISIONS.md` §14). The approach, and the table
it replaced (`nb_extensions_alphanum.csv`, a 2023 snapshot), come from:

> Adèle Desmazières, Roberto Di Cosmo, Valentin Lorentz.
> *50 Years of Programming Language Evolution through the Software Heritage
> looking glass.*
> Proceedings of the 22nd International Conference on Mining Software
> Repositories (MSR 2025), pages 372–383.

We refer to that 2023 table throughout this repo as **SWH-MSR-ARV** (where
ARV = Adèle Desmazières, Roberto Di Cosmo, Valentin Lorentz). Figures in the
older analyses (`docs/SWH_EXTENSIONS_DECISIONS.md` §§1–13, the COBOL study)
trace back to it; figures on the site now come from the 2026-06-04 export.

### How to cite

If you publish work that uses any of:

- the per-extension popularity numbers on `/ext/<slug>/` pages,
- the priority ranking on `/review/extensions/`,
- the "in SWH but unattributed" tier breakdown in
  `docs/SWH_EXTENSIONS_DECISIONS.md`,

please cite the MSR 2025 paper above, and acknowledge Software Heritage as
its dataset page asks: the footnote "This work was made possible by Software
Heritage, the universal source code archive: https://www.softwareheritage.org"
plus

> Jean-François Abramatic, Roberto Di Cosmo, Stefano Zacchiroli.
> *Building the universal archive of source code.* Commun. ACM 61(10):29–31, 2018.
> <https://doi.org/10.1145/3183558>

> Roberto Di Cosmo, Stefano Zacchiroli. *Software Heritage: why and how to
> preserve software source code.* iPRES 2017.
> <https://hdl.handle.net/11353/10.931064>

and name the export: SWH Aggregated Contents, 2026-06-04. The website's
per-extension panel and the `/ext/index.html` page both name the export and
the MSR 2025 paper, with a link back to this file.

## Other upstream sources of language metadata

| Source | Used for | Reference |
|---|---|---|
| GitHub Linguist | language list, primary/secondary extensions, content-disambiguation heuristics | <https://github.com/github-linguist/linguist> (MIT) |
| Pygments | language list, file glob patterns | <https://pygments.org/> (BSD) |
| PLDB | language list, paradigms, first-appeared dates | <https://pldb.io/> (CC0) |
| Hyperpolyglot | side-by-side language comparisons | <https://hyperpolyglot.org/> |
| Rosetta Code | task examples per language | <https://rosettacode.org/> |
| Esolang.org | catalog of esoteric languages | <https://esolangs.org/> |
| Wikipedia "programming language" category | encyclopedic metadata | <https://en.wikipedia.org/wiki/Category:Programming_languages> |
| Software Heritage archive | source-of-truth code repository | <https://www.softwareheritage.org/> |
