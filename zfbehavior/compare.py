"""Validation of our tracks against EthoVision raw exports (same trial)."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional, Tuple

import numpy as np
import pandas as pd

from .ethovision import EthoTrack, to_mm


def _interp_to(t_src: np.ndarray, v_src: np.ndarray, t_dst: np.ndarray, max_dt: float) -> np.ndarray:
    """Nearest-sample lookup of v_src at times t_dst (NaN if no sample within max_dt)."""
    ok = np.isfinite(v_src)
    t, v = t_src[ok], v_src[ok]
    out = np.full(len(t_dst), np.nan)
    if len(t) == 0:
        return out
    j = np.clip(np.searchsorted(t, t_dst), 1, len(t) - 1)
    left, right = j - 1, j
    use_left = np.abs(t_dst - t[left]) <= np.abs(t[right] - t_dst)
    k = np.where(use_left, left, right)
    near = np.abs(t[k] - t_dst) <= max_dt
    out[near] = v[k[near]]
    return out


def _fit_axis(a: np.ndarray, b: np.ndarray) -> Tuple[float, float, float, float]:
    """b ~ s*a + o. Returns (s, o, r, rms_residual)."""
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 10:
        return np.nan, np.nan, np.nan, np.nan
    s, o = np.polyfit(a[ok], b[ok], 1)
    r = abs(float(np.corrcoef(a[ok], b[ok])[0, 1]))   # sign is absorbed by the scale (y flip)
    rms = float(np.sqrt(np.mean((s * a[ok] + o - b[ok]) ** 2)))
    return float(s), float(o), r, rms


@dataclass
class PositionComparison:
    n_ours: int
    n_etho: int
    n_both: int
    both_frac_of_etho: float
    ours_only: int           # we found the animal, EthoVision did not
    etho_only: int           # EthoVision found it, we did not
    x_scale: float           # cm (or EthoVision unit) per px fitted, x
    y_scale: float
    x_r: float
    y_r: float
    rms_px: float            # residual after linear alignment, in our pixels
    rms_unit: float          # ... in EthoVision units
    time_offset_s: float


def compare_positions(ours: pd.DataFrame, etho: EthoTrack, time_offset_s: float = 0.0,
                      max_dt: Optional[float] = None) -> PositionComparison:
    """Compare per-frame positions of one of our tracks with one EthoVision arena.

    ours: rows of our tracks table for a single track_id (time_s, x_px, y_px).
    A linear map per axis absorbs calibration, origin and y-axis direction;
    the residual RMS is the actual disagreement.
    """
    t = ours["time_s"].to_numpy(float) + time_offset_s
    x, y = ours["x_px"].to_numpy(float), ours["y_px"].to_numpy(float)
    te = etho.data["time_s"].to_numpy(float)
    dt = float(np.nanmedian(np.diff(te))) if len(te) > 1 else 0.04
    max_dt = max_dt if max_dt is not None else 0.6 * dt
    xe = _interp_to(te, etho.data["x"].to_numpy(float), t, max_dt)
    ye = _interp_to(te, etho.data["y"].to_numpy(float), t, max_dt)
    ours_ok, etho_ok = np.isfinite(x), np.isfinite(xe)
    sx, ox, rx, rmsx = _fit_axis(x, xe)
    sy, oy, ry, rmsy = _fit_axis(y, ye)
    both = ours_ok & etho_ok
    resid_unit = np.sqrt((sx * x[both] + ox - xe[both]) ** 2 + (sy * y[both] + oy - ye[both]) ** 2)
    scale = np.sqrt(abs(sx * sy)) if np.isfinite(sx) and np.isfinite(sy) else np.nan
    rms_unit = float(np.sqrt(np.mean(resid_unit ** 2))) if both.any() else np.nan
    n_etho = int(np.isfinite(etho.data["x"].to_numpy(float)).sum())
    return PositionComparison(
        n_ours=int(ours_ok.sum()), n_etho=n_etho, n_both=int(both.sum()),
        both_frac_of_etho=float(both.sum() / etho_ok.sum()) if etho_ok.any() else np.nan,
        ours_only=int((ours_ok & ~etho_ok).sum()), etho_only=int((~ours_ok & etho_ok).sum()),
        x_scale=sx, y_scale=sy, x_r=rx, y_r=ry,
        rms_px=rms_unit / scale if scale else np.nan, rms_unit=rms_unit,
        time_offset_s=time_offset_s)


def bin_distance(time_s: np.ndarray, dist: np.ndarray, bin_s: float, t0: float = 0.0) -> pd.DataFrame:
    """Sum per-sample distances into consecutive bins of bin_s starting at t0."""
    ok = np.isfinite(dist) & (time_s >= t0)
    k = np.floor((time_s[ok] - t0) / bin_s).astype(int)
    s = pd.Series(dist[ok]).groupby(k).sum()
    return pd.DataFrame({"bin": s.index + 1, "t_start_s": t0 + s.index * bin_s, "distance": s.to_numpy()})


def compare_distance_bins(ours: pd.DataFrame, etho: EthoTrack, bin_s: float = 60.0,
                          time_offset_s: float = 0.0) -> Tuple[pd.DataFrame, dict]:
    """Per-bin distance moved: ours (mm) vs EthoVision (converted to mm)."""
    t = ours["time_s"].to_numpy(float) + time_offset_s
    ours_b = bin_distance(t, ours["step_mm"].to_numpy(float), bin_s)
    etho_b = bin_distance(etho.data["time_s"].to_numpy(float), to_mm(etho, "distance"), bin_s)
    m = ours_b.merge(etho_b, on=["bin", "t_start_s"], suffixes=("_ours", "_etho"))
    a, b = m["distance_ours"].to_numpy(float), m["distance_etho"].to_numpy(float)
    ok = np.isfinite(a) & np.isfinite(b)
    stats = {"n_bins": int(ok.sum()), "r": np.nan, "slope": np.nan,
             "mean_ratio_ours_over_etho": np.nan, "mean_abs_rel_diff": np.nan}
    if ok.sum() >= 3:
        stats["r"] = float(np.corrcoef(a[ok], b[ok])[0, 1])
        stats["slope"] = float(np.polyfit(b[ok], a[ok], 1)[0])
        nz = ok & (b > 0)
        if nz.any():
            stats["mean_ratio_ours_over_etho"] = float(np.mean(a[nz] / b[nz]))
            stats["mean_abs_rel_diff"] = float(np.mean(np.abs(a[nz] - b[nz]) / b[nz]))
    return m, stats


def comparison_report(pos: PositionComparison, bins_stats: dict) -> str:
    d = asdict(pos)
    lines = ["Position agreement (after linear alignment):",
             f"  frames ours/etho/both: {d['n_ours']} / {d['n_etho']} / {d['n_both']} "
             f"({d['both_frac_of_etho']:.1%} of EthoVision samples matched)",
             f"  ours-only {d['ours_only']}, etho-only {d['etho_only']}",
             f"  correlation x {d['x_r']:.4f}, y {d['y_r']:.4f}; residual RMS {d['rms_px']:.2f} px "
             f"({d['rms_unit']:.4f} EthoVision units); scale {d['x_scale']:.5f}, {d['y_scale']:.5f} unit/px",
             "Distance per bin:",
             f"  n={bins_stats['n_bins']}, r={bins_stats['r']:.4f}, slope(ours vs etho)={bins_stats['slope']:.3f}, "
             f"mean ratio={bins_stats['mean_ratio_ours_over_etho']:.3f}, "
             f"mean |rel diff|={bins_stats['mean_abs_rel_diff']:.1%}"]
    return "\n".join(lines)
