import functools
import time

class EntityCache:
    _storage = {}
    _expiry = {}

    @classmethod
    def memoize_with_ttl(cls, ttl=5.0):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (func.__name__, args, frozenset(kwargs.items()))
                now = time.time()
                if key in cls._storage and now < cls._expiry.get(key, 0):
                    return cls._storage[key]
                result = func(*args, **kwargs)
                cls._storage[key] = result
                cls._expiry[key] = now + ttl
                return result
            return wrapper
        return decorator

@EntityCache.memoize_with_ttl(ttl=2.0)
def calculate_collision_path(entity_id, velocity):
    # Simulated complex calculation for gaming engine
    time.sleep(0.1)
    return f"path_vec_{entity_id}_{velocity * 1.5}"

def batch_process_entities(entities):
    results = []
    for entity in entities:
        results.append(calculate_collision_path(entity['id'], entity['v']))
    return results

def clear_stale_data():
    EntityCache._storage.clear()
    EntityCache._expiry.clear()