"""End-to-end regression on short synthetic videos."""
import numpy as np
import pytest

from zfbehavior.config import config_from_dict, load_config
from zfbehavior.metrics import analyze
from zfbehavior.synthetic import make_adult_tank_video, make_larva_plate_video
from zfbehavior.tracking import track_video


@pytest.fixture(scope="module")
def larva(tmp_path_factory):
    d = tmp_path_factory.mktemp("larva")
    gt, meta, info = make_larva_plate_video(d / "larva.mp4", rows=2, cols=3, duration_s=8,
                                            phases=[("light", 4), ("dark", 4)], empty_wells=["B3"])
    return d / "larva.mp4", gt, meta, info


def test_larva_plate_tracking(larva):
    path, gt, meta, info = larva
    cfg = config_from_dict({"extends": "larva_24well", "arenas": {"rows": 2, "cols": 3}})
    res = track_video(path, cfg, progress=False)
    assert len(res.arenas) == 6
    assert abs(res.arenas[0].px_per_mm - info["px_per_mm"]) / info["px_per_mm"] < 0.03
    m = res.raw.merge(gt, on=["frame", "arena"], suffixes=("", "_gt"))
    err = np.hypot(m.x_px - m.x_px_gt, m.y_px - m.y_px_gt)
    assert np.nanmedian(err) < 0.5 and np.nanpercentile(err, 95) < 4.0
    assert m.x_px.isna().mean() < 0.02
    d = np.abs((m.heading_deg - m.heading_deg_gt + 180) % 360 - 180)
    assert np.nanmedian(d) < 5 and np.nanmean(d > 90) < 0.02
    ana = analyze(res.raw, res.arenas, res.info, cfg, res.frames)
    s = ana.summary.set_index("track_id")
    assert s.loc["B3", "detected_frac"] < 0.02 and not s.loc["B3", "qc_pass"]
    assert s.loc["B3", "qc_note"].startswith("never detected")
    assert (s.drop("B3")["distance_mm"] > 0).all()
    assert {"center_frac", "periphery_frac", "bout_count"} <= set(s.columns)
    assert len(ana.timebins) == 6 * int(np.ceil(8 / cfg.metrics.time_bin_s))


def test_adult_tank_single(tmp_path):
    gt, info = make_adult_tank_video(tmp_path / "adult.mp4", duration_s=6, anxiety=0.3)
    cfg = config_from_dict({"extends": "adult_novel_tank", "arenas": {
        "type": "rects", "rects": [info["tank_rect"]], "ids": ["tank1"], "size_mm": info["tank_mm"]}})
    res = track_video(tmp_path / "adult.mp4", cfg, progress=False)
    m = res.raw.merge(gt, on=["frame", "animal"], suffixes=("", "_gt"))
    err = np.hypot(m.x_px - m.x_px_gt, m.y_px - m.y_px_gt)
    assert np.nanmedian(err) < 0.5 and m.x_px.isna().mean() < 0.01
    ana = analyze(res.raw, res.arenas, res.info, cfg, res.frames)
    s = ana.summary.iloc[0]
    assert abs(s["top_frac"] + s["middle_frac"] + s["bottom_frac"] - 1) < 1e-6
    assert s["distance_mm"] > 0


def test_config_presets_load():
    for name in ("larva_96well", "larva_48well", "larva_24well", "adult_novel_tank", "adult_open_field"):
        cfg = load_config(name)
        assert cfg.name == name
    assert load_config("larva_48well").arenas.rows == 6
