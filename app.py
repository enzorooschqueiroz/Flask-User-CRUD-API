from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    "db": "users",
    "host": "mongodb",  # Use 'mongodb' as the hostname, not 'localhost'
    "port": 27017,
    "username": "admin",
    "password": "admin",
    "authentication_source": "admin"
}


api = Api(app)
db = MongoEngine(app)


class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True)
    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    birth_date = db.DateTimeField(required=True)

class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


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
