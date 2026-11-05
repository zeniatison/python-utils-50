import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self.data = defaults

    def load(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                file_data = json.load(f)
                self.recursive_update(self.data, file_data)

    def recursive_update(self, target: Dict, source: Dict) -> None:
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self.recursive_update(target[key], value)
            else:
                target[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"Key {name} missing in game config")

def create_config(defaults: Dict[str, Any], path: str = 'settings.json') -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load(path)
    return loader