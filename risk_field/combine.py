import numpy as np
from .utils import sigmoid

def strength_field(channels, obstacle_union_mask, origin_coeff=1.8,
                   combine='sum', weights=None, renorm=False):
    
    ch = np.asarray(channels, dtype=np.float32)
    N, H, W = ch.shape

    if combine == 'sum':
        S = np.sum(ch, axis=0)
    elif combine == 'mean':
        S = np.mean(ch, axis=0)
    elif combine == 'max':
        S = np.max(ch, axis=0)
    else:
        raise ValueError

    M_union = (obstacle_union_mask > 0)
    valid = ~M_union

    eps = 1e-12
    S_out = np.zeros_like(S)

    vmin, vmax = float(S[valid].min()), float(S[valid].max())
    rng = vmax - vmin + eps

    S_out[valid] = (S[valid] - vmin) / rng

    obstacle_value = (vmax * origin_coeff - vmin) / rng
    S_out[M_union] = obstacle_value

    if renorm:
        smin, smax = S_out.min(), S_out.max()
        S_out = (S_out - smin) / (smax - smin + eps)

    return S_out