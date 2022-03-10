from email.policy import HTTP
from flask import request
from flask_restx import Resource,Namespace, fields
from http import HTTPStatus
from flask_jwt_extended import jwt_required

from .models import TrucksCargo

trucks_cargo_namespace=Namespace('trucks-cargo', description="A Namespace for managing truck cargo operations and searching")



cargo_model = trucks_cargo_namespace.model(
	"RequestCargo", {
		'id':fields.Integer(),
		'request_cargo_status': fields.String(description="Status of the request",
			required=True, enum=['SEARCHING', 'FOUND', 'CANCEL']
		)
	}
)




@trucks_cargo_namespace.route('/request-cargos/')
class RequestCargoGetCreate(Resource):


	@trucks_cargo_namespace.marshal_with(cargo_model)
	@jwt_required()
	def get(self):
		"""
			Get all Request-Cargos
		"""
		trucks_cargos = TrucksCargo.query.all()

		return trucks_cargos, HTTPStatus.OK

	@trucks_cargo_namespace.expect(cargo_model)
	@jwt_required()
	def post(self):
		"""
			Create new Request-Cargo
		"""
		data = trucks_cargo_namespace.payload

		# current_user = 

		return data, HTTPStatus.CREATED