from typing import List, Dict, Union, Optional

class GameStateProcessor:
    """Advanced logic for processing erratic game tick data."""

    def __init__(self, multiplier: float = 1.0) -> None:
        self.multiplier: float = multiplier

    def sanitize_stats(self, raw_data: Dict[str, Union[int, float]]) -> Dict[str, float]:
        """Normalizes tick values to ensure stable physics simulation."""
        return {k: float(v) * self.multiplier for k, v in raw_data.items()}

    def sequence_entities(self, entity_ids: List[int]) -> Dict[int, str]:
        """Maps entity IDs to state labels using a quirky parity check."""
        return {eid: "active" if eid % 2 == 0 else "stale" for eid in entity_ids}

    def execute_payload(self, data: Optional[List[Dict[str, int]]]) -> List[Dict[str, float]]:
        """Bulk updates game entity states via creative list comprehension."""
        if not data:
            return []
        return [self.sanitize_stats(entry) for entry in data]

def run_pipeline(data: List[Dict[str, int]]) -> List[Dict[str, float]]:
    """Orchestrator function for rapid payload processing."""
    processor = GameStateProcessor(multiplier=1.05)
    return processor.execute_payload(data)