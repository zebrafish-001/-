"""Background model and noise estimate."""
from __future__ import annotations

from typing import List, Optional, Tuple

import cv2
import numpy as np

from .config import BackgroundConfig
from .video import Video, to_gray


def sample_indices(start: int, end: int, n: int) -> np.ndarray:
    n = max(1, min(n, end - start))
    return np.unique(np.linspace(start, end - 1, n).round().astype(int))


def compute_background(video: Video, cfg: BackgroundConfig, start: int,
                       end: Optional[int], polarity: str = "dark") -> Tuple[np.ndarray, List[np.ndarray]]:
    """Return (background, sample_frames).

    Frames spread over the analysed interval are combined pixel-wise:

    * ``auto``: for dark animals the 90th percentile (light animals: 10th),
      so an animal is removed unless it covers the same pixels in >90 % of
      the sampled frames - robust to animals that rest a lot;
    * ``median``: classic median background;
    * ``image``: a recorded empty-arena image.

    An animal that never moves becomes part of a computed background and
    cannot be detected - use ``background.method: image`` in that case.
    """
    if end is None:
        end = start + max(cfg.n_frames, 1) * 50
    samples = []
    for i in sample_indices(start, end, cfg.n_frames):
        f = video.read_frame(int(i))
        if f is not None:
            samples.append(f)
    if not samples:
        raise RuntimeError(f"could not read frames from {video.path}")
    if cfg.method == "image":
        img = cv2.imread(str(cfg.image), cv2.IMREAD_UNCHANGED)
        if img is None:
            raise FileNotFoundError(f"background image not readable: {cfg.image}")
        bg = to_gray(img)
        if bg.shape != samples[0].shape:
            raise ValueError(f"background image size {bg.shape} != video frame size {samples[0].shape}")
        return bg, samples
    stack = np.stack(samples)
    q = 50.0
    if cfg.method == "auto":
        q = {"dark": 90.0, "light": 10.0}.get(polarity, 50.0)
    bg = np.percentile(stack, q, axis=0, method="nearest").astype(np.uint8)
    return bg, samples


def difference(gray: np.ndarray, bg: np.ndarray, polarity: str) -> np.ndarray:
    if polarity == "dark":
        return cv2.subtract(bg, gray)
    if polarity == "light":
        return cv2.subtract(gray, bg)
    return cv2.absdiff(gray, bg)


def estimate_threshold(bg: np.ndarray, samples: List[np.ndarray], mask: np.ndarray,
                       k: float, min_threshold: float, blur_ksize: int = 0,
                       polarity: str = "dark") -> Tuple[float, float]:
    """Auto threshold = baseline + k * sigma (at least ``min_threshold``).

    sigma is the pixel noise, estimated robustly (MAD) from differences
    between sampled frames, so it is not inflated by a percentile background;
    baseline is the median frame-background difference (the offset that a
    percentile background introduces).  Animals cover few pixels and do not
    affect the medians.  Returns (threshold, sigma).
    """
    ks = (blur_ksize | 1, blur_ksize | 1) if blur_ksize and blur_ksize > 1 else None

    def prep(img):
        return cv2.GaussianBlur(img, ks, 0) if ks else img

    use = samples[: min(len(samples), 21)]
    pair, base = [], []
    for a, b in zip(use[:-1], use[1:]):
        d = prep(a).astype(np.int16) - prep(b).astype(np.int16)
        v = d[mask].astype(np.float32)
        pair.append(v - np.median(v))
    for f in use:
        base.append(np.median(difference(prep(f), prep(bg), polarity)[mask]))
    if pair:
        v = np.abs(np.concatenate(pair))
        sigma = float(np.median(v) / 0.6745 / np.sqrt(2))
    else:
        sigma = 0.0
    baseline = float(np.median(base)) if base else 0.0
    return max(float(min_threshold), baseline + k * sigma), sigma
