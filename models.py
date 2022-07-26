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

    @staticmethod
    def search_client(_name):
        query = Client.query.filter_by(name=_name).first()
        return query

    @staticmethod
    def add_client(_name, _phone_number):
        client = Client(name=_name, phone_number=_phone_number)
        db.session.add(client)
        db.session.commit()

        return client

    @staticmethod
    def delete_client(_id):
        is_successful = Client.query.filter_by(id=_id).delete()
        db.session.commit()
        return bool(is_successful)


class Driver(db.Model):
    __tablename__ = 'driver'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    car_number = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Unicode(20))
    
    orders = relationship("Order")

    @staticmethod
    def add_driver(_name,_car_number, _phone_number):
        driver = Driver(name=_name, car_number=_car_number, phone_number=_phone_number)
        db.session.add(driver)
        db.session.commit()

        return driver

    @staticmethod
    def search_driver(_name):
        query = Driver.query.filter_by(name=_name).first()
        return query

    @staticmethod
    def delete_driver(_id):
        is_successful = Driver.query.filter_by(id=_id).delete()
        db.session.commit()
        return bool(is_successful)


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=True)
    price = db.Column(db.SmallInteger)
    status = db.Column(db.Enum(StatusEnum))

    @staticmethod
    def add_order(_client_id, _price):
        order = Order(client_id=_client_id, price=_price, status=StatusEnum.NOT_ACCEPTED)
        db.session.add(order)
        db.session.commit()

        return order

    @staticmethod
    def search_order_by_client(_client_name):
        _client_id = Client.search_client(_client_name).id
        query = Order.query.filter_by(client_id=_client_id).first()
        return query
    
    @staticmethod
    def search_order_by_id(_id):
        query = Order.query.filter_by(id=_id).first()
        return query

    @staticmethod
    def change_order(_id, args):
        query = Order.query.filter_by(id=_id).first()

        can_be_changed = query.status is StatusEnum.NOT_ACCEPTED
        result_change_message = []
        
        if 'client_id' in args and can_be_changed:
            query.client_id = args['client_id']
            change_message = "Client id is successefully changed"
            result_change_message.append(change_message)

        if 'driver_id' in args and can_be_changed:
            query.driver_id = args['driver_id']
            change_message = "Driver id is successefully changed"
            result_change_message.append(change_message)

        if 'created' in args and can_be_changed:
            query.created = args['created']
            change_message = "Created date is successefully changed"
            result_change_message.append(change_message)

        if 'price' in args:
            query.price = args['price']
            change_message = "Price is successefully changed"
            result_change_message.append(change_message)

        if len(result_change_message) == 0:
            change_message = "Order was not changed"
            result_change_message.append(change_message)

        db.session.commit()
        return result_change_message
