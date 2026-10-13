"""Synthetic zebrafish videos with ground truth, for testing and demos.

* ``make_larva_plate_video`` - top view of a multi-well plate, one larva per
  well, beat-and-glide swimming; activity depends on group and light/dark phase.
* ``make_adult_tank_video`` - side view of a novel tank; adult fish swim
  between way-points with a depth preference and occasional freezing.

The ground-truth position is the darkness-weighted centroid of the rendered
fish, i.e. what an ideal background-subtraction tracker should report.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import cv2
import numpy as np
import pandas as pd

from .arenas import well_name

SS = 4  # supersampling factor for anti-aliased rendering


def _render_fish(length_px: float, heading_deg: float, kind: str,
                 frac_x: float, frac_y: float) -> Tuple[np.ndarray, float, float]:
    """Render a fish into a small float 'darkness' patch (0..1).

    Returns (patch, ref_x, ref_y): the fish reference point lies at patch
    coordinates (ref_x, ref_y) (sub-pixel, includes frac offsets).
    """
    half = int(math.ceil(length_px * 0.75)) + 3
    size = 2 * half + 1
    big = np.zeros((size * SS, size * SS), np.uint8)
    L = length_px * SS
    cx = (half + frac_x) * SS + (SS - 1) / 2
    cy = (half + frac_y) * SS + (SS - 1) / 2
    th = math.radians(heading_deg)
    ux, uy = math.cos(th), -math.sin(th)      # head direction in image coords
    vx, vy = -uy, ux

    def pt(u, v):
        return (int(round((cx + u * L * ux + v * L * vx) * 16)),
                int(round((cy + u * L * uy + v * L * vy) * 16)))

    if kind == "larva":
        # tapering trunk/tail, then head and eyes (darkest)
        for u in np.linspace(-0.58, 0.18, 26):
            r = 0.012 + 0.058 * (u + 0.58) / 0.76
            val = int(110 + 80 * (u + 0.58) / 0.76)
            cv2.circle(big, pt(u, 0), int(r * L * 16), val, -1, cv2.LINE_AA, 4)
        cv2.ellipse(big, pt(0.28, 0), (int(0.15 * L * 16), int(0.10 * L * 16)),
                    -heading_deg, 0, 360, 200, -1, cv2.LINE_AA, 4)
        for side in (-1, 1):
            cv2.circle(big, pt(0.32, side * 0.06), int(0.045 * L * 16), 255, -1, cv2.LINE_AA, 4)
    else:  # adult, side view
        cv2.ellipse(big, pt(0.02, 0), (int(0.40 * L * 16), int(0.11 * L * 16)),
                    -heading_deg, 0, 360, 220, -1, cv2.LINE_AA, 4)
        cv2.ellipse(big, pt(0.28, 0), (int(0.14 * L * 16), int(0.09 * L * 16)),
                    -heading_deg, 0, 360, 245, -1, cv2.LINE_AA, 4)
        tail = np.array([pt(-0.36, 0), pt(-0.55, 0.11), pt(-0.50, 0), pt(-0.55, -0.11)], np.int32)
        cv2.fillPoly(big, [tail], 170, cv2.LINE_AA, 4)
    patch = cv2.resize(big, (size, size), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
    return patch, half + frac_x, half + frac_y


def _composite(frame: np.ndarray, patch: np.ndarray, x: float, y: float, ref: Tuple[float, float],
               fish_gray: float) -> Tuple[float, float]:
    """Darken frame with patch so that patch ref point lands on (x, y).

    Returns the darkness-weighted centroid of the fish in frame coordinates.
    """
    ix, iy = int(math.floor(x)), int(math.floor(y))
    half = (patch.shape[0] - 1) // 2
    x0, y0 = ix - half, iy - half
    h, w = frame.shape
    xa, ya = max(x0, 0), max(y0, 0)
    xb, yb = min(x0 + patch.shape[1], w), min(y0 + patch.shape[0], h)
    if xb <= xa or yb <= ya:
        return float("nan"), float("nan")
    p = patch[ya - y0:yb - y0, xa - x0:xb - x0]
    roi = frame[ya:yb, xa:xb]
    contrast = np.clip(roi - fish_gray, 0, None)
    roi -= p * contrast
    wgt = p * contrast
    s = wgt.sum()
    if s <= 0:
        return float("nan"), float("nan")
    gy, gx = np.mgrid[ya:yb, xa:xb]
    return float((wgt * gx).sum() / s), float((wgt * gy).sum() / s)


def _writer(path: Path, fps: float, w: int, h: int) -> cv2.VideoWriter:
    path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*("MJPG" if path.suffix.lower() == ".avi" else "mp4v"))
    wr = cv2.VideoWriter(str(path), fourcc, fps, (w, h), isColor=False)
    if not wr.isOpened():
        raise RuntimeError(f"cannot write video {path}")
    return wr


# ----------------------------------------------------------------------------
# larvae

def make_larva_plate_video(path, rows: int = 4, cols: int = 6, duration_s: float = 20.0,
                           fps: float = 25.0, px_per_mm: float = 8.0, well_mm: float = 15.6,
                           pitch_mm: float = 19.3, larva_mm: float = 4.0,
                           groups: Optional[Dict[str, Sequence[int]]] = None,
                           phases: Sequence[Tuple[str, float]] = (("light", 1e9),),
                           empty_wells: Sequence[str] = (), noise: float = 2.0,
                           seed: int = 0) -> Tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Write a plate video. Returns (ground_truth, metadata, info).

    groups maps group name -> list of plate columns (0-based).  Default: left
    half 'control', right half 'treated' (treated larvae are hypoactive).
    phases: sequence of (light|dark, duration_s), cycled until the end;
    larvae swim more in the dark (visual motor response).
    """
    rng = np.random.default_rng(seed)
    path = Path(path)
    if groups is None:
        groups = {"control": range(cols // 2), "treated": range(cols // 2, cols)}
    col_group = {c: g for g, cs in groups.items() for c in cs}
    pitch = pitch_mm * px_per_mm
    R = well_mm / 2 * px_per_mm
    margin = pitch * 0.75
    W = int(round(2 * margin + (cols - 1) * pitch)) // 2 * 2
    H = int(round(2 * margin + (rows - 1) * pitch)) // 2 * 2
    bg = np.full((H, W), 205.0, np.float32)
    bg += np.linspace(-8, 8, W)[None, :]                      # illumination gradient
    centers = {}
    for r in range(rows):
        for c in range(cols):
            cx, cy = margin + c * pitch, margin + r * pitch
            centers[well_name(r, c)] = (cx, cy, r, c)
            cv2.circle(bg, (int(cx * 16), int(cy * 16)), int(R * 16), 192, -1, cv2.LINE_AA, 4)
            cv2.circle(bg, (int(cx * 16), int(cy * 16)), int(R * 16), 120, 2, cv2.LINE_AA, 4)
    L = larva_mm * px_per_mm
    wr = _writer(path, fps, W, H)
    n_frames = int(round(duration_s * fps))
    sub = 4
    dts = 1.0 / (fps * sub)
    # per-larva state
    larvae = []
    for name, (cx, cy, r, c) in centers.items():
        if name in empty_wells:
            continue
        g = col_group.get(c, "control")
        rr = R - 0.45 * L
        a, d = rng.uniform(0, 2 * np.pi), rng.uniform(0, rr * 0.8)
        larvae.append(dict(well=name, group=g, cx=cx, cy=cy, rmax=rr, x=cx + d * np.cos(a),
                           y=cy + d * np.sin(a), h=rng.uniform(0, 360), next_bout=rng.exponential(1.0),
                           bout_t=-1.0, bout_T=0.0, bout_v=0.0, bout_turn=0.0, activity=rng.lognormal(0, 0.25)))
    phase_seq = list(phases)

    def light_at(t):
        tot = sum(d for _, d in phase_seq)
        t = t % tot
        for name, d in phase_seq:
            if t < d:
                return name
            t -= d
        return phase_seq[-1][0]

    gt = []
    for f in range(n_frames):
        t = f / fps
        lit = light_at(t)
        for _ in range(sub):
            for lv in larvae:
                if lv["bout_t"] < 0:
                    lv["next_bout"] -= dts
                    if lv["next_bout"] <= 0:
                        lv["bout_t"] = 0.0
                        lv["bout_T"] = rng.uniform(0.16, 0.28)
                        dist = rng.gamma(4, 0.5) * (0.7 if lv["group"] != "control" else 1.0)
                        lv["bout_v"] = dist * px_per_mm * math.pi / (2 * lv["bout_T"])
                        big = rng.random() < 0.3
                        lv["bout_turn"] = (rng.normal(90, 25) * rng.choice([-1, 1]) if big
                                           else rng.normal(0, 20))
                else:
                    T = lv["bout_T"]
                    ph = lv["bout_t"] / T
                    if ph < 0.3:
                        lv["h"] = (lv["h"] + lv["bout_turn"] * dts / (0.3 * T)) % 360
                    v = lv["bout_v"] * math.sin(math.pi * ph)
                    th = math.radians(lv["h"])
                    nx, ny = lv["x"] + v * math.cos(th) * dts, lv["y"] - v * math.sin(th) * dts
                    dx, dy = nx - lv["cx"], ny - lv["cy"]
                    rd = math.hypot(dx, dy)
                    if rd > lv["rmax"]:  # wall: slide along it and turn inwards
                        nx = lv["cx"] + dx / rd * lv["rmax"]
                        ny = lv["cy"] + dy / rd * lv["rmax"]
                        inward = math.degrees(math.atan2(dy, -dx))
                        lv["h"] = (inward + rng.normal(0, 40)) % 360
                    lv["x"], lv["y"] = nx, ny
                    lv["bout_t"] += dts
                    if lv["bout_t"] >= T:
                        lv["bout_t"] = -1.0
                        ibi = 1.1 if lv["group"] == "control" else 2.4
                        if lit == "dark":
                            ibi *= 0.45
                        lv["next_bout"] = rng.exponential(ibi / lv["activity"]) + 0.1
        frame = bg + rng.normal(0, noise, bg.shape).astype(np.float32)
        frame += rng.normal(0, 0.5)
        for lv in larvae:
            fx, fy = lv["x"] - math.floor(lv["x"]), lv["y"] - math.floor(lv["y"])
            patch, rx, ry = _render_fish(L, lv["h"], "larva", fx, fy)
            gx, gy = _composite(frame, patch, lv["x"], lv["y"], (rx, ry), 45.0)
            gt.append((f, t, lv["well"], gx, gy, lv["h"], lv["bout_t"] >= 0, lit))
        wr.write(np.clip(frame, 0, 255).astype(np.uint8))
    wr.release()
    gt_df = pd.DataFrame(gt, columns=["frame", "time_s", "arena", "x_px", "y_px", "heading_deg",
                                      "in_bout", "light"])
    meta = pd.DataFrame([{"arena": n, "group": ("empty" if n in empty_wells else col_group.get(c, "control"))}
                         for n, (_, _, r, c) in centers.items()])
    info = {"fps": fps, "px_per_mm": px_per_mm, "well_mm": well_mm, "rows": rows, "cols": cols,
            "width": W, "height": H, "radius_px": R,
            "first_center": list(centers[well_name(0, 0)][:2]),
            "last_center": list(centers[well_name(rows - 1, cols - 1)][:2])}
    return gt_df, meta, info


# ----------------------------------------------------------------------------
# adults

def make_adult_tank_video(path, duration_s: float = 30.0, fps: float = 25.0,
                          px_per_mm: float = 3.0, tank_mm: Tuple[float, float] = (250.0, 150.0),
                          fish_mm: float = 35.0, n_fish: int = 1, anxiety: float = 0.3,
                          noise: float = 2.0, seed: int = 0) -> Tuple[pd.DataFrame, dict]:
    """Side-view novel tank video.  anxiety in [0, 1]: higher = more bottom
    dwelling and freezing.  Returns (ground_truth, info)."""
    rng = np.random.default_rng(seed)
    path = Path(path)
    tw, th = tank_mm[0] * px_per_mm, tank_mm[1] * px_per_mm
    mx, my = 40, 30
    W, H = int(tw + 2 * mx) // 2 * 2, int(th + 2 * my) // 2 * 2
    bg = np.full((H, W), 95.0, np.float32)
    x0, y0 = mx, my
    yy = np.linspace(0, 1, int(th))[:, None]
    bg[y0:y0 + int(th), x0:x0 + int(tw)] = 222 - 14 * yy
    gravel_h = int(0.04 * th)
    gr = rng.normal(150, 18, (gravel_h, int(tw))).astype(np.float32)
    bg[y0 + int(th) - gravel_h:y0 + int(th), x0:x0 + int(tw)] = gr
    cv2.rectangle(bg, (x0, y0), (x0 + int(tw), y0 + int(th)), 60, 3)
    L = fish_mm * px_per_mm
    wr = _writer(path, fps, W, H)
    n_frames = int(round(duration_s * fps))
    marg = 0.35 * L
    xlo, xhi = x0 + marg, x0 + tw - marg
    ylo, yhi = y0 + marg * 0.6, y0 + th - gravel_h - marg * 0.6
    fish = []
    for k in range(n_fish):
        fish.append(dict(x=rng.uniform(xlo, xhi), y=yhi - rng.uniform(0, 0.2) * (yhi - ylo),
                         h=rng.choice([0.0, 180.0]), v=0.0, wx=None, wy=None, freeze=0.0))
    gt = []

    def new_waypoint(t):
        explore = min(1.0, t / max(duration_s * 0.6, 1e-6)) * (1 - anxiety)
        a = 1.0 + 4.0 * explore
        depth = rng.beta(a, 1.2)  # 1 = bottom
        return rng.uniform(xlo, xhi), ylo + depth * (yhi - ylo)

    dts = 1.0 / fps
    for f in range(n_frames):
        t = f * dts
        frame = bg + rng.normal(0, noise, bg.shape).astype(np.float32)
        for k, fi in enumerate(fish):
            if fi["freeze"] > 0:
                fi["freeze"] -= dts
                fi["v"] = 0.0
            else:
                if rng.random() < (0.02 + 0.10 * anxiety) * dts:
                    fi["freeze"] = rng.uniform(2.5, 6.0)
                if fi["wx"] is None or math.hypot(fi["wx"] - fi["x"], fi["wy"] - fi["y"]) < 8 * px_per_mm:
                    fi["wx"], fi["wy"] = new_waypoint(t)
                want = math.degrees(math.atan2(-(fi["wy"] - fi["y"]), fi["wx"] - fi["x"]))
                d = (want - fi["h"] + 180) % 360 - 180
                fi["h"] = (fi["h"] + np.clip(d, -200 * dts, 200 * dts) + rng.normal(0, 4)) % 360
                target_v = rng.lognormal(math.log(55), 0.25) * px_per_mm
                fi["v"] += (target_v - fi["v"]) * 0.15
                thr = math.radians(fi["h"])
                fi["x"] = float(np.clip(fi["x"] + fi["v"] * math.cos(thr) * dts, xlo, xhi))
                fi["y"] = float(np.clip(fi["y"] - fi["v"] * math.sin(thr) * dts, ylo, yhi))
            fx, fy = fi["x"] - math.floor(fi["x"]), fi["y"] - math.floor(fi["y"])
            patch, rx, ry = _render_fish(L, fi["h"], "adult", fx, fy)
            gx, gy = _composite(frame, patch, fi["x"], fi["y"], (rx, ry), 50.0)
            gt.append((f, t, k + 1, gx, gy, fi["h"], fi["freeze"] > 0))
        wr.write(np.clip(frame, 0, 255).astype(np.uint8))
    wr.release()
    gt_df = pd.DataFrame(gt, columns=["frame", "time_s", "animal", "x_px", "y_px", "heading_deg", "frozen"])
    info = {"fps": fps, "px_per_mm": px_per_mm, "tank_rect": [x0, y0, round(tw), round(th)],
            "tank_mm": list(tank_mm), "width": W, "height": H}
    return gt_df, info
