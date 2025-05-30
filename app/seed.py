from app.extensions import db, migrate
from app import create_app
from flask_migrate import upgrade as migrate_upgrade

def seed_database():

    from app.models.User import User
    from app.models.Product import Product
    from app.models.Category import Category
    from app.models.Customer import Customer
    from app.models.Sale import Sale

    from datetime import datetime, timezone
    from random import choice, randint
    from werkzeug.security import generate_password_hash

    if User.query.first():
        print("ja existem dados")
        return

    try:
        category_names = ["Computadores", "Periféricos", "Acessórios", "Impressão"]
        categories = [Category(name=name) for name in category_names]
        db.session.add_all(categories)
        db.session.flush()

        product_data = [
            ("Portátil Lenovo", "Portátil com 16GB RAM", 799.99, 15, "Computadores"),
            ("Monitor Dell", "24 polegadas Full HD", 149.99, 30, "Periféricos"),
            ("Teclado Mecânico", "Switches azuis", 89.90, 50, "Periféricos"),
            ("Rato sem fio", "Conexão Bluetooth", 29.99, 40, "Acessórios"),
            ("Impressora HP", "Multifunções", 119.00, 20, "Impressão"),
            ("Pen Drive 64GB", "USB 3.0", 12.99, 100, "Acessórios"),
            ("Portátil ASUS", "Core i5, SSD 512GB", 899.99, 10, "Computadores"),
            ("Webcam Logitech", "HD 1080p", 69.90, 25, "Periféricos"),
            ("Headset Gamer", "Som surround 7.1", 79.99, 35, "Periféricos"),
            ("Tinteiros HP", "Preto e cor", 34.90, 60, "Impressão"),
        ]
        products = [
            Product(
                name=name,
                description=desc,
                price=price,
                stock_quantity=stock,
                category=next(c for c in categories if c.name == cat),
                active=True
            )
            for name, desc, price, stock, cat in product_data
        ]
        db.session.add_all(products)

        customer_data = [
            ("Carlos Mendes", "carlos.mendes@gmail.com", "+351912345671"),
            ("Isabel Costa", "isabel.costa@gmail.com", "+351912345672"),
            ("Rui Oliveira", "rui.oliveira@gmail.com", "+351912345673"),
            ("Teresa Martins", "teresa.martins@gmail.com", "+351912345674"),
            ("Bruno Ferreira", "bruno.ferreira@gmail.com", "+351912345675"),
            ("Vera Lopes", "vera.lopes@gmail.com", "+351912345676"),
            ("Fábio Dias", "fabio.dias@gmail.com", "+351912345677"),
            ("Helena Sousa", "helena.sousa@gmail.com", "+351912345678"),
            ("Pedro Rocha", "pedro.rocha@gmail.com", "+351912345679"),
            ("Joana Ramos", "joana.ramos@gmail.com", "+351912345680"),
        ]
        customers = [
            Customer(name=name, email=email, phone=phone, active=True, registered_at=datetime.now(timezone.utc))
            for name, email, phone in customer_data
        ]
        db.session.add_all(customers)

        user_data = [
            ("Admin", "admin@store.com", "admin123", "admin"),
            ("João Silva", "joao@store.com", "joao123", "user"),
            ("Maria Santos", "maria@store.com", "maria123", "user"),
            ("Carlos Lima", "carlos@store.com", "carlos123", "user"),
            ("Sofia Costa", "sofia@store.com", "sofia123", "user"),
            ("André Rocha", "andre@store.com", "andre123", "user"),
            ("Beatriz Alves", "beatriz@store.com", "beatriz123", "user"),
            ("Tiago Neves", "tiago@store.com", "tiago123", "user"),
            ("Ana Reis", "ana@store.com", "ana123", "user"),
            ("Ricardo Fonseca", "ricardo@store.com", "ricardo123", "user"),
        ]
        users = [
            User(name=name, 
                email=email, 
                password=generate_password_hash(pw), 
                role=role, 
                active=True)
            for name, email, pw, role in user_data
        ]
        db.session.add_all(users)
        db.session.flush()

        sales = []
        for _ in range(10):
            product = choice(products)
            quantity = randint(1, 3)
            total_value = round(product.price * quantity, 2)
            sale = Sale(
                product=product,
                customer=choice(customers),
                user=choice(users),
                quantity=quantity,
                total_value=total_value,
                sale_date=datetime.now(timezone.utc)
            )
            sales.append(sale)
        db.session.add_all(sales)

        db.session.commit()
    except Exception as e:
        print(f"Erro ao tentar popular as tabelas {e}")

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        migrate_upgrade()
        seed_database()