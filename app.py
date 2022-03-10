# import os
# from flask import Flask
# from flask_migrate import Migrate
# import click
# from flask.cli import with_appcontext
# from flask_restx import Api
# from api.user_account.views import user_account_namespace

# from config import db,config

# from flask_migrate import Migrate
from api import create_app
# from config import db

# # ========================================================
# # Create App
# # ========================================================
# def create_app():
#     config_map = {
#             'development': config.DevelopmentConfig(),
#             'testing': config.TestingConfig(),
#             'production': config.ProductionConfig(),
#     }

#     config_obj = config_map['development']

#     app = Flask(__name__)
#     api = Api(app)

#     api.add_namespace(user_account_namespace, path='/user-account')

#     app.config.from_object(config_obj)
#     db.init_app(app)

#     return app


# ========================================================
# Run App
# ========================================================
app = create_app('development')

# migrate = Migrate(app, db)

def runserver():
    print("Server is runing")
    app.run(port=5050)


if __name__ == '__main__':
        runserver()