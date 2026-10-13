"""Text measurement with a metric-compatible sans font (Liberation Sans ≈ Arial/Helvetica).

Widths are returned in points when ``size_pt`` is given, because a TrueType font rendered
at N pixels has the same advance widths as the same font at N points (1:1 scale).
"""
from __future__ import annotations

import functools
import os
import subprocess
from typing import List, Optional

_CANDIDATES = {
    "regular": ["LiberationSans-Regular.ttf", "Arial.ttf", "arial.ttf", "DejaVuSans.ttf"],
    "bold": ["LiberationSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"],
}
_SEARCH_DIRS = ["/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts"),
                "C:/Windows/Fonts", "/Library/Fonts", "/System/Library/Fonts"]


@functools.lru_cache(maxsize=None)
def find_font(weight: str = "regular") -> Optional[str]:
    names = _CANDIDATES[weight]
    for d in _SEARCH_DIRS:
        if not os.path.isdir(d):
            continue
        for root, _dirs, files in os.walk(d):
            for n in names:
                if n in files:
                    return os.path.join(root, n)
    try:
        out = subprocess.run(["fc-match", "-f", "%{file}", "Liberation Sans" + (":bold" if weight == "bold" else "")],
                             capture_output=True, text=True, timeout=10).stdout.strip()
        if out and os.path.exists(out):
            return out
    except Exception:
        pass
    return None


@functools.lru_cache(maxsize=256)
def _font(size_pt: float, weight: str):
    from PIL import ImageFont
    path = find_font(weight)
    px = max(1, int(round(size_pt * 10)))  # measure at 10x for sub-point precision
    if path:
        return ImageFont.truetype(path, px)
    return ImageFont.load_default()


def text_width(text: str, size_pt: float, weight: str = "regular") -> float:
    """Advance width of ``text`` in points."""
    if not text:
        return 0.0
    f = _font(size_pt, weight)
    try:
        w = f.getlength(text)
    except AttributeError:  # very old Pillow
        w = f.getsize(text)[0]
    return w / 10.0


def wrap(text: str, max_width_pt: float, size_pt: float, weight: str = "regular", max_lines: int = 3,
         break_words: bool = True) -> List[str]:
    """Greedy word wrap; CJK text is wrapped per character. Returns at most ``max_lines`` lines
    (the last line is NOT truncated — the QA step flags overflow instead of hiding it)."""
    if not text:
        return []
    text = text.replace("\\n", "\n")
    lines: List[str] = []
    for para in text.split("\n"):
        tokens = _break_long(_tokenise(para), max_width_pt, size_pt, weight) if break_words else _tokenise(para)
        cur = ""
        for tok in tokens:
            cand = (cur + tok) if (not cur or tok in ",.;:!?)]" or cur.endswith(" ") or _is_cjk(tok) or _is_cjk(cur[-1:])) else (cur + " " + tok)
            if text_width(cand.strip(), size_pt, weight) <= max_width_pt or not cur:
                cur = cand
            else:
                lines.append(cur.strip())
                cur = tok
        if cur.strip():
            lines.append(cur.strip())
    return lines


def _is_cjk(s: str) -> bool:
    return bool(s) and any("\u4e00" <= ch <= "\u9fff" or "\u3000" <= ch <= "\u30ff" for ch in s)


def _tokenise(s: str) -> List[str]:
    toks: List[str] = []
    buf = ""
    for ch in s:
        if ch == " ":
            if buf:
                toks.append(buf)
                buf = ""
        elif _is_cjk(ch):
            if buf:
                toks.append(buf)
                buf = ""
            toks.append(ch)
        else:
            buf += ch
    if buf:
        toks.append(buf)
    return toks


def _break_long(tokens: List[str], max_w: float, size_pt: float, weight: str) -> List[str]:
    """Split any single token wider than the box into hyphenated chunks that fit."""
    out: List[str] = []
    for tok in tokens:
        if text_width(tok, size_pt, weight) <= max_w or len(tok) < 4 or _is_cjk(tok):
            out.append(tok)
            continue
        buf = ""
        for ch in tok:
            if text_width(buf + ch + "-", size_pt, weight) > max_w and buf:
                out.append(buf + "-")
                buf = ch
            else:
                buf += ch
        if buf:
            out.append(buf)
    return out
