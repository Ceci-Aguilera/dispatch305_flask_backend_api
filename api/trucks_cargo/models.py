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

class USAState(Enum):
    FL='FL'
    CA='CA'




class TrucksCargo(db.Model):

    __tablename__='truckscargos'

    id = db.Column(db.Integer(), primary_key=True)
    request_cargo_status = db.Column(db.Enum(RequestStatus), default=RequestStatus.SEARCHING)
    pricing = db.Column(db.Float(), default=0.0)
    miles = db.Column(db.Float(), default=0.0)
    weight = db.Column(db.Float(), default=0.0)
    state_from = db.Column(db.Enum(USAState), default=USAState.FL)
    city_from = db.Column(db.String(50), nullable=True)
    state_to = db.Column(db.Enum(USAState), default=USAState.FL)
    city_to = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    date_founded = db.Column(db.DateTime(), default=datetime.utcnow)
    date_pick_up = db.Column(db.DateTime(), default=datetime.utcnow)
    date_delivery = db.Column(db.DateTime(), default=datetime.utcnow)
    user = db.Column(db.Integer(), db.ForeignKey("users.id"))
    dispatcher = db.Column(db.Integer(), db.ForeignKey("useradmin.id"))
    broker = db.Column(db.Integer(), db.ForeignKey("brokers.id"))

    def __str__(self):
        return str(self.id) + " - " + str(self.request_cargo_status)
    
    def __repr__(self):
        return f"<RequestCargo {self.id} - {self.request_cargo_status}>"




class Broker(db.Model):

    __tablename__='brokers'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    trucks_cargos = db.relationship("TrucksCargo", backref='broker_user', lazy=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.name)

    def __repr__(self):
        return f"<Broker {self.id} - {self.name}>"