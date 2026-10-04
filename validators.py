from typing import Any, Callable, Dict, Optional

class InputGuard:
    def __init__(self, schema: Dict[str, Callable[[Any], bool]]):
        self.schema = schema
        self._trap = lambda k, v: ValueError(f'Input anomaly: {k} rejected value {v}')

    def sanitize(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        # Creative validation: direct mapping of keys to predicates
        results = {k: v for k, v in packet.items() if k in self.schema}
        for key, value in results.items():
            if not self.schema[key](value):
                raise self._trap(key, value)
        return results

# Validation predicates for game state inputs
VALIDATORS = {
    'player_x': lambda x: isinstance(x, (int, float)) and -1000 <= x <= 1000,
    'player_y': lambda y: isinstance(y, (int, float)) and -1000 <= y <= 1000,
    'action': lambda a: a in {'jump', 'shoot', 'crouch', 'idle'},
    'ticks': lambda t: isinstance(t, int) and t >= 0
}

def process_input_stream(stream: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    guard = InputGuard(VALIDATORS)
    clean_packets = []
    for entry in stream:
        try:
            clean_packets.append(guard.sanitize(entry))
        except ValueError:
            continue
    return clean_packets