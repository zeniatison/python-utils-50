from typing import List, Dict, Any, Union, Optional

class GameStateProcessor:
    def __init__(self, entities: List[Dict[str, Any]]) -> None:
        self.entities = entities

    def get_active_players(self, min_health: int = 1) -> List[Dict[str, Any]]:
        """
        Filters entities list returning only living players.
        Uses a generator expression for memory-efficient iteration.
        """
        return [e for e in self.entities if e.get('type') == 'player' and e.get('hp', 0) >= min_health]

    def calculate_entity_density(self, area_volume: float) -> float:
        """
        Calculates distribution ratio of entities within defined volume.
        Raises ValueError if volume is non-positive.
        """
        if area_volume <= 0:
            raise ValueError("Spatial volume must be a positive scalar.")
        return len(self.entities) / area_volume

    def augment_state(self, key: str, value: Any) -> None:
        """
        Injects metadata into all managed entities dynamically.
        """
        for entity in self.entities:
            entity[key] = value

def process_collision_batch(events: List[Dict[str, Union[int, str]]]) -> Dict[str, int]:
    """
    Aggregates collision types from a raw event stream.
    Returns a frequency map of collision impact levels.
    """
    summary: Dict[str, int] = {}
    for event in events:
        impact = str(event.get('severity', 'minor'))
        summary[impact] = summary.get(impact, 0) + 1
    return summary