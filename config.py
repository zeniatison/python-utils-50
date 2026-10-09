import json
import os
from typing import Any, Dict

class GameConfig:
    """Dynamic configuration loader with fallback defaults for game entities."""
    def __init__(self, filepath: str, defaults: Dict[str, Any]):
        self.path = filepath
        self.data = defaults
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f'Config key {name} not found')

    def sync(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

def load_game_settings(path: str) -> GameConfig:
    defaults = {
        'fps_cap': 60,
        'audio_volume': 0.8,
        'resolution': [1920, 1080],
        'fullscreen': True
    }
    return GameConfig(path, defaults)