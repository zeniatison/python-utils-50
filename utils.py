import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('gaming_utils')

class GameStateError(Exception):
    pass

def robust_game_action(retries: int = 3, default_value: Any = None):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except (ValueError, TypeError, GameStateError) as e:
                    attempts += 1
                    logger.warning(f"Action failed {func.__name__}: {e}. Retry {attempts}/{retries}")
                    if attempts == retries:
                        break
            return default_value
        return wrapper
    return decorator

@robust_game_action(retries=2, default_value=0)
def calculate_xp_gain(base_xp, multiplier):
    if not isinstance(base_xp, (int, float)) or not isinstance(multiplier, (int, float)):
        raise ValueError("XP and multiplier must be numeric values")
    if base_xp < 0:
        raise GameStateError("Negative XP is mathematically invalid")
    return base_xp * multiplier

def validate_player_payload(data: dict):
    try:
        return all(key in data for key in ('player_id', 'level'))
    except (AttributeError, TypeError):
        return False