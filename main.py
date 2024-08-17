from flask import Flask
from routes.routes import routes
from services.logging_service import setup_logging
from config import DevelopmentConfig, ProductionConfig
import os

# Initialize logging
setup_logging()

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on the environment
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Register routes and error handlers
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
