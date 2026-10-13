"""Behavioural states, bouts, zones and windowed summary metrics."""
from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from matplotlib.path import Path as MplPath

from .arenas import Arena
from .config import (Config, MetricsConfig, ZoneConfig, expand_events, expand_phases,
                     zone_edges, zone_labels)
from .postprocess import angle_diff, process_track

ID_COLS = ["video", "track_id", "arena", "animal"]


# ----------------------------------------------------------------------------
# helpers

def runs(mask: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Start/end (exclusive) indices of True runs."""
    m = np.concatenate([[0], np.asarray(mask, bool).astype(np.int8), [0]])
    d = np.diff(m)
    return np.flatnonzero(d == 1), np.flatnonzero(d == -1)


def _nanmean(v) -> float:
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    return float(v.mean()) if v.size else float("nan")


def _nanmax(v) -> float:
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    return float(v.max()) if v.size else float("nan")


def _gt(v: np.ndarray, thr: float) -> np.ndarray:
    return np.nan_to_num(v, nan=-np.inf) > thr


def _lt(v: np.ndarray, thr: float) -> np.ndarray:
    return np.nan_to_num(v, nan=np.inf) < thr


# ----------------------------------------------------------------------------
# zones

def assign_zone(z: ZoneConfig, arena: Arena, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Integer zone code per frame (-1 where the position is unknown)."""
    ok = np.isfinite(x) & np.isfinite(y)
    code = np.full(len(x), -1, np.int8)
    if z.type == "center_periphery":
        if arena.shape == "circle":
            p = arena.params
            rf = np.hypot(x - p["cx"], y - p["cy"]) / p["r"]
        else:
            xn, yn = arena.normalized(x, y)
            rf = np.maximum(np.abs(xn - 0.5), np.abs(yn - 0.5)) * 2
        code[ok] = np.where(rf[ok] < z.center_fraction, 0, 1)
    elif z.type in ("vertical_bands", "horizontal_bands"):
        xn, yn = arena.normalized(x, y)
        v = yn if z.type == "vertical_bands" else xn
        code[ok] = np.digitize(np.clip(v[ok], 0, 1), zone_edges(z))
    elif z.type == "polygon":
        xn, yn = arena.normalized(x, y)
        inside = MplPath(np.asarray(z.points, float)).contains_points(np.c_[xn[ok], yn[ok]])
        code[ok] = np.where(inside, 0, 1)
    return code


def entries(code: np.ndarray) -> np.ndarray:
    """True on frames where the animal arrives in a zone different from the previous known one."""
    out = np.zeros(len(code), bool)
    v = np.flatnonzero(code >= 0)
    if len(v) > 1:
        out[v[1:]] = code[v[1:]] != code[v[:-1]]
    return out


# ----------------------------------------------------------------------------
# per-track annotation

def annotate(T: Dict[str, np.ndarray], arena: Arena, dt: float, m: MetricsConfig) -> None:
    """Add behavioural state arrays to track dict T (in place)."""
    speed = T["speed_mm_s"]
    w = int(round(m.speed_smoothing_s / dt))
    if w > 1:
        s = pd.Series(speed).rolling(w, center=True, min_periods=1).mean().to_numpy().copy()
        s[~np.isfinite(speed)] = np.nan
    else:
        s = speed
    T["speed_state"] = s
    T["moving"] = _gt(s, m.move_threshold_mm_s)
    still = _lt(s, m.immobile_threshold_mm_s) & T["valid"]
    st, en = runs(still)
    long_ = (en - st) * dt >= m.min_immobile_s
    imm = np.zeros(len(s), bool)
    imm_start = np.zeros(len(s), bool)
    for a, b in zip(st[long_], en[long_]):
        imm[a:b] = True
        imm_start[a] = True
    T["immobile"], T["immobile_start"] = imm, imm_start
    for z in m.zones:
        c = assign_zone(z, arena, T["x_px"], T["y_px"])
        T[f"zone:{z.name}"] = c
        T[f"entry:{z.name}"] = entries(c)


def _heading_near(h: np.ndarray, idx: Sequence[int]) -> float:
    for i in idx:
        if 0 <= i < len(h) and np.isfinite(h[i]):
            return float(h[i])
    return float("nan")


def find_bouts(T: Dict[str, np.ndarray], dt: float, m: MetricsConfig) -> pd.DataFrame:
    """Movement bouts: speed above threshold, short pauses merged, short runs dropped."""
    st, en = runs(_gt(T["speed_state"], m.bout_threshold_mm_s))
    if len(st) > 1:
        gap = st[1:] - en[:-1]
        merge = gap * dt <= m.bout_merge_gap_s
        keep_start = np.concatenate([[True], ~merge])
        keep_end = np.concatenate([~merge, [True]])
        st, en = st[keep_start], en[keep_end]
    dur = (en - st) * dt
    ok = dur >= m.bout_min_duration_s - 1e-9
    st, en = st[ok], en[ok]
    cols = ["bout", "start_frame", "end_frame", "start_s", "duration_s", "distance_mm",
            "net_displacement_mm", "peak_speed_mm_s", "mean_speed_mm_s", "turn_deg",
            "abs_turn_deg", "interbout_s"]
    if len(st) == 0:
        return pd.DataFrame(columns=cols)
    t, step, spd = T["time_s"], T["step_mm"], T["speed_mm_s"]
    x, y, h = T["x_mm"], T["y_mm"], T["heading_deg"]
    rows = []
    for k, (a, b) in enumerate(zip(st, en)):
        i0 = max(a - 1, 0)
        dist = float(np.nansum(step[a:b]))
        net = float(np.hypot(x[b - 1] - x[i0], y[b - 1] - y[i0]))
        hb = _heading_near(h, [a - 1, a - 2, a - 3])
        ha = _heading_near(h, [b, b + 1, b + 2, b - 1])
        turn = float(angle_diff(ha, hb)) if np.isfinite(ha) and np.isfinite(hb) else np.nan
        rows.append([k + 1, int(T["frame"][a]), int(T["frame"][b - 1]), float(t[a]), (b - a) * dt,
                     dist, net, _nanmax(spd[a:b]), dist / ((b - a) * dt), turn, abs(turn), np.nan])
    df = pd.DataFrame(rows, columns=cols)
    df["_i0"], df["_i1"] = st, en
    if len(df) > 1:
        df.loc[df.index[:-1], "interbout_s"] = (st[1:] - en[:-1]) * dt
    return df


# ----------------------------------------------------------------------------
# summaries

def summarize(T: Dict[str, np.ndarray], bouts: pd.DataFrame, i0: int, i1: int,
              t_start: float, t_end: float, dt: float, m: MetricsConfig) -> dict:
    sl = slice(i0, i1)
    n = i1 - i0
    valid = T["valid"][sl]
    nv = int(valid.sum())
    vt = nv * dt
    step = T["step_mm"][sl]
    dist = float(np.nansum(step))
    moving = T["moving"][sl]
    nm = int(moving.sum())
    r = {
        "t_start_s": t_start, "t_end_s": t_end, "duration_s": t_end - t_start,
        "n_frames": n,
        "detected_frac": float(T["detected"][sl].mean()) if n else np.nan,
        "valid_frac": nv / n if n else np.nan,
        "distance_mm": dist,
        "mean_speed_mm_s": dist / vt if vt > 0 else np.nan,
        "max_speed_mm_s": _nanmax(T["speed_mm_s"][sl]),
        "active_time_s": nm * dt,
        "active_frac": nm / nv if nv else np.nan,
        "mean_speed_active_mm_s": float(np.nansum(step[moving])) / (nm * dt) if nm else np.nan,
        "immobile_time_s": float(T["immobile"][sl].sum()) * dt,
        "immobile_frac": float(T["immobile"][sl].sum()) / nv if nv else np.nan,
        "immobile_episodes": int(T["immobile_start"][sl].sum()),
    }
    # bouts starting inside the window
    if len(bouts):
        b = bouts[(bouts["_i0"] >= i0) & (bouts["_i0"] < i1)]
    else:
        b = bouts
    nb = len(b)
    turns = b["abs_turn_deg"].to_numpy(float) if nb else np.array([])
    turns = turns[np.isfinite(turns)]
    r.update({
        "bout_count": nb,
        "bout_rate_per_min": nb / (vt / 60) if vt > 0 else np.nan,
        "bout_mean_duration_s": _nanmean(b["duration_s"]) if nb else np.nan,
        "bout_mean_distance_mm": _nanmean(b["distance_mm"]) if nb else np.nan,
        "bout_mean_peak_speed_mm_s": _nanmean(b["peak_speed_mm_s"]) if nb else np.nan,
        "bout_mean_abs_turn_deg": float(turns.mean()) if turns.size else np.nan,
        "bout_turn_frac": float((turns > m.turn_threshold_deg).mean()) if turns.size else np.nan,
        "mean_interbout_s": _nanmean(b["interbout_s"]) if nb else np.nan,
    })
    dh = np.abs(T["dheading_deg"][sl])
    dh_m = dh[moving & np.isfinite(dh)]
    r["mean_abs_ang_vel_deg_s"] = float(dh_m.mean()) / dt if dh_m.size else np.nan
    r["meander_deg_per_mm"] = float(dh_m.sum()) / dist if dist > 0 and dh_m.size else np.nan
    r["mean_dist_wall_mm"] = _nanmean(T["dist_wall_mm"][sl])
    t = T["time_s"][sl]
    for z in m.zones:
        code = T[f"zone:{z.name}"][sl]
        ent = T[f"entry:{z.name}"][sl]
        for k, lab in enumerate(zone_labels(z)):
            inz = code == k
            cnt = int(inz.sum())
            first = np.flatnonzero(inz)
            r[f"{lab}_time_s"] = cnt * dt
            r[f"{lab}_frac"] = cnt / nv if nv else np.nan
            r[f"{lab}_entries"] = int((ent & inz).sum())
            # never entered -> censored at the window length
            r[f"{lab}_latency_s"] = float(t[first[0]] - t_start) if first.size else t_end - t_start
            r[f"{lab}_distance_mm"] = float(np.nansum(step[inz]))
    if "nnd_mm" in T:
        r["mean_nnd_mm"] = _nanmean(T["nnd_mm"][sl])
        r["mean_iid_mm"] = _nanmean(T["iid_mm"][sl])
    return r


def event_response(T: Dict[str, np.ndarray], te: float, w: float, dt: float,
                   m: MetricsConfig) -> dict:
    t = T["time_s"]
    a, b, c = np.searchsorted(t, [te - w, te, te + w])
    step, spd = T["step_mm"], T["speed_mm_s"]
    post = spd[b:c]
    above = np.flatnonzero(_gt(post, m.response_threshold_mm_s))
    pk = _nanmax(post)
    return {
        "event_time_s": te,
        "distance_pre_mm": float(np.nansum(step[a:b])),
        "distance_post_mm": float(np.nansum(step[b:c])),
        "mean_speed_pre_mm_s": float(np.nansum(step[a:b])) / ((b - a) * dt) if b > a else np.nan,
        "mean_speed_post_mm_s": float(np.nansum(step[b:c])) / ((c - b) * dt) if c > b else np.nan,
        "peak_speed_post_mm_s": pk,
        "responded": bool(above.size),
        "latency_s": float(t[b + above[0]] - te) if above.size else np.nan,
    }


# ----------------------------------------------------------------------------
# full analysis

@dataclass
class AnalysisResult:
    tracks: pd.DataFrame
    bouts: pd.DataFrame
    summary: pd.DataFrame
    timebins: pd.DataFrame
    phases: pd.DataFrame
    events: pd.DataFrame
    frames: Optional[pd.DataFrame] = None


def _windows_bins(t0: float, t1: float, size: float) -> List[Tuple[float, float]]:
    if not size or size <= 0:
        return []
    out, s = [], t0
    while s < t1 - 1e-9:
        out.append((s, min(s + size, t1)))
        s += size
    return out


def _shoaling(tracks: Dict[str, Dict[str, np.ndarray]], arena_of: Dict[str, str]) -> None:
    """Nearest-neighbour and mean inter-individual distance (mm) per frame."""
    by_arena: Dict[str, List[str]] = {}
    for tid, a in arena_of.items():
        by_arena.setdefault(a, []).append(tid)
    for a, tids in by_arena.items():
        if len(tids) < 2:
            continue
        P = np.stack([np.c_[tracks[t]["x_mm"], tracks[t]["y_mm"]] for t in tids], axis=1)
        d = np.linalg.norm(P[:, :, None, :] - P[:, None, :, :], axis=3)
        n = len(tids)
        iu = np.triu_indices(n, 1)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            iid = np.nanmean(d[:, iu[0], iu[1]], axis=1)
            d[:, np.arange(n), np.arange(n)] = np.nan
            nnd = np.nanmin(d, axis=2)
        for k, tid in enumerate(tids):
            tracks[tid]["nnd_mm"] = nnd[:, k]
            tracks[tid]["iid_mm"] = iid


def analyze(raw: pd.DataFrame, arenas: Sequence[Arena], info: dict, cfg: Config,
            frames: Optional[pd.DataFrame] = None) -> AnalysisResult:
    fps = float(info["fps"])
    dt = info.get("frame_step", 1) / fps
    m = cfg.metrics
    arena_by_id = {a.id: a for a in arenas}
    video_name = info.get("video_name", "")
    tracks: Dict[str, Dict[str, np.ndarray]] = {}
    meta: Dict[str, dict] = {}
    for tid, g in raw.groupby("track_id", sort=False):
        g = g.sort_values("frame")
        arena = arena_by_id[g["arena"].iloc[0]]
        rawd = {c: g[c].to_numpy() for c in ("x_px", "y_px", "heading_deg", "heading_conf")}
        T = process_track(rawd, arena, dt, cfg.postprocess)
        T["frame"] = g["frame"].to_numpy()
        T["time_s"] = g["time_s"].to_numpy(float)
        tracks[tid] = T
        meta[tid] = {"arena": arena.id, "animal": int(g["animal"].iloc[0]),
                     "row": arena.row, "col": arena.col,
                     "px_per_mm": arena.px_per_mm,
                     "units": "mm" if arena.px_per_mm else "px"}
    _shoaling(tracks, {t: v["arena"] for t, v in meta.items()})

    phases = expand_phases(m)
    events = expand_events(m)
    any_t = next(iter(tracks.values()))["time_s"]
    t_first, t_last = float(any_t[0]), float(any_t[-1]) + dt
    bins = _windows_bins(t_first, t_last, m.time_bin_s)
    for p in phases:
        if p.end_s <= t_first or p.start_s >= t_last:
            warnings.warn(f"phase '{p.name}' ({p.start_s}-{p.end_s} s) lies outside the analysed video")

    track_frames, bout_frames, summ, tb, ph, ev = [], [], [], [], [], []
    for tid, T in tracks.items():
        arena = arena_by_id[meta[tid]["arena"]]
        annotate(T, arena, dt, m)
        bouts = find_bouts(T, dt, m)
        ids = {"video": video_name, "track_id": tid, "arena": meta[tid]["arena"],
               "animal": meta[tid]["animal"]}
        t = T["time_s"]

        def idx(a, b):
            return int(np.searchsorted(t, a - 1e-9)), int(np.searchsorted(t, b - 1e-9))

        s = summarize(T, bouts, 0, len(t), t_first, t_last, dt, m)
        s.update({"row": meta[tid]["row"], "col": meta[tid]["col"],
                  "px_per_mm": meta[tid]["px_per_mm"], "units": meta[tid]["units"]})
        summ.append({**ids, **s})
        for k, (a, b) in enumerate(bins):
            tb.append({**ids, "bin": k + 1, **summarize(T, bouts, *idx(a, b), a, b, dt, m)})
        for p in phases:
            a, b = max(p.start_s, t_first), min(p.end_s, t_last)
            if b <= a:
                continue
            base = p.name.rsplit("_", 1)[0] if p.name.rsplit("_", 1)[-1].isdigit() else p.name
            ph.append({**ids, "phase": p.name, "phase_type": base,
                       **summarize(T, bouts, *idx(a, b), a, b, dt, m)})
        for e in events:
            if t_first <= e.time_s < t_last:
                ev.append({**ids, "event": e.name,
                           **event_response(T, e.time_s, m.event_window_s, dt, m)})
        if len(bouts):
            bout_frames.append(bouts.drop(columns=["_i0", "_i1"]).assign(**ids))
        skip = ("dheading_deg", "immobile_start")
        cols = {k: (v.astype(np.float32) if v.dtype == np.float64 and k != "time_s" else v)
                for k, v in T.items() if not k.startswith("entry:") and k not in skip}
        df = pd.DataFrame(cols)
        for z in m.zones:
            labs = np.array(zone_labels(z) + [""], dtype=object)
            df[f"zone:{z.name}"] = pd.Categorical(labs[df[f"zone:{z.name}"].to_numpy()],
                                                  categories=zone_labels(z))
        for k, v in ids.items():
            df.insert(0, k, v)
        track_frames.append(df)

    tracks_df = pd.concat(track_frames, ignore_index=True)
    tracks_df = tracks_df.rename(columns={c: c.replace("zone:", "zone_") for c in tracks_df.columns})
    lead = ["video", "track_id", "arena", "animal", "frame", "time_s"]
    tracks_df = tracks_df[lead + [c for c in tracks_df.columns if c not in lead]]
    summary = pd.DataFrame(summ)
    summary["qc_pass"] = summary["valid_frac"] >= cfg.qc.min_valid_fraction
    summary["qc_note"] = np.select(
        [summary["detected_frac"] == 0, ~summary["qc_pass"]],
        ["never detected (empty well / immobile animal?)", "low tracking coverage"], "")
    bouts_df = (pd.concat(bout_frames, ignore_index=True) if bout_frames else pd.DataFrame())
    if len(bouts_df):
        bouts_df = bouts_df[ID_COLS + [c for c in bouts_df.columns if c not in ID_COLS]]
    return AnalysisResult(tracks_df, bouts_df, summary, pd.DataFrame(tb), pd.DataFrame(ph),
                          pd.DataFrame(ev), frames)
