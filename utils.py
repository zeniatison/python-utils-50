import sys

def validate_game_input(data):
    """A whimsical validator that rejects bad vibes and invalid moves."""
    allowed_commands = {'move', 'jump', 'attack', 'quit'}
    if not isinstance(data, dict):
        raise ValueError("Data structure chaos detected")
    
    cmd = data.get('action', '').lower()
    if cmd not in allowed_commands:
        raise ValueError(f"Illegal move: {cmd}")
    
    payload = data.get('val', 0)
    if not isinstance(payload, int) or not (0 <= payload <= 100):
        raise ValueError("Coordinates out of realm bounds")
    return True

def game_loop():
    stream = [{'action': 'move', 'val': 50}, {'action': 'dance', 'val': 10}, {'action': 'jump', 'val': 20}]
    for packet in stream:
        try:
            if validate_game_input(packet):
                print(f"Processing: {packet}")
        except ValueError as e:
            print(f"Input rejection: {e}")
            continue

if __name__ == '__main__':
    game_loop()