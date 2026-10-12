import os
from typing import Dict, Any

class GameConfig:
    _storage: Dict[str, Any] = {}

    def __init__(self, env: str = "development"):
        self.env = env
        self.refresh()

    def refresh(self) -> None:
        self._storage = {
            "debug": self.env == "development",
            "tick_rate": 60 if self.env == "production" else 30,
            "assets_path": os.getenv("ASSET_DIR", "./assets"),
            "max_players": int(os.getenv("MAX_PLAYERS", "32"))
        }

    def __getattr__(self, name: str) -> Any:
        if name not in self._storage:
            raise AttributeError(f"Config property '{name}' missing")
        return self._storage[name]

    def __getitem__(self, key: str) -> Any:
        return self._storage.get(key)

    def __repr__(self) -> str:
        return f"<GameConfig env={self.env} stats={self._storage}>"

def get_global_config() -> GameConfig:
    return GameConfig(os.getenv("GAME_ENV", "development"))