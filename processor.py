import math
from typing import Dict, List, Any, Generator

class InvalidInputError(Exception):
    """Raised when incoming client packet violates schema or physics bounds."""
    pass

class FrameProcessor:
    def __init__(self, max_speed: float = 300.0):
        self.max_speed = max_speed
        self.last_ts = 0.0
        self.last_pos = (0.0, 0.0)

    def validate_and_process(self, stream: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        for tick, packet in enumerate(stream):
            try:
                if not isinstance(packet, dict):
                    raise InvalidInputError(f"Tick {tick}: packet is non-dict structure")
                
                missing = {'ts', 'x', 'y', 'cmd'} - packet.keys()
                if missing:
                    raise InvalidInputError(f"Tick {tick}: missing fields {missing}")

                ts, x, y, cmd = packet['ts'], packet['x'], packet['y'], packet['cmd']

                if not isinstance(ts, (int, float)) or ts < self.last_ts:
                    raise InvalidInputError(f"Tick {tick}: rewind or invalid timestamp {ts}")

                if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
                    raise InvalidInputError(f"Tick {tick}: non-numeric coords ({x}, {y})")

                dt = ts - self.last_ts if self.last_ts > 0 else 0.016
                dist = math.hypot(x - self.last_pos[0], y - self.last_pos[1])
                if dt > 0 and (dist / dt) > self.max_speed:
                    raise InvalidInputError(f"Tick {tick}: speed anomalous ({dist/dt:.1f} u/s)")

                self.last_ts = ts
                self.last_pos = (float(x), float(y))

                yield {
                    "tick": tick,
                    "status": "ok",
                    "cmd": str(cmd).lower(),
                    "position": self.last_pos
                }
            except InvalidInputError as err:
                yield {
                    "tick": tick,
                    "status": "rejected",
                    "reason": str(err)
                }
