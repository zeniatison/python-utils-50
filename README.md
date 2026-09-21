# python-utils-50

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`python-utils-50` is a lightweight Python toolkit designed to streamline common game development math and state management tasks for Pygame and Pyglet projects. It provides developers with highly optimized utilities for 2D vector physics, grid-based pathfinding, and fast sprite sheet slicing to accelerate prototype creation.

## Features

* **Fast Vector2D Operations:** Optimized math functions for distances, angles, and collision detection without the overhead of heavy external frameworks.
* **A\* Pathfinding Grid:** A lightweight, drop-in grid pathfinder tailored for 2D tile-based games and RPGs.
* **Sprite Sheet Slicer:** Automated utility to split sprite sheets into individual frame buffers based on custom pixel grids or frame counts.
* **Dynamic State Manager:** A clean, event-driven state machine to manage transitions between main menus, game loops, and pause screens.

## Installation

Install the package directly from PyPI using pip:

```bash
pip install python-utils-50
```

## Quick Start

```python
from python_utils_50.vector import Vector2D
from python_utils_50.sprites import slice_sheet

# 1. Quick 2D vector math
player_pos = Vector2D(120, 250)
enemy_pos = Vector2D(450, 610)
distance = player_pos.distance_to(enemy_pos)
print(f"Enemy is {distance:.2f} pixels away.")

# 2. Slice a 128x32 sprite sheet into four 32x32 frames
frames = slice_sheet("assets/hero_walk.png", frame_width=32, frame_height=32)
print(f"Successfully loaded {len(frames)} animation frames.")
```

## License

Distributed under the MIT License. See `LICENSE` for more information.