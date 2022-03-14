from flask_admin.contrib.sqla import ModelView, fields
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.actions import action
from flask_admin.form import Select2Widget
from flask import render_template, flash, Markup
from wtforms.fields import PasswordField

from api.user_account.models import User
from api.trucks_cargo.models import TrucksCargo, RequestStatus, Broker
from api.message.models import Message
from .models import UserAdmin


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



    def _authority_letter_formatter(view, context, model, name):
        if model.email:
           markupstring = "<a href='/user-account/pdf-browser-viewer/%s/authority_letter' target='_blank'>Authority Letter.pdf</a>" % (model.email)
           return Markup(markupstring)
        else:
           return ""

    def _w9_formatter(view, context, model, name):
        if model.email:
           markupstring = "<a href='/user-account/pdf-browser-viewer/%s/w9' target='_blank'>W9.pdf</a>" % (model.email)
           return Markup(markupstring)
        else:
           return ""

    def _insurance_formatter(view, context, model, name):
        if model.email:
           markupstring = "<a href='/user-account/pdf-browser-viewer/%s/insurance' target='_blank'>Insurance.pdf</a>" % (model.email)
           return Markup(markupstring)
        else:
           return ""

    def _noa_formatter(view, context, model, name):
        if model.email:
           markupstring = "<a href='/user-account/pdf-browser-viewer/%s/noa' target='_blank'>NOA.pdf</a>" % (model.email)
           return Markup(markupstring)
        else:
           return ""

    column_formatters = {
        'authority_letter': _authority_letter_formatter,
        'w9': _w9_formatter,
        'insurance': _insurance_formatter,
        'noa': _noa_formatter
    }



    column_list=('email', 'contact_name', 'company_name', 'phone', 'pending_bill', 'is_active', 'current_plan', 'authority_letter', 'w9', 'insurance', 'noa')

    form_excluded_columns = ['password_hash', 'is_staff', 'is_admin', 'trucks_cargos']


    def get_query(self):
        if current_user.has_role('admin'):
            return super(UserView, self).get_query()
        else:
            return super(UserView, self).get_query().filter(
                User.dispatcher == current_user.id
            )

    def get_count_query(self):
        if current_user.has_role('admin'):
            super(UserView, self).get_count_query()
        else:
            return super(UserView, self).get_count_query().filter(
                User.dispatcher == current_user.id
            )

    

class TruckCargoView(ModelView):
    column_searchable_list = [User.contact_name, User.phone, User.company_name, User.email, Broker.name, ]
    column_exclude_list = ['date_founded', ]
    column_filters = ['request_cargo_status']

    form_excluded_columns = ['date_created', ]

    def get_query(self):
        if current_user.has_role('admin'):
            return super(TruckCargoView, self).get_query()
        else:
            return super(TruckCargoView, self).get_query().filter(
                TrucksCargo.dispatcher == current_user.id
            )

    def get_count_query(self):
        if current_user.has_role('admin'):
            super(TruckCargoView, self).get_count_query()
        else:
            return super(TruckCargoView, self).get_count_query().filter(
                TrucksCargo.dispatcher == current_user.id
            )

    form_extra_fields = {
        'driver': fields.QuerySelectField(
            label='Driver',
            query_factory=lambda: User.query.filter_by(dispatcher=current_user.id) if current_user.has_role('staff')  else User.query.all(),
            widget=Select2Widget()
        ),
        'user_dispatcher': fields.QuerySelectField(
            label='Dispatcher',
            query_factory=lambda: UserAdmin.query.filter_by(id=current_user.id) if current_user.has_role('staff')  else UserAdmin.query.all(),
            widget=Select2Widget()
        ),
    }



class BrokerView(ModelView):
    column_searchable_list = ['name', ]
    column_filters = ['name', ]
    column_exclude_list = ['trucks_cargos',  ]

    form_excluded_columns = ['trucks_cargos', ]




class MessageView(ModelView):

    def is_accessible(self):
        return current_user.has_role('admin')

    column_searchable_list = ['name', 'email', 'phone']
    column_exclude_list = ['comment',  ]
    column_filters = ['visto']



class UserAdminView(ModelView):

    column_exclude_list = ('password', 'confirmed_at',)
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
        return current_user.has_role('admin') or current_user.has_role('staff')

    @expose('/')
    def index(self):
        inactive_users = User.query.filter_by(is_active=False).count() if current_user.has_role('admin') else 0
        seraching_cargos = TrucksCargo.query.filter_by(request_cargo_status=RequestStatus.SEARCHING).count() if current_user.has_role('admin') else TrucksCargo.query.filter_by(request_cargo_status=RequestStatus.SEARCHING, dispatcher = current_user.id).count()
        unread_messages = Message.query.filter_by(visto=False).count() if current_user.has_role('admin') else 0
        return self.render("admin/custom_index.html", inactive_users=inactive_users, seraching_cargos=seraching_cargos, unread_messages=unread_messages)