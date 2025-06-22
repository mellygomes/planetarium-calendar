from app.models.evento import Evento
from datetime import datetime

from app.instances import db
from flask import request, redirect, url_for

from app import create_app
app = create_app()

def adicionar_evento():
    if (request.method == 'POST' and
        'data_evento' in request.form and
        'titulo' in request.form and
        'horario_inicio' in request.form and
        'horario_fim' in request.form and
        'localizacao' in request.form and
        'categoria' in request.form and
        'descricao' in request.form):
        
        data = request.form['data_evento']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        local = request.form['localizacao']
        horario_inicio = request.form['horario_inicio']
        horario_fim = request.form['horario_fim']
        categoria = request.form['categoria']

        evento = Evento(data, titulo, descricao, local, horario_inicio, horario_fim, categoria)

        try:
            db.session.add(evento)
            db.session.commit()

            dt = datetime.strptime(data, "%Y-%m-%d")
            return redirect(url_for('admin_calendario_mes', ano=dt.year, mes=dt.month)) # -> Mostrar uma mensagem de sucesso depois
        except Exception as e:
            db.session.rollback()
            print("Erro ao salvar evento:", e)
            return redirect(url_for('homepage'))  # redirecionar com erro (pode passar erro=True)

    # Se não passou pelo if, retorna algo
    return "Dados do formulário ausentes ou inválidos", 400


def excluir_evento():
    pass

def editar_evento():
    pass