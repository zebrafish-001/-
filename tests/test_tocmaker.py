import os
import zipfile

import pytest
import yaml

from tocmaker import icons
from tocmaker.layout import build_scene
from tocmaker.presets import find_preset, get_preset, list_presets
from tocmaker.qa import run_qa
from tocmaker.render_pptx import render_pptx
from tocmaker.render_svg import render_svg
from tocmaker.spec import TEMPLATES, TocSpec
from tocmaker.templates_lib import EXAMPLES, example_spec
from tocmaker.textmetrics import text_width, wrap


def test_presets_sizes():
    acs = get_preset("est")
    assert abs(acs.width_mm - 82.55) < 0.01 and abs(acs.height_mm - 44.45) < 0.01
    assert get_preset("elsevier").px() == (1328, 531)
    assert get_preset("cell").px() == (1200, 1200)
    assert abs(find_preset("Environment International").width_mm - get_preset("elsevier").width_mm) < 0.5
    assert len(list_presets()) >= 8


def test_text_metrics_and_wrap():
    assert text_width("Placental", 8, "bold") > text_width("Pla", 8, "bold")
    lines = wrap("Prenatal PFAS exposure in a prospective cohort", 60, 8, "bold", 3)
    assert len(lines) >= 2 and all(text_width(l, 8, "bold") <= 60 for l in lines)
    # a very long word gets hyphenated instead of overflowing
    lines = wrap("neurodevelopment", 40, 8, "bold", 3)
    assert len(lines) >= 2 and lines[0].endswith("-")
    # CJK wraps per character
    assert len(wrap("斑马鱼幼鱼神经行为毒性", 30, 8)) >= 2


def test_icon_index_and_search():
    idx = icons.build_index()
    assert len(idx) >= 200
    hit = icons.search("zebrafish")[0]
    assert hit.source == "envtox"
    assert icons.get("pregnant-woman").recolorable
    assert icons.get("healthicons/body/lungs").monochrome
    svg = icons.placed_svg(icons.get("liver"), 0, 0, 20, 20, "#111111", "#AA0000")
    assert "#111111" in svg and "#AA0000" in svg and "#1F2937" not in svg


@pytest.mark.parametrize("template", TEMPLATES)
def test_every_template_renders(tmp_path, template):
    assert template in EXAMPLES
    spec = TocSpec.from_dict(yaml.safe_load(example_spec(template, "acs")))
    scene, lay = build_scene(spec)
    svg = render_svg(scene, lay.preset)
    assert svg.startswith("<svg") and 'width="82.550mm"' in svg
    assert not [w for w in lay.warnings if "overflow" in w or "wider" in w], lay.warnings
    rep = run_qa(spec, scene, lay, lay.preset, svg)
    assert rep["status"] in ("pass", "warn"), rep
    out = tmp_path / f"{template}.pptx"
    warns = render_pptx(scene, lay.preset, str(out))
    assert out.exists() and not warns
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
        assert any(n.endswith(".svg") for n in names)
        slide = z.read("ppt/slides/slide1.xml").decode()
        assert "svgBlip" in slide and "<p:cxnSp>" in slide


def test_qa_flags_font_floor_and_missing_icon():
    d = yaml.safe_load(example_spec("flow", "acs"))
    d["panels"][0]["icons"] = ["no-such-icon-xyz"]
    spec = TocSpec.from_dict(d)
    scene, lay = build_scene(spec)
    rep = run_qa(spec, scene, lay, lay.preset, render_svg(scene, lay.preset))
    assert any(i["code"] == "layout" and "No icon" in i["message"] for i in rep["issues"])


def test_cli_render(tmp_path):
    from tocmaker.cli import main
    spec = tmp_path / "s.yaml"
    spec.write_text(example_spec("cohort", "elsevier"), encoding="utf-8")
    assert main(["render", str(spec), "-o", str(tmp_path / "o"), "--dpi", "100"]) == 0
    assert (tmp_path / "o" / "toc.svg").exists() and (tmp_path / "o" / "toc.pptx").exists()
    from PIL import Image
    assert Image.open(tmp_path / "o" / "toc.png").size[0] == 443  # 112.44 mm at 100 dpi
