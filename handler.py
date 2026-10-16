import time
import random
from functools import wraps

def loot_generator(rarity_table: dict):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            roll = random.random()
            cumulative = 0
            for item, chance in rarity_table.items():
                cumulative += chance
                if roll <= cumulative:
                    return item
            return 'common_junk'
        return wrapper
    return decorator

def entity_serializer(obj):
    return {k: v for k, v in vars(obj).items() if not k.startswith('_')}

def frame_rate_throttle(fps=60):
    target = 1.0 / fps
    last_time = [time.time()]
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_time[0]
            if elapsed < target:
                time.sleep(target - elapsed)
            result = func(*args, **kwargs)
            last_time[0] = time.time()
            return result
        return wrapper
    return decorator

def batch_process(data, chunk_size=10):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

class GameStateManager:
    def __init__(self):
        self.registry = {}

    def track(self, key, value):
        self.registry[key] = {'val': value, 'ts': time.time()}

    def cleanup(self, max_age):
        now = time.time()
        self.registry = {k: v for k, v in self.registry.items() if now - v['ts'] < max_age}