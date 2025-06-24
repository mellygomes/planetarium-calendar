from flask_login import current_user
from app.controllers import usuario_controller, evento_controller
from datetime import datetime

from app import create_app
app = create_app()

from flask import render_template, render_template_string # Renderiza as paginas html

@app.route("/")
def homepage():
    if current_user.is_authenticated:
        return render_template('homepage.html', usuario=current_user, upcoming_events=evento_controller.get_lista_eventos_proximos())
    else:
        return render_template('homepage.html', upcoming_events=evento_controller.get_lista_eventos_proximos())

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/eventos")
def eventos():
    return render_template("eventos.html", eventos=evento_controller.get_lista_eventos_recentes())

@app.route("/calendario")
def calendario():
    anoAtual=datetime.now().year

    anos = [ano for ano in range(anoAtual-5, anoAtual+5, 1)] # -> Mostra sempre 5 anos anteriores e 
    return render_template("calendario-anual.html", anos=anos, anoAtual=anoAtual)

@app.route("/calendario/<int:ano>-<int:mes>")
def calendario_mes(ano, mes):

    if current_user.is_authenticated == False or current_user.tipo_usuario == 'comum' :
        html = render_template_string(evento_controller.render_mes_html(ano, mes))
        return render_template("calendario-mes.html", mes_html=html)
    
    elif current_user.is_authenticated and current_user.tipo_usuario == 'admin':
        html = render_template_string(evento_controller.render_admin_mes_html(ano, mes))
        return render_template("calendario-mes-admin.html", mes_html=html)
    
    else:
        html = render_template_string(evento_controller.render_mes_html(ano, mes))
        return render_template("/admin/calendario/<int:ano>-<int:mes>", mes_html=html)

# --------------------------------------------------------------- Rotas de acoes

@app.route('/cadastrar_usuario', methods=['POST'])
def route_cadastrar_usuario():
    return usuario_controller.cadastrar_usuario()

@app.route('/fazer_login', methods=['POST'])
def route_fazer_login():
    return usuario_controller.login()

@app.route('/logout')
def route_logout():
    return usuario_controller.logout()

# ------------------------------------------------ Calendario

import calendar
@app.route('/calendario/<int:ano>')
def calendario_html(ano):
    calendario = {}

    for mes in range(1, 13):
        weeks = calendar.monthcalendar(ano, mes)

        # garantir que haja exatamente 6 semanas (6 linhas na tabela)
        while len(weeks) < 6:
            weeks.append([0, 0, 0, 0, 0, 0, 0])

        calendario[mes] = weeks

    return render_template_string(evento_controller.render_calendario_html(calendario, ano))

# ------------------- admin

@app.route('/admin/adicionar-evento', methods=['POST'])
def route_adicionar_evento():
    return evento_controller.adicionar_evento()
