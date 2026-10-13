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


# ----------------------------------------------------------------- PubMed / Elsevier route (no Europe PMC needed)
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ELSEVIER_JOURNALS = ["Environ Int", "J Hazard Mater", "Sci Total Environ", "Ecotoxicol Environ Saf", "Environ Pollut",
                     "Chemosphere", "Environ Res", "Water Res", "Eco Environ Health", "Environ Sci Ecotechnol"]


def pii_code(pii: str) -> str:
    return re.sub(r"[^0-9A-Za-z]", "", pii or "")


def elsevier_ga_urls(pii: str):
    code = pii_code(pii)
    if not code:
        return []
    return [f"https://ars.els-cdn.com/content/image/1-s2.0-{code}-ga1_lrg.jpg",
            f"https://ars.els-cdn.com/content/image/1-s2.0-{code}-ga1.jpg",
            f"https://ars.els-cdn.com/content/image/1-s2.0-{code}-fx1_lrg.jpg",
            f"https://ars.els-cdn.com/content/image/1-s2.0-{code}-fx1.jpg"]


def pubmed_elsevier_candidates(sess, journals, years: str, want: int, sleep: float, topic: str = TOPIC, log=print):
    """PubMed E-utilities: esearch (open access filter) -> esummary (pii, doi, title) for Elsevier journals."""
    y0, y1 = (years.split("-") + [years])[:2]
    out = []
    per = max(10, want // max(1, len(journals)) + 5)
    for j in journals:
        q = f'"{j}"[Journal] AND ("open access"[filter] OR "free full text"[sb]) AND {y0}:{y1}[dp] AND {topic}'
        r = sess.get(f"{EUTILS}/esearch.fcgi", params=dict(db="pubmed", term=q, retmax=per, retmode="json", sort="pub_date"), timeout=60)
        r.raise_for_status()
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        log(f"{j}: {len(ids)} candidates")
        if not ids:
            continue
        time.sleep(sleep)
        r = sess.get(f"{EUTILS}/esummary.fcgi", params=dict(db="pubmed", id=",".join(ids), retmode="json"), timeout=60)
        r.raise_for_status()
        res = r.json().get("result", {})
        for pid in ids:
            d = res.get(pid) or {}
            aids = {x.get("idtype"): x.get("value") for x in d.get("articleids", [])}
            out.append(dict(pmid=pid, pmcid=aids.get("pmc", ""), doi=aids.get("doi", ""), pii=aids.get("pii", ""),
                            title=d.get("title", ""), journal=d.get("source", j), year=(d.get("pubdate", "") or "")[:4],
                            article_type=";".join(d.get("pubtype", []) or [])))
        time.sleep(sleep)
    return out


def download_from_index(records, out: str, sleep: float = 0.5, log=print) -> int:
    """Download graphical abstracts for records that carry ga_url / pii (seed_index.csv from the PubMed MCP, or esummary)."""
    sess = _session()
    os.makedirs(os.path.join(out, "images"), exist_ok=True)
    got = 0
    index_path = os.path.join(out, "index.jsonl")
    with open(index_path, "a", encoding="utf-8") as idx:
        for rec in records:
            urls = [u for u in [rec.get("ga_url"), rec.get("ga_url_small")] if u] or elsevier_ga_urls(rec.get("pii", ""))
            if not urls:
                continue
            key = rec.get("pmcid") or rec.get("pmid") or pii_code(rec.get("pii", ""))
            dest = os.path.join(out, "images", f"{key}.jpg")
            if os.path.exists(dest):
                continue
            ok = False
            for u in urls:
                try:
                    r = sess.get(u, timeout=120, headers={"Referer": "https://www.sciencedirect.com/"})
                except Exception as e:
                    log(f"  ! {key}: {e}")
                    break
                if r.status_code == 200 and r.headers.get("Content-Type", "").startswith("image") and len(r.content) > 2000:
                    with open(dest, "wb") as fh:
                        fh.write(r.content)
                    rec = dict(rec, image=f"images/{key}.jpg", image_url=u, how="pii-pattern")
                    ok = True
                    break
                time.sleep(sleep)
            if ok:
                got += 1
                idx.write(json.dumps(rec, ensure_ascii=False) + "\n")
                idx.flush()
                log(f"[{got}] {key} {rec.get('journal','')} {rec.get('year','')}")
            else:
                log(f"  - {key}: no graphical abstract at the Elsevier URL pattern")
            time.sleep(sleep)
    write_views(out)
    return got


def load_seed(path: str):
    recs = []
    if path.endswith(".jsonl"):
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    recs.append(json.loads(line))
    else:
        with open(path, "r", newline="", encoding="utf-8") as fh:
            recs = list(csv.DictReader(fh))
    return recs


def main(a) -> int:
    try:
        if getattr(a, "seed", None):
            recs = load_seed(a.seed)
            got = download_from_index(recs, a.out, a.sleep)
            print(f"downloaded {got} graphical abstracts from {len(recs)} seed records into {a.out}")
            return 0
        if getattr(a, "source", "europepmc") == "pubmed":
            sess = _session()
            recs = pubmed_elsevier_candidates(sess, a.journal or ELSEVIER_JOURNALS, a.years, a.n, a.sleep)
            if a.dry_run:
                os.makedirs(a.out, exist_ok=True)
                with open(os.path.join(a.out, "pubmed_candidates.jsonl"), "w", encoding="utf-8") as fh:
                    for r in recs:
                        fh.write(json.dumps(dict(r, ga_url=(elsevier_ga_urls(r["pii"]) or [""])[0]), ensure_ascii=False) + "\n")
                print(f"wrote {len(recs)} candidates")
                return 0
            got = download_from_index(recs[: a.n * 3], a.out, a.sleep)
            print(f"downloaded {got} graphical abstracts into {a.out}")
            return 0
        got = harvest(a.journal or DEFAULT_JOURNALS, a.years, a.n, a.out, a.dry_run, a.sleep, a.query)
    except Exception as e:
        msg = str(e)
        if "403" in msg or "CONNECT" in msg or "Name or service" in msg or "Max retries" in msg:
            print("Network blocked: this harvester needs HTTPS access to ars.els-cdn.com (+ eutils.ncbi.nlm.nih.gov for "
                  "--source pubmed, or www.ebi.ac.uk/europepmc.org for --source europepmc). Add them to the environment's "
                  "allowed domains, or run on your own machine.", file=sys.stderr)
        print(f"harvest failed: {e}", file=sys.stderr)
        return 2
    print(f"harvested {got} graphical abstracts into {a.out}")
    return 0
