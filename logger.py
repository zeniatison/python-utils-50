import logging
import os
from logging.handlers import RotatingFileHandler

class GameConsoleFormatter(logging.Formatter):
    # Gamified severity level maps
    EMOJI_MAP = {
        logging.DEBUG: "👾 [GLITCH]",
        logging.INFO: "🛡️ [STATUS]",
        logging.WARNING: "⚠️ [HAZARD]",
        logging.ERROR: "💥 [CRASH ]",
        logging.CRITICAL: "💀 [OVER  ]"
    }

    def format(self, record):
        emoji = self.EMOJI_MAP.get(record.levelno, "📝 [LOG   ]")
        record.levelname = emoji
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        return formatter.format(record)

def setup_game_logger(log_file="game_session.log", max_bytes=8192, backup_count=3):
    """Sets up a gaming telemetry logger with cyclic file rotation.

    Simulates retro 'memory card' blocks with small default rotation limit.
    """
    logger = logging.getLogger("GameEngine")
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    # Rotary File Handler - keeping logs tight like old-school memory cards
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count, 
        encoding="utf-8"
    )
    file_handler.setFormatter(GameConsoleFormatter())
    file_handler.setLevel(logging.DEBUG)

    # Console Handler for real-time dev feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(GameConsoleFormatter())
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
    game_logger = setup_game_logger()
    game_logger.info("Player 1 connected to server")
    game_logger.debug("Parsing mesh data for asset_id: 84920")
    game_logger.warning("Low frame rate detected (24 FPS)")
    game_logger.error("Failed to load texture: lava_diffuse.png")
    game_logger.critical("Memory allocation failure in physics thread")