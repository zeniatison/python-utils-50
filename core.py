import functools
import time

class GameRegistry:
    def __init__(self):
        self._registry = {}
        self._manifest = []

    def register(self, tag):
        def decorator(func):
            self._registry[tag] = func
            self._manifest.append(tag)
            return func
        return decorator

    def execute_pipeline(self, *args, **kwargs):
        results = []
        for tag in self._manifest:
            start = time.perf_counter()
            res = self._registry[tag](*args, **kwargs)
            results.append((tag, res, time.perf_counter() - start))
        return results

def throttle(rate_limit):
    def decorator(func):
        state = {'last_call': 0}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - state['last_call']
            if elapsed < rate_limit:
                return None
            state['last_call'] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

class EntityStream:
    def __init__(self, entities):
        self.data = list(entities)

    def filter_by_power(self, threshold):
        return [e for e in self.data if e.get('power', 0) > threshold]

    def apply_batch(self, func):
        return [func(e) for e in self.data]

registry = GameRegistry()