from unittest import result
import pytest
import datetime
from app import change_order
import order_iteractions
from models import Order, Client, Driver, StatusEnum

@pytest.fixture(autouse=True)
def run_before_test():
    Client.clear_client_table()
    Driver.clear_driver_table()
    Order.clear_order_table()

class TestOrder:
    cl_name = "Any Client"
    changed_cl_name = "Changed Client"
    cl_phone = "+3 (099) 333-55-22"
    changed_cl_phone = "+3 (088) 444-66-33"
    dr_name = "Any Driver"
    changed_dr_name = "Changed Driver"
    dr_phone = "+3 (077) 596-09-02"
    changed_dr_phone = "+3 (099) 123-56-09"
    dr_carnum = "BH4570"
    changed_dr_carnum = "TY4569"
    order_price = 400
    changed_order_price = 1000

    def test_add_order(self):
        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.query.filter_by(name=self.cl_name).first()
        client_id = client.id

        order = Order.add_order(_client_name=client.name, _price=self.order_price)
        
        assert order.client_id == client_id
        assert order.price == self.order_price
        assert order.status == StatusEnum.NOT_ACCEPTED
        
    def test_search_order_by_client(self):
        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.query.filter_by(name=self.cl_name).first()
        client_id = client.id
        
        Order.add_order(_client_name=client.name, _price=self.order_price)

        order = Order.search_order_by_client(_client_name=client.name)
        
        assert order is not None

        assert order.client_id == client_id
        assert order.price == self.order_price
        
    def test_search_order_by_id(self):
        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.query.filter_by(name=self.cl_name).first()
        client_id = client.id
        
        order = Order.add_order(_client_name=client.name, _price=self.order_price)
        order_id = order.id
        
        order = Order.search_order_by_id(_id=order_id)
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id
        
    def test_change_order_client(self):
        
        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        changed_client = Client.add_client(_name=self.changed_cl_name, _phone_number=self.changed_cl_phone)
        assert changed_client is not None
        changed_client_id = {"client_id":changed_client.id}
        
        order = Order.add_order(_client_name=client.name, _price=self.order_price)
        assert order is not None
        assert order.client_id == client.id

        result = Order.change_order(_id=order.id, _req_args=changed_client_id)

        assert order.client_id == changed_client.id
        assert result == {'success': 'Client id is successefully changed'}
        
    def test_change_order_driver(self):
        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum, _phone_number=self.dr_phone)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.order_price)
        assert order is not None
        assert order.client_id == client.id
        assert order.driver_id is None

        driver_id = {"driver_id": driver.id}

        result = Order.change_order(_id=order.id, _req_args=driver_id)

        assert order.driver_id == driver.id
        assert result == {'success': 'Driver id is successefully changed'}

        changed_driver = Driver.add_driver(_name=self.changed_dr_name, _car_number=self.changed_dr_carnum, _phone_number=self.changed_dr_phone)
        assert changed_driver is not None
        changed_driver_id = {"driver_id":changed_driver.id}

        result = Order.change_order(_id=order.id, _req_args=changed_driver_id)

        assert order.driver_id == changed_driver.id
        assert result == {'success': 'Driver id is successefully changed'}

    def test_change_order_date(self):
        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        order = Order.add_order(_client_name=client.name, _price=self.order_price)
        assert order is not None
        assert order.client_id == client.id
        assert order.driver_id is None

        date = {"created": "12.12.2022"}

        result = Order.change_order(_id=order.id, _req_args=date)

        assert order.created == "12.12.2022"
        
    def test_change_order_price(self):
        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        order = Order.add_order(_client_name=client.name, _price=self.order_price)
        assert order is not None

        changed_price = {"price": self.changed_order_price}
        result = Order.change_order(_id=order.id, _req_args=changed_price)

        assert order.price == self.changed_order_price
        assert result == {'success': 'Price is successefully changed'}

    def test_change_order_negative(self):
        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        order = Order.add_order(_client_name=client.name, _price=self.order_price)
        assert order is not None

        result = Order.change_order(_id=order.id, _req_args={})

        assert result == {'error': 'Order was not changed'}

    def test_accept_order(self):
        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum, _phone_number=self.dr_phone)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.order_price)
        assert order is not None

        accepted_order = order_iteractions.accept_order(_id=order.id, _driver_id=driver.id)
        assert accepted_order.id == order.id
        assert accepted_order.price == order.price
        assert accepted_order.client_id == client.id
        assert accepted_order.driver_id == driver.id
        assert accepted_order.status == StatusEnum.IN_PROGRESS

    def test_cancel_order(self):
        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum, _phone_number=self.dr_phone)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.order_price)
        assert order is not None

        accepted_order = order_iteractions.accept_order(_id=order.id, _driver_id=driver.id)
        assert accepted_order is not None
        assert accepted_order.id == order.id
        assert accepted_order.price == order.price
        assert accepted_order.client_id == client.id
        assert accepted_order.driver_id == driver.id
        assert accepted_order.status == StatusEnum.IN_PROGRESS

        cancelled_order = order_iteractions.cancel_order(_id=order.id)
        assert cancelled_order is not None
        assert cancelled_order.status == StatusEnum.CANCELLED
        
    def test_finish_order(self):
        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum, _phone_number=self.dr_phone)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.order_price)
        assert order is not None

        accepted_order = order_iteractions.accept_order(_id=order.id, _driver_id=driver.id)
        assert accepted_order is not None
        assert accepted_order.id == order.id
        assert accepted_order.price == order.price
        assert accepted_order.client_id == client.id
        assert accepted_order.driver_id == driver.id
        assert accepted_order.status == StatusEnum.IN_PROGRESS

        cancelled_order = order_iteractions.finish_order(_id=order.id)
        assert cancelled_order is not None
        assert cancelled_order.status == StatusEnum.DONE