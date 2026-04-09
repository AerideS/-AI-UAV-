import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_overlap_maps(
    masks: list[np.ndarray],
    channels: np.ndarray,
    M: np.ndarray,
    S: np.ndarray,
    R: np.ndarray,
    O: np.ndarray,
    save_path: str = "overlap_maps.png",
) -> None:
    """
    Plot input masks/channels and resulting M, S, R, O maps.
    """
    n_channels = channels.shape[0]
    ncols = max(n_channels, 4)
    nrows = 2

    fig, axes = plt.subplots(nrows, ncols, figsize=(4.0 * ncols, 7.5))
    axes = np.atleast_2d(axes)

    # First row: obstacle masks or channels
    for i in range(ncols):
        ax = axes[0, i]
        ax.axis("off")
        if i < len(masks):
            ax.imshow(masks[i], cmap="gray", vmin=0, vmax=1)
            ax.set_title(f"Obstacle Mask {i+1}")
        elif i < n_channels:
            ax.imshow(channels[i], cmap="viridis")
            ax.set_title(f"Field $\\phi_{i+1}$")
        else:
            ax.set_visible(False)

    # Second row: M, S, R, O
    maps = [M, S, R, O]
    titles = [
        "Multiplicity $M(x)$",
        "Strength $S(x)$",
        "Core $R(x)$",
        "Combined Risk $O(x)$",
    ]

    for i in range(ncols):
        ax = axes[1, i]
        ax.axis("off")
        if i < 4:
            im = ax.imshow(maps[i], cmap="inferno")
            ax.set_title(titles[i])
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        else:
            ax.set_visible(False)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close(fig)