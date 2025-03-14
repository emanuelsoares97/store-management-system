from flask import Flask
from routes.api.produtos import produto_bp
from routes.api.login import login_bp

def init_routes(app: Flask):
    """Registra todos os Blueprints da aplicação"""
    blueprints = [produto_bp, login_bp]  # Lista de Blueprints

    for bp in blueprints:
        app.register_blueprint(bp, url_prefix="/api")  # Registra cada um
