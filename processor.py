import math
from typing import Dict, Any, Callable, List

class InvalidInputPacket(Exception):
    pass

def validate_coords(packet: Dict[str, Any]) -> Dict[str, Any]:
    x, y = packet.get("x"), packet.get("y")
    if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
        raise InvalidInputPacket("Coordinates must be numeric values")
    if math.isnan(x) or math.isnan(y) or not (-1000 <= x <= 1000 and -1000 <= y <= 1000):
        raise InvalidInputPacket("Player position outside valid arena bounds")
    return packet

def validate_action(packet: Dict[str, Any]) -> Dict[str, Any]:
    allowed_actions = {"move", "attack", "cast_spell", "use_item"}
    if packet.get("action") not in allowed_actions:
        raise InvalidInputPacket(f"Unrecognized player action: {packet.get('action')}")
    return packet

def validate_sequence(packet: Dict[str, Any]) -> Dict[str, Any]:
    tick = packet.get("tick")
    if not isinstance(tick, int) or tick < 0:
        raise InvalidInputPacket("Non-sequential or negative tick header")
    return packet

class GameInputProcessor:
    def __init__(self):
        self.validators: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = [
            validate_sequence,
            validate_action,
            validate_coords,
        ]
        self.processed_count = 0
        self.dropped_count = 0

    def process_stream(self, raw_stream: List[Any]) -> List[Dict[str, Any]]:
        clean_queue = []
        for raw_packet in raw_stream:
            try:
                if not isinstance(raw_packet, dict):
                    raise InvalidInputPacket("Malformed frame container structure")

                validated_packet = raw_packet
                for validator in self.validators:
                    validated_packet = validator(validated_packet)

                clean_queue.append(validated_packet)
                self.processed_count += 1
            except InvalidInputPacket:
                self.dropped_count += 1
                continue
        return clean_queue
