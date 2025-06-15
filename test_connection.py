from app import create_app
from app.instances import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        result = db.session.execute(text('SELECT 1'))
        print("Conexao bem sucedida com o banco de dados")
    except Exception as e:
        print("Erro ao conectar com o banco de dados: ")
        print(e)