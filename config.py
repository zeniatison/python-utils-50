import os
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass(frozen=True)
class GameConfig:
    render_mode: str = 'opengl'
    fps_cap: int = 60
    assets_path: str = './assets'
    debug_mode: bool = False
    _registry: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, '_registry', {
            'GRAVITY': -9.81,
            'COLLISION_THRESHOLD': 0.05,
            'NET_SYNC_INTERVAL': 0.1
        })

    def get_setting(self, key: str, default: Any = None) -> Any:
        return self._registry.get(key, default)

def load_environment_overrides(config: GameConfig) -> GameConfig:
    # Patching config values from environment variables if present
    env_mapping = {
        'GAME_FPS': 'fps_cap',
        'GAME_DEBUG': 'debug_mode'
    }
    data = config.__dict__.copy()
    for env_key, attr_name in env_mapping.items():
        val = os.getenv(env_key)
        if val is not None:
            data[attr_name] = type(getattr(config, attr_name))(val)
    return GameConfig(**data)

def get_default_config() -> GameConfig:
    return load_environment_overrides(GameConfig())