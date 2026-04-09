import numpy as np

def adjust_risk(field, safety, p_soft=2.0, p_hard=2.0):
    arr = np.asarray(field, dtype=np.float32)
    s = float(np.clip(safety, 0.0, 1.0))

    R_soft = arr ** p_soft
    R_hard = 1.0 - (1.0 - arr) ** p_hard

    return (1 - s) * R_soft + s * R_hard