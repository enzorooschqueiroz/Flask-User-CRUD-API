import os
from dotenv import load_dotenv

load_dotenv()


class DevConfig:

    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_DB'),
        'host': os.getenv('MONGODB_HOST'),
        'username': os.getenv('MONGODB_USERNAME'),
        'password': os.getenv('MONGODB_PASSWORD')
    }

class ProdConfig:
    
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_KEY')
    }


class MockConfig:
    
    MONGODB_SETTINGS = {
        'db': 'users',
        'host': 'mongomock://localhost'
    }

