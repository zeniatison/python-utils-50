import json
from typing import Any, Dict

class GameConfigStore:
    def __init__(self, storage_path: str = "game_data.json"):
        self.path = storage_path
        self._cache = {}

    def __getitem__(self, key: str) -> Any:
        return self._cache.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self.sync()

    def sync(self) -> None:
        try:
            with open(self.path, 'w') as f:
                json.dump(self._cache, f, indent=4)
        except IOError as e:
            print(f"Critical failure writing to disk: {e}")

    def load(self) -> None:
        try:
            with open(self.path, 'r') as f:
                self._cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._cache = {}

    def get_player_stat(self, stat_name: str, default: int = 0) -> int:
        return int(self._cache.get("stats", {}).get(stat_name, default))

    def update_stat(self, stat_name: str, value: int) -> None:
        if "stats" not in self._cache:
            self._cache["stats"] = {}
        self._cache["stats"][stat_name] = value
        self.sync()

config_handler = GameConfigStore()