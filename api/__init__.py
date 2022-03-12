import os
from flask import Flask
from flask_migrate import Migrate
import click
from flask.cli import with_appcontext
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .user_account.views import user_account_namespace
from .trucks_cargo.views import trucks_cargo_namespace
from .message.views import message_namespace

from .user_account.models import User
from .trucks_cargo.models import TrucksCargo
from .message.models import Message

from config import db,config


# ========================================================
# Create App
# ========================================================
def create_app(config_env='development'):
    config_map = {
            'development': config.DevelopmentConfig(),
            'testing': config.TestingConfig(),
            'production': config.ProductionConfig(),
    }

    config_obj = config_map[config_env]

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_obj)
    
    db.init_app(app)
    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    api = Api(app)

    api.add_namespace(user_account_namespace, path='/user-account')
    api.add_namespace(trucks_cargo_namespace, path='/trucks-cargo')
    api.add_namespace(message_namespace, path='/message')

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User,
            "TrucksCargo": TrucksCargo,
            "Message": Message,
        }

    return app