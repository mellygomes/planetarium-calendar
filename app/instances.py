from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_login import LoginManager
login_manager = LoginManager()

def init_instances(app):
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login'