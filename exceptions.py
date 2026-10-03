import functools
import time

class GamePerformanceError(Exception):
    """Base exception for high-frequency gaming operations."""
    pass

def cache_frame_data(func):
    """Lru cache with TTL-like expiration for transient state."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        now = time.monotonic()
        if key in cache:
            val, expiry = cache[key]
            if now < expiry:
                return val
        result = func(*args, **kwargs)
        cache[key] = (result, now + 0.016)
        return result
    return wrapper

class BufferOverflowException(GamePerformanceError):
    def __init__(self, buffer_id):
        super().__init__(f"Buffer {buffer_id} exceeded latency constraints")

class HotPathViolation(GamePerformanceError):
    def __init__(self, func_name):
        super().__init__(f"Function {func_name} executed outside time budget")

@cache_frame_data
def calculate_hitbox(coords):
    # Simulate expensive geometry math
    return tuple(x * 1.05 for x in coords)