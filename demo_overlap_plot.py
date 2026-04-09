import os
import numpy as np

from risk_field import (
    screened_poisson_field,
    multiplicity_field,
    strength_field,
    core_field,
    combined_overlap_risk,
    plot_overlap_maps,
)


def make_rect_mask(h: int, w: int, x0: int, y0: int, x1: int, y1: int) -> np.ndarray:
    mask = np.zeros((h, w), dtype=np.float32)
    mask[y0:y1, x0:x1] = 1.0
    return mask


def main() -> None:
    h, w = 220, 220

    # 예시: 서로 겹치는 영향권이 생기도록 건물 3개 배치
    mask1 = make_rect_mask(h, w, 55, 60, 75, 80)
    mask2 = make_rect_mask(h, w, 105, 40, 125, 60)
    mask3 = make_rect_mask(h, w, 130, 120, 150, 140)

    masks = [mask1, mask2, mask3]
    obstacle_union_mask = np.clip(mask1 + mask2 + mask3, 0, 1)

    # 각 건물 채널별 screened poisson risk field
    channels = np.stack(
        [
            screened_poisson_field(mask1, lam=1800, order=2, origin_coeff=1.1),
            screened_poisson_field(mask2, lam=1800, order=2, origin_coeff=1.1),
            screened_poisson_field(mask3, lam=1800, order=2, origin_coeff=1.1),
        ],
        axis=0,
    )

    # M, S, R 계산
    M = multiplicity_field(
        channels,
        tau=0.35,
        beta=0.08,
        obstacle_union_mask=obstacle_union_mask,
        origin_coeff=1.6,
        renorm=True,
    )

    S = strength_field(
        channels,
        obstacle_union_mask=obstacle_union_mask,
        origin_coeff=1.6,
        combine="sum",
        renorm=True,
    )

    R = core_field(
        channels,
        tau_c=0.20,
        beta_c=0.06,
        obstacle_union_mask=obstacle_union_mask,
        origin_coeff=1.6,
        renorm=True,
    )

    O = combined_overlap_risk(
        M=M,
        S=S,
        R=R,
        gamma=1.0,
        eta=1.0,
        renorm=True,
    )

    os.makedirs("results", exist_ok=True)
    plot_overlap_maps(
        masks=masks,
        channels=channels,
        M=M,
        S=S,
        R=R,
        O=O,
        save_path="results/overlap_maps.png",
    )

    print("Saved: results/overlap_maps.png")


if __name__ == "__main__":
    main()