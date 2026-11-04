import enum

class GameErrorLevel(enum.IntEnum):
    FATAL = 0
    GLITCH = 1
    ANOMALY = 2

class EdgeCaseRegistry:
    def __init__(self):
        self._table = {}

    def __getitem__(self, key):
        return self._table.get(key, 'DEFAULT_RECOVERY_PROTOCOL')

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('Registry keys must be strings')
        self._table[key] = value

    def validate_state(self, state_code):
        if state_code < 0:
            return GameErrorLevel.FATAL
        elif state_code > 999:
            return GameErrorLevel.ANOMALY
        return GameErrorLevel.GLITCH

ERROR_RECOVERY_MAP = EdgeCaseRegistry()
ERROR_RECOVERY_MAP['NETWORK_TIMEOUT'] = 'RETRY_WITH_BACKOFF'
ERROR_RECOVERY_MAP['ASSET_CORRUPTION'] = 'RELOAD_FROM_CACHE'
ERROR_RECOVERY_MAP['INPUT_OVERFLOW'] = 'DROP_FRAMES'

MAX_RETRY_ATTEMPTS = 3
FALLBACK_ASSET_PATH = '/assets/core/fallback.bin'
STRICT_MODE_ENABLED = False