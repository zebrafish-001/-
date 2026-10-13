"""Harvest open-access graphical abstracts (TOC images) into a local reference database.

Strategy (needs outbound HTTPS to www.ebi.ac.uk and europepmc.org; optionally api.crossref.org):
  1. Europe PMC REST search restricted to OPEN_ACCESS:y and the target journals.
  2. For each PMCID fetch the JATS full-text XML; the graphical abstract is marked as
     <abstract abstract-type="graphical"> (Elsevier/Cell), or a <fig> whose label/caption
     says "Graphical abstract"/"TOC", or a graphic whose href contains "ga1"/"fx1"/"toc".
  3. Download the figure from Europe PMC's render endpoint and store it with metadata
     (DOI, title, journal, year, licence, source URL) in index.csv + index.jsonl, and build
     a contact-sheet HTML for browsing.

Images are for private study of layout conventions only; each record carries its licence.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
from typing import Dict, Iterable, List, Optional

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
DEFAULT_JOURNALS = [
    "Environ Int", "Environ Sci Technol", "Environ Sci Technol Lett", "Environ Health Perspect",
    "J Hazard Mater", "Sci Total Environ", "Ecotoxicol Environ Saf", "Environ Pollut", "Environ Res",
    "Chemosphere", "Water Res", "Eco Environ Health", "Environ Sci Ecotechnol", "Innovation (Camb)",
    "iScience", "Toxics", "Environ Health (Wash)",
]
TOPIC = ('(exposure OR toxicity OR pollutant OR "environmental health" OR cohort OR epidemiolog* OR zebrafish '
         'OR PFAS OR microplastic* OR "heavy metal*" OR "air pollution" OR pesticide*)')


def _session():
    import requests
    s = requests.Session()
    s.headers["User-Agent"] = "tocmaker-harvest/0.1 (academic reference collection; contact via repo)"
    return s


def search_pmcids(sess, query: str, want: int, sleep: float) -> List[Dict]:
    out, cursor = [], "*"
    while len(out) < want * 3:
        r = sess.get(f"{EPMC}/search", params=dict(query=query, format="json", pageSize=100, cursorMark=cursor,
                                                   resultType="lite"), timeout=60)
        r.raise_for_status()
        j = r.json()
        hits = j.get("resultList", {}).get("result", [])
        if not hits:
            break
        for h in hits:
            if h.get("pmcid"):
                out.append(dict(pmcid=h["pmcid"], doi=h.get("doi", ""), title=h.get("title", ""),
                                journal=h.get("journalTitle", ""), year=h.get("pubYear", ""), pmid=h.get("pmid", "")))
        nxt = j.get("nextCursorMark")
        if not nxt or nxt == cursor:
            break
        cursor = nxt
        time.sleep(sleep)
    return out


_GA_HINT = re.compile(r"graphical\s*abstract|toc\s*graphic|table\s*of\s*contents|visual\s*abstract", re.I)
_HREF_HINT = re.compile(r"(^|[^a-z])(ga\d*|fx\d*|toc|gr_?abs|abs\d*)($|[^a-z])", re.I)


def find_graphical_abstract(xml: str) -> Optional[Dict[str, str]]:
    """Return {'href':..., 'how':...} for the graphical-abstract graphic in a JATS document."""
    from lxml import etree
    try:
        root = etree.fromstring(xml.encode("utf-8") if isinstance(xml, str) else xml,
                                etree.XMLParser(recover=True, huge_tree=True))
    except Exception:
        return None
    if root is None:
        return None
    XL = "{http://www.w3.org/1999/xlink}href"

    def hrefs(el):
        return [g.get(XL) or g.get("href") for g in el.iter("graphic", "inline-graphic") if (g.get(XL) or g.get("href"))]

    for ab in root.iter("abstract"):
        if (ab.get("abstract-type") or "").lower() in ("graphical", "graphical-abstract", "toc", "visual"):
            h = hrefs(ab)
            if h:
                return dict(href=h[0], how="abstract-type=graphical")
    for fig in root.iter("fig"):
        if (fig.get("fig-type") or "").lower() in ("graphical", "graphical-abstract", "toc"):
            h = hrefs(fig)
            if h:
                return dict(href=h[0], how="fig-type")
        txt = " ".join(t for t in fig.itertext())[:300]
        if _GA_HINT.search(txt):
            h = hrefs(fig)
            if h:
                return dict(href=h[0], how="caption-text")
    for g in root.iter("graphic"):
        h = g.get(XL) or g.get("href") or ""
        if _HREF_HINT.search(os.path.basename(h)):
            return dict(href=h, how="href-pattern")
    for ab in root.iter("abstract"):
        h = hrefs(ab)
        if h:
            return dict(href=h[0], how="graphic-in-abstract")
    return None


def _licence(xml: str) -> str:
    m = re.search(r'<license[^>]*?(?:xlink:href|href)="([^"]+)"', xml)
    if m:
        return m.group(1)
    m = re.search(r"<license[^>]*>(.*?)</license>", xml, re.S)
    return re.sub(r"<[^>]+>", " ", m.group(1)).strip()[:200] if m else ""


def harvest(journals: Iterable[str], years: str, n: int, out: str, dry_run: bool = False, sleep: float = 0.34,
            query: Optional[str] = None, log=print) -> int:
    sess = _session()
    os.makedirs(os.path.join(out, "images"), exist_ok=True)
    y0, y1 = (years.split("-") + [years])[:2]
    if not query:
        jq = " OR ".join(f'JOURNAL:"{j}"' for j in journals)
        query = f"({jq}) AND OPEN_ACCESS:y AND HAS_FT:y AND PUB_YEAR:[{y0} TO {y1}] AND {TOPIC}"
    log(f"query: {query}")
    cands = search_pmcids(sess, query, n, sleep)
    log(f"{len(cands)} open-access candidates")
    index_path = os.path.join(out, "index.jsonl")
    seen = set()
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as fh:
            for line in fh:
                try:
                    seen.add(json.loads(line)["pmcid"])
                except Exception:
                    pass
    got = sum(1 for _ in seen)
    with open(index_path, "a", encoding="utf-8") as idx:
        for c in cands:
            if got >= n:
                break
            if c["pmcid"] in seen:
                continue
            time.sleep(sleep)
            try:
                r = sess.get(f"{EPMC}/{c['pmcid']}/fullTextXML", timeout=60)
                if r.status_code != 200:
                    continue
                ga = find_graphical_abstract(r.text)
                if not ga:
                    continue
                href = ga["href"]
                img_url = f"https://europepmc.org/articles/{c['pmcid']}/bin/{href}"
                if not re.search(r"\.(jpg|jpeg|png|gif|tif|tiff)$", href, re.I):
                    img_url += ".jpg"
                rec = dict(c, href=href, how=ga["how"], image_url=img_url, licence=_licence(r.text), image="")
                if not dry_run:
                    time.sleep(sleep)
                    ir = sess.get(img_url, timeout=120)
                    if ir.status_code != 200 or not ir.content:
                        rec["error"] = f"image HTTP {ir.status_code}"
                    else:
                        ext = ".jpg" if "jpeg" in ir.headers.get("Content-Type", "jpeg") else ".png"
                        fn = f"{c['pmcid']}{ext}"
                        with open(os.path.join(out, "images", fn), "wb") as fh:
                            fh.write(ir.content)
                        rec["image"] = f"images/{fn}"
                        got += 1
                else:
                    got += 1
                idx.write(json.dumps(rec, ensure_ascii=False) + "\n")
                idx.flush()
                log(f"[{got}/{n}] {c['pmcid']} {c['journal']} {c['year']} ({ga['how']})")
            except Exception as e:  # keep going on individual failures
                log(f"  ! {c['pmcid']}: {e}")
    write_views(out)
    return got


def write_views(out: str):
    """index.csv + contact_sheet.html from index.jsonl."""
    path = os.path.join(out, "index.jsonl")
    if not os.path.exists(path):
        return
    recs = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            try:
                recs.append(json.loads(line))
            except Exception:
                pass
    cols = ["pmcid", "doi", "journal", "year", "title", "image", "image_url", "licence", "how"]
    with open(os.path.join(out, "index.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in recs:
            w.writerow(r)
    cards = []
    for r in recs:
        src = r.get("image") or r.get("image_url", "")
        cards.append(f'<figure><img src="{src}" loading="lazy"><figcaption><b>{r.get("journal","")}</b> {r.get("year","")}'
                     f' · <a href="https://doi.org/{r.get("doi","")}">{r.get("doi","")}</a><br>{r.get("title","")[:140]}'
                     f'<br><small>{r.get("licence","")}</small></figcaption></figure>')
    html = ("<!doctype html><meta charset=utf-8><title>TOC reference sheet</title><style>body{font-family:sans-serif;margin:16px}"
            ".g{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}figure{margin:0;border:1px solid #ddd;"
            "padding:8px;border-radius:6px}img{width:100%;height:auto;background:#fafafa}figcaption{font-size:12px;margin-top:6px}</style>"
            f"<h1>{len(recs)} graphical abstracts</h1><div class=g>{''.join(cards)}</div>")
    with open(os.path.join(out, "contact_sheet.html"), "w", encoding="utf-8") as fh:
        fh.write(html)


def main(a) -> int:
    try:
        got = harvest(a.journal or DEFAULT_JOURNALS, a.years, a.n, a.out, a.dry_run, a.sleep, a.query)
    except Exception as e:
        msg = str(e)
        if "403" in msg or "CONNECT" in msg or "Name or service" in msg or "Max retries" in msg:
            print("Network blocked: this harvester needs HTTPS access to www.ebi.ac.uk and europepmc.org "
                  "(add them to the environment's allowed domains, or run on your own machine).", file=sys.stderr)
        print(f"harvest failed: {e}", file=sys.stderr)
        return 2
    print(f"harvested {got} graphical abstracts into {a.out}")
    return 0
