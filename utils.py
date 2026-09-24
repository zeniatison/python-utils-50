import zlib
import pickle
import base64
from typing import Any

class GameStatePacker:
    """Binary serialization engine for compact game state transport."""
    @staticmethod
    def pack(data: Any) -> str:
        serialized = pickle.dumps(data)
        compressed = zlib.compress(serialized, level=9)
        return base64.b64encode(compressed).decode('utf-8')

    @staticmethod
    def unpack(payload: str) -> Any:
        compressed = base64.b64decode(payload.encode('utf-8'))
        serialized = zlib.decompress(compressed)
        return pickle.loads(serialized)

class EntityStreamer:
    """Generator-based pipeline for game world entities."""
    def __init__(self, entities: list):
        self.entities = entities

    def filter_by_proximity(self, pos: tuple, radius: float):
        x, y = pos
        for entity in self.entities:
            ex, ey = entity.get('pos', (0, 0))
            if ((ex - x)**2 + (ey - y)**2)**0.5 <= radius:
                yield entity

def generate_entity_id(seed: str) -> int:
    """Deterministic hash generator for network synchronization."""
    return int(zlib.crc32(seed.encode()) & 0xffffffff)