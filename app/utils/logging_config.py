import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File handler for all logs
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    # Error file handler
    error_handler = RotatingFileHandler(
        'logs/error.log',
        maxBytes=1024*1024,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)

    return root_logger
