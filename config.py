import os
from flask import Flask, Blueprint, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(app.root_path, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

migrate = Migrate(app, db)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
config_bp = Blueprint('config', __name__)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

def create_db():
    db.drop_all()
    db.create_all()
    response_text = '{ "message": "Database created." }'
    response = Response(response_text, 200, mimetype='application/json')
    return response
