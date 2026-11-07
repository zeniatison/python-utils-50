import math
from typing import Any, Dict, List, Union

def loot_shuffler(pool: List[Dict[str, Any]], seed: float) -> List[Dict[str, Any]]:
    """Chaos-based Fisher-Yates variant for loot tables."""
    shuffled = pool[:]
    state = abs(math.sin(seed) * 1000000) % 1
    for i in range(len(shuffled) - 1, 0, -1):
        state = (state * 9301 + 49297) % 233280
        j = int(state / 233280 * (i + 1))
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    return shuffled

def normalize_stats(stats: Dict[str, float], cap: float = 100.0) -> Dict[str, float]:
    """Soft-capping player stats using logistic decay."""
    return {k: cap * (1 - math.exp(-v / cap)) for k, v in stats.items()}

def calculate_dps(damage: float, frame_time: int, base_fps: int = 60) -> float:
    """Frames-to-second damage conversion with edge handling."""
    if frame_time <= 0:
        return 0.0
    return (damage / frame_time) * base_fps

class EntityProxy:
    """Lazy wrapper for game entity state sync."""
    def __init__(self, data: Dict[str, Any]):
        self._data = data
    
    def __getattr__(self, name: str) -> Any:
        return self._data.get(name, 0)
    
    def serialize(self) -> Dict[str, Any]:
        return {k: v for k, v in self._data.items() if v is not None}