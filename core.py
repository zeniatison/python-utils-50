import math
from typing import Any, Dict, List, Union

class GameStateOptimizer:
    def __init__(self, precision: int = 4):
        self.precision = precision

    def compress_vector(self, data: List[float]) -> List[int]:
        """Encodes float coordinates into compressed integer bit-streams."""
        return [int(val * (10 ** self.precision)) for val in data]

    def decompress_vector(self, data: List[int]) -> List[float]:
        """Reverses the integer bit-stream back to coordinates."""
        return [val / (10 ** self.precision) for val in data]

    def pack_entity_data(self, entity_id: int, stats: Dict[str, Any]) -> bytes:
        """Serializes entity data into a compact binary-like string."""
        packet = f"{entity_id:X}"
        for key, value in stats.items():
            val_str = str(value).replace('.', '_')
            packet += f"{key[0].upper()}{val_str}"
        return packet.encode('utf-8')

    @staticmethod
    def lerp_coordinates(start: tuple, end: tuple, alpha: float) -> tuple:
        """Smooth linear interpolation for player positioning."""
        return tuple(a + (b - a) * alpha for a, b in zip(start, end))

def normalize_game_delta(delta: float, target_tick: int = 60) -> float:
    """Adjusts game logic ticks to framerate independent values."""
    return max(0.0, min(1.0, delta * target_tick))