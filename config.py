import functools
import sys

class GameConfig:
    __slots__ = ('_cache', '_data')

    def __init__(self):
        self._cache = {}
        self._data = {'fps_cap': 144, 'render_distance': 1000}

    @staticmethod
    def fast_memoize(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        return wrapper

    def get_setting(self, key):
        return self._data.get(key)

    @fast_memoize
    def calculate_tick_rate(self, multiplier):
        return self._data['fps_cap'] * multiplier

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Config {name} not found')

    def batch_update(self, **kwargs):
        for k, v in kwargs.items():
            self._data[k] = v
        self.calculate_tick_rate.cache_clear() if hasattr(self.calculate_tick_rate, 'cache_clear') else None

def get_instance():
    if 'instance' not in sys.modules[__name__].__dict__:
        sys.modules[__name__].instance = GameConfig()
    return sys.modules[__name__].instance