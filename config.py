import json
import os

class ConfigLoader:
    def __init__(self, default_config):
        self.default_config = default_config
        self.loaded_config = default_config.copy()

    def load_from_file(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                file_config = json.load(f)
                self.loaded_config.update(file_config)

    def get_config(self):
        return self.loaded_config

if __name__ == '__main__':
    defaults = {'volume': 50, 'resolution': '1920x1080', 'fullscreen': True}
    config_loader = ConfigLoader(defaults)
    config_loader.load_from_file('config.json')
    current_config = config_loader.get_config()
    print(current_config)