
from asyncore import dispatcher
from datetime import date, timedelta
import decimal
from email.policy import default
from http import HTTPStatus
from http.client import HTTPResponse
from operator import and_
import os
from threading import Thread
from time import sleep

from flask_admin.contrib.sqla import ModelView, fields
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.actions import action
from flask_admin.form import Select2Widget
from flask import render_template, flash, Markup, Blueprint, send_from_directory, request, current_app
from wtforms.fields import PasswordField, BooleanField

import flask_mail


from api.user_account.models import User, CurrentPlanStatus
from api.trucks_cargo.models import TrucksCargo, RequestStatus, Broker
from api.message.models import Message
from .models import UserAdmin


from flask_security import current_user, login_required, RoleMixin, Security, SQLAlchemyUserDatastore, UserMixin, utils


staff_namespace = Blueprint(
    'staff', __name__, template_folder='templates', url_prefix='/staff')


class UserView(ModelView):

    def is_accessible(self):
        return current_user.has_role('admin')

    @action('sendbillinginfo', 'Send Bill', 'Are you sure you want to send bill?')
    def action_sendbillinginfo(self, ids):
        count = 0
        for _id in ids:
            send_email_driver(_id)
            count += 1
        flash("Bill sent to {0} client(s)".format(count))

    column_select_related_list = ('trucks_cargos',)
    column_searchable_list = ['company_name', 'contact_name', 'email', 'phone']
    column_exclude_list = ['password_hash', 'is_staff', 'is_admin', ]
    column_filters = ['is_active', 'pending_bill']

    def _authority_letter_formatter(view, context, model, name):
        if model.email:
            markupstring = "<a href='/user-account/pdf-browser-viewer/%s/authority_letter' target='_blank'>Authority Letter.pdf</a>" % (
                model.email)
            return Markup(markupstring)
        else:
            return ""

    def _w9_formatter(view, context, model, name):
        if model.email:
            markupstring = "<a href='/user-account/pdf-browser-viewer/%s/w9' target='_blank'>W9.pdf</a>" % (
                model.email)
            return Markup(markupstring)
        else:
            return ""

    def _insurance_formatter(view, context, model, name):
        if model.email:
            markupstring = "<a href='/user-account/pdf-browser-viewer/%s/insurance' target='_blank'>Insurance.pdf</a>" % (
                model.email)
            return Markup(markupstring)
        else:
            return ""

    def _noa_formatter(view, context, model, name):
        if model.email:
            markupstring = "<a href='/user-account/pdf-browser-viewer/%s/noa' target='_blank'>NOA.pdf</a>" % (
                model.email)
            return Markup(markupstring)
        else:
            return ""

    column_formatters = {
        'authority_letter': _authority_letter_formatter,
        'w9': _w9_formatter,
        'insurance': _insurance_formatter,
        'noa': _noa_formatter
    }

    column_list = ('email', 'contact_name', 'company_name', 'phone', 'pending_bill',
                   'is_active', 'current_plan', 'authority_letter', 'w9', 'insurance', 'noa')

    form_excluded_columns = ['password_hash',
                             'is_staff', 'is_admin', 'trucks_cargos']

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

    action_disallowed_list = ['delete']












