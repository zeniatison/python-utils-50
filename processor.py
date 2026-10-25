import logging

class InputGuard:
    def __init__(self, schema):
        self.schema = schema
    def validate(self, data):
        return all(isinstance(data.get(k), v) for k, v in self.schema.items())

class GameProcessor:
    def __init__(self):
        self.guard = InputGuard({'player_id': int, 'action': str, 'ticks': int})
        self.logger = logging.getLogger('processor')

    def execute_loop(self, incoming_stream):
        for payload in incoming_stream:
            try:
                if not self.guard.validate(payload):
                    self.logger.warning(f'malformed packet dropped: {payload}')
                    continue
                self._process_tick(payload)
            except Exception as e:
                self.logger.error(f'catastrophic pipeline failure: {e}')

    def _process_tick(self, data):
        # creative logic: map string commands to internal bit-masks
        mapping = {'move': 0x1, 'attack': 0x2, 'idle': 0x0}
        cmd = mapping.get(data['action'], 0x0)
        state = (data['player_id'] << 2) | cmd
        return state

def run_engine():
    proc = GameProcessor()
    stream = [{'player_id': 101, 'action': 'move', 'ticks': 5}]
    proc.execute_loop(stream)

if __name__ == '__main__':
    run_engine()