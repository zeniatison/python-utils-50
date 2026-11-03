import time
import random
from functools import wraps

def retry_gaming_network(attempts=3, backoff_base=1.5, jitter=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    if i == attempts - 1:
                        break
                    sleep_time = (backoff_base ** i) + (random.random() if jitter else 0)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

@retry_gaming_network(attempts=4, backoff_base=2)
def sync_game_state(payload):
    # Simulate network instability in gaming sessions
    if random.random() < 0.7:
        raise ConnectionError("Packet loss detected in match")
    return {"status": "synced", "data": payload}

if __name__ == "__main__":
    try:
        result = sync_game_state({"player_pos": (10, 20)})
        print(f"Sync success: {result}")
    except ConnectionError as e:
        print(f"Critical network failure: {e}")