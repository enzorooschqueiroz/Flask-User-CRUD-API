from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine
import re
from datetime import datetime  # Adicione esta importação

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    "db": "users",
    "host": "mongodb",
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

    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        # Verifica a formatação do CPF
        if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
            return False

        # Obtém apenas os números do CPF, ignorando pontuações
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se o CPF possui 11 números ou se todos são iguais
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validação do primeiro dígito verificador
        sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador
        sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def post(self):
        data = _user_parser.parse_args()

        # Validação do CPF
        if not User.validate_cpf(data['cpf']):  # Chama validate_cpf da classe User
            return {"message": "Invalid CPF"}, 400

        response = UserModel(**data).save()      
        return {"message": "User %s created successfully" %response.id}

    def get(self, cpf):
        user = UserModel.objects(cpf=cpf).first()
        if user:
            return jsonify(user), 200
        return {"message": "User not found"}, 404

# Definindo endpoints
api.add_resource(Users, '/users', endpoint='users_list')
api.add_resource(User, '/user', '/user/<string:cpf>', endpoint='user_detail')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
