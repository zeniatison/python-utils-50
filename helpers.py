import random
import time
from typing import Any, Callable, TypeVar, List

T = TypeVar('T')

def roll_dice(sides: int = 6) -> int:
    """Simulates a fair dice roll with extra entropy."""
    random.seed(time.time_ns())
    return random.randint(1, sides)

def throttle_calls(interval: float) -> Callable:
    """Decorator to prevent spamming game engine loops."""
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.monotonic()
            if now - last_called[0] >= interval:
                last_called[0] = now
                return func(*args, **kwargs)
        return wrapper
    return decorator

def batch_process(items: List[T], chunk_size: int = 10) -> List[List[T]]:
    """Chunking logic for entity updates."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

def normalize_vector(vec: tuple[float, float]) -> tuple[float, float]:
    """2D vector normalization for player movement."""
    magnitude = (vec[0]**2 + vec[1]**2) ** 0.5
    if magnitude == 0:
        return (0.0, 0.0)
    return (vec[0] / magnitude, vec[1] / magnitude)

def coin_flip(chance: float = 0.5) -> bool:
    """Weighted boolean decision for loot drops."""
    return random.random() < chance