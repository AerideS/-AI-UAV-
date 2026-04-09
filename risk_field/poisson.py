import numpy as np

def screened_poisson_field(mask, lam=2000, order=4, origin_coeff=1.0):
    src = mask.astype(np.float32)
    src_bin = (src > 0).astype(np.float32)

    fsrc = np.fft.fft2(src)

    h, w = src.shape
    kx = np.fft.fftfreq(w).reshape(1, -1)
    ky = np.fft.fftfreq(h).reshape(-1, 1)
    k2 = (2 * np.pi * kx) ** 2 + (2 * np.pi * ky) ** 2

    filt = 1.0 / (1.0 + lam * k2) ** order

    phi = np.real(np.fft.ifft2(fsrc * filt))

    eps = 1e-12
    max_phi = float(phi.max() + eps)
    obstacle_value = max_phi * origin_coeff

    phi = np.maximum(phi, obstacle_value * src_bin)

    phi_min, phi_max = float(phi.min()), float(phi.max())
    phi = (phi - phi_min) / (phi_max - phi_min + eps)

    return phi