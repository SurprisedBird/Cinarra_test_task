
from models import Order, StatusEnum
from config import db

def accept_order(_id, _driver_id):
    query = Order.query.filter_by(id=_id).first()
    query.driver_id = _driver_id
    if query.status == StatusEnum.NOT_ACCEPTED:
        query.status = StatusEnum.IN_PROGRESS
        db.session.commit()

    return query

def cancel_order(_id):
    query = Order.query.filter_by(id=_id).first()
    if query.status == StatusEnum.NOT_ACCEPTED or query.status == StatusEnum.IN_PROGRESS:
        query.status = StatusEnum.CANCELLED
        db.session.commit()

    return query

def finish_order(_id):
    query = Order.query.filter_by(id=_id).first()
    if query.status == StatusEnum.IN_PROGRESS:
        query.status = StatusEnum.DONE
        db.session.commit()

    return query