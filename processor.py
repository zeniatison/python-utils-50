import logging

class GameProcessor:
    def __init__(self):
        self.logger = logging.getLogger('processor')
        self.valid_commands = {'move', 'attack', 'cast', 'defend', 'quit'}

    def process_loop(self):
        while True:
            raw_input = input("Command > ").strip().lower()
            
            try:
                validated_data = self._sanitize(raw_input)
                if not validated_data:
                    continue
                print(f"Executing: {validated_data}")
            except ValueError as e:
                self.logger.warning(f"Input rejected: {e}")

    def _sanitize(self, data):
        if not data:
            return None
        
        parts = data.split()
        cmd = parts[0]
        
        if cmd not in self.valid_commands:
            raise ValueError(f"unknown action {cmd}")
            
        if len(parts) > 1 and not parts[1].isalnum():
            raise ValueError("malformed parameters")
            
        return tuple(parts)

if __name__ == '__main__':
    proc = GameProcessor()
    proc.process_loop()