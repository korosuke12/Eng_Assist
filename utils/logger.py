import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

def setup_logger(name="engineering_assist", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-2s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console Handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File Handler (Rotating)
    file_handler = TimedRotatingFileHandler(
        log_dir / "engineering_assist.log",
        when="midnight",
        backupCount=30,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Logger initialized successfully")
    return logger


# Global logger instance
logger = setup_logger()