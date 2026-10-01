from functools import wraps
import math
from typing import Any, Callable, Dict, Union


class GameStateCorruptionError(Exception):
    """Raised when critical game state is beyond recovery."""

    pass


def safe_stat_evaluator(default_value: float = 0.0) -> Callable:
    """Decorator catching edge cases in dynamic gameplay mathematical expressions."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> float:
            try:
                result = func(*args, **kwargs)
                if isinstance(result, (int, float)):
                    if math.isnan(result) or math.isinf(result):
                        return default_value
                    return float(max(0.0, result))
                return default_value
            except (ZeroDivisionError, TypeError, ValueError, KeyError):
                return default_value
            except Exception as err:
                raise GameStateCorruptionError(
                    f"Fatal state mismatch in {func.__name__}: {err}"
                ) from err

        return wrapper

    return decorator


class CombatProcessor:
    def __init__(self, base_power: float):
        self.base_power = max(1.0, float(base_power))

    @safe_stat_evaluator(default_value=1.0)
    def calculate_effective_dps(
        self, attack_speed: Union[int, float, str], armor: Union[int, float, str]
    ) -> float:
        speed = float(attack_speed)
        raw_armor = float(armor)

        if raw_armor >= 100:
            mitigation = 0.99
        else:
            mitigation = raw_armor / (raw_armor + 50)

        dps = (self.base_power / (1.0 / speed)) * (1.0 - mitigation)
        return dps

    def process_encounter_log(
        self, combat_data: list[Dict[str, Any]]
    ) -> list[float]:
        results = []
        for entry in combat_data:
            speed = entry.get("speed", 1.0)
            armor = entry.get("armor", 0)
            results.append(self.calculate_effective_dps(speed, armor))
        return results
