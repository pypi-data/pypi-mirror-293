import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_logging(log_file="email_validator.log"):
    """Set up logging configuration for development environment."""
    if os.getenv('ENV') == 'development':
        logging.basicConfig(
            level=logging.INFO,  # DEBUG level for development
            format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
