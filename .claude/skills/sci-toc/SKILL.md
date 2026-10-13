---
name: sci-toc
description: Design and render a journal TOC graphic / graphical abstract (摘要图, TOC 图, 图文摘要, graphical abstract, visual abstract) for environmental-toxicology and population-health papers, output as journal-sized SVG + editable PPTX + 300-dpi PNG/TIFF with an automated QA report. Use whenever the user mentions TOC 图, 摘要图, graphical abstract, 图文摘要, ES&T/Environ Int/JHM/STOTEN submission artwork, 投稿配图, or wants a one-panel schematic that summarises a paper. Runs `python -m tocmaker.cli` from this repo.
---

# sci-toc — TOC graphic from a paper abstract

`tocmaker/` turns a short YAML spec into a journal-sized TOC graphic. One spec → `toc.svg`
(vector, exact mm), `toc.pptx` (every box/arrow/label a native shape, icons as embedded SVG you
can *Convert to Shape*), `toc.png`/`toc.pdf` (300 dpi), `toc_qa.json` (gates). Do not hand-draw SVG
or write python-pptx code yourself: write the spec, render, look, iterate.

## Workflow

1. **Extract the story** from the abstract / user text. Fill this table before touching YAML:

   | slot | question | example |
   |---|---|---|
   | exposure | what stressor, which matrix/window | prenatal PFAS, maternal serum, T1 |
   | organism | model system or population (+ n, place, years) | zebrafish larvae 5 dpf · 12,480 adults, 3 cities |
   | mechanism | the one biological link the paper argues | placental inflammation · gut dysbiosis |
   | outcome | the health endpoint | lower birth weight · incident hypertension |
   | key number | the single estimate worth a badge | HR 1.18 per 10 µg/m³ |
   | method | only if the method *is* the contribution | Cox + mediation |

   One message per graphic. If the paper has two stories, pick the one in the title.

2. **Pick journal + pattern.** `python -m tocmaker.cli presets` lists canvases (`acs` 3.25×1.75 in,
   `elsevier` 1328×531 px, `cell` square, `rsc`, `springer`, `mdpi`, `crt`, `advsci`, `wide`; any
   journal name also works via fuzzy lookup, backed by `tocmaker/db/journal_specs.yaml`).
   Choose a narrative pattern from `tocmaker/db/patterns.yaml` (12 skeletons: exposure→mechanism→
   outcome, cohort pipeline, multi-source→model→endpoints, hub, two-stream convergence, cycle, …).
   Templates: `flow`, `cohort`, `split`, `hub`, `two_row`, `cycle`.

3. **Write the spec** (`python -m tocmaker.cli init --template flow --journal acs -o toc.yaml` gives a
   filled example). Rules of thumb that the QA will otherwise flag:
   - ≤ 20 words on an ACS canvas, ≤ 30 on Elsevier; labels 2–4 words, sublabel for n/matrix/time.
   - 1–2 icons per panel, ≤ 6 icons total. Search: `python -m tocmaker.cli icons search 孕妇 placenta`.
     House set `envtox/*` (42 recolourable icons: zebrafish, organs, exposure sources, mechanism,
     mini-plots) first; then `healthicons/*` (MIT), `bioicons/*` (CC0 subset vendored; full sets via
     `scripts/fetch_icon_sets.sh`). Avoid CC-BY-SA icons for journal art.
   - Roles drive colour: `exposure` warm, `organism` blue, `mechanism` teal, `outcome` plum,
     `method` grey. Palettes: `envtox` (default), `calm`, `alert`, `mono`.
   - ACS TOC art traditionally *hints* the finding (↑/↓, no numbers); Elsevier/Cell want the key
     finding shown. The QA prints an info line, not an error — follow the target journal.
   - Badges hold the number; arrows can carry a 1–2 word label (`mediates`, `KE1`); `style: dashed`
     for indirect links, `inhibit` for ⊣.

4. **Render and look.** `python -m tocmaker.cli render toc.yaml -o out --preview` then Read
   `out/toc.png` (and `out/toc_pptx_preview.png` to confirm the deck matches). Fix anything the QA
   lists as `error` (overflow, type below the journal floor, missing icon) and anything that looks
   wrong to you (icon too small, label wrapped to 3 lines, dead space). Typical fixes: shorten a
   label, move detail into `sublabel`, drop an icon, change template, `font_pt: 7.5`,
   `options: {gap_pt: 8}`, `weight: 1.3` on the panel that needs room.

5. **Deliver** `toc.svg` (submit as-is or convert to TIFF with `--tiff`), `toc.pptx` (for the user
   to retouch in PowerPoint; slide = true TOC size, use `--pptx-scale 2` for a bigger working slide),
   `toc.png`, and the QA summary. State the licence/attribution lines the QA printed (`info/attribution`).

## Spec cheat-sheet

```yaml
journal: elsevier        # or acs | cell | rsc | springer | mdpi | crt | advsci | wide | "Environment International"
palette: envtox          # envtox | calm | alert | mono
template: flow           # flow | cohort | split | hub | two_row | cycle
title: ""                # optional top line (rarely needed)
footer: "n = 1,203 mother–infant pairs"
font_pt: 8               # optional; default = journal preference
panels:                  # order = reading order
  - role: exposure       # exposure | organism | mechanism | outcome | method | neutral
    label: Prenatal PFAS exposure
    sublabel: maternal serum, 1st trimester
    icons: [pregnant-woman, {id: chemical-flask-hazard, scale: 0.9, flip: false, tint: auto}]
    badge: ""            # pill with the key number
    items: []            # short bullet list (outcome lists)
    weight: 1.0          # relative width in flow/cohort
    box: true            # tinted background
arrows:                  # optional; defaults follow the template
  - {from: 0, to: 1, label: "", style: solid}   # solid | dashed | inhibit | none
# split: left/center/right; hub: center + hub_direction in|out; two_row: rows + converge
```

## Reference material

- `tocmaker/db/journal_specs.md` — sizes, text rules, required-or-optional, publisher design quotes.
- `tocmaker/db/patterns.yaml` — narrative skeletons for env-tox / population-health papers.
- `tocmaker/db/reference/` — harvested open-access graphical abstracts (`toc harvest`, needs
  network access to Europe PMC); browse `contact_sheet.html` for layout conventions before designing.
- `tocmaker/assets/icons/envtox/_contact_sheet.png` — the house icon set at a glance.

## When the user wants something the templates cannot do

Render the closest template, open the PPTX and describe the manual edit (PowerPoint keeps every
element editable). Do not fall back to raster AI image generation for journal TOC art: ACS requires
original author artwork and several journals ban generative images.
