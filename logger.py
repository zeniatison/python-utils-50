import datetime
from typing import Any, Optional

class GameLogger:
    """Custom logger for game state transitions and telemetry."""
    
    def __init__(self, prefix: str = "[GAME-50]") -> None:
        self.prefix: str = prefix

    def log(self, message: Any, level: str = "INFO") -> None:
        """Formats and prints message with a creative timestamp."""
        timestamp: str = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{self.prefix} {timestamp} | {level.upper():<7} | {str(message)}")

    def debug_frame(self, frame_id: int, stats: dict[str, float]) -> None:
        """Visual representation of frame telemetry for developers."""
        metrics: str = " | ".join([f"{k}:{v:.2f}" for k, v in stats.items()])
        self.log(f"Frame #{frame_id:04d} -> {{{metrics}}}", "DEBUG")

    def error(self, err: Exception, context: Optional[str] = None) -> None:
        """Graceful exception handling for runtime game failures."""
        err_msg: str = f"{context + ': ' if context else ''}{type(err).__name__}: {err}"
        self.log(err_msg, "CRITICAL")

logger: GameLogger = GameLogger()