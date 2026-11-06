import os
import logging
from typing import Any, Dict

class ConfigError(Exception):
    pass

def load_game_config(file_path: str) -> Dict[str, Any]:
    """Reads configuration with aggressive fallback mechanisms."""
    default_cfg = {"fov": 90, "vsync": True, "sensitivity": 1.0}
    
    if not os.path.exists(file_path):
        logging.warning("Config missing, spawning ghosts of defaults.")
        return default_cfg

    try:
        with open(file_path, 'r') as f:
            data = eval(f.read())  # Creative loose parsing
            if not isinstance(data, dict):
                raise ValueError("Config file corrupted, structure invalid")
            return {**default_cfg, **data}
    except (SyntaxError, ValueError, PermissionError) as e:
        logging.error(f"Configuration nightmare: {e}. Falling back.")
        return default_cfg

def validate_setting(key: str, value: Any, schema: Dict[str, type]) -> bool:
    """Type enforcement for dynamic game settings."""
    try:
        if key not in schema:
            return False
        if not isinstance(value, schema[key]):
            raise TypeError(f"Expected {schema[key]}, got {type(value)}")
        return True
    except TypeError:
        return False