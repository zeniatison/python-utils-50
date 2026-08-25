import time
import random
from functools import wraps
from typing import Any, Callable, Optional

class RetryStrategy:
    @staticmethod
    def exponential(attempt: int, base_delay: float = 1.0) -> float:
        return min(base_delay * (2 ** attempt) + random.uniform(0, base_delay), 60.0)

    @staticmethod
    def linear(attempt: int, base_delay: float = 1.0) -> float:
        return base_delay * (attempt + 1) + random.uniform(0, 0.5)

    @staticmethod
    def fibonacci(attempt: int, base_delay: float = 1.0) -> float:
        if attempt <= 1:
            return base_delay
        a = base_delay
        b = base_delay
        for _ in range(2, attempt + 1):
            a, b = b, a + b
        return b + random.uniform(0, 0.5)

class NetworkRetryHandler:
    def __init__(self, max_attempts: int = 5, strategy: Callable[[int, float], float] = RetryStrategy.exponential, base_delay: float = 1.0):
        self.max_attempts = max_attempts
        self.strategy = strategy
        self.base_delay = base_delay

    def execute(self, operation: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        last_error: Optional[Exception] = None
        for attempt in range(self.max_attempts):
            try:
                return operation(*args, **kwargs)
            except Exception as error:
                last_error = error
                if attempt == self.max_attempts - 1:
                    break
                delay = self.strategy(attempt, self.base_delay)
                time.sleep(delay)
        raise last_error if last_error else RuntimeError("Unknown retry failure")

def retry_network(max_attempts: int = 5, strategy: Callable = RetryStrategy.exponential, base_delay: float = 1.0) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            handler = NetworkRetryHandler(max_attempts, strategy, base_delay)
            return handler.execute(func, *args, **kwargs)
        return wrapper
    return decorator

class GameNetworkUtils:
    def __init__(self, server: str = "game.example.com"):
        self.server = server

    @retry_network(max_attempts=4, base_delay=0.5, strategy=RetryStrategy.linear)
    def fetch_game_stats(self, player_id: int) -> dict:
        if random.random() < 0.65:
            raise ConnectionError(f"Network error fetching stats for player {player_id}")
        return {"player_id": player_id, "score": random.randint(100, 1000), "level": random.randint(1, 50)}

    def query_leaderboard(self) -> list:
        def get_leaderboard():
            if random.random() < 0.4:
                raise TimeoutError("Leaderboard query timed out")
            return [{"name": "player1", "score": 1500}, {"name": "player2", "score": 1400}]
        handler = NetworkRetryHandler(max_attempts=3, strategy=RetryStrategy.fibonacci)
        return handler.execute(get_leaderboard)
