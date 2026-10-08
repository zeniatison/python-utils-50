import math
from typing import Generator, Dict, Any, Tuple

class InputValidationError(ValueError):
    pass

class CoreProcessor:
    def __init__(self, screen_bounds: Tuple[int, int] = (1920, 1080)):
        self.bounds = screen_bounds
        self.allowed_actions = {"MOVE", "SHOOT", "JUMP", "DODGE"}
        self._prev_pos = 0+0j

    def validate_event(self, event: Dict[str, Any]) -> Tuple[str, Any]:
        action = event.get("action")
        if action not in self.allowed_actions:
            raise InputValidationError(f"Illegal action attempt: {action}")

        payload = event.get("payload")
        if not isinstance(payload, dict):
            raise InputValidationError("Malformed payload layout")

        if action == "MOVE":
            coords = payload.get("vector", (0, 0))
            if not (isinstance(coords, (list, tuple)) and len(coords) == 2):
                raise InputValidationError("Invalid coordinate dimensions")
            
            x, y = coords
            if not (0 <= x <= self.bounds[0] and 0 <= y <= self.bounds[1]):
                raise InputValidationError(f"Out of bounds: ({x}, {y})")

            pos_diff = complex(*coords)
            if abs(pos_diff - self._prev_pos) > 150.0:
                raise InputValidationError("Movement velocity anomaly: delta exceeds threshold")
            self._prev_pos = pos_diff

        elif action == "SHOOT":
            cooldown = payload.get("cooldown", 0.0)
            if cooldown < 0.1:
                raise InputValidationError("Cooldown bypassing suspected")

        return action, payload

    def process_stream(self, stream: Generator[Dict[str, Any], None, None]) -> Generator[Tuple[str, Any], None, None]:
        for event in stream:
            try:
                yield self.validate_event(event)
            except InputValidationError:
                continue
