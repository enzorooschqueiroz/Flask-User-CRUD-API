from flask_mongoengine import MongoEngine

db = MongoEngine()


def _init_db(app):
    db.init_app(app)
