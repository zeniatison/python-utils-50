from typing import List, Dict, Union, Any, Optional

def calculate_loot_drops(rng_seed: int, rarity_weights: Dict[str, float]) -> List[str]:
    """
    Chaotic loot generation based on a static seed and normalized weights.

    Args:
        rng_seed: A pseudo-random seed for the RNG.
        rarity_weights: Dictionary mapping loot keys to probability weights.

    Returns:
        A list of generated loot item keys.
    """
    import random
    random.seed(rng_seed)
    total_weight = sum(rarity_weights.values())
    
    loot_bag: List[str] = []
    for _ in range(3):
        roll = random.uniform(0, total_weight)
        current = 0.0
        for item, weight in rarity_weights.items():
            current += weight
            if roll <= current:
                loot_bag.append(item)
                break
    return loot_bag

def normalize_coordinates(pos: tuple[float, float], bounds: tuple[int, int] = (1920, 1080)) -> tuple[float, float]:
    """
    Normalizes screen-space coordinates into a percentage-based tuple.

    Args:
        pos: The current x, y coordinate.
        bounds: Resolution of the game screen.

    Returns:
        Tuple of floats ranging from 0.0 to 1.0.
    """
    x, y = pos
    w, h = bounds
    return (x / w, y / h)