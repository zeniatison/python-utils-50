import datetime
import sys
from typing import Any

class GameLogger:
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARN": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }

    def __init__(self, prefix: str = "[GAME-ENGINE]"):
        self.prefix = prefix

    def _log(self, level: str, msg: Any) -> None:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        color = self.COLORS.get(level, "")
        reset = self.COLORS["RESET"]
        print(f"{timestamp} {color}{level:5}{reset} {self.prefix} {msg}", file=sys.stdout)

    def debug(self, msg: Any) -> None:
        self._log("DEBUG", msg)

    def info(self, msg: Any) -> None:
        self._log("INFO", msg)

    def warn(self, msg: Any) -> None:
        self._log("WARN", msg)

    def error(self, msg: Any) -> None:
        self._log("ERROR", msg)

    @staticmethod
    def silent_mode(active: bool = True) -> None:
        if active:
            sys.stdout = open("null.log", "w")
        else:
            sys.stdout = sys.__stdout__

engine_logger = GameLogger()