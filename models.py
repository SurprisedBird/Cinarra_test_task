from config import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum


class StatusEnum(enum.Enum):
    NOT_ACCEPTED = 'not_accepted'
    IN_PROGRESS = 'in_progress'
    CANCELLED = 'cancelled'
    DONE = 'done'

class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Unicode(20))
    
    orders = relationship("Order")

    def json(self):
        return{'name': self.name}


class Driver(db.Model):
    __tablename__ = 'driver'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    car_number = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Unicode(20))
    
    orders = relationship("Order")

    
class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=True)
    price = db.Column(db.SmallInteger)
    status = db.Column(db.Enum(StatusEnum))

 
