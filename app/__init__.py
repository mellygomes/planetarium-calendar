from flask import Flask
from app.instances import init_instances
from app.auth import init_auth
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.secret_key = os.getenv('SECRET_KEY')

    init_instances(app)
    
    init_auth()

    return app
