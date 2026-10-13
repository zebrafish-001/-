import numpy as np
import pandas as pd

from zfbehavior.compare import compare_distance_bins, compare_positions
from zfbehavior.ethovision import EthoTrack, read_raw_export, to_mm


def write_export(path, delim=",", decimal=".", xlsx=False):
    t = np.arange(0, 2.0, 0.04)
    amp = 0.1 + 0.4 * (t // 0.5)              # speed differs between 0.5 s bins
    x = 1.0 + amp * np.sin(6 * t)
    y = -0.5 + amp * np.cos(6 * t)
    header = [
        ["Number of header lines:", "8"],
        ["Experiment", "VMR test"],
        ["Trial name", "Trial     3"],
        ["Arena name", "Arena 12"],
        ["Subject name", "A12"],
        ["Trial time", "Recording time", "X center", "Y center", "Area", "Distance moved",
         "Velocity", "Movement(Moving / Center-point)", "In zone(center / Center-point)"],
        ["s", "s", "cm", "cm", "cm²", "cm", "cm/s", "-", "-"],
    ]
    rows = []
    for i, ti in enumerate(t):
        if i == 5:
            rows.append([f"{ti:.3f}", f"{ti:.3f}", "-", "-", "-", "-", "-", "-", "-"])
            continue
        d = 0.0 if i == 0 else float(np.hypot(x[i] - x[i - 1], y[i] - y[i - 1]))
        rows.append([f"{ti:.3f}", f"{ti:.3f}", f"{x[i]:.4f}", f"{y[i]:.4f}", "0.0123",
                     f"{d:.5f}", f"{d / 0.04:.4f}", "1", "0"])
    if xlsx:
        pd.DataFrame(header + rows).to_excel(path, header=False, index=False)
        return t, x, y
    with open(path, "w", encoding="utf-8") as fh:
        for r in header + rows:
            cells = [c.replace(".", decimal) if decimal != "." and c[:1].lstrip("-").isdigit() else c
                     for c in r]
            fh.write(delim.join(f'"{c}"' for c in cells) + "\n")
    return t, x, y


def test_read_txt_comma(tmp_path):
    p = tmp_path / "Raw data-VMR-Trial 3-Arena 12.txt"
    t, x, y = write_export(p)
    tr = read_raw_export(p)
    assert tr.trial == "Trial     3" and tr.arena == "Arena 12" and tr.subject == "A12"
    assert tr.units["x"] == "cm" and tr.columns["distance"] == "Distance moved"
    assert "movement_moving" in tr.data and "in_zone_center" in tr.data
    assert len(tr.data) == len(t)
    assert np.isnan(tr.data["x"].iloc[5]) and np.isclose(tr.data["x"].iloc[6], x[6], atol=1e-4)
    assert np.isclose(tr.sample_rate, 25.0)
    assert np.allclose(to_mm(tr, "x")[6:], tr.data["x"].to_numpy()[6:] * 10)


def test_read_semicolon_decimal_comma(tmp_path):
    p = tmp_path / "raw.txt"
    t, x, y = write_export(p, delim=";", decimal=",")
    tr = read_raw_export(p)
    assert np.isclose(tr.data["y"].iloc[1], y[1], atol=1e-4)


def test_read_xlsx(tmp_path):
    p = tmp_path / "raw.xlsx"
    t, x, y = write_export(p, xlsx=True)
    tr = read_raw_export(p)
    assert np.isclose(tr.data["x"].iloc[10], x[10], atol=1e-4)


def test_compare(tmp_path):
    p = tmp_path / "raw.txt"
    t, x, y = write_export(p)
    tr = read_raw_export(p)
    # our track: same motion in px, y axis flipped, origin shifted, 1 missing frame
    ppm = 12.0
    ours = pd.DataFrame({"time_s": t, "x_px": 100 + x * 10 * ppm, "y_px": 300 - y * 10 * ppm})
    ours.loc[20, ["x_px", "y_px"]] = np.nan
    ours["step_mm"] = np.hypot(ours.x_px.diff(), ours.y_px.diff()) / ppm
    pc = compare_positions(ours, tr)
    assert pc.x_r > 0.999 and pc.y_r > 0.999
    assert pc.rms_px < 0.05 and pc.y_scale < 0
    assert pc.ours_only == 1 and pc.etho_only == 1
    m, st = compare_distance_bins(ours, tr, bin_s=0.5)
    assert st["n_bins"] == 4 and st["r"] > 0.99 and abs(st["mean_ratio_ours_over_etho"] - 1) < 0.1
