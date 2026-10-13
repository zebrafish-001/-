"""Configuration: typed dataclasses loaded from YAML presets / user files.

A user config may start with ``extends: <preset name or yaml path>``; the
preset is loaded first and the user values are deep-merged on top of it.
Unknown keys raise an error so that typos in YAML files are caught early.
"""
from __future__ import annotations

import copy
import dataclasses
import typing
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Union

import yaml

PRESET_DIR = Path(__file__).parent / "presets"


@dataclass
class VideoConfig:
    fps: Optional[float] = None          # override the fps stored in the file
    start_s: float = 0.0                 # analyse from this time (s)
    end_s: Optional[float] = None        # ... up to this time (s); None = end of video
    frame_step: int = 1                  # process every n-th frame


@dataclass
class ArenaConfig:
    # plate | circles | rects | polygons | full_frame
    type: str = "plate"
    rows: int = 8
    cols: int = 12
    auto_detect: bool = True
    # manual plate grid: centres of the first (A1) and last (e.g. H12) well, in px
    first_center: Optional[List[float]] = None
    last_center: Optional[List[float]] = None
    radius_px: Optional[float] = None
    # Hough circle detection tuning (plate auto-detection)
    min_radius_px: Optional[float] = None
    max_radius_px: Optional[float] = None
    hough_param2: float = 30.0
    circles: Optional[List[List[float]]] = None        # [[cx, cy, r], ...]
    rects: Optional[List[List[float]]] = None          # [[x, y, w, h], ...]
    polygons: Optional[List[List[List[float]]]] = None  # [[[x, y], ...], ...]
    ids: Optional[List[str]] = None
    # physical size used for calibration: circle diameter (mm) or rect [w, h] (mm)
    size_mm: Optional[Union[float, List[float]]] = None
    mask_scale: float = 1.0              # shrink (<1) / grow (>1) arena masks
    margin_px: int = 0                   # full_frame only: ignore this many border px


@dataclass
class CalibrationConfig:
    px_per_mm: Optional[float] = None    # overrides arenas.size_mm when set


@dataclass
class BackgroundConfig:
    method: str = "auto"                 # auto (polarity-aware percentile) | median | image
    n_frames: int = 60
    image: Optional[str] = None          # path to a pre-recorded background image


@dataclass
class DetectionConfig:
    polarity: str = "dark"               # dark (fish darker than bg) | light | both
    threshold: Union[float, str] = "auto"
    auto_threshold_k: float = 6.0        # auto threshold = k * robust noise sigma
    min_threshold: float = 8.0
    blur_ksize: int = 3
    morph_open_px: int = 0
    morph_close_px: int = 0
    min_area_px: int = 4
    max_area_px: int = 5000
    # when the arena is calibrated these take precedence over the px limits
    min_area_mm2: Optional[float] = None
    max_area_mm2: Optional[float] = None
    animals_per_arena: int = 1


@dataclass
class PostprocessConfig:
    max_speed_mm_s: float = 250.0        # faster apparent motion = tracking error
    max_gap_s: float = 0.4               # interpolate gaps up to this length
    smooth_window_s: float = 0.0         # rolling-mean smoothing of positions
    min_distance_moved_mm: float = 0.1   # jitter filter (EthoVision style MDM)
    heading_conf_threshold: float = 0.15


@dataclass
class ZoneConfig:
    name: str = "zones"
    # center_periphery | vertical_bands | horizontal_bands | polygon
    type: str = "center_periphery"
    center_fraction: float = 0.5         # center_periphery: inner radius / R
    edges: Optional[List[float]] = None  # band edges as fractions of arena size
    labels: Optional[List[str]] = None
    points: Optional[List[List[float]]] = None  # polygon in arena-normalised coords (0-1)


@dataclass
class PhaseConfig:
    name: str = "phase"
    start_s: float = 0.0
    end_s: float = 0.0


@dataclass
class PhaseCycleConfig:
    sequence: List[List[Any]] = field(default_factory=list)  # [[light, 600], [dark, 600]]
    repeat: int = 1
    start_s: float = 0.0


@dataclass
class EventConfig:
    name: str = "event"
    time_s: float = 0.0


@dataclass
class EventSeriesConfig:
    name: str = "stim"
    start_s: float = 0.0
    interval_s: float = 1.0
    count: int = 1


