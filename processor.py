import math
from dataclasses import dataclass
from typing import Dict, Any, List, Iterator


@dataclass(frozen=True)
class CommandFrame:
    frame_id: int
    player_id: str
    move_axis: tuple[float, float]
    actions: list[str]


class FrameValidationError(Exception):
    pass


class GameInputProcessor:
    ALLOWED_ACTIONS = {"LIGHT_ATTACK", "HEAVY_ATTACK", "BLOCK", "DASH", "INTERACT"}

    def __init__(self, raw_frames: List[Dict[str, Any]]):
        self.raw_frames = raw_frames
        self.corrupted_count = 0

    def _validate_raw_payload(self, raw: Dict[str, Any]) -> CommandFrame:
        if not isinstance(raw, dict):
            raise FrameValidationError("Payload must be a dictionary")

        required_keys = {"frame_id", "player_id", "move_axis", "actions"}
        if not required_keys.issubset(raw.keys()):
            missing = required_keys - raw.keys()
            raise FrameValidationError(f"Missing required packet keys: {missing}")

        x, y = raw["move_axis"]
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            raise FrameValidationError("Move axis coordinates must be numeric")

        magnitude = math.hypot(x, y)
        if magnitude > 1.001:
            raise FrameValidationError(f"Stick vector magnitude exceeds limit: {magnitude:.2f}")

        actions = raw["actions"]
        if not isinstance(actions, list) or not set(actions).issubset(self.ALLOWED_ACTIONS):
            raise FrameValidationError("Invalid or unknown action requested")

        return CommandFrame(
            frame_id=int(raw["frame_id"]),
            player_id=str(raw["player_id"]),
            move_axis=(float(x), float(y)),
            actions=list(actions)
        )

    def run_loop(self) -> Iterator[CommandFrame]:
        last_frame_id = -1
        for packet in self.raw_frames:
            try:
                frame = self._validate_raw_payload(packet)
                if frame.frame_id <= last_frame_id:
                    raise FrameValidationError(f"Out-of-order frame ID: {frame.frame_id}")
                
                last_frame_id = frame.frame_id
                yield frame
            except (FrameValidationError, TypeError, ValueError):
                self.corrupted_count += 1
                continue
