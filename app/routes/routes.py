from flask_login import current_user
from app.controllers import usuario_controller, evento_controller
from datetime import datetime

from app import create_app
app = create_app()

from flask import render_template, render_template_string # Renderiza as paginas html

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

@app.route("/calendario")
def calendario():
    anoAtual=datetime.now().year

    anos = [ano for ano in range(anoAtual-5, anoAtual+5, 1)]
    return render_template("calendario-anual.html", anos=anos, anoAtual=anoAtual)

@app.route("/calendario/<int:ano>-<int:mes>")
def calendario_mes(ano, mes):

    if current_user.is_authenticated == False or current_user.tipo_usuario == 'comum' :
        html = render_template_string(render_mes_html(ano, mes))
        return render_template("calendario-mes.html", mes_html=html)
    
    elif current_user.is_authenticated and current_user.tipo_usuario == 'admin':
        html = render_template_string(render_admin_mes_html(ano, mes))
        return render_template("calendario-mes-admin.html", mes_html=html)
    
    else:
        html = render_template_string(render_mes_html(ano, mes))
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

    return render_template_string(render_calendario_html(calendario, ano))
    

def render_calendario_html(calendario, ano):
    html = ""

    for mes, semanas in calendario.items():
        nome_mes = calendar.month_name[mes]

        if (mes - 1) % 3 == 0:
            html += "<div class='row'>"

        html += f"<div class='mes-container col-4'> <a href='/calendario/{ano}-{mes}'><h4 class='bosta'>{nome_mes}</h4><table class='table table-bordered text-center'>"
        html += "<thead><tr>" + "".join(f"<th>{dia}</th>" for dia in ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]) + "</tr></thead><tbody>"

        for semana in semanas:
            html += "<tr>" + "".join(f"<td><div class='dia'><p>{dia if dia != 0 else '&nbsp'}</p></div></td>" for dia in semana) + "</tr>"

        html += f"</tbody></table></a></div>"

        # fecha a linha a cada 3 meses
        if mes % 3 == 0:
            html += "</div>"

    # caso o último <div class="row"> não tenha sido fechado (ex: se o loop acabar no mês 11)
    if mes % 3 != 0:
        html += "</div>"

    return html

# def render_mes_html(ano, mes):
#     html = ""

#     nome_mes = calendar.month_name[mes]
#     semanas = calendar.monthcalendar(ano, mes)

#     html += f"<div class='mes-unico-container'><h4>{nome_mes} {ano}</h4><table class='table table-bordered text-center'>"
#     html += "<thead><tr>" + "".join(f"<th>{dia}</th>" for dia in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]) + "</tr></thead><tbody>"

#     for semana in semanas:
#         html += "<tr>" + "".join(f"<td><div class='dia'><p>{dia if dia != 0 else '&nbsp'}</p></div></td>" for dia in semana) + "</tr>"

#     html += "</tbody></table></div>"

#     return html

# ---------------------------------------------------------- rotas admin

def render_admin_mes_html(ano, mes):
    html = ""

    nome_mes = calendar.month_name[mes]
    semanas = calendar.monthcalendar(ano, mes)

    html += f"<div class='mes-unico-container'><h4>{nome_mes} {ano}</h4><table class='table table-bordered text-center'>"
    html += "<thead><tr>" + "".join(f"<th>{dia}</th>" for dia in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]) + "</tr></thead><tbody>"

    for semana in semanas:
        html += "<tr>" + "".join(f"<td><div class='dia-admin'>{"<button data-data="+str(ano)+"-"+str(mes)+"-"+str(dia)+" onclick='openPopup(this)'>"+str(dia)+"</button>" if dia != 0 else "&nbsp"}</div></td>" for dia in semana) + "</tr>"

    html += "</tbody></table></div>"

    return html

@app.route("/admin/calendario/<int:ano>-<int:mes>")
def admin_calendario_mes(ano, mes):
    html = render_template_string(render_admin_mes_html(ano, mes))

    return render_template("calendario-mes-admin.html", mes_html=html)

# ---------------------------------------------------------- TESTES
import json
import ephem
from datetime import timedelta

def calcular_dia_mundial_astronomia(ano):
    equinocio = datetime(ano, 9, 22)
    proximo_quarto_crescente = ephem.next_first_quarter_moon(ephem.Date(equinocio)).datetime()

    dias_para_sabado = (5 - proximo_quarto_crescente.weekday()) % 7
    sabado = proximo_quarto_crescente + timedelta(days=dias_para_sabado)

    if abs((sabado - proximo_quarto_crescente).days) > 3:
        sabado -= timedelta(days=7)

    return sabado.date()


def carregar_eventos_astronomicos(ano):
    with open("app/datas_astronomicas.json", "r", encoding="utf-8") as f:
        datas = json.load(f)

    eventos = {}

    for evento in datas:
        if evento.get("movel"):
            data = calcular_dia_mundial_astronomia(ano)
        elif evento.get("data"):
            dia, mes = map(int, evento["data"].split("-"))
            data = datetime(ano, mes, dia).date()
        else:
            continue  # ignora eventos sem data válida

        eventos[str(data)] = evento["nome"]

    return eventos



def render_mes_html(ano, mes):
    eventos = carregar_eventos_astronomicos(ano)

    nome_mes = calendar.month_name[mes]
    semanas = calendar.monthcalendar(ano, mes)

    html = f"<div class='mes-unico-container'><h4>{nome_mes} {ano}</h4><table class='table table-bordered text-center'>"
    html += "<thead><tr>" + "".join(f"<th>{dia}</th>" for dia in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]) + "</tr></thead><tbody>"

    for semana in semanas:
        html += "<tr>"
        for dia in semana:
            if dia == 0:
                html += "<td><div class='dia'>&nbsp;</div></td>"
            else:
                data_str = f"{ano}-{mes:02d}-{dia:02d}"
                nome_evento = eventos.get(data_str)

                if nome_evento:
                    html += f"""
                    <td>
                        <div class='dia evento-astronomico' data-dia='{dia}'>
                            <p>{dia}</p>
                            <div class='nome-evento'>{nome_evento}</div>
                        </div>
                    </td>
                    """
                else:
                    html += f"<td><div class='dia' data-dia='{dia}'><p>{dia}</p></div></td>"
        html += "</tr>"

    html += "</tbody></table></div>"
    return html
@app.route('/admin/adicionar-evento', methods=['POST'])
def route_adicionar_evento():
    return evento_controller.adicionar_evento()