@dataclass
class MetricsConfig:
    speed_smoothing_s: float = 0.0       # window for the speed used for state calls
    move_threshold_mm_s: float = 2.0
    immobile_threshold_mm_s: float = 1.0
    min_immobile_s: float = 1.0
    bout_threshold_mm_s: float = 2.0
    bout_min_duration_s: float = 0.04
    bout_merge_gap_s: float = 0.04
    turn_threshold_deg: float = 30.0
    time_bin_s: float = 60.0
    zones: List[ZoneConfig] = field(default_factory=list)
    phases: List[PhaseConfig] = field(default_factory=list)
    phase_cycle: Optional[PhaseCycleConfig] = None
    events: List[EventConfig] = field(default_factory=list)
    event_series: List[EventSeriesConfig] = field(default_factory=list)
    event_window_s: float = 1.0
    response_threshold_mm_s: float = 10.0


@dataclass
class QCConfig:
    min_valid_fraction: float = 0.8


@dataclass
class OutputConfig:
    tracks_format: str = "csv"           # csv | csv.gz | parquet
    save_tracks: bool = True
    plots: bool = True
    report: bool = True
    overlay_video: bool = False


@dataclass
class Config:
    name: str = "custom"
    video: VideoConfig = field(default_factory=VideoConfig)
    arenas: ArenaConfig = field(default_factory=ArenaConfig)
    calibration: CalibrationConfig = field(default_factory=CalibrationConfig)
    background: BackgroundConfig = field(default_factory=BackgroundConfig)
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    postprocess: PostprocessConfig = field(default_factory=PostprocessConfig)
    metrics: MetricsConfig = field(default_factory=MetricsConfig)
    qc: QCConfig = field(default_factory=QCConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    def save(self, path: Union[str, Path]) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(self.to_dict(), fh, sort_keys=False, allow_unicode=True)


class ConfigError(ValueError):
    pass


# ----------------------------------------------------------------------------
# dict -> dataclass conversion

def _strip_optional(tp):
    if typing.get_origin(tp) is Union:
        args = [a for a in typing.get_args(tp) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return tp


def _convert(tp, value, where: str):
    tp = _strip_optional(tp)
    if value is None:
        return None
    if dataclasses.is_dataclass(tp):
        if not isinstance(value, dict):
            raise ConfigError(f"{where}: expected a mapping, got {value!r}")
        return _from_dict(tp, value, where)
    origin = typing.get_origin(tp)
    if origin in (list, List):
        (item_tp,) = typing.get_args(tp) or (Any,)
        if not isinstance(value, (list, tuple)):
            raise ConfigError(f"{where}: expected a list, got {value!r}")
        return [_convert(item_tp, v, f"{where}[{i}]") for i, v in enumerate(value)]
    if tp is float and isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if tp is int and isinstance(value, (int, float)) and not isinstance(value, bool):
        if float(value) != int(value):
            raise ConfigError(f"{where}: expected an integer, got {value!r}")
        return int(value)
    return value


def _from_dict(cls, data: dict, where: str = "config"):
    hints = typing.get_type_hints(cls)
    names = {f.name for f in dataclasses.fields(cls)}
    unknown = set(data) - names
    if unknown:
        raise ConfigError(
            f"{where}: unknown key(s) {sorted(unknown)}; valid keys: {sorted(names)}")
    kwargs = {k: _convert(hints[k], v, f"{where}.{k}") for k, v in data.items()}
    return cls(**kwargs)


def deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def list_presets() -> List[str]:
    return sorted(p.stem for p in PRESET_DIR.glob("*.yaml"))


def _resolve_preset_path(name: str, relative_to: Optional[Path] = None) -> Path:
    p = Path(name)
    if p.suffix in (".yaml", ".yml"):
        if not p.is_absolute() and relative_to is not None:
            p = relative_to / p
        return p
    preset = PRESET_DIR / f"{name}.yaml"
    if not preset.exists():
        raise ConfigError(f"unknown preset '{name}'. available: {list_presets()}")
    return preset


def _load_raw(path: Path, _seen=None) -> dict:
    _seen = set() if _seen is None else _seen
    path = path.resolve()
    if path in _seen:
        raise ConfigError(f"circular 'extends' involving {path}")
    _seen.add(path)
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: top level must be a mapping")
    parent = data.pop("extends", None)
    if parent:
        base = _load_raw(_resolve_preset_path(parent, path.parent), _seen)
        data = deep_merge(base, data)
    return data


def config_from_dict(data: dict) -> Config:
    data = dict(data)
    parent = data.pop("extends", None)
    if parent:
        data = deep_merge(_load_raw(_resolve_preset_path(parent)), data)
    cfg = _from_dict(Config, data)
    validate(cfg)
    return cfg


def load_config(path_or_preset: Union[str, Path, None]) -> Config:
    """Load a YAML config file, or a preset by name (e.g. ``larva_96well``)."""
    if path_or_preset is None:
        cfg = Config()
        validate(cfg)
        return cfg
    p = Path(path_or_preset)
    if not p.exists():
        p = _resolve_preset_path(str(path_or_preset))
    cfg = _from_dict(Config, _load_raw(p))
    validate(cfg)
    return cfg


def validate(cfg: Config) -> None:
    a, d, m = cfg.arenas, cfg.detection, cfg.metrics
    if a.type not in ("plate", "circles", "rects", "polygons", "full_frame"):
        raise ConfigError(f"arenas.type '{a.type}' not supported")
    if d.polarity not in ("dark", "light", "both"):
        raise ConfigError("detection.polarity must be dark, light or both")
    if isinstance(d.threshold, str) and d.threshold != "auto":
        raise ConfigError("detection.threshold must be a number or 'auto'")
    if d.animals_per_arena < 1:
        raise ConfigError("detection.animals_per_arena must be >= 1")
    if cfg.video.frame_step < 1:
        raise ConfigError("video.frame_step must be >= 1")
    if cfg.background.method not in ("auto", "median", "image"):
        raise ConfigError("background.method must be auto, median or image")
    if cfg.background.method == "image" and not cfg.background.image:
        raise ConfigError("background.method=image requires background.image")
    if cfg.output.tracks_format not in ("csv", "csv.gz", "parquet"):
        raise ConfigError("output.tracks_format must be csv, csv.gz or parquet")
    labels: List[str] = []
    for z in m.zones:
        if z.type not in ("center_periphery", "vertical_bands", "horizontal_bands", "polygon"):
            raise ConfigError(f"zone '{z.name}': unknown type '{z.type}'")
        labels += zone_labels(z)
    dup = {x for x in labels if labels.count(x) > 1}
    if dup:
        raise ConfigError(f"zone labels must be unique across zone sets, duplicated: {sorted(dup)}")


def zone_labels(z: ZoneConfig) -> List[str]:
    if z.type == "center_periphery":
        return list(z.labels or ["center", "periphery"])
    if z.type == "polygon":
        return list(z.labels or [z.name, f"outside_{z.name}"])
    if z.edges:
        n = len(z.edges) + 1
    elif z.labels:
        n = len(z.labels)
    else:
        n = 3 if z.type == "vertical_bands" else 2
    default = {
        ("vertical_bands", 3): ["top", "middle", "bottom"],
        ("vertical_bands", 2): ["top", "bottom"],
        ("horizontal_bands", 2): ["left", "right"],
        ("horizontal_bands", 3): ["left", "center_x", "right"],
    }.get((z.type, n), [f"{z.name}_{i + 1}" for i in range(n)])
    labels = list(z.labels or default)
    if len(labels) != n:
        raise ConfigError(f"zone '{z.name}': {n} bands but {len(labels)} labels")
    return labels


def zone_edges(z: ZoneConfig) -> List[float]:
    if z.edges:
        return list(z.edges)
    n = len(z.labels) if z.labels else 3 if z.type == "vertical_bands" else 2
    return [i / n for i in range(1, n)]


def expand_phases(m: MetricsConfig) -> List[PhaseConfig]:
    """Explicit phases plus those generated by ``phase_cycle``."""
    phases = list(m.phases)
    pc = m.phase_cycle
    if pc and pc.sequence:
        t = pc.start_s
        for cycle in range(1, pc.repeat + 1):
            for item in pc.sequence:
                if len(item) != 2:
                    raise ConfigError("phase_cycle.sequence items must be [name, duration_s]")
                name, dur = str(item[0]), float(item[1])
                phases.append(PhaseConfig(name=f"{name}_{cycle}", start_s=t, end_s=t + dur))
                t += dur
    return phases


def expand_events(m: MetricsConfig) -> List[EventConfig]:
    events = list(m.events)
    for s in m.event_series:
        for i in range(s.count):
            events.append(EventConfig(name=f"{s.name}_{i + 1}", time_s=s.start_s + i * s.interval_s))
    return sorted(events, key=lambda e: e.time_s)
