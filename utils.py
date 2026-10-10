import functools
import zlib
import pickle
from typing import Any, Callable

def gaming_data_compressor(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> bytes:
        result = func(*args, **kwargs)
        raw_data = pickle.dumps(result)
        return zlib.compress(raw_data, level=9)
    return wrapper

def gaming_data_decompressor(payload: bytes) -> Any:
    decompressed = zlib.decompress(payload)
    return pickle.loads(decompressed)

class StatsAggregator:
    def __init__(self):
        self._store = {}

    def track(self, key: str, value: int):
        self._store[key] = self._store.get(key, 0) + value

    def export(self) -> bytes:
        return zlib.compress(pickle.dumps(self._store))

@gaming_data_compressor
def generate_mock_player_data(player_id: int) -> dict:
    return {
        'uid': player_id,
        'inventory': ['sword', 'shield', 'potion'],
        'stats': {'str': 10, 'dex': 12, 'int': 8}
    }