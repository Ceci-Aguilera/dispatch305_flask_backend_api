import os
from http import HTTPStatus
from datetime import datetime
from datetime import timedelta
from datetime import timezone


from flask import request, redirect, make_response, send_from_directory
from flask_restx import Resource,Namespace, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
	create_access_token,
	create_refresh_token,
	jwt_required,
	get_jwt_identity,
	get_jwt
)

from werkzeug.utils import secure_filename


import flask_mail

import os
from threading import Thread
from time import sleep

import secrets
import base64


from .models import User
from flask import current_app, render_template
from config import db



user_account_namespace=Namespace('user-account', description="A Namespace for user account management")

signup_model = user_account_namespace.model(
	"User", {
		'company_name': fields.String(required=True, description="A company name"),
		'contact_name': fields.String(required=True, description="A contact name"),
		'email': fields.String(required=True, description="An email"),
		'phone': fields.String(required=True, description="An phone"),
		'password': fields.String(required=True, description="A password"),
		'current_plan': fields.String(description="A current plan",
			required=True, enum=['BASICO', 'VIP']
		)
	}
)

login_model = user_account_namespace.model(
	"Login", {
		'email': fields.String(required=True, description="An email"),
		'password': fields.String(required=True, description="A password"),
	}
)

user_info_model = user_account_namespace.model(
	"User", {
		'company_name': fields.String(required=True, description="A company name"),
		'contact_name': fields.String(required=True, description="A contact name"),
		'email': fields.String(required=True, description="An email"),
		'phone': fields.String(required=True, description="An phone"),
		'pending_bill':fields.Float(required=True, description="A pending bill"),
		'current_plan': fields.String(description="A current plan",
			required=True, enum=['BASICO', 'VIP']
		)
	}
)





@user_account_namespace.route('/signup')
class SignUp(Resource):


	@user_account_namespace.expect(signup_model)
	@user_account_namespace.marshal_with(signup_model)
	def post(self):
		"""
			SIGN UP a New User
		"""
		print(User.query.all())

		data = user_account_namespace.payload

		try:
			new_user = User(
				email=data.get('email'),
				company_name=data.get('company_name'),
				contact_name=data.get('contact_name'),
				phone=data.get('phone'),
				password_hash=generate_password_hash('default123!'),
				current_plan=data.get('current_plan')
			)
			
			new_user.save()



			return "Success", HTTPStatus.CREATED
			
		except:
			return "Error", HTTPStatus.BAD_REQUEST

@user_account_namespace.route('/login')
class LogIn(Resource):

	
	@user_account_namespace.expect(login_model)
	def post(self):
		"""
			LOGIN And Generate JWT
		"""
		data = request.get_json()

		email = data.get('email')
		password = data.get('password')

		user = User.query.filter_by(email=email).first()

		if user is not None and check_password_hash(user.password_hash, password):
			
			access_token = create_access_token(identity=user.email)
			refresh_token = create_refresh_token(identity=user.email)

			response = {
				'access_token': access_token,
				'refresh_token': refresh_token
			}

			return response, HTTPStatus.OK


@user_account_namespace.route('/refresh-token')
class RefreshToken(Resource):

	
	@jwt_required(refresh=True)
	def post(self):
		"""
			Refresh JWT Token
		"""

		email = get_jwt_identity()

		access_token = create_access_token(identity=email)

		return {"access_token": access_token}, HTTPStatus.OK


@user_account_namespace.route('/upload-documents/<email>')
class UploadNewDocuments(Resource):

	def post (self, email):
		"""
			Upload Documents for New User Account
		"""

		try:

			user = User.query.filter_by(email=email).first()

			# Create or find folder for user
			target = os.path.join(current_app.config['UPLOAD_FOLDER'], '{}'.format(email))
			if not os.path.isdir(target):
				os.mkdir(target)

			print("Path For User Created")

			documents_upload = request.files.getlist("documents")
			for doc_upload in documents_upload:
				filename = doc_upload.filename
				destination = "/".join([target, filename])
				doc_upload.save(destination)

			print("All Files Saved")

			return "Success", HTTPStatus.OK

		except:
			return "Error", HTTPStatus.BAD_REQUEST






@user_account_namespace.route('/check-auth')
class CheckAuth(Resource):

	
	@jwt_required(refresh=False)
	@user_account_namespace.marshal_with(user_info_model)
	def get(self):
		"""
			Check if User is Logged in and send data of User
		"""

		try:
			email = get_jwt_identity()
			user = User.query.filter_by(email=email).first()

			return user, HTTPStatus.OK

		except:
			return "Error", HTTPStatus.BAD_REQUEST




@user_account_namespace.route('/edit-info')
class EditInfo(Resource):

	
	@jwt_required(refresh=False)
	@user_account_namespace.marshal_with(user_info_model)
	def post(self):
		"""
			Edit info in User Account
		"""

		try:
			email = get_jwt_identity()
			user = User.query.filter_by(email=email).first()

			data = request.get_json()
			user.contact_name = data.get("contact_name");
			user.company_name = data.get("company_name");
			user.phone = data.get("phone")
			user.update()

			return user, HTTPStatus.OK

		except:
			return "Error", HTTPStatus.BAD_REQUEST


