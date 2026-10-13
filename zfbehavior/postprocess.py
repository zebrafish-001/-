"""Trajectory cleaning and kinematics (per track)."""
from __future__ import annotations

import math
from typing import Dict, Optional

import numpy as np
import pandas as pd

from .arenas import Arena
from .config import PostprocessConfig


def jump_filter(x: np.ndarray, y: np.ndarray, max_step: float, reacquire: int = 3) -> np.ndarray:
    """Boolean mask of plausible points.

    A point is rejected when it is further from the last accepted point than
    ``max_step`` x (frames elapsed).  If ``reacquire`` consecutive rejected
    points are mutually consistent the animal is considered re-acquired there
    (protects against a wrong first detection locking the filter).
    """
    n = len(x)
    keep = np.isfinite(x) & np.isfinite(y)
    if not np.isfinite(max_step) or n == 0:
        return keep
    xs, ys = x.tolist(), y.tolist()
    ok = keep.tolist()
    m2 = max_step * max_step
    last = -1
    cand = []
    for i in range(n):
        if not ok[i]:
            continue
        if last < 0:
            last = i
            continue
        g = i - last
        if (xs[i] - xs[last]) ** 2 + (ys[i] - ys[last]) ** 2 <= m2 * g * g:
            last, cand = i, []
            continue
        if cand:
            j = cand[-1]
            g2 = i - j
            if (xs[i] - xs[j]) ** 2 + (ys[i] - ys[j]) ** 2 <= m2 * g2 * g2:
                cand.append(i)
            else:
                cand = [i]
        else:
            cand = [i]
        ok[i] = False
        if len(cand) >= reacquire:
            for j in cand:
                ok[j] = True
            last, cand = cand[-1], []
    return np.asarray(ok, bool)


def nan_runs(valid: np.ndarray):
    """(start, end) index pairs of runs where valid is False (end exclusive)."""
    m = np.concatenate([[0], (~valid).astype(np.int8), [0]])
    d = np.diff(m)
    return np.flatnonzero(d == 1), np.flatnonzero(d == -1)


def interpolate_gaps(v: np.ndarray, max_gap: int) -> np.ndarray:
    """Linearly fill interior NaN gaps of length <= max_gap."""
    v = v.astype(float).copy()
    ok = np.isfinite(v)
    if max_gap <= 0 or ok.sum() < 2:
        return v
    idx = np.arange(len(v))
    filled = np.interp(idx, idx[ok], v[ok])
    for s, e in zip(*nan_runs(ok)):
        if s > 0 and e < len(v) and e - s <= max_gap:
            v[s:e] = filled[s:e]
    return v


def rolling_mean(v: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return v
    out = pd.Series(v).rolling(window, center=True, min_periods=1).mean().to_numpy().copy()
    out[~np.isfinite(v)] = np.nan
    return out


def min_distance_filter(x: np.ndarray, y: np.ndarray, threshold: float):
    """Hold the position until the animal moved >= threshold from the held point."""
    if threshold <= 0:
        return x.copy(), y.copy()
    xs, ys = x.tolist(), y.tolist()
    xf, yf = [math.nan] * len(xs), [math.nan] * len(xs)
    hx = hy = math.nan
    t2 = threshold * threshold
    for i in range(len(xs)):
        xi, yi = xs[i], ys[i]
        if xi != xi:  # NaN: re-anchor after the gap
            hx = hy = math.nan
            continue
        if hx != hx or (xi - hx) ** 2 + (yi - hy) ** 2 >= t2:
            hx, hy = xi, yi
        xf[i], yf[i] = hx, hy
    return np.asarray(xf), np.asarray(yf)


def angle_diff(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Signed smallest difference a - b in degrees, in (-180, 180]."""
    d = (np.asarray(a) - np.asarray(b) + 180.0) % 360.0 - 180.0
    return np.where(d == -180.0, 180.0, d)


def fix_heading(heading: np.ndarray, conf: np.ndarray, threshold: float) -> np.ndarray:
    """Flip low-confidence head directions to be continuous with the previous frame."""
    h = heading.tolist()
    c = conf.tolist()
    prev = math.nan
    for i in range(len(h)):
        hi = h[i]
        if hi != hi:
            continue
        if c[i] < threshold and prev == prev:
            d = (hi - prev + 180.0) % 360.0 - 180.0
            if abs(d) > 90.0:
                hi = (hi + 180.0) % 360.0
                h[i] = hi
        prev = hi
    return np.asarray(h, float)


def process_track(raw: Dict[str, np.ndarray], arena: Arena, dt: float,
                  cfg: PostprocessConfig) -> Dict[str, np.ndarray]:
    """Clean one track and compute per-frame kinematics.

    raw must contain x_px, y_px, heading_deg, heading_conf arrays (frame order).
    """
    ppm = arena.px_per_mm or 1.0
    x0, y0 = raw["x_px"].astype(float), raw["y_px"].astype(float)
    detected = np.isfinite(x0)
    keep = jump_filter(x0, y0, cfg.max_speed_mm_s * ppm * dt)
    x = np.where(keep, x0, np.nan)
    y = np.where(keep, y0, np.nan)
    max_gap = int(round(cfg.max_gap_s / dt))
    x, y = interpolate_gaps(x, max_gap), interpolate_gaps(y, max_gap)
    valid = np.isfinite(x)
    interpolated = valid & ~keep
    w = int(round(cfg.smooth_window_s / dt))
    x, y = rolling_mean(x, w), rolling_mean(y, w)
    xf, yf = min_distance_filter(x, y, cfg.min_distance_moved_mm * ppm)
    step_px = np.hypot(np.diff(xf, prepend=np.nan), np.diff(yf, prepend=np.nan))
    step_mm = step_px / ppm
    if len(step_mm):
        step_mm[0] = 0.0 if valid[0] else np.nan
    speed = step_mm / dt
    heading = np.where(keep, raw["heading_deg"].astype(float), np.nan)
    heading = fix_heading(heading, np.nan_to_num(raw["heading_conf"].astype(float)),
                          cfg.heading_conf_threshold)
    dh = angle_diff(heading, np.roll(heading, 1))
    if len(dh):
        dh[0] = np.nan
    cx, cy = arena.center
    return {
        "x_px": x, "y_px": y,
        "x_mm": (x - cx) / ppm, "y_mm": (y - cy) / ppm,
        "detected": detected, "valid": valid, "interpolated": interpolated,
        "step_mm": step_mm, "speed_mm_s": speed,
        "heading_deg": heading, "dheading_deg": dh, "ang_vel_deg_s": dh / dt,
        "dist_wall_mm": arena.dist_to_wall_px(x, y) / ppm,
    }
