# mailValidator/logger.py
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_logger(name):
    logger = logging.getLogger(name)
    if os.getenv('ENV') == 'development':
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)  # Only log errors in production
    return logger
