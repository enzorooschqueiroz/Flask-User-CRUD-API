import os


class DevConfig:

    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_DB'),
        'host': os.getenv('MONGODB_HOST'),
        'username': os.getenv('MONGODB_USERNAME'),
        'password': os.getenv('MONGODB_PASSWORD')
    }

class ProdConfig:
    
    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://admin:mJSMWoEYU4DDxAE@manageusers.sxnyu.mongodb.net/users?retryWrites=true&w=majority&appName=ManageUsers'
    }


class MockConfig:
    
    MONGODB_SETTINGS = {
        'db': 'users',
        'host': 'mongomock://localhost'
    }

