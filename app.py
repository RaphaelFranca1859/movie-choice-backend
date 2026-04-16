from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from models import db  # Importamos o db aqui

# 1. Carregar as variáveis de ambiente do .env
load_dotenv()

# 2. Inicializar o app Flask
app = Flask(__name__)
CORS(app)

# 3. Configurações do App e do Banco de Dados
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-padrao-caso-nao-haja-env')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4. Inicializar o banco de dados com o app
db.init_app(app)

# 5. Criar as tabelas automaticamente (Contexto do App)
# Isso garante que o banco seja criado assim que o servidor subir
with app.app_context():
    db.create_all()

# 6. Importar rotas (IMPORTANTE: Sempre APÓS a inicialização do app e db)
# Isso evita erros onde as rotas tentam usar o app antes de ele existir
from route import *

# Rota básica de teste
@app.route('/healthcheck', methods=['GET'])
def health_check():
    return {"status": "online", "message": "Backend do MovieChoice funcionando!"}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)