import functools
import zlib
import base64
import json
from typing import Any, Dict

def pack_game_state(state: Dict[str, Any]) -> str:
    """Compresses game state dictionary into a transportable string."""
    serialized = json.dumps(state).encode('utf-8')
    compressed = zlib.compress(serialized, level=9)
    return base64.b64encode(compressed).decode('utf-8')

def unpack_game_state(payload: str) -> Dict[str, Any]:
    """Restores game state from a compressed payload."""
    decoded = base64.b64decode(payload.encode('utf-8'))
    decompressed = zlib.decompress(decoded)
    return json.loads(decompressed.decode('utf-8'))

def loot_generator(pool: Dict[str, float]):
    """Uses weighted probability distribution for drop logic."""
    import random
    items = list(pool.keys())
    weights = list(pool.values())
    
    def selector():
        return random.choices(items, weights=weights, k=1)[0]
    
    return selector

class ManaBurnGuard:
    """Context manager for resource-heavy gameplay state transitions."""
    def __init__(self, state_dict: Dict):
        self.state = state_dict
        self.backup = None

    def __enter__(self):
        self.backup = self.state.copy()
        return self.state

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.state.clear()
            self.state.update(self.backup)
        return False