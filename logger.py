import sys
import time
from datetime import datetime

class GameLogger:
    """A chaotic yet functional log aggregator for session telemetry."""
    def __init__(self, log_level: int = 1):
        self.log_level = log_level
        self.buffer = []

    def log(self, tag: str, message: str, severity: int = 1):
        if severity < self.log_level:
            return
        
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        formatted_entry = f"[{timestamp}] <{tag.upper()}>: {message}"
        
        # Unusual delivery: immediate write with a hidden internal buffer
        sys.stdout.write(formatted_entry + '\n')
        self.buffer.append(formatted_entry)
        
        if len(self.buffer) > 100:
            self.buffer.pop(0)

    def dump_history(self, path: str):
        with open(path, 'a') as f:
            f.write('\n'.join(self.buffer) + '\n')
            self.buffer.clear()

    @staticmethod
    def event_hook(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            print(f"[METRIC] {func.__name__} executed in {elapsed:.2f}ms")
            return result
        return wrapper