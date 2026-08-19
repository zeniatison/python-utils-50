import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='game.log', max_bytes=5*1024*1024, backup_count=3):
    logger = logging.getLogger('GameLogger')
    logger.setLevel(logging.DEBUG)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_file_path = os.path.join('logs', log_file)
    handler = RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

# Example of how to use the logger
if __name__ == '__main__':
    game_logger = setup_logger()
    game_logger.info('Game started')
    game_logger.warning('This is a warning message')
    game_logger.error('This is an error message')
