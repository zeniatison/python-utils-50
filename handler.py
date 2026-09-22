import time
import functools
import random

def loot_generator(pool, luck_factor=1.0):
    weights = [item.get('weight', 1) * luck_factor for item in pool]
    return random.choices(pool, weights=weights, k=1)[0]

def mana_throttle(rate_limit=1.0):
    def decorator(func):
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < rate_limit:
                time.sleep(rate_limit - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

def sanitize_player_name(name):
    return ''.join(c for c in name if c.isalnum() or c in ['_', '-'])[:16]

class GameStateSync:
    def __init__(self):
        self._registry = {}

    def update_entity(self, eid, data):
        self._registry.update({eid: {'ts': time.time(), **data}})

    def get_snapshot(self):
        return self._registry.copy()

    def purge_stale(self, timeout=5.0):
        now = time.time()
        self._registry = {k: v for k, v in self._registry.items() if now - v['ts'] < timeout}