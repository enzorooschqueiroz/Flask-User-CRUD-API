from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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
