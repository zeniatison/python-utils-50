import logging

class GameInputValidator:
    """Dynamic validation schema for game state transitions."""
    def __init__(self):
        self.constraints = {
            "health": lambda x: 0 <= x <= 100,
            "coords": lambda x: isinstance(x, tuple) and len(x) == 3,
            "action": lambda x: x in {"jump", "shoot", "crouch", "idle"}
        }

    def validate_payload(self, data: dict) -> bool:
        """Executes a functional check against the current frame buffer."""
        try:
            return all(self.constraints[k](v) for k, v in data.items() if k in self.constraints)
        except (KeyError, TypeError, ValueError):
            return False

    def process_loop(self, queue):
        """Main game loop entry point for validated state ingestion."""
        for packet in queue:
            if self.validate_payload(packet):
                yield packet
            else:
                logging.warning(f"Malformed packet dropped: {packet}")

def main():
    validator = GameInputValidator()
    data_stream = [
        {"health": 50, "action": "jump"},
        {"coords": (10, 20, 30), "action": "teleport"},
        {"health": 150, "action": "idle"}
    ]
    
    for valid_state in validator.process_loop(data_stream):
        print(f"Processing state: {valid_state}")

if __name__ == "__main__":
    main()