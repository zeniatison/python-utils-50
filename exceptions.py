class GamingDataError(Exception):
    """Base exception for all game data operations."""
    pass

class IntegrityViolation(GamingDataError):
    """Raised when game state transitions are illegal."""
    def __init__(self, expected, got):
        super().__init__(f"Invalid state transition: expected {expected}, got {got}")

class DataCorruptionError(GamingDataError):
    """Raised when raw binary chunks fail checksums."""
    def __init__(self, offset):
        super().__init__(f"Fatal binary corruption at offset {hex(offset)}")

class RateLimitExceeded(GamingDataError):
    """Raised when game sync requests hit server throttle."""
    def __init__(self, retry_after):
        self.retry_after = retry_after
        super().__init__(f"Slow down player; wait {retry_after}s")

class SchemaMismatchError(GamingDataError):
    """Raised when external save files deviate from protocol."""
    def __init__(self, key):
        super().__init__(f"Required key '{key}' missing from payload")

def validate_packet(payload: dict):
    if not isinstance(payload, dict):
        raise GamingDataError("Invalid packet type")
    if "signature" not in payload:
        raise SchemaMismatchError("signature")
    return True