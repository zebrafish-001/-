"""PubMed E-utilities 客户端（标准库实现，带限速与重试）。

NCBI 无 API key 时限 3 req/s；设 NCBI_API_KEY 环境变量可到 10 req/s。
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
_last_call = [0.0]


def _throttle() -> None:
    interval = 0.12 if os.environ.get("NCBI_API_KEY") else 0.40
    wait = _last_call[0] + interval - time.time()
    if wait > 0:
        time.sleep(wait)
    _last_call[0] = time.time()


def _get(endpoint: str, params: dict) -> dict:
    params = dict(params)
    params.setdefault("retmode", "json")
    key = os.environ.get("NCBI_API_KEY")
    if key:
        params["api_key"] = key
    url = f"{BASE}/{endpoint}?{urllib.parse.urlencode(params)}"
    last_err: Exception | None = None
    for attempt in range(4):
        _throttle()
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
            last_err = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"PubMed 请求失败（已重试）: {endpoint} {params.get('term', '')[:80]}") from last_err


def count(term: str, mindate: str | None = None, maxdate: str | None = None) -> int:
    """esearch 计数。mindate/maxdate 形如 '2021' 或 '2021/01/01'。"""
    params: dict = {"db": "pubmed", "term": term, "retmax": 0}
    if mindate or maxdate:
        params.update(datetype="pdat", mindate=mindate or "1900", maxdate=maxdate or "3000")
    data = _get("esearch.fcgi", params)
    return int(data["esearchresult"]["count"])


def search_ids(term: str, retmax: int = 10, sort: str = "pub_date") -> list[str]:
    data = _get("esearch.fcgi", {"db": "pubmed", "term": term, "retmax": retmax, "sort": sort})
    return list(data["esearchresult"].get("idlist", []))


def summaries(pmids: list[str]) -> list[dict]:
    """esummary：返回 [{pmid, title, journal, pubdate, authors}]。"""
    if not pmids:
        return []
    data = _get("esummary.fcgi", {"db": "pubmed", "id": ",".join(pmids)})
    result = data.get("result", {})
    out = []
    for pid in result.get("uids", []):
        rec = result.get(pid, {})
        authors = [a.get("name", "") for a in rec.get("authors", [])][:3]
        out.append({
            "pmid": pid,
            "title": rec.get("title", ""),
            "journal": rec.get("fulljournalname", rec.get("source", "")),
            "pubdate": rec.get("pubdate", ""),
            "authors": authors,
        })
    return out


def yearly_counts(term: str, years: list[int]) -> dict[int, int]:
    return {y: count(term, mindate=str(y), maxdate=str(y)) for y in years}
