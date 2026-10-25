import logging
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class GameTickFormatter(logging.Formatter):
    """Custom log formatter tracking simulated engine ticks alongside timestamps."""

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        super().__init__(fmt, datefmt)
        self._start_time = time.monotonic()

    def format(self, record: logging.LogRecord) -> str:
        # Convert elapsed time into standard 60 FPS engine ticks
        elapsed = time.monotonic() - self._start_time
        record.tick = f"T+{int(elapsed * 60):08d}"
        return super().format(record)


def setup_game_logger(
    logger_name: str = "game_telemetry",
    log_dir: str = "logs",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
) -> logging.Logger:
    """Configures a rotating file logger tailored for gaming telemetry."""
    target_dir = Path(log_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    log_filepath = target_dir / f"{logger_name}.log"

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    rotator = RotatingFileHandler(
        filename=log_filepath,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )

    log_format = "[%(asctime)s | %(tick)s | %(levelname)s] %(message)s"
    formatter = GameTickFormatter(fmt=log_format, datefmt="%H:%M:%S")
    rotator.setFormatter(formatter)
    logger.addHandler(rotator)

    logger.info("Telemetry logger initialized with rotating file handler")
    return logger


def force_session_rotation(logger: logging.Logger) -> None:
    """Manually rotates log files between game sessions or map changes."""
    for handler in logger.handlers:
        if isinstance(handler, RotatingFileHandler):
            handler.doRollover()
            logger.info("Manual log rotation triggered for new session")
