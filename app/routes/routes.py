from flask_login import current_user
from app.controllers import usuario_controller
from datetime import datetime

from app import create_app
app = create_app()

from flask import jsonify, render_template, render_template_string # Motor que renderiza as paginas html

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
    anoAtual=datetime.now().year

    anos = [ano for ano in range(anoAtual-5, anoAtual+5, 1)]
    return render_template("calendario-anual.html", anos=anos, anoAtual=anoAtual)

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

# @app.route('/calendario/<int:ano>')
# def get_calendario(ano):
#     cal = calendar.Calendar(firstweekday=0)
#     dados = {
#         mes: list(cal.itermonthdays(ano, mes)) for mes in range(1, 13)
#     }
#     return jsonify(dados)

@app.route('/calendario/<int:ano>')
def calendario_html(ano):
    calendario = {}

    for mes in range(1, 13):
        weeks = calendar.monthcalendar(ano, mes)
        calendario[mes] = weeks  # lista de semanas com 7 elementos

    return render_template_string(render_calendario_html(calendario))
    

def render_calendario_html(calendario):
    html = ""

    for mes, semanas in calendario.items():
        nome_mes = calendar.month_name[mes]

        if (mes - 1) % 3 == 0:
            html += "<div class='row'>"

        html += f"<div class='mes-container col-4'><h4>{nome_mes}</h4><table class='table table-bordered text-center'>"
        html += "<thead><tr>" + "".join(f"<th>{dia}</th>" for dia in ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]) + "</tr></thead><tbody>"

        for semana in semanas:
            html += "<tr>" + "".join(f"<td>{dia if dia != 0 else ''}</td>" for dia in semana) + "</tr>"

        html += f"</tbody></table></div>"

        # fecha a linha a cada 3 meses
        if mes % 3 == 0:
            html += "</div>"

    # caso o último <div class="row"> não tenha sido fechado (ex: se o loop acabar no mês 11)
    if mes % 3 != 0:
        html += "</div>"

    return html
    