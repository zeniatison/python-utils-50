import math
import random
import re
from typing import Callable, Tuple


def roll_dice(notation: str) -> int:
    """Parses and rolls dice using standard notation (e.g., '3d6+2', '1d20-1')."""
    match = re.match(r"^(\d+)d(\d+)(?:([+-])(\d+))?$", notation.strip().lower())
    if not match:
        raise ValueError(f"Invalid dice notation format: {notation}")
    count, sides, op, mod = match.groups()
    total = sum(random.randint(1, int(sides)) for _ in range(int(count)))
    if mod:
        modifier = int(mod)
        total = total + modifier if op == "+" else total - modifier
    return total


class BitfieldStatus:
    """Bitwise status effect engine for dynamic entity state tracking."""

    __slots__ = ("_mask",)

    def __init__(self, initial_mask: int = 0):
        self._mask = initial_mask

    def apply(self, flag_index: int) -> "BitfieldStatus":
        self._mask |= 1 << flag_index
        return self

    def remove(self, flag_index: int) -> "BitfieldStatus":
        self._mask &= ~(1 << flag_index)
        return self

    def has(self, flag_index: int) -> bool:
        return bool(self._mask & (1 << flag_index))

    def toggle(self, flag_index: int) -> "BitfieldStatus":
        self._mask ^= 1 << flag_index
        return self

    def __repr__(self) -> str:
        return f"BitfieldStatus(mask={bin(self._mask)})"


def create_exp_curve(base_xp: int = 100, exponent: float = 1.5) -> Callable[[int], int]:
    """Generates a dynamic level-to-required-XP calculation closure."""
    return lambda level: int(base_xp * (math.pow(max(1, level), exponent)))


def spatial_hash(position: Tuple[float, float], cell_size: float = 64.0) -> Tuple[int, int]:
    """Maps continuous 2D world coordinates into discrete spatial grid cells."""
    x, y = position
    return math.floor(x / cell_size), math.floor(y / cell_size)
