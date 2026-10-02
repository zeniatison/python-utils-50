import functools

def validate_game_input(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = args[0] if args else kwargs.get('data')
        if not isinstance(data, dict):
            raise ValueError('input must be a dictionary')
        if 'action' not in data or 'uid' not in data:
            raise KeyError('missing required protocol keys')
        return func(*args, **kwargs)
    return wrapper

class InputProcessor:
    def __init__(self):
        self.state = 'active'

    @validate_game_input
    def process_tick(self, data):
        """Executes logic flow for game events."""
        action = data['action']
        uid = data['uid']
        return f'processed {action} for entity {uid}'

def run_loop(input_queue):
    processor = InputProcessor()
    for item in input_queue:
        try:
            result = processor.process_tick(item)
            print(f'Log: {result}')
        except (ValueError, KeyError) as e:
            print(f'Drop: invalid packet - {e}')

if __name__ == '__main__':
    mock_data = [{'action': 'move', 'uid': 1}, {'malformed': 'data'}]
    run_loop(mock_data)