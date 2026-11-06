import math
from typing import List, Tuple, Dict, Set

class OptimizedSpatialGrid:
    """Fast spatial hash grid using bitwise cell encoding for gaming entity collision lookup."""
    __slots__ = ('cell_size', 'shift', 'grid')

    def __init__(self, cell_size: int = 64):
        self.cell_size = cell_size
        self.shift = (cell_size & (cell_size - 1) == 0) and cell_size.bit_length() - 1
        self.grid: Dict[int, Set[int]] = {}

    def _hash_coords(self, x: float, y: float) -> int:
        if self.shift:
            cx = int(x) >> self.shift
            cy = int(y) >> self.shift
        else:
            cx = int(x // self.cell_size)
            cy = int(y // self.cell_size)
        return ((cx & 0xFFFFFFFF) << 32) | (cy & 0xFFFFFFFF)

    def insert_entity(self, entity_id: int, x: float, y: float, radius: float = 0.0) -> None:
        if radius <= 0:
            key = self._hash_coords(x, y)
            self.grid.setdefault(key, set()).add(entity_id)
            return

        min_cx = int((x - radius) // self.cell_size)
        max_cx = int((x + radius) // self.cell_size)
        min_cy = int((y - radius) // self.cell_size)
        max_cy = int((y + radius) // self.cell_size)

        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                key = ((cx & 0xFFFFFFFF) << 32) | (cy & 0xFFFFFFFF)
                self.grid.setdefault(key, set()).add(entity_id)

    def get_nearby(self, x: float, y: float, radius: float = 0.0) -> Set[int]:
        if radius <= 0:
            key = self._hash_coords(x, y)
            return set(self.grid.get(key, ()))

        min_cx = int((x - radius) // self.cell_size)
        max_cx = int((x + radius) // self.cell_size)
        min_cy = int((y - radius) // self.cell_size)
        max_cy = int((y + radius) // self.cell_size)

        results: Set[int] = set()
        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                key = ((cx & 0xFFFFFFFF) << 32) | (cy & 0xFFFFFFFF)
                if key in self.grid:
                    results.update(self.grid[key])
        return results

    def clear(self) -> None:
        self.grid.clear()
