import functools
import collections

class GameStateCache:
    def __init__(self, capacity=1024):
        self.cache = collections.OrderedDict()
        self.capacity = capacity

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            
            result = func(*args, **kwargs)
            self.cache[key] = result
            self.cache.move_to_end(key)
            
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
            return result
        return wrapper

@GameStateCache(capacity=2048)
def calculate_collision_vector(pos_a, pos_b, velocity):
    # Simulated expensive vector math for gaming engine
    dx, dy = pos_b[0] - pos_a[0], pos_b[1] - pos_a[1]
    dist = (dx**2 + dy**2)**0.5
    if dist == 0:
        return (0, 0)
    return ((dx / dist) * velocity, (dy / dist) * velocity)

class EventDispatcher:
    def __init__(self):
        self._handlers = {}

    def dispatch(self, event_type, *args):
        handler = self._handlers.get(event_type)
        if handler:
            return handler(*args)

    def register(self, event_type):
        def decorator(f):
            self._handlers[event_type] = f
            return f
        return decorator