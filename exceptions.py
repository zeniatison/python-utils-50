from typing import Optional, Any

class GamingEngineError(Exception):
    """Base exception for all game-related runtime anomalies."""
    def __init__(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context: dict[str, Any] = context or {}

class AssetLoadError(GamingEngineError):
    """Raised when a texture or mesh refuses to manifest."""
    def __init__(self, asset_path: str, reason: str) -> None:
        super().__init__(f"Failed to conjure asset at {asset_path}: {reason}")

class StateCorruptionError(GamingEngineError):
    """Raised when the game state enters an forbidden dimension."""
    def __init__(self, state_name: str, expected_type: type) -> None:
        msg = f"State {state_name} corrupted, expected {expected_type.__name__}"
        super().__init__(msg, {"state": state_name, "expected": expected_type})

class InputLatencyWarning(Warning):
    """Non-fatal notification for sluggish input processing."""
    def __init__(self, delay_ms: float) -> None:
        self.message: str = f"Input lag detected: {delay_ms}ms over threshold"
        super().__init__(self.message)