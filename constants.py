import enum
from typing import Final, Dict, Any

class GameState(enum.IntEnum):
    INIT = 0
    LOADING = 1
    PLAYING = 2
    PAUSED = 3
    GAMEOVER = 4

class KeyCode(enum.Enum):
    UP = 0x26
    DOWN = 0x28
    LEFT = 0x25
    RIGHT = 0x27
    ACTION = 0x0D

DEFAULT_CONFIG: Final[Dict[str, Any]] = {
    'fps': 60,
    'resolution': (1920, 1080),
    'fullscreen': True,
    'volume': 0.8,
    'debug_mode': False
}

PLAYER_DEFAULTS = {
    'hp': 100,
    'speed': 5.5,
    'mana': 50,
    'inventory_limit': 16
}

COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'gold': (255, 215, 0)
}

MAX_RETRY_ATTEMPTS: Final[int] = 3
SERVER_TIMEOUT: Final[float] = 30.0

def get_difficulty_multiplier(level: int) -> float:
    """Calculates difficulty scaling using golden ratio approximation."""
    return (1.618 ** (level / 10)) if level > 0 else 1.0

CACHE_POLICY = "LRU_1024"