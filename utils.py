import functools
import time

class CacheNode:
    def __init__(self, val, ttl):
        self.val = val
        self.expiry = time.time() + ttl

_memo_store = {}

def heavy_gaming_compute(ttl=5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in _memo_store and _memo_store[key].expiry > now:
                return _memo_store[key].val
            
            result = func(*args, **kwargs)
            _memo_store[key] = CacheNode(result, ttl)
            return result
        return wrapper
    return decorator

def batch_process_entities(data_list, chunk_size=1024):
    # Using a generator for memory-efficient iteration
    for i in range(0, len(data_list), chunk_size):
        yield data_list[i:i + chunk_size]

def optimized_math_vector_op(arr):
    # Unconventional local binding for micro-optimization
    _map = map
    _pow = pow
    return list(_map(lambda x: _pow(x, 2), arr))