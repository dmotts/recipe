from flask import Blueprint, render_template, jsonify, Response, request
from models import db, Recipe, Comment, Rating, Favorite
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
        recipes = Recipe.query.all()
        return render_template('recipe.html', title='Mottley Drink', recipes=recipes)
    except Exception as e:
        logger.error(f"Failed to render template: {e}")
        return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500

@recipe_routes.route('/download_pdf/<int:recipe_id>')
def download_pdf(recipe_id):
    if not Config.ENABLE_PDF_DOWNLOAD:
        logger.warning("Attempted to access PDF download, but the feature is disabled.")
        return jsonify({"error": "PDF download is disabled"}), 403

    logger.info("Download PDF route accessed.")
    try:
        recipe = Recipe.query.get_or_404(recipe_id)
        html_content = pdf_generator.get_html('recipe_detail.html', recipe=recipe)
        html_with_css = pdf_generator.inject_css(html_content)
        pdf_content = pdf_generator.convert_html_to_pdf(html_with_css)

        return Response(
            pdf_content,
            mimetype='application/pdf',
            headers={
                "Content-Disposition": f"attachment;filename={recipe.title}.pdf"
            }
        )
    except Exception as e:
        logger.error(f"Failed to generate PDF: {str(e)}")
        return jsonify({"error": "Failed to generate PDF"}), 500

@recipe_routes.route('/rate_recipe/<int:recipe_id>', methods=['POST'])
def rate_recipe(recipe_id):
    rating_value = request.form.get('rating')
    rating = Rating(rating=rating_value, user_id=current_user.id, recipe_id=recipe_id)
    db.session.add(rating)
    db.session.commit()
    return jsonify({"message": "Recipe rated successfully."})

@recipe_routes.route('/comment/<int:recipe_id>', methods=['POST'])
def comment(recipe_id):
    content = request.form.get('content')
    comment = Comment(content=content, user_id=current_user.id, recipe_id=recipe_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully."})

@recipe_routes.route('/favorite/<int:recipe_id>', methods=['POST'])
def favorite(recipe_id):
    favorite = Favorite(user_id=current_user.id, recipe_id=recipe_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Recipe favorited successfully."})
