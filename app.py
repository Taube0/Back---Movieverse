from flask import Flask, render_template
from flask_cors import CORS
import os
import logging
from db import init_db, db
from routes import register_routes
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configuração do CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuração do banco de dados
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise RuntimeError("DATABASE_URL não está definido no .env")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

# Inicialize o banco de dados com a aplicação Flask
init_db(app)

# Registre as rotas definidas no routes.py
register_routes(app)

# Rota para servir a página inicial
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
