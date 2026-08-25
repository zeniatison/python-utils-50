import math
import random
from collections import defaultdict

class Entity:
    def __init__(self, x=0, y=0, vx=0, vy=0, health=100):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.health = health

class CoreOptimizer:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.spatial_grid = defaultdict(list)
        self.distance_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
    def _get_grid_key(self, x, y):
        return (int(x // self.grid_size), int(y // self.grid_size))
    def add_entity(self, entity):
        key = self._get_grid_key(entity.x, entity.y)
        self.spatial_grid[key].append(entity)
    def get_nearby_entities(self, x, y, radius):
        key = self._get_grid_key(x, y)
        nearby = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cell_key = (key[0] + dx, key[1] + dy)
                if cell_key in self.spatial_grid:
                    for ent in self.spatial_grid[cell_key]:
                        dist = self._cached_distance(x, y, ent.x, ent.y)
                        if dist <= radius:
                            nearby.append(ent)
        return nearby
    def _cached_distance(self, x1, y1, x2, y2):
        key = (int(x1), int(y1), int(x2), int(y2))
        if key in self.distance_cache:
            self.cache_hits += 1
            return self.distance_cache[key]
        self.cache_misses += 1
        dx = x2 - x1
        dy = y2 - y1
        dist = math.sqrt(dx ** 2 + dy ** 2)
        self.distance_cache[key] = dist
        if len(self.distance_cache) > 500:
            to_remove = random.choice(list(self.distance_cache.keys()))
            del self.distance_cache[to_remove]
        return dist
    def update_positions(self, entities, delta):
        for ent in entities:
            old_key = self._get_grid_key(ent.x, ent.y)
            ent.x += ent.vx * delta
            ent.y += ent.vy * delta
            new_key = self._get_grid_key(ent.x, ent.y)
            if old_key != new_key:
                if ent in self.spatial_grid[old_key]:
                    self.spatial_grid[old_key].remove(ent)
                self.spatial_grid[new_key].append(ent)
    def get_performance_stats(self):
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0
        return {"hits": self.cache_hits, "misses": self.cache_misses, "hit_rate_percent": round(hit_rate, 2), "cache_size": len(self.distance_cache), "grid_cells": len(self.spatial_grid)}