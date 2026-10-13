"""Arenas (wells / tanks): geometry, masks, auto-detection of well plates."""
from __future__ import annotations

import string
import warnings
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple

import cv2
import numpy as np
from matplotlib.path import Path as MplPath

from .config import ArenaConfig, CalibrationConfig


class ArenaError(RuntimeError):
    pass


@dataclass
class Arena:
    id: str
    shape: str                      # circle | rect | polygon
    params: dict                    # circle: cx, cy, r; rect: x, y, w, h; polygon: points
    px_per_mm: Optional[float] = None
    row: Optional[int] = None       # plate position (0-based), if any
    col: Optional[int] = None
    meta: dict = field(default_factory=dict)

    # -- geometry -----------------------------------------------------------
    @property
    def center(self) -> Tuple[float, float]:
        p = self.params
        if self.shape == "circle":
            return p["cx"], p["cy"]
        if self.shape == "rect":
            return p["x"] + p["w"] / 2, p["y"] + p["h"] / 2
        pts = np.asarray(p["points"], float)
        return float(pts[:, 0].mean()), float(pts[:, 1].mean())

    @property
    def bbox(self) -> Tuple[float, float, float, float]:
        """(x0, y0, x1, y1) in px."""
        p = self.params
        if self.shape == "circle":
            return p["cx"] - p["r"], p["cy"] - p["r"], p["cx"] + p["r"], p["cy"] + p["r"]
        if self.shape == "rect":
            return p["x"], p["y"], p["x"] + p["w"], p["y"] + p["h"]
        pts = np.asarray(p["points"], float)
        return pts[:, 0].min(), pts[:, 1].min(), pts[:, 0].max(), pts[:, 1].max()

    def scaled(self, s: float) -> "Arena":
        """Copy shrunk/grown around the centre by factor s."""
        if s == 1.0:
            return self
        p = dict(self.params)
        cx, cy = self.center
        if self.shape == "circle":
            p["r"] = p["r"] * s
        elif self.shape == "rect":
            p["w"], p["h"] = p["w"] * s, p["h"] * s
            p["x"], p["y"] = cx - p["w"] / 2, cy - p["h"] / 2
        else:
            pts = np.asarray(p["points"], float)
            p["points"] = (np.array([cx, cy]) + (pts - [cx, cy]) * s).tolist()
        return Arena(self.id, self.shape, p, self.px_per_mm, self.row, self.col, dict(self.meta))

    def outline(self, n: int = 90) -> np.ndarray:
        """Closed outline as (k, 2) array of px coordinates."""
        p = self.params
        if self.shape == "circle":
            t = np.linspace(0, 2 * np.pi, n)
            return np.c_[p["cx"] + p["r"] * np.cos(t), p["cy"] + p["r"] * np.sin(t)]
        if self.shape == "rect":
            x0, y0, x1, y1 = self.bbox
            return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]], float)
        pts = np.asarray(p["points"], float)
        return np.vstack([pts, pts[:1]])

    def draw(self, img: np.ndarray, value, thickness: int = -1) -> None:
        """Rasterise the arena into img (filled when thickness=-1)."""
        p = self.params
        sh = 4  # sub-pixel precision for cv2 drawing
        if self.shape == "circle":
            c = (int(round(p["cx"] * 16)), int(round(p["cy"] * 16)))
            cv2.circle(img, c, int(round(p["r"] * 16)), value, thickness, cv2.LINE_8, sh)
        else:
            pts = np.round(self.outline()[:-1] * 16).astype(np.int32)
            if thickness < 0:
                cv2.fillPoly(img, [pts], value, cv2.LINE_8, sh)
            else:
                cv2.polylines(img, [pts], True, value, thickness, cv2.LINE_8, sh)

    def mask(self, shape_hw: Tuple[int, int]) -> np.ndarray:
        m = np.zeros(shape_hw, np.uint8)
        self.draw(m, 255)
        return m > 0

    def contains(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        x, y = np.asarray(x, float), np.asarray(y, float)
        p = self.params
        if self.shape == "circle":
            return (x - p["cx"]) ** 2 + (y - p["cy"]) ** 2 <= p["r"] ** 2
        if self.shape == "rect":
            x0, y0, x1, y1 = self.bbox
            return (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)
        ok = np.isfinite(x) & np.isfinite(y)
        out = np.zeros(x.shape, bool)
        out[ok] = MplPath(np.asarray(p["points"], float)).contains_points(np.c_[x[ok], y[ok]])
        return out

    def dist_to_wall_px(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Distance from (x, y) to the arena border (positive inside)."""
        x, y = np.asarray(x, float), np.asarray(y, float)
        p = self.params
        if self.shape == "circle":
            return p["r"] - np.hypot(x - p["cx"], y - p["cy"])
        if self.shape == "rect":
            x0, y0, x1, y1 = self.bbox
            return np.minimum.reduce([x - x0, x1 - x, y - y0, y1 - y])
        pts = np.asarray(p["points"], np.float32).reshape(-1, 1, 2)
        out = np.full(x.shape, np.nan)
        for i in np.flatnonzero(np.isfinite(x) & np.isfinite(y)):
            out[i] = cv2.pointPolygonTest(pts, (float(x[i]), float(y[i])), True)
        return out

    def normalized(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Position as fractions of the arena bounding box (0 = left/top, 1 = right/bottom)."""
        x0, y0, x1, y1 = self.bbox
        return (np.asarray(x, float) - x0) / (x1 - x0), (np.asarray(y, float) - y0) / (y1 - y0)

    # -- (de)serialisation --------------------------------------------------
    def to_dict(self) -> dict:
        return {"id": self.id, "shape": self.shape, "params": self.params,
                "px_per_mm": self.px_per_mm, "row": self.row, "col": self.col, "meta": self.meta}

    @classmethod
    def from_dict(cls, d: dict) -> "Arena":
        return cls(d["id"], d["shape"], d["params"], d.get("px_per_mm"),
                   d.get("row"), d.get("col"), d.get("meta") or {})


# ----------------------------------------------------------------------------
# construction

def well_name(row: int, col: int) -> str:
    letters = string.ascii_uppercase
    r = letters[row] if row < 26 else letters[row // 26 - 1] + letters[row % 26]
    return f"{r}{col + 1}"


def _plate_from_grid(origin, col_vec, row_vec, radius, rows, cols) -> List[Arena]:
    arenas = []
    for r in range(rows):
        for c in range(cols):
            cx, cy = np.asarray(origin) + c * np.asarray(col_vec) + r * np.asarray(row_vec)
            arenas.append(Arena(well_name(r, c), "circle",
                                {"cx": float(cx), "cy": float(cy), "r": float(radius)},
                                row=r, col=c))
    return arenas


def _cluster_1d(values: np.ndarray, gap: float) -> np.ndarray:
    """Label sorted 1-D values into clusters separated by > gap."""
    order = np.argsort(values)
    labels = np.empty(len(values), int)
    labels[order] = np.concatenate([[0], np.cumsum(np.diff(values[order]) > gap)])
    return labels


def detect_plate(background: np.ndarray, rows: int, cols: int,
                 min_radius: Optional[float] = None, max_radius: Optional[float] = None,
                 param2: float = 30.0) -> Tuple[List[Arena], np.ndarray]:
    """Detect a rows x cols well plate in a background image.

    Circles are found with the Hough transform, assigned to grid positions and
    an affine grid (origin + column/row vectors) is fitted by least squares,
    so a few missed or spurious circles do not matter.
    Returns the arenas and the raw detected circles (n, 3).
    """
    h, w = background.shape[:2]
    pitch0 = min(w / cols, h / rows)
    min_r = int(min_radius or max(4, 0.12 * pitch0))
    max_r = int(max_radius or 0.6 * pitch0)
    img = cv2.GaussianBlur(background, (5, 5), 1.5)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp=1, minDist=max(2 * min_r, 1.6 * min_r + 2),
                               param1=100, param2=param2, minRadius=min_r, maxRadius=max_r)
    if circles is None:
        raise ArenaError("no wells found by Hough transform; set arenas.first_center/"
                         "last_center/radius_px manually or tune min/max_radius_px")
    circles = circles[0]
    med_r = np.median(circles[:, 2])
    circles = circles[np.abs(circles[:, 2] - med_r) < 0.25 * med_r]
    if len(circles) < max(4, 0.3 * rows * cols):
        raise ArenaError(f"only {len(circles)} wells detected for a {rows}x{cols} plate; "
                         "tune arenas.hough_param2 / radius limits or define the grid manually")
    xy = circles[:, :2].astype(float)
    # pitch and rotation from nearest-neighbour vectors
    d = np.linalg.norm(xy[:, None] - xy[None], axis=2)
    np.fill_diagonal(d, np.inf)
    nn = d.argmin(1)
    pitch = float(np.median(d[np.arange(len(xy)), nn]))
    vec = xy[nn] - xy
    ang = np.arctan2(vec[:, 1], vec[:, 0]) % (np.pi / 2)
    ang = np.where(ang > np.pi / 4, ang - np.pi / 2, ang)
    theta = float(np.median(ang))
    rot = np.array([[np.cos(-theta), -np.sin(-theta)], [np.sin(-theta), np.cos(-theta)]])
    xr = xy @ rot.T
    col_lab = _cluster_1d(xr[:, 0], 0.5 * pitch)
    row_lab = _cluster_1d(xr[:, 1], 0.5 * pitch)
    # convert cluster labels to integer grid indices using the pitch
    col_pos = np.array([xr[col_lab == k, 0].mean() for k in range(col_lab.max() + 1)])
    row_pos = np.array([xr[row_lab == k, 1].mean() for k in range(row_lab.max() + 1)])
    col_idx = np.round((col_pos - col_pos.min()) / pitch).astype(int)[col_lab]
    row_idx = np.round((row_pos - row_pos.min()) / pitch).astype(int)[row_lab]
    # choose the rows x cols window that contains most detections
    best = None
    for c0 in range(0, max(1, col_idx.max() - cols + 2)):
        for r0 in range(0, max(1, row_idx.max() - rows + 2)):
            inside = (col_idx >= c0) & (col_idx < c0 + cols) & (row_idx >= r0) & (row_idx < r0 + rows)
            if best is None or inside.sum() > best[0]:
                best = (inside.sum(), c0, r0, inside)
    _, c0, r0, inside = best
    cc, rr, pts = col_idx[inside] - c0, row_idx[inside] - r0, xy[inside]
    if cc.max() < cols - 1 or rr.max() < rows - 1:
        warnings.warn(f"detected wells span only {rr.max() + 1}x{cc.max() + 1} of the "
                      f"{rows}x{cols} plate; outer wells are extrapolated, check the preview")
    for _ in range(2):  # least-squares affine grid with one outlier-rejection pass
        A = np.c_[np.ones(len(cc)), cc, rr]
        coef, *_ = np.linalg.lstsq(A, pts, rcond=None)
        resid = np.linalg.norm(A @ coef - pts, axis=1)
        keep = resid < 0.25 * pitch
        if keep.all() or keep.sum() < 4:
            break
        cc, rr, pts = cc[keep], rr[keep], pts[keep]
    origin, col_vec, row_vec = coef
    radius = float(np.median(circles[inside][:, 2]))
    return _plate_from_grid(origin, col_vec, row_vec, radius, rows, cols), circles


def build_arenas(cfg: ArenaConfig, calib: CalibrationConfig,
                 background: Optional[np.ndarray], frame_shape: Tuple[int, int]) -> List[Arena]:
    h, w = frame_shape
    t = cfg.type
    if t == "plate":
        if cfg.first_center and cfg.last_center and cfg.radius_px:
            f, l = np.asarray(cfg.first_center, float), np.asarray(cfg.last_center, float)
            col_vec = [(l[0] - f[0]) / max(cfg.cols - 1, 1), 0.0]
            row_vec = [0.0, (l[1] - f[1]) / max(cfg.rows - 1, 1)]
            arenas = _plate_from_grid(f, col_vec, row_vec, cfg.radius_px, cfg.rows, cfg.cols)
        elif cfg.auto_detect:
            if background is None:
                raise ArenaError("plate auto-detection needs a background image")
            arenas, _ = detect_plate(background, cfg.rows, cfg.cols, cfg.min_radius_px,
                                     cfg.max_radius_px, cfg.hough_param2)
            if cfg.radius_px:
                for a in arenas:
                    a.params["r"] = float(cfg.radius_px)
        else:
            raise ArenaError("plate arenas need auto_detect: true or first_center/last_center/radius_px")
    elif t == "circles":
        if not cfg.circles:
            raise ArenaError("arenas.circles is empty")
        arenas = [Arena(f"arena{i + 1}", "circle", {"cx": float(c[0]), "cy": float(c[1]), "r": float(c[2])})
                  for i, c in enumerate(cfg.circles)]
    elif t == "rects":
        if not cfg.rects:
            raise ArenaError("arenas.rects is empty")
        arenas = [Arena(f"arena{i + 1}", "rect", {"x": float(r[0]), "y": float(r[1]),
                                                  "w": float(r[2]), "h": float(r[3])})
                  for i, r in enumerate(cfg.rects)]
    elif t == "polygons":
        if not cfg.polygons:
            raise ArenaError("arenas.polygons is empty")
        arenas = [Arena(f"arena{i + 1}", "polygon", {"points": [list(map(float, p)) for p in poly]})
                  for i, poly in enumerate(cfg.polygons)]
    else:  # full_frame
        m = cfg.margin_px
        arenas = [Arena("arena1", "rect", {"x": float(m), "y": float(m),
                                           "w": float(w - 2 * m), "h": float(h - 2 * m)})]
    if cfg.ids:
        if len(cfg.ids) != len(arenas):
            raise ArenaError(f"arenas.ids has {len(cfg.ids)} names for {len(arenas)} arenas")
        for a, name in zip(arenas, cfg.ids):
            a.id = str(name)
    if len({a.id for a in arenas}) != len(arenas):
        raise ArenaError("arena ids must be unique")
    calibrate(arenas, cfg.size_mm, calib.px_per_mm)
    return arenas


def calibrate(arenas: Sequence[Arena], size_mm, px_per_mm: Optional[float]) -> None:
    """Set px_per_mm on every arena (explicit value wins over physical size)."""
    if px_per_mm:
        for a in arenas:
            a.px_per_mm = float(px_per_mm)
        return
    if size_mm is None:
        warnings.warn("no calibration (calibration.px_per_mm or arenas.size_mm): "
                      "distances are reported in pixels")
        for a in arenas:
            a.px_per_mm = None
        return
    vals = []
    for a in arenas:
        if a.shape == "circle":
            d = size_mm[0] if isinstance(size_mm, (list, tuple)) else size_mm
            vals.append(2 * a.params["r"] / float(d))
        elif a.shape == "rect":
            if isinstance(size_mm, (list, tuple)) and len(size_mm) == 2:
                vals.append(0.5 * (a.params["w"] / size_mm[0] + a.params["h"] / size_mm[1]))
            else:
                vals.append(a.params["w"] / float(size_mm))
        else:
            raise ArenaError("polygon arenas need calibration.px_per_mm")
    # identical wells: use the mean so small radius errors do not vary per well
    same = len({a.shape for a in arenas}) == 1 and arenas[0].shape == "circle"
    for a, v in zip(arenas, vals):
        a.px_per_mm = float(np.mean(vals)) if same else float(v)


def arena_label_image(arenas: Sequence[Arena], shape_hw: Tuple[int, int],
                      mask_scale: float = 1.0) -> np.ndarray:
    """int32 image: 0 = outside, i+1 = inside arena i. Borders between arenas are 0."""
    lab = np.zeros(shape_hw, np.int32)
    for i, a in enumerate(arenas):
        a.scaled(mask_scale).draw(lab, i + 1)
    for a in arenas:  # 1 px gap so touching arenas never form one blob
        a.scaled(mask_scale).draw(lab, 0, thickness=1)
    return lab
