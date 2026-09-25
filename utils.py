import time
import functools
import random

def retry_gaming_op(max_attempts=3, backoff=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    sleep_time = backoff * (2 ** attempt) + (random.random() * 0.1)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

class NetworkThrottler:
    def __init__(self, limit):
        self.limit = limit
        self.tokens = limit
        self.last_update = time.monotonic()

    def consume(self):
        now = time.monotonic()
        self.tokens = min(self.limit, self.tokens + (now - self.last_update))
        self.last_update = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False