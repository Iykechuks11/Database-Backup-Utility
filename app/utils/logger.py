import logging
import os

def setup_logger():
    """Configures logging to both file and console."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "backup_activity.log")

    logger = logging.getLogger("DBBackupTool")
    logger.setLevel(logging.INFO)

    # Create format for logs: [2026-03-09 14:30:05] INFO: Message
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')

    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Initialize a global logger instance
logger = setup_logger()