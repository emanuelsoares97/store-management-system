from flask import jsonify, Blueprint
from app.models.User import User

debug_bp = Blueprint("debug", __name__)


@debug_bp.route('/users_count')
def users_count():
    try:
        count = User.query.count()
        return jsonify({"user_count": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500