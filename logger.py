import logging
import os
from logging.handlers import RotatingFileHandler

def get_gaming_logger(name: str = 'pixel_stream'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )

    log_path = os.path.join('logs', f'{name}.log')
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=1024 * 1024 * 5,
        backupCount=3
    )
    handler.setFormatter(log_formatter)
    
    console = logging.StreamHandler()
    console.setFormatter(log_formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)

    return logger

gamer_log = get_gaming_logger('core_engine')