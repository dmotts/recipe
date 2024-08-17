from flask import Blueprint, jsonify
from flask_featureflags import is_active
import logging

logger = logging.getLogger(__name__)

feature_routes = Blueprint('feature_routes', __name__)

@feature_routes.route('/bookmark')
def bookmark():
    if not is_active('ENABLE_BOOKMARK'):
        logger.warning("Attempted to access bookmark feature, but it is disabled.")
        return jsonify({"error": "Bookmark feature is disabled"}), 403

    logger.info("Bookmark feature accessed.")
    # Implement the bookmark feature here
    return jsonify({"message": "Bookmark feature would be implemented here."})

@feature_routes.route('/share')
def share():
    if not is_active('ENABLE_SHARE'):
        logger.warning("Attempted to access share feature, but it is disabled.")
        return jsonify({"error": "Share feature is disabled"}), 403

    logger.info("Share feature accessed.")
    # Implement the share feature here
    return jsonify({"message": "Share feature would be implemented here."})