class TruckCargoAdminView(ModelView):

    def is_accessible(self):
        return current_user.has_role('admin')

    column_searchable_list = [
        User.contact_name, User.phone, User.company_name, User.email, Broker.name, ]
    column_exclude_list = ['date_founded', ]
    column_filters = ['request_cargo_status', 'is_charged']

    form_excluded_columns = ['total_owned', 'date_created', 'is_charged']

    def _documents_formatter(view, context, model, name):
        markupstring = "<a href='/staff/truck-cargos-documents/%s' target='_blank'>Rate and POD</a>" % (
            model.id)
        return Markup(markupstring)

    column_formatters = {
        'documents': _documents_formatter
    }

    # column_list = ('pricing', 'miles', 'weight', 'state_from', 'city_from', 'state_to', 'city_to',
    #                'date_created', 'date_pick_up', 'date_delivery', 'is_charged', 'user_dispatcher', 'driver', 'broker_user', 'documents')

    column_list = ('driver', 'city_from', 'state_from', 'city_to', 'state_to', 'date_pick_up', 'date_delivery', 'miles', 'weight', 'pricing', 'broker_user', 'documents', 'user_dispatcher')

    column_labels = dict(driver='Driver', city_from='Origen', state_from="ST", city_to='Destino', state_to="ST", date_pick_up="Pick UP", date_delivery="Delivery", miles="Miles", weight='Weight', pricing="Price", broker_user="Broker", documents="Documents", user_dispatcher = "Dispatcher")



    form_extra_fields = {
        'driver': fields.QuerySelectField(
            label='Driver',
            query_factory=lambda: User.query.all(),
            widget=Select2Widget()
        ),
        'user_dispatcher': fields.QuerySelectField(
            label='Dispatcher',
            query_factory=lambda: UserAdmin.query.all(),
            widget=Select2Widget()
        ),
    }

    def scaffold_form(self):
        form_class = super(TruckCargoAdminView, self).scaffold_form()
        form_class.charged = BooleanField(default=True)
        return form_class

    def on_model_change(self, form, model, is_created):
        if model.charged == True and model.is_charged == False:
            user = User.query.filter_by(id=model.user).first()
            plan_percent = 0.06 if user.current_plan == CurrentPlanStatus.VIP else 0.04
            plan_admin_percent = 0.02 if user.current_plan == CurrentPlanStatus.VIP else 0.01
            user.pending_bill = decimal.Decimal(user.pending_bill) + decimal.Decimal(
                model.pricing) * decimal.Decimal(plan_percent)
            user.update()
            dispatcher = UserAdmin.query.filter_by(id=model.dispatcher).first()
            dispatcher.amount_owned_to_admin = decimal.Decimal(dispatcher.amount_owned_to_admin) + decimal.Decimal(
                model.pricing) * decimal.Decimal(plan_admin_percent)
            dispatcher.update()
            model.is_charged = True
            model.total_owned = decimal.Decimal(
                model.pricing) * decimal.Decimal(plan_percent)

    def create_model(self, form):
        created_model = super(TruckCargoAdminView, self).create_model(form)
        if created_model.charged == True and created_model.is_charged == False:
            user = User.query.filter_by(id=created_model.user).first()
            plan_percent = 0.06 if user.current_plan == CurrentPlanStatus.VIP else 0.04
            plan_admin_percent = 0.02 if user.current_plan == CurrentPlanStatus.VIP else 0.01
            user.pending_bill = decimal.Decimal(user.pending_bill) + decimal.Decimal(
                created_model.pricing) * decimal.Decimal(plan_percent)
            user.update()
            dispatcher = UserAdmin.query.filter_by(
                id=created_model.dispatcher).first()
            dispatcher.amount_owned_to_admin = decimal.Decimal(dispatcher.amount_owned_to_admin) + decimal.Decimal(
                created_model.pricing) * decimal.Decimal(plan_admin_percent)
            dispatcher.update()
            created_model.is_charged = True
            created_model.total_owned = decimal.Decimal(
                created_model.pricing) * decimal.Decimal(plan_percent)
            created_model.save()
        return created_model


















class TruckCargoView(ModelView):

    def is_accessible(self):
        return current_user.has_role('staff') and current_user.active == True

    column_searchable_list = [
        User.contact_name, User.phone, User.company_name, User.email, Broker.name, ]
    column_exclude_list = ['date_founded', ]
    column_filters = ['request_cargo_status', 'is_charged']

    form_excluded_columns = ['total_owned', 'date_created', 'is_charged']

    def _documents_formatter(view, context, model, name):
        markupstring = "<a href='/staff/truck-cargos-documents/%s' target='_blank'>Rate and POD</a>" % (
            model.id)
        return Markup(markupstring)

    column_formatters = {
        'documents': _documents_formatter
    }

    column_list = ('driver', 'city_from', 'state_from', 'city_to', 'state_to', 'date_pick_up', 'date_delivery', 'miles', 'weight', 'pricing', 'broker_user', 'documents')

    column_labels = dict(driver='Driver', city_from='Origen', state_from="ST", city_to='Destino', state_to="ST", date_pick_up="Pick UP", date_delivery="Delivery", miles="Millas", weight='Peso', pricing="Precio", broker_user="Broker", documents="Documents", user_dispatcher = "Dispatcher")

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
            query_factory=lambda: User.query.filter_by(
                dispatcher=current_user.id) if current_user.has_role('staff') else User.query.all(),
            widget=Select2Widget()
        )
    }

    def scaffold_form(self):
        form_class = super(TruckCargoView, self).scaffold_form()
        form_class.charged = BooleanField(default=True)
        return form_class

    def on_model_change(self, form, model, is_created):
        if model.charged == True and model.is_charged == False:
            user = User.query.filter_by(id=model.user).first()
            plan_percent = 0.06 if user.current_plan == CurrentPlanStatus.VIP else 0.04
            plan_admin_percent = 0.02 if user.current_plan == CurrentPlanStatus.VIP else 0.01
            user.pending_bill = decimal.Decimal(user.pending_bill) + decimal.Decimal(
                model.pricing) * decimal.Decimal(plan_percent)
            user.update()
            dispatcher = UserAdmin.query.filter_by(id=model.dispatcher).first()
            dispatcher.amount_owned_to_admin = decimal.Decimal(dispatcher.amount_owned_to_admin) + decimal.Decimal(
                model.pricing) * decimal.Decimal(plan_admin_percent)
            dispatcher.update()
            model.is_charged = True
            model.total_owned = decimal.Decimal(
                model.pricing) * decimal.Decimal(plan_percent)

    def create_model(self, form):
        created_model = super(TruckCargoView, self).create_model(form)
        if created_model.charged == True and created_model.is_charged == False:
            user = User.query.filter_by(id=created_model.user).first()
            plan_percent = 0.06 if user.current_plan == CurrentPlanStatus.VIP else 0.04
            plan_admin_percent = 0.02 if user.current_plan == CurrentPlanStatus.VIP else 0.01
            user.pending_bill = decimal.Decimal(user.pending_bill) + decimal.Decimal(
                created_model.pricing) * decimal.Decimal(plan_percent)
            user.update()
            dispatcher = UserAdmin.query.filter_by(
                id=created_model.dispatcher).first()
            dispatcher.amount_owned_to_admin = decimal.Decimal(dispatcher.amount_owned_to_admin) + decimal.Decimal(
                created_model.pricing) * decimal.Decimal(plan_admin_percent)
            dispatcher.update()
            created_model.is_charged = True
            created_model.total_owned = decimal.Decimal(
                created_model.pricing) * decimal.Decimal(plan_percent)
            created_model.save()
        return created_model






















