import logging
import os

LOG_FILE_PATH = "/app/logs/app.log"
# Ensure 'logs' directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# Define log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Create logger instance
logger = logging.getLogger("Backend-App")
logger.setLevel(logging.INFO)  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Remove existing handlers to prevent duplicate logs
if logger.hasHandlers():
    logger.handlers.clear()

# Create file handler (write logs to 'logs/app.log')
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Create console handler (print logs to the console)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Prevent Uvicorn from intercepting logs
logging.getLogger("uvicorn").propagate = False

# Log startup message
logger.info("Logging system initialized successfully!")
