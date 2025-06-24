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

def get_lista_eventos_proximos():
    hoje = datetime.today().date()
    proximos_tres_meses = hoje.replace(month=hoje.month + 3)

    eventos = (
        db.session.query(Evento)
        .filter(
            Evento.data_evento <= proximos_tres_meses,
            Evento.data_evento >= hoje
        )
        .all()
    )

    return eventos


def get_lista_eventos_recentes():
    hoje = datetime.today().date()
    tres_anos_atras = hoje.replace(year=hoje.year - 3)

    eventos = (
        db.session.query(Evento)
        .filter(
            Evento.data_evento >= tres_anos_atras,
            Evento.data_evento <= hoje
        )
        .all()
    )

    return eventos

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

# TESTE METEOROS

def carregar_chuvas_meteoros(ano):
    import json

    with open("app/chuvas_meteoros.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    eventos = {}

    for evento in dados:
        nome = evento["nome"]

        dia_inicio, mes_inicio = map(int, evento["inicio"].split("-"))
        dia_fim, mes_fim = map(int, evento["fim"].split("-"))

        data_inicio = date(ano, mes_inicio, dia_inicio)
        data_fim = date(ano, mes_fim, dia_fim)

        # Se o intervalo cruzar o fim do ano (ex: 20-12 até 05-01)
        if data_fim < data_inicio:
            # Vai até 31 de dezembro
            data = data_inicio
            while data <= date(ano, 12, 31):
                eventos.setdefault(str(data), []).append(nome)
                data += timedelta(days=1)
            # Continua em janeiro do ano seguinte
            data = date(ano + 1, 1, 1)
            while data <= date(ano + 1, mes_fim, dia_fim):
                eventos.setdefault(str(data), []).append(nome)
                data += timedelta(days=1)
        else:
            data = data_inicio
            while data <= data_fim:
                eventos.setdefault(str(data), []).append(nome)
                data += timedelta(days=1)

    return eventos


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
    hoje = date.today()

    chuvas_meteoros = carregar_chuvas_meteoros(ano)
    for data, nomes in chuvas_meteoros.items():
        eventos_astronomicos.setdefault(data, []).extend(nomes)

    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    meses_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    nome_mes = meses_ano[mes - 1] # -> -1 porque e começa em 0
    semanas = calendar.monthcalendar(ano, mes)

    html = f"<div class='mes-unico-container'><h4>{nome_mes} {ano}</h4><table class='table table-bordered text-center'>"
    html += "<thead><tr>" + "".join(f"<th>{dia}</th>" for dia in dias_semana) + "</tr></thead><tbody>"

    for semana in semanas:
        html += "<tr>"
        for dia in semana:
            if dia == 0:
                html += "<td><div class='dia-sem-evento'>&nbsp;</div></td>"
            else:
                data_str = f"{ano}-{mes:02d}-{dia:02d}"

                eventos_dia_completos = eventos_astronomicos.get(data_str, [])
                chuvas_dia = [e for e in eventos_dia_completos if e.lower() in [nome.lower() for nomes in chuvas_meteoros.values() for nome in nomes]]
                outros_eventos_dia = [e for e in eventos_dia_completos if e not in chuvas_dia]

                emoji = fases_lua.get(dia, "")

                tem_evento_db = data_str in eventos_por_dia.keys()

                classes = ["dia"]
                if eventos_dia_completos:
                    classes.append("evento-astronomico")
                if tem_evento_db:
                    classes.append("dia-evento")

                if dia == hoje.day and mes == hoje.month and ano == hoje.year:
                    classes.append("hoje")

                html += f"<td><div class='{' '.join(classes)}' data-dia='{dia}'>"
                html += f"<p><span class='numero-dia'>{dia}</span></p>"

                if emoji:
                    html += f"<span class='emoji-lua'>{emoji}</span>"

                if chuvas_dia:
                    nome_chuvas = ", ".join(chuvas_dia)
                    html += f"<span class='emoji-estrela' title='{nome_chuvas}'>🌠</span>"

                html += "<div class='eventos-scroll'>"

                for nome_evento in outros_eventos_dia:
                    nome_limpo = nome_evento.split(" (")[0]
                    html += f"<div class='nome-evento'>{nome_limpo}</div>"

                if tem_evento_db:
                    for evento in eventos_por_dia[data_str][:2]:
                        dia_semana_num = datetime.strptime(data_str, "%Y-%m-%d").weekday()
                        dia_da_semana = dias_semana[dia_semana_num]

                        if dia_semana_num not in (5, 6):
                            dia_da_semana += '-Feira'

                        html += (
                            f"<div class='marcador-evento' "
                            f"data-data='{data_str}' data-titulo='{evento.titulo_evento}' "
                            f"data-local='{evento.local_evento}' data-descricao='{evento.descricao_evento}' data-horario-inicio='{evento.horario_inicio_evento}' "
                            f"data-horario-fim='{evento.horario_fim_evento}' data-categoria='{evento.categoria_evento}' data-dia-semana='{dia_da_semana}' "
                            f"onclick='abrirPopupExplicativo(this)'>{evento.titulo_evento}</div>"
                        )

                html += "</div>"  
                html += "</div></td>"  
        html += "</tr>"

    html += "</tbody></table></div>"
    return html


# ---------------------------------------------------------- admin

def render_admin_mes_html(ano, mes):
    eventos_por_dia = get_eventos_do_mes(ano, mes)  # dict com data_str: lista_de_eventos
    eventos_astronomicos = carregar_eventos_astronomicos(ano)
    fases_lua = fases_lua_do_mes(ano, mes)
    hoje = date.today()

    chuvas_meteoros = carregar_chuvas_meteoros(ano)
    for data, nomes in chuvas_meteoros.items():
        eventos_astronomicos.setdefault(data, []).extend(nomes)

    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    meses_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    nome_mes = meses_ano[mes - 1] # -> -1 porque e começa em 0
    semanas = calendar.monthcalendar(ano, mes)

    html = f"<div class='mes-unico-container'><h4>{nome_mes} {ano}</h4><table class='table table-bordered text-center'>"
    html += "<thead><tr>" + "".join(f"<th>{dia}</th>" for dia in dias_semana) + "</tr></thead><tbody>"

    for semana in semanas:
        html += "<tr>"
        for dia in semana:
            if dia == 0:
                html += "<td><div class='dia-sem-evento'>&nbsp;</div></td>"
            else:
                data_str = f"{ano}-{mes:02d}-{dia:02d}"

                eventos_dia_completos = eventos_astronomicos.get(data_str, [])
                chuvas_dia = [e for e in eventos_dia_completos if e.lower() in [nome.lower() for nomes in chuvas_meteoros.values() for nome in nomes]]
                outros_eventos_dia = [e for e in eventos_dia_completos if e not in chuvas_dia]

                emoji = fases_lua.get(dia, "")

                tem_evento_db = data_str in eventos_por_dia.keys()

                classes = ["dia"]
                if eventos_dia_completos:
                    classes.append("evento-astronomico")
                if tem_evento_db:
                    classes.append("dia-evento")

                if dia == hoje.day and mes == hoje.month and ano == hoje.year:
                    classes.append("hoje")

                html += f"<td><div class='{' '.join(classes)}' data-dia='{dia}' data-data='{data_str}' onclick='openPopup(this)'>"
                html += f"<p><span class='numero-dia'>{dia}</span></p>"

                if emoji:
                    html += f"<span class='emoji-lua'>{emoji}</span>"

                if chuvas_dia:
                    nome_chuvas = ", ".join(chuvas_dia)
                    html += f"<span class='emoji-estrela' title='{nome_chuvas}'>🌠</span>"

                html += "<div class='eventos-scroll'>"

                for nome_evento in outros_eventos_dia:
                    nome_limpo = nome_evento.split(" (")[0]
                    html += f"<div class='nome-evento'>{nome_limpo}</div>"

                if tem_evento_db:
                    for evento in eventos_por_dia[data_str][:2]:
                        dia_semana_num = datetime.strptime(data_str, "%Y-%m-%d").weekday()
                        dia_da_semana = dias_semana[dia_semana_num]

                        if dia_semana_num not in (5, 6):
                            dia_da_semana += '-Feira'

                        html += (
                            f"<div class='marcador-evento' "
                            f"data-data='{data_str}' data-titulo='{evento.titulo_evento}' "
                            f"data-local='{evento.local_evento}' data-descricao='{evento.descricao_evento}' data-horario-inicio='{evento.horario_inicio_evento}' "
                            f"data-horario-fim='{evento.horario_fim_evento}' data-categoria='{evento.categoria_evento}' data-dia-semana='{dia_da_semana}' "
                            f"onclick='abrirPopupExplicativo(this)'>{evento.titulo_evento}</div>"
                        )

                html += "</div>"  
                html += "</div></td>"  
        html += "</tr>"

    html += "</tbody></table></div>"
    return html