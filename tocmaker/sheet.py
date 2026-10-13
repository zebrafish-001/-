"""Contact sheet of icons (PNG) for picking visually."""
from __future__ import annotations

import io
import math
from typing import List

from . import icons as iconlib


def contact_sheet(infos: List[iconlib.IconInfo], out_path: str, cell: int = 110, cols: int = 10) -> str:
    from PIL import Image, ImageDraw, ImageFont
    from .textmetrics import find_font
    n = len(infos)
    rows = max(1, math.ceil(n / cols))
    im = Image.new("RGB", (cols * cell, rows * (cell + 22)), "white")
    d = ImageDraw.Draw(im)
    fp = find_font("regular")
    font = ImageFont.truetype(fp, 10) if fp else ImageFont.load_default()
    for k, info in enumerate(infos):
        r, c = divmod(k, cols)
        x, y = c * cell, r * (cell + 22)
        try:
            png = iconlib.icon_png(info, cell - 20)
            ic = Image.open(io.BytesIO(png)).convert("RGBA")
            im.paste(ic, (x + 10, y + 6), ic)
        except Exception:
            d.rectangle([x + 10, y + 6, x + cell - 10, y + cell - 14], outline="red")
        name = info.id.split("/")[-1]
        d.text((x + 4, y + cell - 10), name[:18], fill="black", font=font)
    im.save(out_path)
    return out_path
