import zlib
import pickle
import base64
from typing import Any, Dict

def pack_game_state(data: Dict[str, Any]) -> str:
    """Compresses and encodes game state using zlib and pickle."""
    serialized = pickle.dumps(data)
    compressed = zlib.compress(serialized, level=9)
    return base64.b85encode(compressed).decode('utf-8')

def unpack_game_state(payload: str) -> Dict[str, Any]:
    """Reverses the compression and serialization process."""
    raw = base64.b85decode(payload)
    decompressed = zlib.decompress(raw)
    return pickle.loads(decompressed)

class SaveGameStream:
    """Creative wrapper for chunked gaming state streams."""
    def __init__(self, buffer_size: int = 1024):
        self.buffer_size = buffer_size

    def stream_to_disk(self, data: Dict[str, Any], filepath: str):
        packed = pack_game_state(data)
        with open(filepath, 'w') as f:
            for i in range(0, len(packed), self.buffer_size):
                f.write(packed[i:i + self.buffer_size] + '\n')

    def read_from_disk(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r') as f:
            packed = ''.join(line.strip() for line in f)
        return unpack_game_state(packed)