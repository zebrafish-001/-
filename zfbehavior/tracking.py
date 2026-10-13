"""Background-subtraction detection and per-arena tracking."""
from __future__ import annotations

import math
import sys
import time
from dataclasses import dataclass
from typing import Callable, List, Optional

import cv2
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

from .arenas import Arena, arena_label_image, build_arenas
from .background import compute_background, difference, estimate_threshold
from .config import Config, DetectionConfig
from .video import Video

FIELDS = ["x_px", "y_px", "area_px", "length_px", "heading_deg", "heading_conf"]
NF = len(FIELDS)


def blob_features(diff: np.ndarray, labels: np.ndarray, i: int, stat: np.ndarray) -> np.ndarray:
    """Intensity-weighted centroid, size, body axis and head direction of blob i.

    The body axis comes from the second central moments.  The head end is
    resolved from the third moment along the axis: the thin tail makes the
    weight distribution skewed towards the tail, so the head points the other way.
    ``heading_deg`` uses the maths convention (0 = right, 90 = up in the image).
    """
    x, y, w, h, area = (int(v) for v in stat[:5])
    roi = diff[y:y + h, x:x + w].astype(np.float32)
    roi[labels[y:y + h, x:x + w] != i] = 0
    m = cv2.moments(roi)
    m00 = m["m00"]
    if m00 <= 0:
        return np.full(NF, np.nan)
    cx, cy = x + m["m10"] / m00, y + m["m01"] / m00
    mu20, mu02, mu11 = m["mu20"] / m00, m["mu02"] / m00, m["mu11"] / m00
    theta = 0.5 * math.atan2(2 * mu11, mu20 - mu02)
    l1 = (mu20 + mu02) / 2 + math.sqrt(((mu20 - mu02) / 2) ** 2 + mu11 ** 2)
    length = 4 * math.sqrt(max(l1, 0.0))
    c, s = math.cos(theta), math.sin(theta)
    m3 = (m["mu30"] * c ** 3 + 3 * m["mu21"] * c * c * s
          + 3 * m["mu12"] * c * s * s + m["mu03"] * s ** 3) / m00
    skew = m3 / l1 ** 1.5 if l1 > 1e-9 else 0.0
    sign = -1.0 if skew > 0 else 1.0
    heading = math.degrees(math.atan2(-sign * s, sign * c)) % 360.0
    return np.array([cx, cy, area, length, heading, abs(skew)])


