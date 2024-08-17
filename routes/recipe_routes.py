from flask import Blueprint, render_template, jsonify, Response
from services.pdf_service import PDFGenerator
from config import Config
import logging

logger = logging.getLogger(__name__)

recipe_routes = Blueprint('recipe_routes', __name__)

pdf_generator = PDFGenerator()

@recipe_routes.route('/')
def recipe():
    logger.info("Rendering recipe page.")
    try:
        return render_template('recipe.html', title='Mottley Drink')
    except Exception as e:
        logger.error(f"Failed to render template: {e}")
        return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500

@recipe_routes.route('/download_pdf')
def download_pdf():
    if not Config.ENABLE_PDF_DOWNLOAD:
        logger.warning("Attempted to access PDF download, but the feature is disabled.")
        return jsonify({"error": "PDF download is disabled"}), 403

    logger.info("Download PDF route accessed.")
    try:
        # Generate PDF content without saving to server
        html_content = pdf_generator.get_html('recipe.html')
        html_with_css = pdf_generator.inject_css(html_content)
        pdf_content = pdf_generator.convert_html_to_pdf(html_with_css)

        # Stream the PDF content as a download to the client
        return Response(
            pdf_content,
            mimetype='application/pdf',
            headers={
                "Content-Disposition": "attachment;filename=Mottley_Drink_Recipe.pdf"
            }
        )
    except Exception as e:
        logger.error(f"Failed to generate PDF: {str(e)}")
        return jsonify({"error": "Failed to generate PDF"}), 500
