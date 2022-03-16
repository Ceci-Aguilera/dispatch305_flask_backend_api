import os
from flask import Flask, redirect
from flask_migrate import Migrate
import click
from flask.cli import with_appcontext
from flask_restx import Api
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from flask_security import current_user, login_required, RoleMixin, Security, SQLAlchemyUserDatastore, UserMixin


from flask_mail import Mail

from .user_account.views import user_account_namespace
from .trucks_cargo.views import trucks_cargo_namespace
from .message.views import message_namespace
# from .admin.views import admin_blueprint
from .admin.views import UserView, TruckCargoView, MessageView, AdminView, UserAdminView, RoleAdminView, BrokerView, staff_namespace

from .user_account.models import User
from .trucks_cargo.models import TrucksCargo, Broker
from .message.models import Message
from .admin.models import UserAdmin, Role

from config import db,config


mail = Mail()

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

    app = Flask(__name__, template_folder='./templates', static_folder='./static')
    CORS(app)
    app.config.from_object(config_obj)

    user_datastore = SQLAlchemyUserDatastore(db, UserAdmin, Role)
    security = Security(app, user_datastore)
    
    db.init_app(app)
    migrate = Migrate(app, db)

    jwt = JWTManager(app)


    api = Api(app)

    api.add_namespace(user_account_namespace, path='/user-account')
    api.add_namespace(trucks_cargo_namespace, path='/trucks-cargo')
    api.add_namespace(message_namespace, path='/message')

    admin = Admin(app, index_view=AdminView())
    admin.add_view(UserView(User, db.session))
    admin.add_view(TruckCargoView(TrucksCargo, db.session))
    admin.add_view(BrokerView(Broker, db.session))
    admin.add_view(MessageView(Message, db.session))
    admin.add_view(UserAdminView(UserAdmin, db.session))
    admin.add_view(RoleAdminView(Role, db.session))

    app.register_blueprint(staff_namespace)

    mail.init_app(app)

    # app.register_blueprint(admin_blueprint, url_prefix="/admin-panel")

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User,
            "TrucksCargo": TrucksCargo,
            "Message": Message,
            'UserAdmin': UserAdmin,
            'Role': Role,
            'Broker': Broker
        }

    # Only needed on first execution to create first user
    @app.before_first_request
    def create_user():

        # user=user_datastore.find_user(email="aguilera.cecilia@outlook.com")
        # user_datastore.delete_user(user)
        # db.session.commit()


        if not user_datastore.find_user(email=config_obj.ADMIN_EMAIL_CREDIENTIAL):
            db.create_all()
            user_datastore.find_or_create_role(name='admin', description='Administrator')
            db.session.commit()
            user_datastore.create_user(email=config_obj.ADMIN_EMAIL_CREDIENTIAL, password=config_obj.ADMIN_PASSWORD_CREDENTIAL, roles=['admin'])
            db.session.commit()
            
        else:
            # user_datastore.create_user(email="someEmail@gmail.com", password="defualt123", roles=['staff'])
            # db.session.commit()
            pass

        

    @app.route('/login')
    @login_required
    def login():
        return redirect('/admin')

    return app

    