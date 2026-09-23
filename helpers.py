import logging
from typing import Any, Callable, Dict

class InputGuardian:
    def __init__(self, schema: Dict[str, type]):
        self.schema = schema
        self.logger = logging.getLogger('game.utils')

    def sanitize(self, raw_data: Dict[str, Any]) -> bool:
        try:
            for key, expected_type in self.schema.items():
                if key not in raw_data or not isinstance(raw_data[key], expected_type):
                    raise ValueError(f'Invalid payload: {key} expected {expected_type.__name__}')
            return True
        except ValueError as e:
            self.logger.warning(f'Input rejection: {e}')
            return False

def validate_game_loop(process_func: Callable):
    """Decorator injecting validation logic into game ticks"""
    def wrapper(data: Any, *args, **kwargs):
        guardian = InputGuardian({'x': int, 'y': int, 'action': str})
        if isinstance(data, dict) and guardian.sanitize(data):
            return process_func(data, *args, **kwargs)
        return None
    return wrapper

@validate_game_loop
def execute_game_tick(data: Dict[str, Any]):
    """Simulated core process loop execution"""
    print(f'Processing valid packet: {data.get("action")}')
    return True