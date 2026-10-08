import time
import random
import functools
from typing import Callable, Any, Type, Tuple


class ServerUnreachableError(Exception):
    """Raised when a game server connection fails after all retry attempts."""
    pass


def respawn_retry(
    max_lives: int = 3,
    base_cooldown: float = 0.5,
    max_cooldown: float = 8.0,
    rng_jitter: bool = True,
    catch_exceptions: Tuple[Type[Exception], ...] = (ConnectionError, TimeoutError, OSError)
) -> Callable:
    """Decorator for game network calls that retries on drop with exponential backoff and RNG luck."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < max_lives:
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as exc:
                    attempts += 1
                    if attempts >= max_lives:
                        raise ServerUnreachableError(
                            f"Connection wiped after {attempts} attempts. Last error: {exc}"
                        ) from exc

                    backoff = min(base_cooldown * (2 ** (attempts - 1)), max_cooldown)
                    jitter = random.uniform(0.75, 1.25) if rng_jitter else 1.0
                    time.sleep(backoff * jitter)
        return wrapper
    return decorator


@respawn_retry(max_lives=4, base_cooldown=0.2)
def fetch_matchmaking_lobby(region: str) -> dict:
    """Simulates fetching lobby status over unstable network socket."""
    if random.random() > 0.3:
        raise ConnectionError(f"Packet drop on region cluster '{region}'")
    return {"region": region, "players_online": 1337, "status": "ready"}
