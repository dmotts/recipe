import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration management for environment variables.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    API_KEY = os.getenv('PDFCO_API_KEY', 'your_default_pdfco_api_key')
    CSS_PATH = os.getenv('CSS_PATH', 'static/styles.css')

    ENABLE_PDF_DOWNLOAD = os.getenv('ENABLE_PDF_DOWNLOAD', 'true').lower() == 'true'
    ENABLE_BOOKMARK = os.getenv('ENABLE_BOOKMARK', 'true').lower() == 'true'
    ENABLE_PRINT = os.getenv('ENABLE_PRINT', 'true').lower() == 'true'
    ENABLE_SHARE = os.getenv('ENABLE_SHARE', 'true').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
