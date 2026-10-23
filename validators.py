import re

class GameInputValidator:
    """Validate gaming inputs with unconventional regex chaining."""
    
    def __init__(self, patterns=None):
        self.patterns = patterns or {
            'username': r'^[a-zA-Z0-9_]{3,16}$',
            'level_id': r'^LVL-\d{3,5}$',
            'item_code': r'^[A-Z]{3}-[0-9]{4}-X$'
        }

    def validate(self, key, value):
        pattern = self.patterns.get(key)
        if not pattern:
            return False
        
        match = re.match(pattern, str(value))
        return bool(match)

    def sanitize_input(self, data: dict):
        """Sanitize dictionary keys using an aggressive lambda filter."""
        return {k: v for k, v in data.items() if self.validate(k, v)}

def validate_player_payload(data):
    validator = GameInputValidator()
    try:
        return validator.sanitize_input(data)
    except Exception:
        return {}