import numpy as np

def apply_dead_zone(value, dz):
    if abs(value) < dz:
        return 0.0
    sign = 1 if value > 0 else -1
    return sign * (abs(value) - dz) / (1.0 - dz)

def smooth(current, previous, alpha):
    return alpha * previous + (1 - alpha) * current

def to_vjoy(value, center, max_val):
    return int(np.clip(center + value * (max_val - center), 1, max_val))