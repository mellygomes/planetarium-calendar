from flask import Flask # Flask para criar o site
from api.routes import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

#rotas
from routes.routes import *

if __name__ == "__main__":
    app.run(debug=True)