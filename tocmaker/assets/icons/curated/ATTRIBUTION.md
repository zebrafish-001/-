# Curated third-party icons

Vendored subsets, chosen for environmental-toxicology / population-health TOC graphics.
Per-file metadata (licence, author, keywords) is in `attribution.json`.

| Folder | Source | Licence | Count |
|---|---|---|---|
| `healthicons/` | Health Icons — https://github.com/resolvetosavelives/healthicons (filled style) | MIT | 94 |
| `bioicons/` | Bioicons — https://github.com/duerrsimon/bioicons (bioicons.com); only icons in the `cc-0` folder | CC0 1.0 | 76 |
| `reactome/` | Reactome Icon Library — https://reactome.org/icon-lib (repo github.com/reactome/reactome_illustrations); subset: human tissue, cell types, cell elements, arrows, backgrounds, env-relevant compounds/receptors/proteins | CC BY 4.0 | ~900 |

MIT requires keeping the licence notice (this file); CC0 requires nothing. **Reactome icons are CC BY 4.0: cite "Reactome Icon Library (https://reactome.org/icon-lib), CC BY 4.0" in the figure legend, SI or Acknowledgements when one is used** — the QA report lists every CC-BY icon in a graphic. File names keep the Reactome id (R-ICO-xxxxxx) for the citation. Neither set needs
attribution inside the figure. The full libraries (4,300+ icons, incl. CC-BY ones that *do* need
attribution) can be fetched with `scripts/fetch_icon_sets.sh`; the QA step reports CC-BY/CC-BY-SA
icons used in a graphic.
