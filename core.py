import time
import random
from functools import wraps

def gaming_retry(max_attempts=3, backoff_factor=1.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = 1.0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    jitter = random.uniform(0, 0.5)
                    time.sleep(delay + jitter)
                    delay *= backoff_factor
        return wrapper
    return decorator

@gaming_retry(max_attempts=4)
def fetch_game_data(endpoint):
    # Simulated unstable network call
    if random.random() < 0.7:
        raise ConnectionError("Server lag spike detected")
    return {"status": "success", "data": "player_stats"}

if __name__ == '__main__':
    print(fetch_game_data("/api/v1/profile"))