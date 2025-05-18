from main import app
from flask import render_template # Motor que renderiza as paginas html

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/login")
def login():
    return render_template("login.html")