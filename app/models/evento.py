from app.instances import db

class Evento(db.Model):
    __tablename__ = 'evento'

    id_evento = db.Column(db.Integer, primary_key=True)
    data_evento = db.Column(db.Date, nullable=False)
    titulo_evento = db.Column(db.String(60), nullable=False)
    descricao_evento = db.Column(db.String(200), nullable=False)
    local_evento = db.Column(db.String(80), nullable=False)
    horario_inicio_evento = db.Column(db.Time, nullable=False)
    horario_fim_evento = db.Column(db.Time, nullable=False)
    # data_fim_evento = db.Column(db.Date, nullable=False)
    categoria_evento = db.Column(db.String(80), nullable=False)

    def __init__(self, data, titulo, descricao, local, horario_inicio, horario_fim, categoria):
        self.data_evento = data
        self.titulo_evento = titulo
        self.descricao_evento = descricao
        self.local_evento = local
        self.horario_inicio_evento = horario_inicio
        self.horario_fim_evento = horario_fim
        # self.data_fim_evento = data_fim
        self.categoria_evento = categoria
