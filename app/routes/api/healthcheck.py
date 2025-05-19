from flask import Blueprint, jsonify

#criado para usar como health check no uptimer de modo que a api nao va a baixo

health_bp = Blueprint("health", __name__)

@health_bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200
