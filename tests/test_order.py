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
    cl_phone = "+3 (099) 333-55-22"

    dr_name = "Any Driver"
    dr_phone = "+3 (077) 596-09-02"
    dr_carnum = "BH4570"

    or_price = 400

    changed_cl_name = "Changed Client"
    changed_cl_phone = "+3 (088) 444-66-33"

    changed_dr_name = "Changed Driver"
    changed_dr_carnum = "TY4569"
    changed_dr_phone = "+3 (099) 123-56-09"

    changed_or_date = "12-12-2022"
    changed_or_price = 1000

    cl_name_negative = "Any Client Negative"
    
    or_id_negative = 2

    def test_add_order(self):
        '''
        Create client with valid name and valid phone number
        Execute add_order("Any Order", 400)
        Order should be not None
        Order name should be "Any Order"
        Order price should be 400
        '''

        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.query.filter_by(name=self.cl_name).first()
        client_id = client.id

        order = Order.add_order(_client_name=client.name, _price=self.or_price)
        assert order is not None
        
        assert order.client_id == client_id
        assert order.price == self.or_price
        assert order.status == StatusEnum.NOT_ACCEPTED
        
    def test_search_order_by_client(self):
        '''
        Create client with valid name and valid phone number
        Create order with valid id and valid price
        Execute search_order_by_client("Any Client")
        Order should be not None
        Order name should be "Any Order"
        Order price should be 400
        '''

        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.query.filter_by(name=self.cl_name).first()
        client_id = client.id
        
        Order.add_order(_client_name=client.name, _price=self.or_price)

        order = Order.search_order_by_client(_client_name=client.name)
        
        assert order is not None

        assert order.client_id == client_id
        assert order.price == self.or_price
        
    def test_search_order_by_id(self):
        '''
        Create client with valid name and valid phone number
        Create order with valid id and valid price
        Execute search_order_by_id(1)
        Order should be not None
        Order name should be "Any Order"
        Order price should be 400
        '''

        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.query.filter_by(name=self.cl_name).first()
        client_id = client.id
        
        order = Order.add_order(_client_name=client.name, _price=self.or_price)
        order_id = order.id
        
        order = Order.search_order_by_id(_id=order_id)
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id

    def test_search_negative(self):
        '''
        Create client with valid name and valid phone number
        Create order with valid id and valid price
        Execute search_order_by_client("Any Client Negative")
        Order should be None
        Execute search_order_by_id(2)
        Order should be None
        '''
        
        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.query.filter_by(name=self.cl_name).first()
        
        order = Order.add_order(_client_name=client.name, _price=self.or_price)

        order = Order.search_order_by_client(_client_name=self.cl_name_negative)
        assert order is None
        
        order = Order.search_order_by_id(_id=self.or_id_negative)
        assert order is None
        
    def test_change_order_client(self):
        '''
        Create two clients with valid names and valid phone numbers
        Save changed client id
        Create order with first client name
        Execute change_order(order.id, changed_client_id)
        Order client_id should be 2
        'Client id is successefully changed' message in "success" key should be in response
        '''

        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        changed_client = Client.add_client(_name=self.changed_cl_name, _phone_number=self.changed_cl_phone)
        assert changed_client is not None
        changed_client_id = {"client_id":changed_client.id}
        
        order = Order.add_order(_client_name=client.name, _price=self.or_price)
        assert order is not None
        assert order.client_id == client.id

        result = Order.change_order(_id=order.id, _req_args=changed_client_id)

        assert order.client_id == 2
        assert result == {'success': 'Client id is successefully changed'}
        
    def test_change_order_driver(self):
        '''
        Create client with valid name and valid phone number
        Create driver with valid name, valid car number and valid phone number
        Create order with client name
        Be sure order is not None and order driver_id is None
        Prepare driver_id json {"driver_id": driver.id}
        Execute change_order(order.id, driver_id)
        Order driver_id should be 1
        'Driver id is successefully changed' message in "success" key should be in response

        Create another driver with valid name, valid car number and valid phone number
        Prepare driver_id json {"driver_id":changed_driver.id}
        Execute change_order(order.id, changed_driver_id)
        Order driver_id should be 2
        'Driver id is successefully changed' message in "success" key should be in response
        '''

        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum, _phone_number=self.dr_phone)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price)
        assert order is not None
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
        '''
        Create client with valid name and valid phone number
        Create order with client name
        Prepare changed_date json {"created": self.changed_or_date}
        Execute change_order(order.id, changed_date)
        Order changed should be 2
        'Order date is successefully changed' message in "success" key should be in response
        '''

        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price)
        assert order is not None
        assert order.client_id == client.id
        assert order.driver_id is None

        changed_date = {"created": self.changed_or_date}

        result = Order.change_order(_id=order.id, _req_args=changed_date)

        assert order.created == "12-12-2022"
        assert result == {'success': 'Order date is successefully changed'}
        
    def test_change_order_price(self):
        '''
        Create client with valid name and valid phone number
        Create order with client name
        Prepare changed_price json {"price": self.changed_or_price}
        Execute change_order(order.id, changed_price)
        Order price should be 1000
        'Order price is successefully changed' message in "success" key should be in response
        '''

        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price)
        assert order is not None

        changed_price = {"price": self.changed_or_price}
        result = Order.change_order(_id=order.id, _req_args=changed_price)

        assert order.price == 1000
        assert result == {'success': 'Order price is successefully changed'}

    def test_change_order_negative(self):
        '''
        Create client with valid name and valid phone number
        Create order with client name
        Execute change_order(order.id, {})
        'Order was not changed' message in "error" key should be in response
        '''

        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price)
        assert order is not None

        result = Order.change_order(_id=order.id, _req_args={})

        assert result == {'error': 'Order was not changed'}

    def test_accept_order(self):
        '''
        Create client with valid name and valid phone number
        Be sure client is not None
        Create driver with valid name, valid car number and valid phone number
        Be sure driver is not None
        Create order with client name
        Be sure order is not None

        Execute accept_order(order.id, driver.id)
        Order client_id should be 1
        Order driver_id should be 1
        Order status should be IN_PROGRESS
        '''

        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum, _phone_number=self.dr_phone)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price)
        assert order is not None

        accepted_order = order_iteractions.accept_order(_id=order.id, _driver_id=driver.id)
        assert accepted_order.client_id == client.id
        assert accepted_order.driver_id == driver.id
        assert accepted_order.status == StatusEnum.IN_PROGRESS

    def test_cancel_order(self):
        '''
        Create client with valid name and valid phone number
        Be sure client is not None
        Create driver with valid name, valid car number and valid phone number
        Be sure driver is not None
        Create order with client name
        Be sure order is not None

        Execute accept_order(order.id, driver.id)
        Order client_id should be 1
        Order driver_id should be 1
        Order status should be IN_PROGRESS

        Execute cancel_order(order.id)
        Order status should be CANCELLED
        '''

        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum, _phone_number=self.dr_phone)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price)
        assert order is not None

        accepted_order = order_iteractions.accept_order(_id=order.id, _driver_id=driver.id)
        assert accepted_order.client_id == client.id
        assert accepted_order.driver_id == driver.id
        assert accepted_order.status == StatusEnum.IN_PROGRESS

        cancelled_order = order_iteractions.cancel_order(_id=order.id)
        assert cancelled_order is not None
        assert cancelled_order.status == StatusEnum.CANCELLED
        
    def test_finish_order(self):
        '''
        Create client with valid name and valid phone number
        Be sure client is not None
        Create driver with valid name, valid car number and valid phone number
        Be sure driver is not None
        Create order with client name
        Be sure order is not None

        Execute accept_order(order.id, driver.id)
        Order client_id should be 1
        Order driver_id should be 1
        Order status should be IN_PROGRESS

        Execute finish_order(order.id)
        Order status should be DONE
        '''

        client = Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum, _phone_number=self.dr_phone)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price)
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