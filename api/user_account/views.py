import os
from http import HTTPStatus


from flask import request
from flask_restx import Resource,Namespace, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
	create_access_token,
	create_refresh_token,
	jwt_required,
	get_jwt_identity
)

from werkzeug.utils import secure_filename



from .models import User
from flask import current_app



user_account_namespace=Namespace('user-account', description="A Namespace for user account management")

signup_model = user_account_namespace.model(
	"User", {
		'company_name': fields.String(required=True, description="A company name"),
		'contact_name': fields.String(required=True, description="A contact name"),
		'email': fields.String(required=True, description="An email"),
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

