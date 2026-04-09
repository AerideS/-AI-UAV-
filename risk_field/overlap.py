import numpy as np


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def _normalize_with_obstacle_override(
    raw: np.ndarray,
    obstacle_union_mask: np.ndarray | None = None,
    origin_coeff: float = 1.8,
    renorm: bool = False,
) -> np.ndarray:
    """
    Normalize raw field using non-obstacle region statistics, then assign
    obstacle pixels to a boosted level.
    """
    if obstacle_union_mask is None:
        union = np.zeros_like(raw, dtype=np.uint8)
    else:
        union = (obstacle_union_mask > 0).astype(np.uint8)

    valid = union == 0
    eps = 1e-12
    out = np.zeros_like(raw, dtype=np.float32)

    if np.any(valid):
        vmin = float(raw[valid].min())
        vmax = float(raw[valid].max())
        rng = (vmax - vmin) + eps

        out[valid] = (raw[valid] - vmin) / rng

        obstacle_value_raw = vmax * float(origin_coeff)
        obstacle_value_norm = (obstacle_value_raw - vmin) / rng
        out[union == 1] = obstacle_value_norm
    else:
        vmin = float(raw.min())
        vmax = float(raw.max())
        rng = (vmax - vmin) + eps
        obstacle_value_raw = vmax * float(origin_coeff)
        obstacle_value_norm = (obstacle_value_raw - vmin) / rng
        out[:] = obstacle_value_norm

    if renorm:
        omin = float(out.min())
        omax = float(out.max())
        out = (out - omin) / (omax - omin + eps)

    return out.astype(np.float32)


def multiplicity_field(
    channels: np.ndarray,
    tau: float = 0.4,
    beta: float = 0.1,
    obstacle_union_mask: np.ndarray | None = None,
    origin_coeff: float = 1.8,
    renorm: bool = False,
) -> np.ndarray:
    """
    M(x): soft count of how many channels are active.
    """
    ch = np.asarray(channels, dtype=np.float32)
    if ch.ndim == 2:
        ch = ch[None, ...]
    raw = np.sum(_sigmoid((ch - tau) / (beta + 1e-12)), axis=0)
    return _normalize_with_obstacle_override(raw, obstacle_union_mask, origin_coeff, renorm)


def strength_field(
    channels: np.ndarray,
    obstacle_union_mask: np.ndarray | None = None,
    origin_coeff: float = 1.8,
    combine: str = "sum",
    weights: np.ndarray | None = None,
    renorm: bool = False,
) -> np.ndarray:
    """
    S(x): overlap strength. By default uses sum over channels.
    """
    ch = np.asarray(channels, dtype=np.float32)
    if ch.ndim == 2:
        ch = ch[None, ...]
    n, _, _ = ch.shape

    if combine == "sum":
        if weights is None:
            raw = np.sum(ch, axis=0)
        else:
            w = np.asarray(weights, dtype=np.float32).reshape(n, 1, 1)
            raw = np.sum(ch * w, axis=0)
    elif combine == "mean":
        if weights is None:
            raw = np.mean(ch, axis=0)
        else:
            w = np.asarray(weights, dtype=np.float32).reshape(n, 1, 1)
            raw = np.sum(ch * w, axis=0) / (float(np.sum(w)) + 1e-12)
    elif combine == "max":
        raw = np.max(ch, axis=0)
    else:
        raise ValueError("combine must be one of {'sum', 'mean', 'max'}")

    return _normalize_with_obstacle_override(raw, obstacle_union_mask, origin_coeff, renorm)


def core_field(
    channels: np.ndarray,
    tau_c: float = 0.01,
    beta_c: float = 0.08,
    obstacle_union_mask: np.ndarray | None = None,
    origin_coeff: float = 1.8,
    renorm: bool = False,
) -> np.ndarray:
    """
    R(x): AND-like overlap core.
    Large only where multiple channels are jointly high.
    """
    ch = np.asarray(channels, dtype=np.float32)
    if ch.ndim == 2:
        ch = ch[None, ...]
    raw = np.prod(_sigmoid((ch - tau_c) / (beta_c + 1e-12)), axis=0)
    return _normalize_with_obstacle_override(raw, obstacle_union_mask, origin_coeff, renorm)