from flask import Flask
from app.routes.api import auth, category, customer, product, sale, user 

def init_routes(app: Flask):
    """Registra todos os Blueprints da aplicação"""
    blueprints = [
        (product.product_bp, "/api/product"),
        (auth.auth_bp, "/api/auth"),
        (user.user_bp, "/api/user"),
        (customer.customer_bp, "/api/customer"),
        (sale.sale_bp, "/api/sale"),
        (category.category_bp, "/api/category")
    ]
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)  # Registra cada um dinamicamente
