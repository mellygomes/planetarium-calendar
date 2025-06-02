from app import create_app

app = create_app()

#rotas
from app.routes.routes import *

if __name__ == "__main__":
    app.run(debug=True)