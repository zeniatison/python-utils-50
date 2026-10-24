import time
import functools
import random

def retry_network_ops(retries=3, delay=1.0, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff
        return wrapper
    return decorator

def sync_game_state(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SYNC-ERR]: {e} - discarding packet")
            return None
    return wrapper

@retry_network_ops(retries=5, delay=0.5)
def fetch_server_data(endpoint):
    # Mock network call
    if random.random() < 0.7:
        raise ConnectionError("Latency spike in lobby service")
    return {"status": "ready", "tick": 128}