from flask import Blueprint, jsonify
from flask_featureflags import is_active
from models import Favorite, db
import logging

logger = logging.getLogger(__name__)

feature_routes = Blueprint('feature_routes', __name__)

@feature_routes.route('/bookmark/<int:recipe_id>', methods=['POST'])
def bookmark(recipe_id):
    if not is_active('ENABLE_BOOKMARK'):
        logger.warning("Attempted to access bookmark feature, but it is disabled.")
        return jsonify({"error": "Bookmark feature is disabled"}), 403

    logger.info(f"User {current_user.id} bookmarking recipe ID {recipe_id}.")
    try:
        favorite = Favorite(user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(favorite)
        db.session.commit()
        logger.info(f"Recipe ID {recipe_id} bookmarked by user {current_user.id}.")
        return jsonify({"message": "Recipe bookmarked successfully."})
    except Exception as e:
        logger.error(f"Failed to bookmark recipe ID {recipe_id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to bookmark recipe"}), 500

@feature_routes.route('/share/<int:recipe_id>', methods=['POST'])
def share(recipe_id):
    if not is_active('ENABLE_SHARE'):
        logger.warning("Attempted to access share feature, but it is disabled.")
        return jsonify({"error": "Share feature is disabled"}), 403

    logger.info(f"User {current_user.id} sharing recipe ID {recipe_id}.")
    # Implement the sharing logic here, e.g., sending an email, posting to social media, etc.
    return jsonify({"message": "Recipe shared successfully."})
