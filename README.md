# python-utils-50

`python-utils-50` is a high-performance Python toolkit designed to streamline common tasks in game development and real-time server management. It provides lightweight wrappers and utilities to handle data serialization, packet parsing, and cross-platform resource pathing for complex gaming projects.

### Features
*   **Packet Buffer Utility:** Optimized byte-stream parsing for custom game protocols using memory-efficient buffer views.
*   **Asset Path Resolver:** A robust path manager that abstracts file system differences between Windows/Linux deployment environments.
*   **Latency Simulator:** Built-in network jitter and packet loss injector for testing client-side prediction in local dev environments.
*   **Thread-Safe State Manager:** Atomic storage utilities for managing global player states and game configurations without race conditions.

### Installation

Ensure you have Python 3.8+ installed. You can install the package directly via pip:

```bash
pip install python-utils-50
```

For manual local installation:

```bash
git clone https://github.com/Developer/python-utils-50.git
cd python-utils-50
pip install -r requirements.txt
python setup.py install
```

### Usage Example

Integrating the asset path resolver into your engine initialization:

```python
from pyutils50.paths import AssetResolver

# Initialize paths relative to your project root
resolver = AssetResolver(base_dir="./assets")

# Resolve cross-platform path to texture or config
config_path = resolver.get_path("configs/settings.json")

print(f"Loading game asset from: {config_path}")
```

### License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.