import yaml
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path='config.yaml'):
    """Loads configuration from YAML file and environment variables."""
    load_dotenv() # import SENDGRID_API_KEY from .env file
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Error: Configuration file '{config_path}' not found.")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file '{config_path}': {e}")
        return None

    # Set SendGrid API Key from environment
    email_section = config.get('email', {})
    api_key = os.getenv('SENDGRID_API_KEY')
    if not api_key:
        logger.warning("Warning: SENDGRID_API_KEY not found in .env file.")
        email_section['password'] = None
    else:
        email_section['password'] = api_key

    return config
