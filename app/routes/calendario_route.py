# import calendar
# from flask import jsonify

# from app import create_app
# app = create_app()

# @app.route('/calendario/<int:ano>')
# def get_calendario(ano):
#     cal = calendar.Calendar(firstweekday=6)
#     dados = {
#         mes: list(cal.itermonthdays(ano, mes)) for mes in range(1, 13)
#     }
#     return jsonify(dados)