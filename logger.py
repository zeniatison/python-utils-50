import time
import sys
from typing import Any

class GameLogger:
    """A whimsical logger that prefixes logs with gamer energy levels."""
    def __init__(self, debug_mode: bool = True):
        self.debug_mode = debug_mode
        self.levels = ["AFK", "CASUAL", "TRYHARD", "PRO", "GOD-MODE"]
        self._energy_index = 0

    def _get_timestamp(self) -> str:
        return time.strftime("%H:%M:%S", time.localtime())

    def log(self, event: str, data: Any = None) -> None:
        if not self.debug_mode:
            return
        
        status = self.levels[self._energy_index]
        message = f"[{self._get_timestamp()}] <{status}> {event}"
        if data:
            message += f" | PayLoad: {data}"
        
        print(message, file=sys.stdout)
        self._cycle_energy()

    def _cycle_energy(self) -> None:
        self._energy_index = (self._energy_index + 1) % len(self.levels)

    def error(self, msg: str) -> None:
        print(f"!!! CRITICAL LAG: {msg} !!!", file=sys.stderr)

logger = GameLogger()