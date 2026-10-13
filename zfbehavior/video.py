"""Thin wrapper around cv2.VideoCapture returning grayscale frames."""
from __future__ import annotations

from pathlib import Path
from typing import Iterator, Optional, Tuple

import cv2
import numpy as np


class VideoError(RuntimeError):
    pass


def to_gray(frame: np.ndarray) -> np.ndarray:
    if frame.ndim == 2:
        return frame
    if frame.shape[2] == 4:
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


class Video:
    def __init__(self, path, fps: Optional[float] = None):
        self.path = Path(path)
        if not self.path.exists() and "%" not in str(path):
            raise VideoError(f"video not found: {path}")
        self.cap = cv2.VideoCapture(str(path))
        if not self.cap.isOpened():
            raise VideoError(f"cannot open video: {path}")
        file_fps = self.cap.get(cv2.CAP_PROP_FPS) or 0.0
        self.fps = float(fps) if fps else float(file_fps)
        if not self.fps or not np.isfinite(self.fps) or self.fps <= 0:
            raise VideoError(
                f"{path}: frame rate unknown, set video.fps in the config")
        self.n_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._pos = 0

    @property
    def shape(self) -> Tuple[int, int]:
        return self.height, self.width

    @property
    def duration_s(self) -> float:
        return self.n_frames / self.fps if self.n_frames else float("nan")

    def frame_range(self, start_s: float = 0.0,
                    end_s: Optional[float] = None) -> Tuple[int, Optional[int]]:
        """Frame interval [start, end); end is None when the length is unknown."""
        start = max(0, int(round(start_s * self.fps)))
        end = None if end_s is None else int(round(end_s * self.fps))
        if self.n_frames:
            end = self.n_frames if end is None else min(end, self.n_frames)
            if start >= self.n_frames:
                raise VideoError(f"start_s={start_s} is beyond the end of the video")
        return start, end

    def read_frame(self, index: int) -> Optional[np.ndarray]:
        if index != self._pos:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ok, frame = self.cap.read()
        self._pos = index + 1 if ok else -1
        return to_gray(frame) if ok else None

    def iter_frames(self, start: int = 0, end: Optional[int] = None,
                    step: int = 1) -> Iterator[Tuple[int, np.ndarray]]:
        """Yield (frame_index, gray_frame) sequentially."""
        if start != self._pos:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        idx = start
        while end is None or idx < end:
            if (idx - start) % step:
                if not self.cap.grab():
                    break
            else:
                ok, frame = self.cap.read()
                if not ok:
                    break
                yield idx, to_gray(frame)
            idx += 1
        self._pos = idx

    def close(self) -> None:
        self.cap.release()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