class BrokerView(ModelView):
    column_searchable_list = ['name', ]
    column_filters = ['name', ]
    column_exclude_list = ['trucks_cargos', ]

    form_excluded_columns = ['trucks_cargos', ]











class MessageView(ModelView):

    def is_accessible(self):
        return current_user.has_role('admin')

    column_searchable_list = ['name', 'email', 'phone']
    column_exclude_list = ['comment', ]
    column_filters = ['visto']













class UserAdminView(ModelView):

    # @action('sendbillinginfo', 'Send Bill', 'Are you sure you want to send bill?')
    # def action_sendbillinginfo(self, ids):
    #     count = 0
    #     for _id in ids:
    #         send_email_staff(_id)
    #         count += 1
    #     flash("Bill sent to {0} dispatchers(s)".format(count))

    column_exclude_list = ('password', 'confirmed_at',)
    form_excluded_columns = ('password', 'confirmed_at',)
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        return form_class

    def on_model_change(self, form, model, is_created):

        if len(model.password2):
            model.password = utils.encrypt_password(model.password2)

    action_disallowed_list = ['delete']












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

        if current_user.has_role('admin'):
            inactive_users = User.query.filter_by(is_active=False).count()
            seraching_cargos = TrucksCargo.query.filter_by(
                request_cargo_status=RequestStatus.SEARCHING).count()
            unread_messages = Message.query.filter_by(visto=False).count()
            return self.render("admin/custom_admin_index.html", inactive_users=inactive_users, seraching_cargos=seraching_cargos, unread_messages=unread_messages)

        else:
            seraching_cargos = TrucksCargo.query.filter_by(
                request_cargo_status=RequestStatus.SEARCHING, dispatcher=current_user.id).count()

            users = User.query.filter_by(
                dispatcher=current_user.id, is_active=True)

            return self.render("admin/custom_staff_index.html", seraching_cargos=seraching_cargos, users=users)












@staff_namespace.route('/truck-cargos-documents/<id>', methods=['GET', 'POST'])
def truck_documents(id):
    if request.method == 'GET':
        return render_template("trucks_cargos/documents.html", id=id)

    elif request.method == 'POST':
        target = os.path.join(
            current_app.config['UPLOAD_FOLDER'], 'trucks-cargos')
        if not os.path.isdir(target):
            os.mkdir(target)

        print(request.files)

        if "rate-confirmation" in request.files:
            documents_upload = request.files["rate-confirmation"]
            filename = documents_upload.filename
            if filename != "":
                filename = "rate-confirmation-" + '{}'.format(id) + ".pdf"
                destination = "/".join([target, filename])
                try:
                    os.remove(destination)
                except:
                    pass
                documents_upload.save(destination)

        if "pod" in request.files:
            documents_upload = request.files["pod"]
            filename = documents_upload.filename
            if filename != "":
                filename = "pod-" + '{}'.format(id) + ".pdf"
                destination = "/".join([target, filename])
                try:
                    os.remove(destination)
                except:
                    pass
                documents_upload.save(destination)

            return render_template("trucks_cargos/documents.html", id=id)


