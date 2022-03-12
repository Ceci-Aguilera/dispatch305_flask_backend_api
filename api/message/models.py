from config import db
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import backref







class CurrentMessageStatus(Enum):
    VISTO='visto'
    NO_VISTO='no visto'





class Message(db.Model):
    __tablename__='messages'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    visto = db.Column(db.Boolean(), default=False)
    comment = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"<Message {self.email} - {self.phone} - {self.visto}>"


    def save(self):
        db.session.add(self)
        db.session.commit()