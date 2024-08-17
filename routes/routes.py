from flask import Blueprint, render_template, jsonify
from services.pdf_service import PDFGenerator
from config import Config
import logging

logger = logging.getLogger(__name__)

routes = Blueprint('routes', __name__)

pdf_generator = PDFGenerator()

@routes.route('/')
def recipe():
    logger.info("Rendering recipe page.")
    return render_template('recipe.html')

@routes.route('/download_pdf')
def download_pdf():
    if not Config.ENABLE_PDF_DOWNLOAD:
        logger.warning("Attempted to access PDF download, but the feature is disabled.")
        return jsonify({"error": "PDF download is disabled"}), 403

    logger.info("Download PDF route accessed.")
    return pdf_generator.generate_pdf('recipe.html', 'Mottley_Drink_Recipe.pdf')

@routes.route('/bookmark')
def bookmark():
    if not Config.ENABLE_BOOKMARK:
        logger.warning("Attempted to access bookmark feature, but it is disabled.")
        return jsonify({"error": "Bookmark feature is disabled"}), 403

    logger.info("Bookmark feature accessed.")
    # Implement the bookmark feature here
    return jsonify({"message": "Bookmark feature would be implemented here."})

@routes.route('/share')
def share():
    if not Config.ENABLE_SHARE:
        logger.warning("Attempted to access share feature, but it is disabled.")
        return jsonify({"error": "Share feature is disabled"}), 403

    logger.info("Share feature accessed.")
    # Implement the share feature here
    return jsonify({"message": "Share feature would be implemented here."})

# Error Handlers
@routes.app_errorhandler(404)
def not_found_error(error):
    logger.error(f"404 error occurred: {error}")
    return render_template('error.html', error_code=404, error_message="Page Not Found"), 404

@routes.app_errorhandler(500)
def internal_error(error):
    logger.error(f"500 error occurred: {error}")
    return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500
