from flask import Flask
from app.routes.api import auth, produtos, utilizador, clientes, vendas, categorias 

def init_routes(app: Flask):
    """Registra todos os Blueprints da aplicação"""
    blueprints = [
        (produtos.produto_bp, "/api/produto"),
        (auth.auth_bp, "/api/auth"),
        (utilizador.utilizador_bp, "/api/utilizador"),
        (clientes.cliente_bp, "/api/cliente"),
        (vendas.venda_bp, "/api/venda"),
        (categorias.category_bp, "/api/categories")
    ]
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)  # Registra cada um dinamicamente
