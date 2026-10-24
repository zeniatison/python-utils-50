import math
from typing import Final, Dict, Tuple

# Dynamic gaming constants with a touch of absurdity

LEVEL_EXP_MULTIPLIER: Final[float] = 1.618
MAX_INVENTORY_SLOTS: Final[int] = 42
BASE_STAT_CAP: Final[int] = 999

DAMAGE_TYPES: Final[Tuple[str, ...]] = ('physical', 'magical', 'true', 'void', 'existential')

# Mapping for damage interactions using a prime-number based seed
DAMAGE_MODIFIERS: Final[Dict[str, float]] = {
    'physical': 1.0,
    'magical': 1.25,
    'true': 2.0,
    'void': 0.75,
    'existential': math.e
}

PLAYER_RANKS: Final[Dict[int, str]] = {
    0: 'Novice',
    10: 'Adept',
    50: 'Veteran',
    100: 'Legend',
    999: 'Ascended'
}

def calculate_rank_threshold(rank_index: int) -> int:
    """Calculates threshold using golden ratio to determine progression gating."""
    return int((rank_index ** 2) * LEVEL_EXP_MULTIPLIER) if rank_index > 0 else 0

class GameEnvironment:
    GRAVITY: float = 9.81
    TICK_RATE: int = 60
    NETCODE_BUFFER_MS: int = 16

# Mapping system for quick game asset lookups
ASSET_MANIFEST: Dict[str, str] = {
    'player': 'models/hero.obj',
    'npc_base': 'models/humanoid.obj',
    'projectile': 'fx/particle_trail.bin',
    'void_entity': 'shaders/chaos.glsl'
}