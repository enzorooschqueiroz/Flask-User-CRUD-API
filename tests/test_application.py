import pytest
from application import create_app


class TestApplication():

    @pytest.fixture
    def client(self): 
        app = create_app('config.MockConfig')
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "Jonh",
            "last_name": "Doe",
            "birth_date": "1990-01-01",
            "cpf": "858.853.850-41",
            "email": "user@example.com"
        }
    
    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "Gabriel",
            "last_name": "Doe",
            "birth_date": "1990-01-01",
            "cpf": "858.853.850-42",
            "email": "user@example.com"
        }
    
    @pytest.fixture
    def updated_user(self):
        return {
            "first_name": "Gabriel Updated",
            "last_name": "Doe Updated",
            "birth_date": "1990-01-01",
            "cpf": "858.853.850-41",  # Mantenha o mesmo CPF do valid_user
            "email": "updated_user@example.com"  # Use um novo email se preferir
        }

    def test_get_users(self, client):
        response = client.get('/users')
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post('/user', json=valid_user)
        assert response.status_code == 201
        assert b"successfully" in response.data

        response = client.post('/user', json=invalid_user)
        assert response.status_code == 400 
        assert b"Invalid" in response.data

    def test_get_user(self, client, valid_user, invalid_user):
        response = client.get('/user/%s' % valid_user["cpf"])
        assert response.status_code == 200

        user_data = response.json
        assert user_data["first_name"] == "Jonh"
        assert user_data["last_name"] == "Doe"
        birth_date = user_data["birth_date"]["$date"]
        assert birth_date == "1990-01-01T00:00:00Z"
        assert user_data["cpf"] == "858.853.850-41"
        assert user_data["email"] == "user@example.com"

        response = client.get('/user/%s' % invalid_user["cpf"])
        assert response.status_code == 404
        assert b"User not found" in response.data

    def test_delete_user(self, client, valid_user, invalid_user):
        response = client.delete('/user/%s' % valid_user["cpf"])
        assert response.status_code == 200
        assert b"User deleted succesfully" in response.data  # Corrigido o erro de digitação

        response = client.delete('/user/%s' % invalid_user["cpf"])
        assert response.status_code == 404
        assert b"User not found" in response.data

    def test_update_user(self, client, valid_user, invalid_user, updated_user):
        
        response = client.post('/user', json=valid_user)
        assert response.status_code == 201

        response = client.put('/user/%s' % valid_user["cpf"], json=updated_user)
        assert response.status_code == 200
        assert b"User updated successfully" in response.data

        response = client.put('/user/%s' % invalid_user["cpf"], json=updated_user)
        assert response.status_code == 404
        assert b"User not found" in response.data
