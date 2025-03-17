from flask import Flask
from routes.api import produtos, login, utilizador, clientes, vendas, categorias 

def init_routes(app: Flask):
    """Registra todos os Blueprints da aplicação"""
    blueprints = [
        (produtos.produto_bp, "/api/produto"),
        (login.login_bp, "/api/login"),
        (utilizador.utilizador_bp, "/api/utilizador"),
        (clientes.cliente_bp, "/api/cliente"),
        (vendas.venda_bp, "/api/venda"),
        (categorias.categoria_bp, "/api/categoria")
    ]
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)  # Registra cada um dinamicamente
