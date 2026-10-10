import math
from typing import Dict, List, Tuple, Set

class FastSpatialGrid:
    """Bit-shifting spatial partition grid for ultra-fast gaming entity proximity queries."""
    
    __slots__ = ('cell_size', 'shift', 'grid')

    def __init__(self, cell_size: int = 64):
        self.cell_size = cell_size
        self.shift = cell_size.bit_length() - 1 if (cell_size & (cell_size - 1)) == 0 and cell_size > 0 else None
        self.grid: Dict[Tuple[int, int], Set[int]] = {}

    def _hash_coords(self, x: float, y: float) -> Tuple[int, int]:
        if self.shift:
            return (int(x) >> self.shift, int(y) >> self.shift)
        return (int(x) // self.cell_size, int(y) // self.cell_size)

    def clear(self) -> None:
        self.grid.clear()

    def insert(self, entity_id: int, x: float, y: float) -> None:
        cell = self._hash_coords(x, y)
        if cell not in self.grid:
            self.grid[cell] = set()
        self.grid[cell].add(entity_id)

    def get_nearby_entities(self, x: float, y: float, radius: float) -> List[int]:
        cx, cy = self._hash_coords(x, y)
        r_cells = math.ceil(radius / self.cell_size)
        
        nearby = []
        for dx in range(-r_cells, r_cells + 1):
            for dy in range(-r_cells, r_cells + 1):
                cell = (cx + dx, cy + dy)
                if cell in self.grid:
                    nearby.extend(self.grid[cell])
        return nearby

class GameCoreLoop:
    """Core engine update tick manager with optimized spatial indexing."""

    def __init__(self, cell_size: int = 64):
        self.spatial_index = FastSpatialGrid(cell_size)
        self.entities: Dict[int, Tuple[float, float]] = {}

    def register_entity(self, entity_id: int, x: float, y: float) -> None:
        self.entities[entity_id] = (x, y)

    def update_frame(self) -> None:
        self.spatial_index.clear()
        for eid, (x, y) in self.entities.items():
            self.spatial_index.insert(eid, x, y)

    def find_targets_in_range(self, x: float, y: float, max_dist: float) -> List[int]:
        candidates = self.spatial_index.get_nearby_entities(x, y, max_dist)
        max_dist_sq = max_dist * max_dist
        
        valid_targets = []
        for eid in candidates:
            ex, ey = self.entities[eid]
            dx, dy = ex - x, ey - y
            if dx * dx + dy * dy <= max_dist_sq:
                valid_targets.append(eid)
        return valid_targets
