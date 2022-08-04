from email import message
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

    def as_dict(self):
        return {"id": self.id, "name": self.name, "phone_number": self.phone_number}

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

    @staticmethod
    def clear_client_table():
        Client.query.delete()
        db.session.commit()


class Driver(db.Model):
    __tablename__ = 'driver'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    car_number = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Unicode(20))
    
    orders = relationship("Order")

    def as_dict(self):
        return {"id": self.id, "name": self.name, "car_number": self.car_number, "phone_number": self.phone_number}
    
    @staticmethod
    def add_driver(_name, _car_number, _phone_number):
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

    @staticmethod
    def clear_driver_table():
        Driver.query.delete()
        db.session.commit()

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.String(100))
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=True)
    price = db.Column(db.SmallInteger)
    status = db.Column(db.Enum(StatusEnum))

    def as_dict(self):
        return {"id": self.id, "created": self.created, "client_id": self.client_id, "driver_id": self.driver_id, "price": self.price, "status": self.status.value}
    
    @staticmethod
    def add_order(_client_name, _price):
        _client_id = Client.search_client(_client_name).id
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
    def change_order(_id, _req_args):
        query = Order.query.filter_by(id=_id).first()

        can_be_changed = query.status is StatusEnum.NOT_ACCEPTED
        result_change_message = []

        is_success = "success"
        
        if 'client_id' in _req_args and can_be_changed:
            query.client_id = _req_args['client_id']
            change_message = "Client id is successefully changed"
            result_change_message.append(change_message)

        if 'driver_id' in _req_args and can_be_changed:
            query.driver_id = _req_args['driver_id']
            change_message = "Driver id is successefully changed"
            result_change_message.append(change_message)

        if 'created' in _req_args and can_be_changed:
            query.created = _req_args['created']
            change_message = "Order date is successefully changed"
            result_change_message.append(change_message)

        if 'price' in _req_args:
            query.price = _req_args['price']
            change_message = "Order price is successefully changed"
            result_change_message.append(change_message)

        if len(result_change_message) == 0:
            change_message = "Order was not changed"
            result_change_message.append(change_message)
            is_success = "error"

        db.session.commit()
        return {is_success:', '.join(str(message) for message in result_change_message)}

    @staticmethod
    def clear_order_table():
        Order.query.delete()
        db.session.commit()