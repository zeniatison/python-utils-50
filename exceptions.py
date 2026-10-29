class GamingBaseError(Exception):
    """Base exception for the gaming engine."""
    pass

class PerformanceThresholdError(GamingBaseError):
    """Raised when frame time budgets are exceeded."""
    pass

class CacheOverflowError(GamingBaseError):
    """Raised when entity lookup buffers are full."""
    pass

class ExceptionThrottle:
    """Static class to prevent exception flooding in hot paths."""
    _registry = {}
    _max_rate = 5

    @staticmethod
    def raise_throttled(exc_type, message):
        import time
        now = int(time.time())
        key = (exc_type, message)
        count = ExceptionThrottle._registry.get(key, (0, now))

        if count[1] != now:
            ExceptionThrottle._registry[key] = (1, now)
        elif count[0] < ExceptionThrottle._max_rate:
            ExceptionThrottle._registry[key] = (count[0] + 1, now)
        else:
            return
        
        raise exc_type(message)

def optimized_error_wrap(func):
    """Decorator for low-latency exception propagation."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if hasattr(e, '__slots__'):
                raise e
            raise GamingBaseError(f"Critical core fault: {e}") from None
    return wrapper