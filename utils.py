import time
import functools
import random
import logging

logger = logging.getLogger('python-utils-50')

def retry_operation(max_attempts=3, delay=1.0, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f'Critical failure in {func.__name__} after {attempts} attempts')
                        raise e
                    
                    jitter = random.uniform(0, 0.1 * current_delay)
                    sleep_time = current_delay + jitter
                    logger.warning(f'Attempt {attempts} failed: {e}. Retrying in {sleep_time:.2f}s...')
                    time.sleep(sleep_time)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

def network_request_wrapper(func):
    return retry_operation(max_attempts=5, delay=0.5)(func)