import logging
import logging.handlers
import os
from app.core.config import get_settings


def setup_logging():
    """
    Configure logging for the application.
    """
    settings = get_settings()
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

    # Avoid stacking duplicate handlers when app module is imported multiple times.
    if logger.handlers:
        return logger
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File logging can fail on serverless/read-only file systems (e.g., Vercel).
    try:
        log_dir = os.path.dirname(settings.LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            settings.LOG_FILE,
            maxBytes=10485760,  # 10MB
            backupCount=10,
        )
        file_handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        logger.warning("File logging disabled: unable to create/write log file", exc_info=True)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)
