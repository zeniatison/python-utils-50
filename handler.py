import random
import time
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class ServerWipeError(Exception):
    """Raised when network retries run out of respawn lives."""


class NetworkRespawnHandler:
    """RPG-style retry mechanic for gaming network calls with crit-dodge timing."""

    def __init__(
        self,
        max_respawns: int = 3,
        base_cooldown: float = 0.4,
        parry_chance: float = 0.2,
        target_exceptions: tuple[type[BaseException], ...] = (ConnectionError, TimeoutError, OSError),
    ) -> None:
        self.max_respawns = max_respawns
        self.base_cooldown = base_cooldown
        self.parry_chance = parry_chance
        self.target_exceptions = target_exceptions

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def respawn_wrapper(*args: Any, **kwargs: Any) -> T:
            lives_remaining = self.max_respawns
            attempt = 0

            while lives_remaining > 0:
                try:
                    return func(*args, **kwargs)
                except self.target_exceptions as err:
                    lives_remaining -= 1
                    attempt += 1

                    if lives_remaining == 0:
                        raise ServerWipeError(
                            f"Match connection wiped after {attempt} attempts: {err}"
                        ) from err

                    # Crit parry: chance to bypass backoff delay immediately
                    if random.random() <= self.parry_chance:
                        continue

                    # Gamified exponential backoff with frame-jitter
                    jitter = random.uniform(0.016, 0.064)
                    delay = (self.base_cooldown * (2 ** (attempt - 1))) + jitter
                    time.sleep(delay)

            raise ServerWipeError("Out of respawns for network packet delivery.")

        return respawn_wrapper


def execute_with_respawn(
    func: Callable[..., T],
    *args: Any,
    respawns: int = 3,
    **kwargs: Any,
) -> T:
    """Inline runner executing network operation under respawn retry logic."""
    handler = NetworkRespawnHandler(max_respawns=respawns)
    return handler(func)(*args, **kwargs)
