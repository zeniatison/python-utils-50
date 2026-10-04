import math
from typing import Callable, Any, Dict

class GlitchMitigator:
    """Creative fallback mechanism for gaming-related physics and state errors."""

    def __init__(self, fallback_defaults: Dict[str, Any] = None):
        self.fallback_defaults = fallback_defaults or {
            "velocity": (0.0, 0.0),
            "health": 100.0,
            "frame_rate": 60,
            "coefficient": 0.5
        }

    def mitigate_edge_case(self, parameter_name: str) -> Callable:
        """Decorator that catches math-related gaming anomalies (NaN, Inf, ZeroDivision)."""
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> Any:
                try:
                    result = func(*args, **kwargs)
                    if isinstance(result, float) and (math.isnan(result) or math.isinf(result)):
                        raise ValueError("unstable float in calculations")
                    if isinstance(result, tuple):
                        if any(isinstance(x, float) and (math.isnan(x) or math.isinf(x)) for x in result):
                            raise ValueError("unstable vector coordinate")
                    return result
                except (ZeroDivisionError, ValueError, OverflowError):
                    fallback = self.fallback_defaults.get(parameter_name, 0.0)
                    return fallback
            return wrapper
        return decorator

mitigator = GlitchMitigator()

@mitigator.mitigate_edge_case("velocity")
def calculate_rebound_velocity(mass: float, acceleration: float) -> tuple:
    if mass == 0:
        raise ZeroDivisionError("mass cannot be zero")
    return (acceleration / mass, (acceleration * 0.95) / mass)

@mitigator.mitigate_edge_case("health")
def apply_damage_modifier(base_damage: float, resistance: float) -> float:
    if resistance < 0:
        return float('nan')
    return base_damage - (base_damage * resistance)
