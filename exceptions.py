class GamingError(Exception):
    """Base exception for all game utilities."""
    pass

class StateCorruptionError(GamingError):
    """Raised when game state becomes invalid."""
    pass

class ResourceLoadError(GamingError):
    """Raised when assets fail to load."""
    pass

def assert_state(condition: bool, message: str = "Invalid game state"): 
    """Quick state check with custom exception."""
    if not condition:
        raise StateCorruptionError(f"[!] {message}")

class CatchAllGamingErrors:
    """Context manager for suppressing benign game glitches."""
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, GamingError):
            print(f"Caught handled glitch: {exc_val}")
            return True
        return False

def validate_fps(fps: float):
    """Ensures frame rate remains within safe bounds."""
    if fps < 0 or fps > 500:
        raise ValueError(f"Impossible FPS count detected: {fps}")

class EngineShutdown(SystemExit):
    """Signal for clean engine termination."""
    def __init__(self, reason: str):
        super().__init__(f"Engine halting: {reason}")