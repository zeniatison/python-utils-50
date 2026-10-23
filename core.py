import sys

def validate_game_state(data):
    if not isinstance(data, dict) or 'id' not in data:
        raise ValueError('corrupt packet: missing identifier')
    if not (0 <= data.get('latency', 0) < 500):
        raise ValueError('latency jitter threshold exceeded')
    return True

def main_loop():
    stream = [{'id': 101, 'latency': 45}, {'id': 'ERR', 'latency': 999}, {'id': 102, 'latency': 12}]
    for packet in stream:
        try:
            if validate_game_state(packet):
                process_frame(packet)
        except ValueError as e:
            print(f'skipping malicious tick: {e}')
            continue

def process_frame(pkt):
    print(f'processing valid frame {pkt["id"]}')

if __name__ == '__main__':
    main_loop()