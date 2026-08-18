# python-utils-50

A comprehensive collection of Python utilities specifically designed for game development. With these tools, developers can streamline common tasks in game mechanics, asset management, and user input processing. 

## Features

- **Game Asset Loader**: Efficiently load and manage game assets, including images, sounds, and fonts, using a single interface.
- **Input Manager**: Simplifies user input handling across keyboard, mouse, and gamepad for enhanced gameplay responsiveness.
- **Math Utilities**: A set of mathematical functions tailored for gaming, such as vector calculations, collision detection, and easing functions.
- **Event System**: An easy-to-use event system for managing game events and notifications, allowing for clean and decoupled gameplay logic.

## Installation

To install `python-utils-50`, simply clone the repository and install the required dependencies:

```bash
git clone https://github.com/Developer/python-utils-50.git
cd python-utils-50
pip install -r requirements.txt
```

You can also install the package directly via pip (if available):

```bash
pip install python-utils-50
```

## Basic Usage Example

Here's a quick example of how to use the Game Asset Loader and Input Manager:

```python
from utils import GameAssetLoader, InputManager

# Load game assets
loader = GameAssetLoader()
loader.load_image('player_sprite', 'assets/player.png')
loader.load_sound('jump_sound', 'assets/jump.wav')

# Initialize input manager
input_manager = InputManager()

# Main game loop
while True:
    input_manager.poll_events()
    
    if input_manager.is_key_pressed('SPACE'):
        print("Jump sound played!")
        loader.play_sound('jump_sound')
```

For more detailed documentation and examples, please refer to the [Wiki](https://github.com/Developer/python-utils-50/wiki).

![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

Contribute to the project, report issues, and suggest features! Your contributions will help improve the tools for everyone in the gaming community.