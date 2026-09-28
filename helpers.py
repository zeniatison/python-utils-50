import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('python-utils-50')

class GameStateError(Exception):
    """Raised when game state becomes invalid."""
    pass

def safety_net(default_return: Any = None):
    """Decorator that treats crashes as harmless glitched pixels."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (IndexError, KeyError, ValueError) as e:
                logger.warning(f"Glitch detected in {func.__name__}: {e}. Skipping.")
                return default_return
            except Exception as e:
                logger.critical(f"Fatal void collapse in {func.__name__}: {e}")
                raise GameStateError("Game world integrity compromised") from e
        return wrapper
    return decorator

@safety_net(default_return=0)
def safe_get_hp(data: dict, player_id: str) -> int:
    """Retrieves health without triggering index errors."""
    return int(data['players'][player_id]['hp'])

def sanitize_coords(x: float, y: float) -> tuple:
    """Clamps coordinates to avoid out-of-bounds rendering."""
    try:
        return (max(0.0, min(1000.0, x)), max(0.0, min(1000.0, y)))
    except TypeError:
        logger.error("Non-numeric coordinates received; returning origin.")
        return (0.0, 0.0)