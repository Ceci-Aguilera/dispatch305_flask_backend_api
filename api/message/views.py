import os
from http import HTTPStatus
from datetime import datetime
from datetime import timedelta
from datetime import timezone


from flask import request, redirect, make_response, send_from_directory
from flask_restx import Resource,Namespace, fields

from werkzeug.utils import secure_filename



from .models import Message
from flask import current_app, render_template
from config import db

message_namespace=Namespace('message', description="A Namespace for messages")

message_comment = message_namespace.model(
    "Message", {
        'visto': fields.Boolean(required=True, description="A visto status"),
        'name': fields.String(required=True, description="A name"),
        'phone': fields.String(required=True, description="A phone"),
        'email': fields.String(required=True, description="An email"),
        'comment': fields.String(required=True, description="A comment"),
    }
)


@message_namespace.route('/create-comment')
class CreateComment(Resource):


    @message_namespace.expect(message_comment)
    @message_namespace.marshal_with(message_comment)
    def post(self):
        """
            Add New Message
        """
        print(Message.query.all())

        data = message_namespace.payload

        if True:
            new_message = Message(
                visto=False,
                name=data.get('name'),
                phone=data.get('phone'),
                email=data.get('email'),
                comment=data.get('comment')
            )
            
            new_message.save()
            
            return "Success", HTTPStatus.CREATED
            
        else:
            return "Error", HTTPStatus.BAD_REQUEST