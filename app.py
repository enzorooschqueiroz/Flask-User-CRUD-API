from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
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

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('cpf',
                          type=str,
                          required=True,
                          help="CPF of the user cannot be blank")
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="Email of the user cannot be blank")
_user_parser.add_argument('first_name',
                          type=str,
                          required=True,
                          help="First name of the user cannot be blank")
_user_parser.add_argument('last_name',
                          type=str,
                          required=True,
                          help="Last name of the user cannot be blank")
_user_parser.add_argument('birth_date',
                          type=str,
                          required=True,
                          help="Birthdate of the user cannot be blank")
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
        data = _user_parser.parse_args()
        UserModel(**data).save()
        return {"message": "AAAAAAAAAAAAA"}

    def get(self, cpf):
        return {'message': 'CPF 1'}

# Definindo um endpoint explícito para evitar conflitos
api.add_resource(Users, '/users', endpoint='users_list')  # Novo endpoint
api.add_resource(User, '/user', '/user/<string:cpf>', endpoint='user_detail')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
