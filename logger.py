import sys
import logging
from typing import Any

class GamingLogger:
    def __init__(self, name: str = 'nexus_log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(handler)

    def safe_log(self, data: Any) -> None:
        try:
            if not isinstance(data, (str, int, float, dict, list)):
                raise ValueError(f"Unsupported game state type: {type(data).__name__}")
            self.logger.info(f"[GAME_STATE]: {data}")
        except (ValueError, TypeError) as e:
            self.logger.error(f"[CRITICAL_FAIL]: {e}")
        except Exception as e:
            self.logger.critical(f"[UNKNOWN_VOID]: {str(e)[:50]}")

    def parse_event(self, event_data: dict) -> None:
        """Graceful recovery for malformed game packets."""
        try:
            player_id = event_data.get('id', 'unknown')
            coords = event_data.get('coords', [0, 0])
            if len(coords) != 2:
                raise IndexError("Malformed spatial coordinates array")
            self.logger.info(f"Player {player_id} moved to {coords}")
        except Exception:
            self.logger.warning("Packet corruption: event skipped")

game_logger = GamingLogger()