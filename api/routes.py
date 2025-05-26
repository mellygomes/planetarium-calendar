import os
import psycopg2
from dotenv import load_dotenv
from flask import Blueprint, jsonify

# load_dotenv()

# url = os.getenv("DATABASE_URL")
# connection = psycopg2.connect(url)

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/status')
def status():
    return jsonify({"status": "online"})


