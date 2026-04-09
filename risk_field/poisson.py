import numpy as np


def screened_poisson_field(
    mask: np.ndarray,
    lam: float = 2000.0,
    order: int = 4,
    origin_coeff: float = 1.0,
) -> np.ndarray:
    """
    Generate a smooth risk field from a binary obstacle mask using
    a screened Poisson-like frequency-domain filter.

    Parameters
    ----------
    mask : np.ndarray
        2D obstacle mask. Nonzero means obstacle.
    lam : float
        Larger -> wider spatial spread.
    order : int
        Larger -> smoother and thicker field.
    origin_coeff : float
        Obstacle pixels are lifted to max_phi * origin_coeff before normalization.

    Returns
    -------
    np.ndarray
        Normalized field in [0, 1].
    """
    src = mask.astype(np.float32)
    src_bin = (src > 0).astype(np.float32)

    fsrc = np.fft.fft2(src)

    h, w = src.shape
    kx = np.fft.fftfreq(w).reshape(1, -1)
    ky = np.fft.fftfreq(h).reshape(-1, 1)
    k2 = (2.0 * np.pi * kx) ** 2 + (2.0 * np.pi * ky) ** 2

    filt = 1.0 / (1.0 + lam * k2) ** order
    phi = np.real(np.fft.ifft2(fsrc * filt))

    eps = 1e-12
    max_phi = float(phi.max() + eps)
    obstacle_value = max_phi * float(origin_coeff)
    phi = np.maximum(phi, obstacle_value * src_bin)

    phi_min = float(phi.min())
    phi_max = float(phi.max())
    phi = (phi - phi_min) / (phi_max - phi_min + eps)
    return phi.astype(np.float32)