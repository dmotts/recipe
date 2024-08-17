from flask import Flask
from flask_featureflags import FeatureFlag
from models import db
from routes.recipe_routes import recipe_routes
from routes.feature_routes import feature_routes
from routes.error_handlers import error_handlers
from services.logging_service import setup_logging
import os

# Initialize logging
setup_logging()

# Initialize Flask app
app = Flask(__name__)
feature_flags = FeatureFlag(app)

# Load configuration based on the environment
config_type = os.getenv('FLASK_ENV', 'development').capitalize() + 'Config'
app.config.from_object(f'config.{config_type}')

# Initialize the database
db.init_app(app)

# Register routes and error handlers
app.register_blueprint(recipe_routes)
app.register_blueprint(feature_routes)
app.register_blueprint(error_handlers)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
