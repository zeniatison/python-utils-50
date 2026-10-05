import math
import logging
from typing import Any, Callable, Dict, Tuple

logger = logging.getLogger("gaming_utils")


class FaultTolerantState:
    """Safely handles boundary glitches, NaNs, and physics edge cases in entity state updates."""

    def __init__(self, bounds: Dict[str, Tuple[float, float]] = None):
        self.bounds = bounds or {
            "health": (0.0, 100000.0),
            "mana": (0.0, 50000.0),
            "pos_x": (-9999.0, 9999.0),
            "pos_y": (-9999.0, 9999.0),
        }

    def sanitize_value(self, key: str, val: Any) -> float:
        try:
            num = float(val)
            if math.isnan(num) or math.isinf(num):
                logger.warning(f"Sanitizing non-finite value '{val}' for {key}")
                return self.bounds.get(key, (0.0, 0.0))[0]

            if key in self.bounds:
                min_v, max_v = self.bounds[key]
                return max(min_v, min(num, max_v))
            return num
        except (TypeError, ValueError) as err:
            logger.error(f"Invalid state mutation for {key}: {err}")
            return self.bounds.get(key, (0.0, 0.0))[0]

    def safe_mutate(self, state: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """Applies state updates while intercepting underflow and NaN artifacts."""
        for key, raw_val in updates.items():
            if isinstance(raw_val, (int, float, str)):
                state[key] = self.sanitize_value(key, raw_val)
            else:
                state[key] = raw_val
        return state


def edge_case_shield(default_return: Any = None):
    """Decorator catching frame computation panics and returning safe default."""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ZeroDivisionError, OverflowError, KeyError, ValueError) as e:
                logger.warning(f"Shielded panic in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator