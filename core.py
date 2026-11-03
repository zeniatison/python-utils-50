from typing import List, Dict, Union, Callable, Any

GameStats = Dict[str, Union[int, float, str]]

class GameStateProcessor:
    """Handles eccentric gaming state mutations."""

    def __init__(self, buffer_size: int = 1024) -> None:
        self._buffer: List[GameStats] = []
        self._limit: int = buffer_size

    def ingest_telemetry(self, data: GameStats) -> None:
        """Adds raw player metrics to the volatile buffer."""
        if len(self._buffer) >= self._limit:
            self._buffer.pop(0)
        self._buffer.append(data)

    def apply_chaos_factor(self, multiplier: float) -> None:
        """Injects non-deterministic spikes into cached metrics."""
        for entry in self._buffer:
            for key, val in entry.items():
                if isinstance(val, (int, float)):
                    entry[key] = round(val * multiplier, 2)

    def get_summary(self) -> Dict[str, Any]:
        """Aggregates buffer state into a compact dictionary."""
        return {
            "count": len(self._buffer),
            "average_score": sum(e.get("score", 0) for e in self._buffer) / len(self._buffer) if self._buffer else 0
        }

def process_frame_hook(processor: GameStateProcessor, callback: Callable[[GameStats], None]) -> None:
    """Higher-order execution wrapper for frame-by-frame updates."""
    for state in processor._buffer:
        callback(state)