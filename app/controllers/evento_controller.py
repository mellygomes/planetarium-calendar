from app.models.evento import Evento
from datetime import datetime
import calendar

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

# ---------------------------------------------------------- admin

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