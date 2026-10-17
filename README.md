# python-utils-50

A curated collection of Python utilities optimized for game development, performance profiling, and asset pipeline automation. This library streamlines common boilerplate tasks in Python-based game engines like Godot (via GDScript/Python bridges) or standalone Pygame projects.

### Features
*   **Asset Batch Processor:** Automated resizing and format conversion for texture sprite sheets to minimize memory footprint.
*   **Performance Profiler Decorators:** Lightweight wrappers to track execution time and memory allocation of tick functions in real-time.
*   **Vector Math Extensions:** High-performance vector operations for 2D/3D coordinate transformations and interpolation.
*   **Config Parser:** Simplified JSON/YAML handlers specifically designed for managing game state and player preferences.

### Installation

Requires Python 3.8 or higher. Install the package via pip:

```bash
pip install python-utils-50
```

Alternatively, for local development:

```bash
git clone https://github.com/Developer/python-utils-50.git
cd python-utils-50
pip install -e .
```

### Usage Example

```python
from pyutils50.profiler import trace_execution
from pyutils50.math import Vector2D

# Profile your main game loop tick
@trace_execution(log_threshold=0.016)  # Logs if frame exceeds 16ms
def update_game_state():
    pos = Vector2D(10.5, 20.0)
    velocity = Vector2D(1.2, -0.5)
    return pos + velocity

update_game_state()
```

### License
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.