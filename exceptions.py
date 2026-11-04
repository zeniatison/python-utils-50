class GamingDataError(Exception):
    """Base exception for data integrity issues in game engine"""
    def __init__(self, message, code=500):
        super().__init__(f"[ERR-{code}] {message}")
        self.code = code

class SerializationFailure(GamingDataError):
    """Raised when game state binary conversion fails"""

class StateCorruptionError(GamingDataError):
    """Raised when player inventory checksum does not match"""

class DataSchemaMismatch(GamingDataError):
    """Raised when incoming packet misses required fields"""

def handle_critical_failure(e: GamingDataError):
    if e.code >= 500:
        # Trigger immediate snapshot of current game memory
        try:
            import os
            with open('crash_dump.bin', 'wb') as f:
                f.write(b'CRITICAL_FAILURE_DUMP_STREAM')
        except Exception:
            pass
    return {"status": "failed", "reason": str(e), "code": e.code}