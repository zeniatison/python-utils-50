from typing import Dict, Any, Callable, Union, Optional

class GameActionHandler:
    """
    Orchestrates player-input routing via a registry of callback functions.
    Uses dynamic binding to keep the game loop lean.
    """
    def __init__(self) -> None:
        self._registry: Dict[str, Callable[[Any], None]] = {}

    def register_command(self, command: str, callback: Callable[[Any], None]) -> None:
        """Bind an input string to an executable payload function."""
        self._registry[command] = callback

    def execute(self, command: str, data: Optional[Any] = None) -> Union[bool, str]:
        """
        Attempt to fire a command; returns success status or debug string.
        Uses a gentle fallback mechanism for unregistered inputs.
        """
        if command not in self._registry:
            return f"unknown action: {command}"
        
        try:
            self._registry[command](data)
            return True
        except Exception as e:
            return f"execution fault in {command}: {str(e)}"

    def __getitem__(self, key: str) -> Callable[[Any], None]:
        """Access the internal command map directly via subscription."""
        return self._registry[key]

    def __repr__(self) -> str:
        """Summary of currently active input mappings."""
        return f"<GameActionHandler with {len(self._registry)} mapped commands>"