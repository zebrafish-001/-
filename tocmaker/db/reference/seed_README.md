# seed_index — graphical-abstract (TOC image) seed list

Built 2026-10-13 with the PubMed MCP tools (`mcp__PubMed__search_articles`,
`mcp__PubMed__get_article_metadata`, `mcp__PubMed__get_copyright_status`). No images were
downloaded; this is metadata only. The images referenced here are intended for a **private
layout study** of graphical-abstract conventions (composition, panel count, typography), not for
redistribution. Each record carries the licence information PubMed/PMC exposes; see the
`license` / `open_access` columns and the `copyright_note` field in the JSONL before reusing any
image beyond private study.

## Files

| file | contents |
|---|---|
| `seed_index.csv` | 183 rows, columns `pmid, pmcid, doi, pii, journal, year, title, article_type, license, open_access, ga_url, ga_url_small, article_url` |
| `seed_index.jsonl` | same 183 records plus `pii_raw` (PubMed form, e.g. `S0160-4120(25)00790-1`), `copyright_note`, `search_set` |
| `seed_README.md` | this file |

## How the list was built

1. One `search_articles` call per journal, `date_from=2023`, `date_to=2025` (publication date),
   `max_results=20`, `sort=pub_date`:

   ```
   "<Journal ISO abbrev>"[Journal] AND ("open access"[filter] OR "pubmed pmc open access"[sb])
     AND (exposure OR pollutant OR toxicity OR cohort OR epidemiolog OR zebrafish OR PFAS
          OR microplastic OR "heavy metal" OR "air pollution" OR pesticide)
   ```
   PubMed translated the OA clause to `"pubmed pmc open access"[Filter]`. This worked for nine
   journals. For **Water Res** it returned only 5 hits, so the fallback query was run as well:

   ```
   "Water Res"[Journal] AND "free full text"[sb] AND (<same topic terms>)
   ```
   (translated to `"loattrfree full text"[Filter]`; 488 hits, first 20 taken). The 20 fallback
   records have no PMC ID and are flagged `open_access = free_full_text_no_pmc`.

2. `get_article_metadata` in batches of 10 PMIDs (204 PMIDs total). Extracted:
   `identifiers.pmid/pmc/doi/pii`, `title`, `journal.iso_abbreviation`,
   `publication_date.year`, `article_types`.

3. Elsevier PII code = `pii` with all non-alphanumerics removed
   (`S0160-4120(25)00790-1` -> `S016041202500790 1` -> `S0160412025007901`).
   `ga_url      = https://ars.els-cdn.com/content/image/1-s2.0-<PII>-ga1_lrg.jpg`
   `ga_url_small= https://ars.els-cdn.com/content/image/1-s2.0-<PII>-ga1.jpg`
   `article_url = https://www.sciencedirect.com/science/article/pii/<PII>`
   The URLs are derived, not verified: articles without a graphical abstract will 404.

4. `get_copyright_status` in batches of 10 for all 204 PMIDs. For 203 of them the tool found only
   the PubMed copyright statement (no CC licence string), so `license = unknown` and the
   statement class is recorded in `copyright_note`. One record (PMID 41312296) resolved via PMC
   to `CC BY 4.0`. Note: Eco Environ Health and Environ Sci Ecotechnol are gold-OA journals and
   the "pubmed pmc open access" filter means every PMC-bearing record is in the PMC Open Access
   Subset, but the specific CC variant (BY / BY-NC-ND) must be read from the article page.

5. Exclusions: records whose `article_types` include Review, Editorial, Comment, Letter,
   Published Erratum or Retracted Publication were dropped (21 removed: 20 Reviews, 1 Retracted
   Publication, PMID 41560851). Everything kept is typed `Journal Article`.

`year` is PubMed's `publication_date.year` (electronic date). A few 2023-issue articles therefore
show 2022, and some 2025-dated records sit in 2026 journal issues; the search itself was bounded
to issue dates 2023-2025.

## Counts per journal (searched -> kept after exclusions)

| journal | searched | kept | with PII | with PMC ID | CC-BY confirmed | reviews/retracted dropped |
|---|---|---|---|---|---|---|
| Environ Int | 20 | 20 | 20 | 20 | 0 | 0 |
| J Hazard Mater | 19 | 17 | 17 | 17 | 0 | 2 |
| Sci Total Environ | 20 | 20 | 20 | 20 | 0 | 0 |
| Ecotoxicol Environ Saf | 20 | 19 | 19 | 19 | 0 | 1 |
| Environ Pollut | 20 | 20 | 20 | 20 | 0 | 0 |
| Chemosphere | 20 | 15 | 15 | 15 | 0 | 5 |
| Environ Res | 20 | 18 | 18 | 18 | 0 | 2 |
| Water Res | 25 (5 OA + 20 free-full-text fallback) | 23 | 23 | 5 | 0 | 2 |
| Eco Environ Health | 20 | 15 | 15 | 15 | 1 | 5 |
| Environ Sci Ecotechnol | 20 | 16 | 16 | 16 | 0 | 4 |
| **total** | **204** | **183** | **183** | **165** | **1** | **21** |

`open_access` values: `pmc_oa_subset` 164, `cc_by_4.0_pmc` 1, `free_full_text_no_pmc` 18.

## Caveats

* Chemosphere / J Hazard Mater / Environ Pollut OA hits from 2023 are dominated by COVID-19-era
  papers (face masks, disinfectants, lockdown air quality); they are still Elsevier research
  articles with graphical abstracts but are topically narrower than the search terms suggest.
* Several J Hazard Mater / Environ Pollut / Chemosphere records carry a publisher-held
  "Copyright (c) Elsevier. All rights reserved." statement: these are typically PMC
  author-manuscript deposits, so the publisher GA image is not CC-licensed even though the
  article is in the PMC OA subset. Treat those images as view-only for the layout study.
* Water Res fallback records (`free_full_text_no_pmc`) are free-to-read on ScienceDirect but not
  in PMC; the same view-only caveat applies.
