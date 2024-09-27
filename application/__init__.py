from flask import Flask
from flask_restful import Api
from .db import _init_db
from .app import User, Users

def create_app(config):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(config)
    _init_db(app)

    # Definindo endpoints
    api.add_resource(Users, '/users', endpoint='users_list')
    api.add_resource(User, '/user', '/user/<string:cpf>', endpoint='user_detail')