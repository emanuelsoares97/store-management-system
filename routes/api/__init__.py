from flask import Flask
from routes.api import produtos, login, utilizador  # Importa os módulos das rotas

def init_routes(app: Flask):
    """Registra todos os Blueprints da aplicação"""
    blueprints = [
        (produtos.produto_bp, "/api/produto"),
        (login.login_bp, "/api/login"),
        (utilizador.utilizador_bp, "/api/utilizador")
    ]  # Lista de Blueprints com seus prefixos individuais

    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)  # Registra cada um dinamicamente
