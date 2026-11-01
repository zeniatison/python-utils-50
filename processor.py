import math
from typing import Any, Iterable, Dict

def calculate_dps(damage: float, interval: float) -> float:
    return damage / max(interval, 0.001)

def normalize_vector(vector: tuple) -> tuple:
    magnitude = math.sqrt(sum(x**2 for x in vector))
    return tuple(x / magnitude for x in vector) if magnitude > 0 else vector

def get_weighted_random(choices: Dict[Any, float]) -> Any:
    import random
    total_weight = sum(choices.values())
    r = random.uniform(0, total_weight)
    cumulative = 0.0
    for item, weight in choices.items():
        cumulative += weight
        if r <= cumulative:
            return item

def apply_cooldown(start_time: float, current_time: float, duration: float) -> bool:
    return (current_time - start_time) >= duration

def batch_process(items: Iterable, chunk_size: int = 5) -> Iterable:
    for i in range(0, len(list(items)), chunk_size):
        yield list(items)[i:i + chunk_size]

def lerp(start: float, end: float, t: float) -> float:
    return start + t * (end - start)

def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))