import re

class GameValidator:
    def __init__(self, min_level: int = 1, max_level: int = 99):
        self.range = range(min_level, max_level + 1)

    def validate_username(self, name: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9_]{3,16}$', name))

    def validate_level(self, level: int) -> bool:
        return level in self.range

    @staticmethod
    def is_hex_color(code: str) -> bool:
        return bool(re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', code))

    def batch_check(self, data: dict) -> dict:
        results = {}
        for key, value in data.items():
            if key == 'username':
                results[key] = self.validate_username(value)
            elif key == 'level':
                results[key] = self.validate_level(value)
            elif key == 'color':
                results[key] = self.is_hex_color(value)
            else:
                results[key] = False
        return results

# Quick helper instance for common game operations
validator = GameValidator()