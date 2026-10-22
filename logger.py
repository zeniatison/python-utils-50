import logging
import os
from logging.handlers import RotatingFileHandler


class GameSessionFilter(logging.Filter):
    """Injects game frame metrics and session IDs into log records."""

    def __init__(self, session_id: str = "LOBBY"):
        super().__init__()
        self.session_id = session_id
        self.current_frame = 0

    def filter(self, record: logging.LogRecord) -> bool:
        self.current_frame += 1
        record.session_id = self.session_id
        record.frame = self.current_frame
        return True


class RotatingGameLogger:
    """Configures rotating logger handlers tuned for gaming telemetry."""

    def __init__(self, log_dir: str = "logs", max_megabytes: float = 2.0, keep_count: int = 3):
        self.log_dir = log_dir
        self.max_bytes = int(max_megabytes * 1024 * 1024)
        self.keep_count = keep_count
        self.filter = GameSessionFilter()
        os.makedirs(self.log_dir, exist_ok=True)

    def build_logger(self, name: str = "gamecore") -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()

        log_path = os.path.join(self.log_dir, f"{name}.log")
        file_handler = RotatingFileHandler(
            log_path, maxBytes=self.max_bytes, backupCount=self.keep_count
        )

        log_format = "[%(asctime)s] [%(session_id)s#f%(frame)06d] [%(levelname)s] %(message)s"
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)

        logger.addFilter(self.filter)
        logger.addHandler(file_handler)
        return logger

    def update_session(self, session_id: str) -> None:
        self.filter.session_id = session_id
        self.filter.current_frame = 0


def create_rotated_logger(session_name: str = "WORLD_01") -> logging.Logger:
    factory = RotatingGameLogger(max_megabytes=1.5, keep_count=5)
    factory.update_session(session_name)
    return factory.build_logger("game_events")
