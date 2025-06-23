from app.models.evento import Evento
from datetime import datetime, date
import calendar
from sqlalchemy import func

import json
import ephem
from datetime import timedelta

from app.instances import db
from flask import request, redirect, url_for

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


# -> retorna todos os eventos entre primeiro e ultimo dia do ano
# def get_eventos_do_ano(ano): 
#     eventos_por_data = (
#         db.session.query(Evento.data_evento, func.count(Evento.id_evento))
#         .filter(
#             Evento.data_evento >= date(ano, 1, 1),
#             Evento.data_evento <= date(ano, 12, 31)
#         )
#         .group_by(Evento.data_evento)
#         .all()
#     )

#     return {data.strftime('%Y-%m-%d') for data, _ in eventos_por_data}

#Tentando fazer TODOS os eventos aparecerem no calendário
def get_eventos_do_ano(ano):
    eventos_db = (
        db.session.query(Evento.data_evento)
        .filter(Evento.data_evento >= date(ano, 1, 1),
                Evento.data_evento <= date(ano, 12, 31))
        .all()
    )
    datas_db = {data.strftime('%Y-%m-%d') for data, in eventos_db}

    # Eventos do JSON (astronômicos)
    eventos_json = carregar_eventos_astronomicos(ano)
    datas_json = set(eventos_json.keys())

    return datas_db.union(datas_json)


def get_eventos_do_mes(ano, mes):
    _, ultimo_dia = calendar.monthrange(ano, mes)

    eventos = (
        db.session.query(Evento)
        .filter(
            Evento.data_evento >= date(ano, mes, 1),
            Evento.data_evento <= date(ano, mes, ultimo_dia)
        )
        .all()
    )

    eventos_por_data = {}
    for evento in eventos:
        data_str = evento.data_evento.strftime('%Y-%m-%d')
        eventos_por_data.setdefault(data_str, []).append(evento)

    return eventos_por_data


def excluir_evento():
    pass

def editar_evento():
    pass

# ---------------------------------------------------------- Eventos do datas_astronomicas.json 

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

        if str(data) not in eventos:
            eventos[str(data)] = []

        eventos[str(data)].append(evento["nome"])

    return eventos

# ---------------------------------------------------------- Renderização do calendario ANUAL
def render_calendario_html(calendario, ano):
    hoje_ano = date.today().strftime('%Y-%m-%d') #Função p mostrar o dia de hoje :)
    html = ""

    eventos_por_dia = get_eventos_do_ano(ano)

    for mes, semanas in calendario.items():
        nome_mes = calendar.month_name[mes]

        if (mes - 1) % 3 == 0:
            html += "<div class='row'>"

        html += f"<div class='mes-container col-4'> <a href='/calendario/{ano}-{mes}'><h4 class='bosta'>{nome_mes}</h4><table class='table table-bordered text-center'>"
        html += "<thead><tr>" + "".join(f"<th>{dia}</th>" for dia in ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]) + "</tr></thead><tbody>"

        for semana in semanas:
            html += "<tr>"

            for dia in semana:
                if dia != 0:
                    data_str = f"{ano}-{mes:02d}-{dia:02d}"

                    classes = ["dia"]
                    if data_str in eventos_por_dia:
                        classes.append("dia-evento")
                    if data_str == hoje_ano:
                        classes.append("hoje-anual")

                    html += f"<td><div class='{' '.join(classes)}'><p>{dia}</p></div></td>"
                else:
                    html += "<td><div class='dia'><p>&nbsp;</p></div></td>"
                
                
            html += "</tr>"


        html += f"</tbody></table></a></div>"

        # fecha a linha a cada 3 meses
        if mes % 3 == 0:
            html += "</div>"

    # caso o último <div class="row"> não tenha sido fechado (ex: se o loop acabar no mês 11)
    if mes % 3 != 0:
        html += "</div>"

    return html

# ---------------------------------------------------------- Fases da lua no calendário MENSAL

