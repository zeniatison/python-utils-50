import random
import time
from typing import Any, List, Dict

class GamingException(Exception):
    """Base exception for unusual gaming mechanics edge cases."""
    def __init__(self, message: str, severity: str = "soft_lock"):
        super().__init__(message)
        self.severity = severity
        self.timestamp = time.time()

class InventoryOverflowError(GamingException):
    """Raised when inventory limits are exceeded. Features a recovery helper."""
    def __init__(self, message: str, current_weight: float, max_weight: float):
        super().__init__(f"{message} ({current_weight}/{max_weight}kg)", severity="encumbered")
        self.current_weight = current_weight
        self.max_weight = max_weight

    def auto_discard_trash(self, inventory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Creative recovery: discards items of low value to free up space."""
        sorted_inv = sorted(inventory, key=lambda x: x.get("value", 0))
        freed_weight = 0.0
        while sorted_inv and (self.current_weight - freed_weight > self.max_weight):
            discarded = sorted_inv.pop(0)
            freed_weight += discarded.get("weight", 1.0)
        return sorted_inv

class RageQuitException(GamingException):
    """Raised when a frustration threshold is exceeded, imposing cooldowns."""
    def __init__(self, reason: str, salty_rating: int = 10):
        super().__init__(
            f"RageQuit initiated: {reason} (Salt Level: {salty_rating}/10)",
            severity="alt_f4"
        )
        self.cooldown_period = salty_rating * 5

    def cooling_down(self) -> bool:
        return time.time() - self.timestamp < self.cooldown_period

def resolve_anomaly(exc: GamingException) -> str:
    """Resolves anomalous gaming errors into actionable state changes."""
    if isinstance(exc, InventoryOverflowError):
        diff = exc.current_weight - exc.max_weight
        return f"cleanup recommended: {diff:.2f} units over limit"
    if isinstance(exc, RageQuitException):
        return f"cooldown mandated: {exc.cooldown_period} seconds remain"
    return "default resurrection path triggered"