class Detector:
    """Finds candidate animals in each arena of a frame."""

    def __init__(self, arenas: List[Arena], shape_hw, background: np.ndarray,
                 det: DetectionConfig, threshold: float, mask_scale: float = 1.0):
        self.arenas = arenas
        self.bg = background
        self.det = det
        self.threshold = float(threshold)
        self.label_img = arena_label_image(arenas, shape_hw, mask_scale)
        self.union = np.where(self.label_img > 0, 255, 0).astype(np.uint8)
        k = det.blur_ksize
        self.blur = (k | 1, k | 1) if k and k > 1 else None
        self.k_open = (cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (det.morph_open_px,) * 2)
                       if det.morph_open_px > 1 else None)
        self.k_close = (cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (det.morph_close_px,) * 2)
                        if det.morph_close_px > 1 else None)

    def diff(self, gray: np.ndarray) -> np.ndarray:
        d = difference(gray, self.bg, self.det.polarity)
        if self.blur:
            d = cv2.GaussianBlur(d, self.blur, 0)
        return d

    def binary(self, diff: np.ndarray) -> np.ndarray:
        _, b = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)
        b = cv2.bitwise_and(b, self.union)
        if self.k_open is not None:
            b = cv2.morphologyEx(b, cv2.MORPH_OPEN, self.k_open)
        if self.k_close is not None:
            b = cv2.bitwise_and(cv2.morphologyEx(b, cv2.MORPH_CLOSE, self.k_close), self.union)
        return b

    def detect(self, gray: np.ndarray) -> List[np.ndarray]:
        """List (one per arena) of (k, NF) arrays, largest blob first, k <= animals_per_arena."""
        n_ar = len(self.arenas)
        out = [np.empty((0, NF))] * n_ar
        diff = self.diff(gray)
        n, labels, stats, cents = cv2.connectedComponentsWithStats(
            self.binary(diff), connectivity=8, ltype=cv2.CV_32S)
        if n <= 1:
            return out
        area = stats[1:, cv2.CC_STAT_AREA]
        comp = np.flatnonzero((area >= self.det.min_area_px) & (area <= self.det.max_area_px)) + 1
        if comp.size == 0:
            return out
        h, w = labels.shape
        cx = np.clip(np.round(cents[comp, 0]).astype(int), 0, w - 1)
        cy = np.clip(np.round(cents[comp, 1]).astype(int), 0, h - 1)
        ar = self.label_img[cy, cx]
        for j in np.flatnonzero(ar == 0):  # centroid fell outside (e.g. curved blob)
            x, y, bw, bh = stats[comp[j], :4]
            sub = self.label_img[y:y + bh, x:x + bw][labels[y:y + bh, x:x + bw] == comp[j]]
            sub = sub[sub > 0]
            ar[j] = np.bincount(sub).argmax() if sub.size else 0
        keep = ar > 0
        comp, ar = comp[keep], ar[keep]
        order = np.lexsort((-stats[comp, cv2.CC_STAT_AREA], ar))
        comp, ar = comp[order], ar[order]
        N = self.det.animals_per_arena
        per = {}
        for c, a in zip(comp, ar):
            lst = per.setdefault(a - 1, [])
            if len(lst) < N:
                lst.append(blob_features(diff, labels, c, stats[c]))
        for a, lst in per.items():
            out[a] = np.vstack(lst)
        return out


class ArenaTracker:
    """Keeps identities of several animals in one arena (Hungarian assignment)."""

    def __init__(self, n: int, max_step_px: float):
        self.n = n
        self.max_step = max_step_px
        self.last = np.full((n, 2), np.nan)
        self.age = np.zeros(n)

    def update(self, dets: np.ndarray) -> np.ndarray:
        out = np.full((self.n, NF), np.nan)
        self.age += 1
        if len(dets) == 0:
            return out
        known = np.isfinite(self.last[:, 0])
        cost = np.linalg.norm(self.last[:, None, :] - dets[None, :, :2], axis=2)
        cost[~known] = 1e9
        rows, cols = linear_sum_assignment(np.nan_to_num(cost, nan=1e9))
        used = set()
        for r, c in zip(rows, cols):
            if known[r] and cost[r, c] > self.max_step * self.age[r]:
                continue
            out[r] = dets[c]
            used.add(c)
        free = [c for c in range(len(dets)) if c not in used]
        empty = [r for r in range(self.n) if not known[r] and np.isnan(out[r, 0])]
        for r, c in zip(empty, free):  # initialise tracks that have never been seen
            out[r] = dets[c]
        ok = np.isfinite(out[:, 0])
        self.last[ok] = out[ok, :2]
        self.age[ok] = 0
        return out


@dataclass
class TrackingResult:
    raw: pd.DataFrame
    frames: pd.DataFrame
    arenas: List[Arena]
    background: np.ndarray
    info: dict


def track_ids(arenas: List[Arena], n_per_arena: int) -> List[tuple]:
    """[(track_id, arena_id, animal_index), ...] in output order."""
    out = []
    for a in arenas:
        for k in range(n_per_arena):
            out.append((a.id if n_per_arena == 1 else f"{a.id}_{k + 1}", a.id, k + 1))
    return out