def fases_lua_do_mes(ano, mes):
    fases = {
        '🌑': ephem.next_new_moon,
        '🌓': ephem.next_first_quarter_moon,
        '🌕': ephem.next_full_moon,
        '🌗': ephem.next_last_quarter_moon
    }

    data_inicio = ephem.Date(f"{ano}/{mes}/1")
    if mes == 12:
        data_limite = ephem.Date(f"{ano+1}/1/1")
    else:
        data_limite = ephem.Date(f"{ano}/{mes+1}/1")

    datas_fases = {}

    for emoji, funcao in fases.items():
        data = funcao(data_inicio)
        while data < data_limite:
            dia = data.datetime().day
            # Se houver mais de uma fase no mesmo dia, só guarda a primeira encontrada
            if dia not in datas_fases:
                datas_fases[dia] = emoji
            data = funcao(data + 1)  # pula para a próxima ocorrência

    return datas_fases

# ---------------------------------------------------------- Renderização do calendario MENSAL

def render_mes_html(ano, mes):
    eventos_por_dia = get_eventos_do_mes(ano, mes)  # dict com data_str: lista_de_eventos
    eventos_astronomicos = carregar_eventos_astronomicos(ano)
    fases_lua = fases_lua_do_mes(ano, mes)
    hoje = date.today() #Função p mostrar o dia de hoje :)

    nome_mes = calendar.month_name[mes]
    semanas = calendar.monthcalendar(ano, mes)

    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

    html = f"<div class='mes-unico-container'><h4>{nome_mes} {ano}</h4><table class='table table-bordered text-center'>"
    html += "<thead><tr>" + "".join(f"<th>{dia}</th>" for dia in dias_semana) + "</tr></thead><tbody>"

    for semana in semanas:
        html += "<tr>"
        for dia in semana:
            if dia == 0:
                html += "<td><div class='dia-sem-evento'>&nbsp;</div></td>"
            else:
                data_str = f"{ano}-{mes:02d}-{dia:02d}"

                eventos_dia = eventos_astronomicos.get(data_str, [])
                emoji = fases_lua.get(dia, "")
                tem_evento_db = data_str in eventos_por_dia.keys()
                eventos_astro_dia = eventos_astronomicos.get(data_str, [])

                classes = ["dia"]

                if eventos_astro_dia:
                    classes.append("evento-astronomico")
                if tem_evento_db:
                    classes.append("dia-evento")
                
                # Pra aparecer o dia de hoje no calendário :D
                if dia == hoje.day and mes == hoje.month and ano == hoje.year:
                    classes.append("hoje")


                html += f"<td><div class='{' '.join(classes)}' data-dia='{dia}'>"
                html += f"<p><span class='numero-dia'>{dia}</span></p>"


                if emoji:
                    html += f"<span class='emoji-lua'>{emoji}</span>"

                html += "<div class='eventos-scroll'>"

                # Eventos astronômicos
                for nome_evento in eventos_dia:
                    nome_limpo = nome_evento.split(" (")[0]
                    html += f"<div class='nome-evento'>{nome_limpo}</div>"

                # Eventos do banco
                if data_str in eventos_por_dia:
                    for evento in eventos_por_dia[data_str][:2]:  # limita a 2 eventos
                        dia_semana_num = datetime.strptime(data_str, "%Y-%m-%d").weekday()
                        dia_da_semana = dias_semana[dia_semana_num] 

                        if dia_semana_num not in (5, 6):  # só adiciona '-Feira' em dias úteis
                            dia_da_semana += '-Feira'

                        html += (
                            f"<div class='marcador-evento' "
                            f"data-data='{data_str}' data-titulo='{evento.titulo_evento}' "

                            f"data-local='{evento.local_evento}' data-descricao='{evento.descricao_evento}' data-horario-inicio='{evento.horario_inicio_evento}' "
                            f"data-horario-fim='{evento.horario_fim_evento}' data-categoria='{evento.categoria_evento}' data-dia-semana='{dia_da_semana}' "
                            f"onclick='abrirPopupExplicativo(this)'>{evento.titulo_evento}</div>"
                        )

                html += "</div>"  # fecha eventos-scroll
                html += "</div></td>"  # fecha .dia e td
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