@staff_namespace.route('/truck-cargos-documents/<id>/<document_name>')
def truck_browser_documents(id, document_name):
    try:
        workingdir = os.path.abspath(os.getcwd())
        filepath = workingdir + '/uploads/trucks-cargos/'
        return send_from_directory(filepath, '{}'.format(document_name) + '-' + '{}'.format(id)+'.pdf')
    except:
        return "No such PDF", HTTPStatus.BAD_REQUEST


@staff_namespace.route('/drivers/bill-document/<id>')
def driver_billing(id):
    """
        View the Email to send to Drivers with Weekly billing info
    """
    
    today = date.today()
    weekday = today.weekday()

    last_sat = today - timedelta(days=(4-weekday))
    # next_frid = today + timedelta(days=(4 - weekday))

    user = User.query.filter_by(id=id).first()
    try:
        trucks_cargos = TrucksCargo.query.filter_by(user=id).filter(
            TrucksCargo.date_founded >= last_sat).all()
    except:
        trucks_cargos = "None"
    # return "Success for user {id}"
    if user.current_plan == CurrentPlanStatus.BASICO:
        return render_template("driver/billing_email.html", user=user, trucks_cargos=trucks_cargos)
    else:
        return render_template("driver/analytics_email.html", user=user, trucks_cargos=trucks_cargos)


@staff_namespace.route('/bill-document/<id>')
def staff_billing(id):
    """
        View the Email to send to Staff members with Weekly billing info
    """

    today = date.today()
    weekday = today.weekday()

    last_sat = today - timedelta(days=(4-weekday))
    # next_frid = today + timedelta(days=(4 - weekday))

    dispatcher = UserAdmin.query.filter_by(id=id).first()
    try:
        trucks_cargos = TrucksCargo.query.filter_by(dispatcher=id).filter(
            TrucksCargo.date_founded >= last_sat).all()
    except:
        trucks_cargos = "None"
    # return "Success for user {id}"
    return render_template("staff/billing_email.html", dispatcher=dispatcher, trucks_cargos=trucks_cargos)





def send_async_email(app, msg):
    from api import mail
    with app.app_context():
        for i in range(5, -1, -1):
            sleep(2)
            print('time:', i)
        from api import mail
        mail.send(msg)

def send_email_driver(id):
    """
        Send the Email to send to Driver with Weekly billing info
    """

    app = current_app._get_current_object()

    today = date.today()
    weekday = today.weekday()

    last_sat = today - timedelta(days=(4-weekday))

    user = User.query.filter_by(id=id).first()
    try:
        trucks_cargos = TrucksCargo.query.filter_by(user=id).filter(
            TrucksCargo.date_founded >= last_sat).all()
    except:
        trucks_cargos = "None"
    

    if(user.current_plan == CurrentPlanStatus.BASICO):
        msg = flask_mail.Message('Billing Information', sender=current_app.config['MAIL_USERNAME'], recipients=[
                             'aguilera.cecilia@outlook.com'])
        msg.html = render_template("driver/billing_email.html", user=user, trucks_cargos=trucks_cargos)
    else:
        msg = flask_mail.Message('This Week Analytics', sender=current_app.config['MAIL_USERNAME'], recipients=[
                             user.email])
        msg.msId = msg.msgId.split('@')[0] + '@' + current_app.config["MAIL_STRING_ID"]
        msg.html = render_template("driver/analytics_email.html", user=user, trucks_cargos=trucks_cargos)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr



def send_email_staff(id):
    """
        Send the Email to send to Staff members with Weekly billing info
    """

    app = current_app._get_current_object()

    today = date.today()
    weekday = today.weekday()

    last_sat = today - timedelta(days=(4-weekday))

    dispatcher = UserAdmin.query.filter_by(id=id).first()
    try:
        trucks_cargos = TrucksCargo.query.filter_by(dispatcher=id).filter(
            TrucksCargo.date_founded >= last_sat).all()
    except:
        trucks_cargos = "None"
    from api import mail
    msg = flask_mail.Message('Billing Information', sender=current_app.config['MAIL_USERNAME'], recipients=[
                             dispatcher.email])
    msg.msId = msg.msgId.split('@')[0] + '@' + current_app.config["MAIL_STRING_ID"]
    msg.html = render_template("staff/billing_email.html", dispatcher=dispatcher, trucks_cargos=trucks_cargos)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr