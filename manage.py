from app import create_app
from flask_migrate import upgrade
from app.seed import seed_database

app = create_app()

with app.app_context():

    seed_database() 
