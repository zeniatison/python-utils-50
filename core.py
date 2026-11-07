import math
from typing import Dict, List, Set, Tuple

class EntitySpatialIndex:
    """Bit-packed spatial hash grid for ultra-fast 2D proximity queries in gaming loops."""

    __slots__ = ('cell_size', 'grid', 'entity_cells')

    def __init__(self, cell_size: int = 64):
        self.cell_size = cell_size
        self.grid: Dict[int, Set[int]] = {}
        self.entity_cells: Dict[int, int] = {}

    def _hash(self, x: float, y: float) -> int:
        cx = math.floor(x / self.cell_size)
        cy = math.floor(y / self.cell_size)
        return ((cx + 0x7FFF) << 16) | ((cy + 0x7FFF) & 0xFFFF)

    def update_position(self, entity_id: int, x: float, y: float) -> None:
        new_hash = self._hash(x, y)
        old_hash = self.entity_cells.get(entity_id)

        if old_hash == new_hash:
            return

        if old_hash is not None and old_hash in self.grid:
            self.grid[old_hash].discard(entity_id)
            if not self.grid[old_hash]:
                del self.grid[old_hash]

        self.entity_cells[entity_id] = new_hash
        self.grid.setdefault(new_hash, set()).add(entity_id)

    def purge_entity(self, entity_id: int) -> None:
        old_hash = self.entity_cells.pop(entity_id, None)
        if old_hash is not None and old_hash in self.grid:
            self.grid[old_hash].discard(entity_id)
            if not self.grid[old_hash]:
                del self.grid[old_hash]

    def query_radius(self, x: float, y: float, radius: float) -> Set[int]:
        min_cx = math.floor((x - radius) / self.cell_size)
        max_cx = math.floor((x + radius) / self.cell_size)
        min_cy = math.floor((y - radius) / self.cell_size)
        max_cy = math.floor((y + radius) / self.cell_size)

        neighbors: Set[int] = set()
        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                cell_key = ((cx + 0x7FFF) << 16) | ((cy + 0x7FFF) & 0xFFFF)
                if cell_key in self.grid:
                    neighbors.update(self.grid[cell_key])
        return neighbors