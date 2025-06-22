from app.instances import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(80), nullable=False)
    email_usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha_usuario = db.Column(db.String(50), nullable=False)
    nascimento_usuario = db.Column(db.String(50), nullable=True)
    tipo_usuario = db.Column(db.String(5), nullable=False)


    def __init__(self, nome, email, senha, nascimento=None, tipo='comum'):
        self.nome_usuario = nome
        self.email_usuario = email
        self.senha_usuario = senha
        self.nascimento_usuario = nascimento
        self.tipo_usuario = tipo

    def get_id(self):
        return str(self.id_usuario)