from config import db
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import backref

# ===========================================
#  HELPERS
# ===========================================
class RequestStatus(Enum):
    SEARCHING='searching'
    FOUND='found'
    CANCEL='cancel'




class TrucksCargo(db.Model):

    __tablename__='requestcargos'

    id = db.Column(db.Integer(), primary_key=True)
    request_cargo_status = db.Column(db.Enum(RequestStatus), default=RequestStatus.SEARCHING)
    pricing = db.Column(db.Float(), primary_key=True)
    state_from = db.Column(db.String(50), nullable=False)
    state_to = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    date_founded = db.Column(db.DateTime(), default=datetime.utcnow)
    user = db.Column(db.Integer(), db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<RequestCargo {self.id} - {self.request_cargo_status}>"