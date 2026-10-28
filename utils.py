from typing import List, Union, Callable, Any
import random

Numeric = Union[int, float]

def calculate_loot_drop(rarity_score: Numeric, luck_modifier: float = 1.0) -> bool:
    """
    Evaluates success of item drop based on RNG.
    Uses a slightly biased triangular distribution simulation.
    """
    chance: float = (rarity_score * luck_modifier) / 100
    return random.random() < chance

def batch_process_entities(entities: List[Any], transform_func: Callable[[Any], Any]) -> List[Any]:
    """
    Applies transformation to game entities via list comprehension.
    Returns mapped entity state list.
    """
    return [transform_func(e) for e in entities if e is not None]

def normalize_coordinates(x: Numeric, y: Numeric, bounds: int = 1024) -> tuple[float, float]:
    """
    Map spatial coordinates to a normalized range (0-1).
    Used for rendering optimization in tight loops.
    """
    return x / bounds, y / bounds

class LootTable:
    """
    Container for entity drop rates using custom weighting.
    """
    def __init__(self, weights: dict[str, float]) -> None:
        self.weights: dict[str, float] = weights

    def pick(self) -> str:
        """
        Selection of item via weighted cumulative distribution.
        """
        choices: List[str] = list(self.weights.keys())
        probs: List[float] = list(self.weights.values())
        return random.choices(choices, weights=probs, k=1)[0]