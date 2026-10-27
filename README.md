# python-utils-50

A curated collection of high-performance Python utilities designed to streamline game development tasks and server-side automation. This library focuses on low-latency calculations and rapid data integration for game engines and discord-based game servers.

## Features

*   **VectorMath Engine:** Optimized 2D/3D coordinate transformations and distance calculations for collision detection.
*   **Player Profile Serializer:** A robust JSON/Binary schema validator for saving and loading player game states efficiently.
*   **Packet Buffer Manager:** Handles asynchronous byte stream parsing for custom multiplayer networking protocols.
*   **Cooldown Manager:** A decorator-based utility to manage player ability refresh rates and prevent action spam.

## Installation

Install the package via pip:

```bash
pip install python-utils-50
```

For developers requiring bleeding-edge features, clone the repository:

```bash
git clone https://github.com/Developer/python-utils-50.git
cd python-utils-50
pip install -r requirements.txt
```

## Basic Usage

Quickly implement a cooldown on a game action using the built-in decorator:

```python
from utils_50 import cooldown

@cooldown(seconds=5.0)
def use_health_potion():
    print("Health potion consumed!")

# This will execute on the first call, 
# and ignore subsequent calls for 5 seconds.
use_health_potion()
use_health_potion() 
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.