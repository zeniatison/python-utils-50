import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str, log_file: str = "game_engine.log") -> logging.Logger:
    """
    A logger that treats your disk like a circular buffer.
    Because logs are like lives in a retro game: 
    once you run out, the old ones are gone.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        # 5MB rotation, keeping 3 backups - enough for a session
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [LEVEL_UP]: %(message)s',
            datefmt='%H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add a console stream because debugging needs immediate feedback
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger