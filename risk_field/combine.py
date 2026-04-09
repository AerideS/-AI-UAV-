import numpy as np


def combined_overlap_risk(
    M: np.ndarray,
    S: np.ndarray,
    R: np.ndarray,
    gamma: float = 1.0,
    eta: float = 1.0,
    renorm: bool = True,
) -> np.ndarray:
    """
    O(x) = norm( S(x) * M(x)^gamma * R(x)^eta )
    """
    eps = 1e-12
    O = S * (M ** gamma) * (R ** eta)

    if renorm:
        omin = float(O.min())
        omax = float(O.max())
        O = (O - omin) / (omax - omin + eps)

    return O.astype(np.float32)