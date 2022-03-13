from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.actions import action
from flask import render_template, flash
from wtforms.fields import PasswordField

from api.user_account.models import User
from api.trucks_cargo.models import TrucksCargo, RequestStatus
from api.message.models import Message


from flask_security import current_user, login_required, RoleMixin, Security, SQLAlchemyUserDatastore, UserMixin, utils

class UserView(ModelView):
    
    @action('sendbillinginfo', 'Send Bill', 'Are you sure you want to send bill?')
    def action_sendbillinginfo(self, ids):
        count = 0
        for _id in ids:
            count += 1
        flash("Bill sent to {0} client(s)".format(count))

    column_select_related_list = ('trucks_cargos',)
    column_searchable_list = ['company_name', 'contact_name', 'email', 'phone']
    column_exclude_list = ['password_hash', 'is_staff', 'is_admin', ]
    column_filters = ['is_active', 'pending_bill']

    form_excluded_columns = ['password_hash', 'is_staff', 'is_admin', 'trucks_cargos']

    

class TruckCargoView(ModelView):
    column_searchable_list = [User.contact_name, User.phone, User.company_name, User.email]
    column_exclude_list = ['date_founded', ]
    column_filters = ['request_cargo_status']

    form_excluded_columns = ['date_founded']



class MessageView(ModelView):
    column_searchable_list = ['name', 'email', 'phone']
    column_exclude_list = ['comment',  ]
    column_filters = ['visto']



class UserAdminView(ModelView):

    column_exclude_list = ('password', 'confirmed_at', )
    form_excluded_columns = ('password', 'confirmed_at',)
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password2 =  PasswordField('New Password')
        return form_class

    def on_model_change(self, form, model, is_created):

        if len(model.password2):
            model.password = utils.encrypt_password(model.password2)



class RoleAdminView(ModelView):

    def is_accessible(self):
        return current_user.has_role('admin')

    def __hash__(self):
        return hash(self.name)




class AdminView(AdminIndexView):

    def is_accessible(self):
        print(current_user)
        print(current_user.roles)
        return current_user.has_role('admin') or current_user.has_role('staff')

    @expose('/')
    def index(self):
        inactive_users = User.query.filter_by(is_active=False).count()
        seraching_cargos = TrucksCargo.query.filter_by(request_cargo_status=RequestStatus.SEARCHING).count()
        print(seraching_cargos)
        unread_messages = Message.query.filter_by(visto=False).count()
        return self.render("admin/custom_index.html", inactive_users=inactive_users, seraching_cargos=seraching_cargos, unread_messages=unread_messages)