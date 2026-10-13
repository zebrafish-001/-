import os
import zipfile

import pytest
from PIL import Image, ImageDraw, ImageFont

from tocmaker.textmetrics import find_font
from tocmaker.vectorize import TraceOptions, detect_text, svg_regions, trace_svg, vectorize


@pytest.fixture(scope="module")
def flat_png(tmp_path_factory):
    p = tmp_path_factory.mktemp("vec") / "flat.png"
    im = Image.new("RGB", (900, 480), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 40, 400, 440], radius=30, fill="#F7E4DE")
    d.ellipse([120, 90, 320, 290], fill="#C8553D")
    d.rectangle([500, 120, 860, 300], fill="#4F8FC0")
    d.ellipse([600, 160, 760, 260], fill="white")  # a hole-like feature
    font = ImageFont.truetype(find_font("bold"), 40)
    d.text((80, 340), "Exposure", fill="#1F2937", font=font)
    im.save(p)
    return str(p)


def test_trace_regions(flat_png, tmp_path):
    opt = TraceOptions(filter_speckle=4)
    svg = trace_svg(flat_png, str(tmp_path / "t.svg"), opt)
    regions, W, H = svg_regions(svg, opt)
    assert (W, H) == (900, 480)
    cols = {r.color for r in regions}
    assert len(regions) >= 4 and any(c.upper().startswith("#C") for c in cols)
    # background dropped
    assert not any(r.bbox[2] - r.bbox[0] > 880 for r in regions)


def test_ocr_detects_label(flat_png):
    boxes = detect_text(flat_png)
    assert boxes and any("Exposure" in b.text for b in boxes)
    assert all(b.w / b.h > 1.2 for b in boxes)


def test_vectorize_end_to_end(flat_png, tmp_path):
    info = vectorize(flat_png, str(tmp_path / "out"), "v", opt=TraceOptions(filter_speckle=4), text_mode="ocr")
    assert os.path.exists(info["pptx"]) and os.path.exists(info["svg"])
    with zipfile.ZipFile(info["pptx"]) as z:
        slide = z.read("ppt/slides/slide1.xml").decode()
        assert "<a:custGeom>" in slide and "Exposure" in slide
        assert any(n.endswith(".svg") for n in z.namelist())
    svg = open(info["svg"], encoding="utf-8").read()
    assert "<text" in svg and 'fill-rule="evenodd"' in svg
