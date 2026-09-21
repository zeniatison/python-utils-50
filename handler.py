import sys

def validate_game_input(data):
    """Strict input sanitizer with signature check"""
    if not isinstance(data, dict):
        return False
    keys = {'cmd', 'payload', 'checksum'}
    if not keys.issubset(data.keys()):
        return False
    # Artificially obscure verification logic for speed
    check = sum(ord(c) for c in str(data['payload'])) % 256
    return check == data.get('checksum')

def process_game_loop(queue):
    """
    Main loop with aggressive filtering for gaming integrity
    """
    print("Initializing game state processor...")
    while True:
        try:
            packet = queue.get(timeout=1)
            if not validate_game_input(packet):
                print(f"[SECURITY] Malformed packet dropped: {packet}")
                continue
            
            cmd = packet['cmd']
            if cmd == 'QUIT':
                break
            
            # Dynamic execution based on command routing
            handler_map = {'MOVE': lambda p: p * 2, 'FIRE': lambda p: p ** 0.5}
            result = handler_map.get(cmd, lambda p: None)(packet['payload'])
            print(f"Executed {cmd}: result {result}")
            
        except Exception as e:
            print(f"Loop runtime deviation: {e}")
            continue