from flask import Flask # Flask para criar o site
app = Flask(__name__)

#rotas
from routes.routes import *

if __name__ == "__main__":
    app.run()