def track_video(video_path, cfg: Config, progress: bool = True,
                log: Callable[[str], None] = lambda s: print(s, file=sys.stderr)) -> TrackingResult:
    t0 = time.time()
    video = Video(video_path, cfg.video.fps)
    start, end = video.frame_range(cfg.video.start_s, cfg.video.end_s)
    bg, samples = compute_background(video, cfg.background, start, end, cfg.detection.polarity)
    arenas = build_arenas(cfg.arenas, cfg.calibration, bg, video.shape)
    det = cfg.detection
    label = arena_label_image(arenas, video.shape, cfg.arenas.mask_scale)
    if det.threshold == "auto":
        thr, sigma = estimate_threshold(bg, samples, label > 0, det.auto_threshold_k,
                                        det.min_threshold, det.blur_ksize, det.polarity)
    else:
        thr, sigma = float(det.threshold), float("nan")
    detector = Detector(arenas, video.shape, bg, det, thr, cfg.arenas.mask_scale)
    N = det.animals_per_arena
    step = cfg.video.frame_step
    ppm = [a.px_per_mm for a in arenas]
    trackers = None
    if N > 1:
        max_step = [(cfg.postprocess.max_speed_mm_s * p * step / video.fps) if p else np.inf for p in ppm]
        trackers = [ArenaTracker(N, ms) for ms in max_step]
    n_tracks = len(arenas) * N
    data, frame_idx, intensity = [], [], []
    total = ((end or video.n_frames or 0) - start) // step if (end or video.n_frames) else 0
    last_report = time.time()
    if progress:
        log(f"[zfb] {video.path.name}: {len(arenas)} arenas, threshold={thr:.1f}, "
            f"~{total} frames to process")
    for idx, gray in video.iter_frames(start, end, step):
        dets = detector.detect(gray)
        row = np.full((n_tracks, NF), np.nan)
        for ai, d in enumerate(dets):
            if N == 1:
                if len(d):
                    row[ai] = d[0]
            else:
                row[ai * N:(ai + 1) * N] = trackers[ai].update(d)
        data.append(row.astype(np.float32))
        frame_idx.append(idx)
        intensity.append(float(gray[::4, ::4].mean()))
        if progress and time.time() - last_report > 10:
            last_report = time.time()
            done = len(frame_idx)
            rate = done / (last_report - t0)
            eta = f", ETA {(total - done) / rate / 60:.1f} min" if total else ""
            log(f"[zfb]   {done}/{total or '?'} frames ({rate:.0f} fps{eta})")
    video.close()
    if not data:
        raise RuntimeError(f"no frames read from {video_path}")
    arr = np.stack(data)                       # (frames, tracks, NF)
    frames = np.asarray(frame_idx)
    ids = track_ids(arenas, N)
    n_f = len(frames)
    raw = pd.DataFrame({
        "frame": np.repeat(frames, n_tracks),
        "time_s": np.repeat(frames / video.fps, n_tracks),
        "track_id": np.tile([t[0] for t in ids], n_f),
        "arena": np.tile([t[1] for t in ids], n_f),
        "animal": np.tile([t[2] for t in ids], n_f),
    })
    flat = arr.reshape(-1, NF)
    for j, name in enumerate(FIELDS):
        raw[name] = flat[:, j]
    frames_df = pd.DataFrame({"frame": frames, "time_s": frames / video.fps,
                              "mean_intensity": intensity,
                              "n_detected": np.isfinite(arr[:, :, 0]).sum(1)})
    info = {
        "video": str(video.path), "video_name": video.path.stem,
        "fps": video.fps, "width": video.width, "height": video.height,
        "n_frames_file": video.n_frames, "start_frame": int(frames[0]),
        "end_frame": int(frames[-1]) + 1, "frame_step": step,
        "n_processed": int(n_f), "threshold": float(thr), "noise_sigma": float(sigma),
        "animals_per_arena": N, "n_arenas": len(arenas),
        "processing_s": round(time.time() - t0, 2),
    }
    if progress:
        log(f"[zfb] {video.path.name}: tracked {n_f} frames in {info['processing_s']:.0f} s, "
            f"detection rate {np.isfinite(arr[:, :, 0]).mean():.1%}")
    return TrackingResult(raw, frames_df, arenas, bg, info)
