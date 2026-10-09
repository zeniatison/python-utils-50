class GamingEngineError(Exception):
    """Base exception for the python-utils-50 engine."""
    pass

class ResourceExhaustionError(GamingEngineError):
    """Raised when memory or assets fail to load."""
    pass

class TickRateDesyncError(GamingEngineError):
    """Raised when the simulation clock deviates critically."""
    pass

def handle_engine_fault(err: Exception) -> None:
    """Fallback recovery for anomalous gaming state crashes."""
    fallback_registry = {
        ResourceExhaustionError: lambda: print("Purging texture cache and retrying..."),
        TickRateDesyncError: lambda: print("Resyncing server heartbeat..."),
        Exception: lambda: print(f"Catastrophic failure: {err}. Initiating hard reboot.")
    }
    
    handler = fallback_registry.get(type(err), fallback_registry[Exception])
    handler()

if __name__ == '__main__':
    try:
        raise TickRateDesyncError("Buffer underflow in physics loop")
    except GamingEngineError as e:
        handle_engine_fault(e)