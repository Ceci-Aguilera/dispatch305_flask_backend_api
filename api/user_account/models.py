from config import db

from enum import Enum

from api.admin.models import Role, roles_users

# ===========================================
#  HELPERS
# ===========================================
class CurrentPlanStatus(Enum):
    BASICO='basico'
    VIP='vip'


class User(db.Model):

    __tablename__='users'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    company_name = db.Column(db.String(50), nullable=True)
    contact_name = db.Column(db.String(50), nullable=True)
    password_hash = db.Column(db.Text(), nullable=False)
    phone = db.Column(db.String(50), nullable=True)

    pending_bill = db.Column(db.Float(), default=0.0)

    current_plan = db.Column(db.Enum(CurrentPlanStatus), default=CurrentPlanStatus.BASICO)
    

    is_active = db.Column(db.Boolean(), default=False)

    dispatcher = db.Column(db.Integer(), db.ForeignKey("useradmin.id"))

    trucks_cargos = db.relationship("TrucksCargo", backref='driver', lazy=True)

    last_token_password = db.Column(db.String(256), nullable=True, default='-1')


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()


    def __str__(self):
        return str(self.id) + " - " + str(self.email)

    def __repr__(self):
        return f"<User {self.email} - {self.company_name}>"
