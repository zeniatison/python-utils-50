# python-utils-50

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Developed by Developer, `python-utils-50` is a lightweight, high-performance toolkit designed to accelerate game development workflows in Python. It provides critical, production-ready utilities for handling 2D grid pathfinding, game loop ticking, and real-time state serialization.

## Features

* **Deterministic Game Tick:** A microsecond-accurate game loop manager that prevents physics drift across variable frame rates.
* **Optimized A\* Pathfinding:** High-performance 2D grid routing designed specifically for real-time NPC pathfinding and collision avoidance.
* **Binary State Packer:** Fast, zero-overhead serialization utility designed for rapid multiplayer state synchronization over UDP.

## Installation

Install the package directly from PyPI using pip:

```bash
pip install python-utils-50
```

## Quick Start

Here is a quick example demonstrating how to set up a fixed-timestep game loop and find a path on a grid:

```python
from python_utils_50.loop import GameLoop
from python_utils_50.grid import Grid2D

# 1. Initialize a 10x10 game grid and block a coordinate
grid = Grid2D(width=10, height=10)
grid.add_obstacle(x=3, y=3)

# 2. Find a path from top-left to bottom-right
path = grid.find_path(start=(0, 0), target=(9, 9))
print(f"Optimal NPC Path: {path}")

# 3. Run a locked 60 FPS game loop
loop = GameLoop(target_fps=60)
while loop.running:
    dt = loop.tick()
    # Your game update and rendering logic goes here
    # (Example exits immediately for demonstration)
    break
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.