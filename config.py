import json
import os

class ConfigLoader:
    def __init__(self, default_config, user_config_path='config.json'):
        self.default_config = default_config
        self.user_config_path = user_config_path
        self.config = self.load_config()

    def load_config(self):
        config = self.default_config.copy()  # Start with defaults
        if os.path.exists(self.user_config_path):
            with open(self.user_config_path, 'r') as file:
                user_config = json.load(file)
                config.update(user_config)  # Override defaults with user settings
        return config

    def get(self, key, default=None):
        return self.config.get(key, default)

# Example usage
if __name__ == '__main__':
    default_settings = {
        'fullscreen': False,
        'volume': 75,
        'resolution': {'width': 1920, 'height': 1080}
    }
    config_loader = ConfigLoader(default_settings)
    print(config_loader.get('fullscreen'))
    print(config_loader.get('volume'))
    print(config_loader.get('resolution'))