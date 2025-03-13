from flask import Flask
from routes import init_routes
from config import DEBUG,SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"]= SECRET_KEY
app.config["DEBUG"] = DEBUG


# Inicializa as rotas
init_routes(app)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
