from flask import Flask
from config import Config
from database import Database 
from routes.api import init_routes

app = Flask(__name__)

# Aplicar configurações do Flask
app.config.from_object(Config)

# Registrar modelos e garantir que o banco de dados está configurado corretamente
Database.registrar_modelos()

# Inicializar rotas da API
init_routes(app)

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
