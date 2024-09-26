from flask import Flask
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine

app = Flask(__name__)
api = Api(app)
db = MongoEngine(app)

app.config['MONGODB_SETTING'] = {
    "db": "users",
    "host": "mongodb",
    "port": 27017,
    "user": "admin",
    "password": "admin"  # Inserir credenciais do MongoDB aqui
}

class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True)
    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    birth_date = db.DateTimeField(required=True)

class Users(Resource):
    def get(self):
        return {'message': 'user 1'}


class User(Resource):
    def post(self):
        return {'message': 'teste'}

    def get(self, cpf):
        return {'message': 'CPF 1'}

# Definindo um endpoint explícito para evitar conflitos
api.add_resource(Users, '/users', endpoint='users_list')  # Novo endpoint
api.add_resource(User, '/user', '/user/<string:cpf>', endpoint='user_detail')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