@user_account_namespace.route('/pdf-viewer/<email>/<document_name>')
class PDFViewer(Resource):
	def get(self, email, document_name):
		"""
			View Document PDF
		"""
		try:
			workingdir = os.path.abspath(os.getcwd())
			filepath = workingdir + '/uploads/' + '{}'.format(email) + '/'
			return send_from_directory(filepath, '{}'.format(document_name) + '-' + '{}'.format(email)+'.pdf')
		except:
			return "No such PDF", HTTPStatus.BAD_REQUEST




@user_account_namespace.route('/update-document/<email>/<document_name>')
class UpdateDocument(Resource):

	def post (self, email, document_name):
		"""
			Change Uploaded documents for account
		"""

		# try:
		if True:

			user = User.query.filter_by(email=email).first()

			# Create or find folder for user
			target = os.path.join(current_app.config['UPLOAD_FOLDER'], '{}'.format(email))
			if not os.path.isdir(target):
				os.mkdir(target)


			documents_upload = request.files["document"]
			filename = documents_upload.filename
			destination = "/".join([target, filename])
			try:
				os.remove(destination)
			except:
				pass
			documents_upload.save(destination)


			return "Success", HTTPStatus.OK

		# except:
		else:
			return "Error", HTTPStatus.BAD_REQUEST




@user_account_namespace.route('/reset-password')
class ResetPassword(Resource):

	
	@jwt_required(refresh=False)
	@user_account_namespace.marshal_with(user_info_model)
	def post(self):
		"""
			Reset password in User Account
		"""

		try:
			email = get_jwt_identity()
			user = User.query.filter_by(email=email).first()

			data = request.get_json()
			password = data.get('password')
			re_password = data.get("re_password")

			if password != re_password:
				return "Error", HTTPStatus.BAD_REQUEST

			user.password_hash = generate_password_hash(password)

			user.update()

			return user, HTTPStatus.OK

		except:
			return "Error", HTTPStatus.BAD_REQUEST


@user_account_namespace.route('/pdf-browser-viewer/<email>/<document_name>')
class PDFBrowserViewer(Resource):
	def get(self, email, document_name):
		"""
			View Document PDF
		"""
		try:
			workingdir = os.path.abspath(os.getcwd())
			filepath = workingdir + '/uploads/' + '{}'.format(email) + '/'
			return send_from_directory(filepath, '{}'.format(document_name) + '-' + '{}'.format(email)+'.pdf')
		except:
			return "No such PDF", HTTPStatus.BAD_REQUEST







def send_async_email(app, msg):
    from api import mail
    with app.app_context():
        for i in range(5, -1, -1):
            sleep(2)
            print('time:', i)
        from api import mail
        mail.send(msg)




@user_account_namespace.route('/send-request-reset-password')
class SendRequestResetPassword(Resource):

	def post(self):
		
		app = current_app._get_current_object()

		data = request.get_json()

		# try:
		if True:
			user = User.query.filter_by(email=data.get('email')).first()
			email_in_bytes = bytes(user.email, 'utf-8')
			last_uid_password = base64.urlsafe_b64encode(email_in_bytes)
			last_uid_password = last_uid_password.decode('UTF-8')
			user.last_token_password = secrets.token_hex(16)
			user.update()

			msg = flask_mail.Message('Reset Password Requested', sender=current_app.config['MAIL_USERNAME'], recipients=[
                             user.email])

			msg.msId = msg.msgId.split('@')[0] + '@' + current_app.config["MAIL_STRING_ID"]

			msg.html = render_template("user-account/send-request-reset-password.html",uid=last_uid_password, token=user.last_token_password)

			thr = Thread(target=send_async_email, args=[app, msg])
			thr.start()
			return "Success", HTTPStatus.OK
		# except:
		else:
			return "Error", HTTPStatus.BAD_REQUEST



@user_account_namespace.route('/reset-password/<uid>/<token>')
class ResetPassword(Resource):

	def post(self, uid, token):
		
		app = current_app._get_current_object()

		data = request.get_json()

		password = data.get('password')
		re_password = data.get('re_password')

		if(password != re_password):
			return "Error", HTTPStatus.BAD_REQUEST

		# try:
		if True:
			email_in_bytes = bytes(uid, 'utf-8')
			last_uid_password = base64.urlsafe_b64decode(email_in_bytes)
			email = last_uid_password.decode('UTF-8')

			print(email)

			user = User.query.filter_by(email=email, last_token_password=token).first()

			user.last_token_password = "-1"
			user.password_hash = generate_password_hash(password)
			user.update()

			return "Success", HTTPStatus.OK
		# except:
		else:
			return "Error", HTTPStatus.BAD_REQUEST