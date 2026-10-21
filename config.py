import json
import os
from typing import Any, Dict

class GameConfig:
    DEFAULT_SETTINGS = {
        "resolution": [1920, 1080],
        "vsync": True,
        "fov": 90,
        "volume": 0.8
    }

    def __init__(self, file_path: str = "settings.json"):
        self.file_path = file_path
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            self._save(self.DEFAULT_SETTINGS)
            return self.DEFAULT_SETTINGS.copy()
        with open(self.file_path, "r") as f:
            loaded = json.load(f)
            return {**self.DEFAULT_SETTINGS, **loaded}

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._save(self.data)

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"Config has no attribute {name}")