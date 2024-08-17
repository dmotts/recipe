from flask import Blueprint, render_template
import logging

logger = logging.getLogger(__name__)

error_handlers = Blueprint('error_handlers', __name__)

@error_handlers.app_errorhandler(404)
def not_found_error(error):
    logger.error(f"404 error occurred: {error}")
    return render_template('error.html', error_code=404, error_message="Page Not Found"), 404

@error_handlers.app_errorhandler(500)
def internal_error(error):
    logger.error(f"500 error occurred: {error}")
    return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500

