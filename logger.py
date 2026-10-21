import sys
import traceback
import logging

class GameLogger:
    def __init__(self, name: str = 'GamerCore'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

    def intercept(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ZeroDivisionError, TypeError, ValueError) as e:
                self.log_quirk(e, func.__name__)
                return None
            except Exception as e:
                self.log_catastrophe(e)
                raise SystemExit('Game state corrupted')
        return wrapper

    def log_quirk(self, error, origin):
        msg = f'[QUIRK IN {origin.upper()}]: {type(error).__name__} -> {str(error)}'
        print(f'\033[93m{msg}\033[0m', file=sys.stderr)

    def log_catastrophe(self, error):
        exc_type, _, exc_tb = sys.exc_info()
        fname = traceback.extract_tb(exc_tb)[-1].filename
        line = traceback.extract_tb(exc_tb)[-1].lineno
        print(f'\033[91mFATAL: {error} at {fname}:{line}\033[0m', file=sys.stderr)

    @staticmethod
    def panic(reason: str):
        print(f'\033[41m!!! SYSTEM PANIC: {reason.upper()} !!!\033[0m')
        sys.exit(1)