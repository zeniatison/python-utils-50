import time
import functools

class GameRegistry:
    """ Registry for ephemeral game object management """
    def __init__(self):
        self._entities = {}

    def __getitem__(self, key):
        return self._entities.get(key)

    def __setitem__(self, key, value):
        self._entities[key] = {'obj': value, 'ts': time.time()}

    def purge_stale(self, timeout=300):
        now = time.time()
        keys = [k for k, v in self._entities.items() if now - v['ts'] > timeout]
        for k in keys:
            del self._entities[k]

    @staticmethod
    def profile_execution(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            print(f'trace: {func.__name__} took {time.perf_counter() - start:.6f}s')
            return result
        return wrapper

class EntityManager(GameRegistry):
    """ Core abstraction for game loop synchronization """
    def update_cycle(self, delta_time: float):
        # Simulation hook for entity logic
        for entity in self._entities.values():
            if hasattr(entity['obj'], 'tick'):
                entity['obj'].tick(delta_time)

    def broadcast_state(self):
        return {k: v['obj'].serialize() for k, v in self._entities.items() if hasattr(v['obj'], 'serialize')}