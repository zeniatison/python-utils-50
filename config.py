import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'settings.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self.settings = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._save(self.defaults)
            return self.defaults
        with open(self.path, 'r') as f:
            return {**self.defaults, **json.load(f)}

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.settings.get(key, fallback)

    def update(self, key: str, value: Any) -> None:
        self.settings[key] = value
        self._save(self.settings)

    def __getitem__(self, item: str) -> Any:
        return self.settings[item]

# Gaming-specific default configuration generator
def get_default_gaming_config() -> Dict[str, Any]:
    return {
        'resolution': [1920, 1080],
        'vsync': True,
        'fov': 90,
        'sensitivity': 1.5,
        'audio_master': 0.8
    }