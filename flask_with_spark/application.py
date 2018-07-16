import os
from flask import Flask
from flaskext.markdown import Markdown
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from flask_celery import Celery

db = MongoEngine()
mongo = PyMongo()
celery= Celery()

def create_app(**config_overrides):
    app = Flask("flask_spark")
    Bootstrap(app)
    Markdown(app)
    #Update settings from settings.py
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    #If other settings came it update that settings.
    app.config.update(config_overrides)


    db.init_app(app)
    mongo.init_app(app)
    celery.init_app(app)


    from user.views import user_app
    from shopping.views import shopping_app
    app.register_blueprint(user_app)
    app.register_blueprint(shopping_app)

    return app
