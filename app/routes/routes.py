from flask_login import current_user
from app.controllers import usuario_controller

from app import create_app
app = create_app()

from flask import jsonify, render_template # Motor que renderiza as paginas html

@app.route("/")
def homepage():
    if current_user.is_authenticated:
        return render_template('homepage.html', usuario=current_user)
    else:
        return render_template('homepage.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/calendario-mes")
def calendario_mes():
    return render_template("calendario-mes.html")

@app.route("/calendario")
def calendario():
    anos = [ano for ano in range(2020, 2031, 1)]
    return render_template("calendario-anual.html", anos=anos)

# @app.route("/cadastro2")
# def cadastro2():
#     return render_template("cadastro2.html")

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

import calendar

@app.route('/calendario/<int:ano>')
def get_calendario(ano):
    cal = calendar.Calendar(firstweekday=6)
    dados = {
        mes: list(cal.itermonthdays(ano, mes)) for mes in range(1, 13)
    }
    return jsonify(dados)
    
    