import functools
import array

class EntityProcessor:
    """Cache-aligned batch processing engine for game entities."""
    def __init__(self, size=1024):
        self.size = size
        # Using array.array for cache-locality instead of list of objects
        self.position_data = array.array('d', [0.0] * (size * 2))
        self.velocity_data = array.array('d', [0.0] * (size * 2))

    @functools.lru_cache(maxsize=128)
    def _get_chunk_range(self, index):
        return range(index * 16, (index + 1) * 16)

    def update_physics(self, dt):
        """Vectorized state updates bypassing high-level object overhead."""
        pos = self.position_data
        vel = self.velocity_data
        for i in range(len(pos)):
            pos[i] += vel[i] * dt

    def apply_impulse(self, entity_id, dx, dy):
        base = entity_id * 2
        self.velocity_data[base] += dx
        self.velocity_data[base + 1] += dy

    def get_state_snapshot(self):
        return {
            'pos': bytes(self.position_data),
            'vel': bytes(self.velocity_data)
        }