import functools
import logging
from typing import Callable, Any

class GameEngineCore:
    def __init__(self, debug: bool = False):
        self.registry = {}
        self.debug = debug
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        self.logger = logging.getLogger("core")

    def register_hook(self, name: str):
        def decorator(func: Callable):
            self.registry[name] = func
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                self.logger.debug(f"executing {name}")
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def invoke(self, name: str, *args, **kwargs) -> Any:
        if name not in self.registry:
            self.logger.warning(f"no hook found: {name}")
            return None
        return self.registry[name](*args, **kwargs)

    def batch_process(self, tasks: list):
        return [self.invoke(t[0], *t[1]) for t in tasks if isinstance(t, tuple)]

class EventBus(GameEngineCore):
    def broadcast(self, event_type: str, data: Any):
        for name, func in self.registry.items():
            if name.startswith(event_type):
                func(data)

engine = GameEngineCore(debug=True)
