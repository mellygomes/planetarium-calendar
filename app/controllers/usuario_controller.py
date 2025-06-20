from app.models.usuario import Usuario 

from app.instances import db
from flask import request, redirect, url_for, render_template
from flask_login import login_user, logout_user

from app import create_app
app = create_app()

def cadastrar_usuario():
    if request.method == 'POST' and 'nome_usuario' in request.form and 'email_usuario' in request.form and 'senha_usuario' in request.form:
        nome_usuario = request.form['nome_usuario']
        email_usuario = request.form['email_usuario']
        senha_usuario = request.form['senha_usuario']

        usuario=Usuario(nome_usuario, email_usuario, senha_usuario)
        db.session.add(usuario)
        db.session.commit()

        if usuario.id_usuario:
            login_user(usuario)
            return redirect(url_for('login'))
        else:
            return redirect(url_for('cadastro'), erro=True)
    
def login():
    if request.method == 'POST' and 'email_usuario' in request.form and 'senha_usuario' in request.form:
        email = request.form['email_usuario']
        senha = request.form['senha_usuario']
        usuario = Usuario.query.filter_by(email_usuario=email).first()

    if usuario and usuario.senha_usuario == senha:
        login_user(usuario)
        return redirect(url_for('homepage'))
    else:
        print("erro")
        return render_template('login.html', erro=True)

def logout():
    logout_user()
    return redirect(url_for('homepage'))

        