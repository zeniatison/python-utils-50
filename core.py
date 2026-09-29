import time
import functools
import random

def gaming_retry(max_attempts=3, backoff=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    wait_time = backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(wait_time)
        return wrapper
    return decorator

@gaming_retry(max_attempts=5, backoff=1.0)
def fetch_server_state(endpoint):
    # Simulate network instability in game matchmaking
    if random.random() < 0.7:
        raise ConnectionError("Latency spike detected")
    return {"status": "ready", "players": 42}

class GameNetworkClient:
    def __init__(self, host):
        self.host = host

    def execute(self, command):
        @gaming_retry(max_attempts=3)
        def perform():
            return f"Command {command} executed on {self.host}"
        return perform()