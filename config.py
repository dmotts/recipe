import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Base configuration class.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    API_KEY = os.getenv('PDFCO_API_KEY', 'your_default_pdfco_api_key')
    CSS_PATH = os.getenv('CSS_PATH', 'static/styles.css')

    # Determine the environment and set the database URL
    if os.getenv('FLASK_ENV') == 'production':
        SQLALCHEMY_DATABASE_URI = os.getenv('SUPABASE_DATABASE_URL')  # Use Supabase PostgreSQL in production
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///recipes.db'  # Use SQLite in development

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    if not SECRET_KEY or SECRET_KEY == 'default_secret_key':
        raise ValueError("SECRET_KEY is not set or is using an insecure default key.")
