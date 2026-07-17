import logging
import os

# Get the absolute path to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Ensure the logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Handler for app.log (INFO and above)
    app_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)

    # Handler for error.log (ERROR only)
    error_handler = logging.FileHandler(os.path.join(LOG_DIR, "error.log"))
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Console handler so you can still see logs in the terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(app_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger

logger = get_logger("food_delivery_app")