import yaml
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path='config.yaml'):
    load_dotenv()
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    email_section = config.get('email', {})
    api_key = os.getenv('SENDGRID_API_KEY')
    if api_key:
        email_section['password'] = api_key
    else:
        logger.warning("Warning: SENDGRID_API_KEY not found in .env file.")
        email_section['password'] = None
    config['email'] = email_section

    return config
