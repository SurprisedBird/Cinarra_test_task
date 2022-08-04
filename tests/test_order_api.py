from http import client
from pydoc import cli
import pytest
from app import app
from config import db
from models import Client, Driver, Order, StatusEnum

@pytest.fixture(autouse=True)
def run_before_test():
    Client.clear_client_table()
    Driver.clear_driver_table()
    Order.clear_order_table()

class TestOrderAPI:
    client = app.test_client()

    # Valid client properties
    cl_name_v = "Any Client"
    cl_phone_v = "3 (099) 555-22-11"
    cl_id_v = 1

    # Valid driver properties
    dr_name_v = "Any Driver"
    dr_car_number_v = "AB0000YZ"
    dr_phone_v = "+3 (099) 333-55-22"
    dr_id_v = 1

    # Valid order properties
    or_price_v = 100
    or_client_id_v = 1
    or_driver_id_v = 1
    or_id_v = 1

    # Data for changed order
    changed_client_id = 2
    changed_driver_id = 1
    changed_created = "12-12-2022"
    changed_price = 500

    # Invalid client properties
    cl_names_inv = ["", "Any Client1", "Any Client^", "AbcdeAbcdeAbcdeAbcdeAbcdeAbcdeAbcdeAbcdeA"]

    # Invalid order properties
    or_prices_inv = ["", "100B", "100.", "123456"]
    or_client_id_inv = ["1@", " 1"]
    or_dates_inv = ["11-11-20222", "11-11-20c", "11-11-2^", "8@"]
    ids_inv = ["1>", "1<"]

    def test_add_order(self):
        '''
        Execute /add_order POST method with valid client name and order price
        Response code should be 200
        Added order attributes in json format should be in response
        '''
        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None
        
        resp = self.client.post(f'/add_order?client_name={self.cl_name_v}&price={self.or_price_v}')
        assert resp.status_code == 200
        assert resp.json == {'client_id': 1, 'driver_id': None, 'created': None, 'id': 1, 'price': 100, 'status': 'not_accepted'}
    
    def test_add_order_negative(self):
        '''
        Execute /add_order_negative POST method with invalid name, invalid price, without name and without price
        Response code should be 200
        Relevant error messages should be in response
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None
        
        for name_inv in self.cl_names_inv:
            resp = self.client.post(f'/add_order?client_name={name_inv}&price={self.or_price_v}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Client name is not valid"

        for price_inv in self.or_prices_inv:
            resp = self.client.post(f'/add_order?client_name={self.cl_name_v}&price={price_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Order price is not valid"

        resp = self.client.post(f'/add_order?price={self.or_price_v}')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'client_name' is a required property"

        resp = self.client.post(f'/add_order?client_name={self.cl_name_v}')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'price' is a required property"

    def test_search_order_by_client_name(self):
        '''
        Execute /search_order_by_client GET method with valid client name
        Response code should be 200
        Found order attributes in json format should be in response
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        Order.add_order(_client_name=client.name, _price=self.or_price_v)

        resp = self.client.get(f'/search_order_by_client?name={self.cl_name_v}')
        assert resp.json == {'client_id': 1, 'driver_id': None, 'created': None, 'id': 1, 'price': 100, 'status': 'not_accepted'}

    def test_search_order_by_id(self):
        '''
        Execute /search_order_by_id GET method with valid client name
        Response code should be 200
        Found order attributes in json format should be in response
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        Order.add_order(_client_name=client.name, _price=self.or_price_v)

        resp = self.client.get(f'/search_order_by_id?id={client.id}')
        assert resp.json == {'client_id': 1, 'driver_id': None, 'created': None, 'id': 1, 'price': 100, 'status': 'not_accepted'}


    def test_search_order_negative(self):
        '''
        Execute /search_driver GET method with invalid client name and without client name
        Response code should be 200
        Relevant error messages should be in response

        Execute /search_order_by_id GET method with invalid order id
        Response code should be 200
        Relevant error messages should be in response

        Execute /search_order_by_id GET method without order id
        Response code should be 405
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        Order.add_order(_client_name=client.name, _price=self.or_price_v)

        for name_inv in self.cl_names_inv:
            resp = self.client.get(f'/search_order_by_client?name={name_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Client name is not valid"

        resp = self.client.post(f'/add_order')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'client_name' is a required property"

        for id_inv in self.ids_inv:
            resp = self.client.get(f'/search_order_by_id?id={id_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Order id is not valid"

        resp = self.client.post(f'/search_order_by_id')
        assert resp.status_code == 405

    def test_change_order_params_by_steps(self):
        '''
        Create two clients with valid name and phone number
        Create driver with valid name, car number and phone number
        Create order with valid client name and price

        Execute /change_order POST method with valid client id (2)
        Response code should be 200
        Client id should be equaled 2
        "Client id is successefully changed" message with "success" key should be in response

        Execute /change_order POST method with valid driver id (1)
        Response code should be 200
        Driver id should be equaled 1
        "Driver id is successefully changed" message with "success" key should be in response

        Execute /change_order POST method with valid order date ('12-12-2022')
        Response code should be 200
        Order date should be equaled '12-12-2022'
        "Order date is successefully changed" message with "success" key should be in response

        Execute /change_order POST method with valid order price (500)
        Response code should be 200
        Order price should be equaled 500
        "Order price is successefully changed" message with "success" key should be in response
        '''

        first_client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert first_client is not None

        second_client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert second_client is not None

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_car_number_v,
        _phone_number=self.dr_phone_v)
        assert driver is not None

        order = Order.add_order(_client_name=first_client.name, _price=self.or_price_v)

        resp = self.client.post(f'/change_order?id={self.or_id_v}&client_id={self.changed_client_id}')
        order = Order.query.filter_by(id=self.or_id_v).first()

        assert resp.status_code == 200
        assert order.client_id == 2
        assert resp.json == {'success': 'Client id is successefully changed'}

        resp = self.client.post(f'/change_order?id={self.or_id_v}&driver_id={self.changed_driver_id}')
        order = Order.query.filter_by(id=self.or_id_v).first()

        assert resp.status_code == 200
        assert order.driver_id == 1
        assert resp.json == {'success': 'Driver id is successefully changed'}

        resp = self.client.post(f'/change_order?id={self.or_id_v}&created={self.changed_created}')
        order = Order.query.filter_by(id=self.or_id_v).first()

        assert resp.status_code == 200
        assert order.created == '12-12-2022'
        assert resp.json == {'success': 'Order date is successefully changed'}

        resp = self.client.post(f'/change_order?id={self.or_id_v}&price={self.changed_price}')
        order = Order.query.filter_by(id=self.or_id_v).first()

        assert resp.status_code == 200
        assert order.price == 500
        assert resp.json == {'success': 'Order price is successefully changed'}

    def test_change_order_all_params(self):
        '''
        Create two clients with valid name and phone number
        Create driver with valid name, car number and phone number
        Create order with valid client name and price

        Execute /change_order POST method with valid client id (2), driver_id (1), order date ('12-12-2022') and order price(500)
        Response code should be 200
        Relevant success messages for each attribute with "success" key should be in response
        Client id should be equaled 2
        Driver id should be equaled 1
        Order date should be equaled '12-12-2022'
        Order price should be equaled 500
        '''

        first_client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert first_client is not None

        second_client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert second_client is not None

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_car_number_v,
        _phone_number=self.dr_phone_v)
        assert driver is not None

        order = Order.add_order(_client_name=first_client.name, _price=self.or_price_v)

        resp = self.client.post(f'/change_order?id={self.or_id_v}&client_id={self.changed_client_id}&driver_id={self.changed_driver_id}&created={self.changed_created}&price={self.changed_price}')
        order = Order.query.filter_by(id=self.or_id_v).first()

        assert resp.status_code == 200
        assert resp.json == {'success': 'Client id is successefully changed, Driver id is successefully changed, Order date is successefully changed, Order price is successefully changed'}
        
        assert order.client_id == 2
        assert order.driver_id == 1
        assert order.created == "12-12-2022"
        assert order.price == 500

    def test_change_order_negative(self):
        '''
        Create client with valid name and phone number
        Create driver with valid name, car number and phone number
        Create order with valid client name and price

        Execute /change_order POST method with invalid client id, invalid driver_id, invalid order date and invalid order price
        Response code should be 200
        Relevant error messages for each attribute with "error" key should be in response
        
        Execute /change_order POST method without any attributes
        "Order was not changed" message with "error" key should be in response      
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_car_number_v,
        _phone_number=self.dr_phone_v)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price_v)
        assert order is not None

        for id_inv in self.ids_inv:
            resp = self.client.post(f'/change_order?id={self.or_id_v}&client_id={id_inv}')
            assert resp.json == {'error': 'Client id is not valid'}

        for id_inv in self.ids_inv:
            resp = self.client.post(f'/change_order?id={self.or_id_v}&driver_id={id_inv}')
            assert resp.json == {'error': 'Driver id is not valid'}

        for date_inv in self.or_dates_inv:
            resp = self.client.post(f'/change_order?id={self.or_id_v}&created={date_inv}')
            assert resp.json == {'error': 'Order date is not valid'}

        for price_inv in self.or_prices_inv:
            resp = self.client.post(f'/change_order?id={self.or_id_v}&price={price_inv}')
            assert resp.json == {'error': 'Order price is not valid'}

        resp = self.client.post(f'/change_order?id={self.or_id_v}')
        order = Order.query.filter_by(id=self.or_id_v).first()

        assert resp.status_code == 200
        assert resp.json == {'error': 'Order was not changed'}

    def test_accept_order(self):
        '''
        Create client with valid name and phone number
        Create driver with valid name, car number and phone number
        Create order with valid client name and price

        Execute /accept_order POST method with valid order id and valid driver id
        Response code should be 200
        "in_progress" status with "status" key should be in response     
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_car_number_v,
        _phone_number=self.dr_phone_v)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price_v)
        assert order is not None
        assert order.status == StatusEnum.NOT_ACCEPTED

        resp = self.client.post(f'/accept_order?id={order.id}&driver_id={driver.id}')
        assert resp.status_code == 200
        assert resp.json.get("status") == "in_progress"

        order = Order.query.filter_by(id=self.or_id_v).first()
        assert order.driver_id == 1
        assert order.status == StatusEnum.IN_PROGRESS

    def test_accept_order_negative(self):
        '''
        Create client with valid name and phone number
        Create driver with valid name, car number and phone number
        Create order with valid client name and price

        Execute /accept_order POST method with invalid order id, invalid driver id, without order id and without driver id
        Response code should be 200
        Relevant error messages for each attribute with "error" key should be in response     
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_car_number_v,
        _phone_number=self.dr_phone_v)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price_v)
        assert order is not None
        assert order.status == StatusEnum.NOT_ACCEPTED

        for id_inv in self.ids_inv:
            resp = self.client.post(f'/accept_order?id={id_inv}&driver_id={self.dr_id_v}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Order id is not valid"

        for id_inv in self.ids_inv:
            resp = self.client.post(f'/accept_order?id={self.or_id_v}&driver_id={id_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Driver id is not valid"

        resp = self.client.post(f'/accept_order?&driver_id={self.dr_id_v}')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'id' is a required property"

        resp = self.client.post(f'/accept_order?&id={self.or_id_v}')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'driver_id' is a required property"

    def test_cancel_order_from_not_accepted(self):
        '''
        Create client with valid name and phone number
        Create driver with valid name, car number and phone number
        Create order with valid client name and price
        Be sure order is not None and status is NOT_ACCEPTED

        Execute /cancel_order POST method with valid order id
        Response code should be 200
        "cancelled" status with "status" key should be in response     
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_car_number_v,
        _phone_number=self.dr_phone_v)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price_v)
        assert order is not None
        assert order.status == StatusEnum.NOT_ACCEPTED

        resp = self.client.post(f'/cancel_order?id={order.id}')
        assert resp.status_code == 200
        assert resp.json.get("status") == "cancelled"

        order = Order.query.filter_by(id=self.or_id_v).first()
        assert order.status == StatusEnum.CANCELLED

    def test_cancel_order_from_in_progress(self):
        '''
        Create client with valid name and phone number
        Create driver with valid name, car number and phone number
        Create order with valid client name and price
        Be sure order is not None and status is NOT_ACCEPTED

        Execute /accept_order POST method with valid order id and valid driver id
        Response code should be 200
        Be sure order status is IN_PROGRESS

        Execute /cancel_order POST method with valid order id
        Response code should be 200
        "cancelled" status with "status" key should be in response     
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_car_number_v,
        _phone_number=self.dr_phone_v)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price_v)
        assert order is not None
        assert order.status == StatusEnum.NOT_ACCEPTED

        self.client.post(f'/accept_order?id={self.or_id_v}&driver_id={self.dr_id_v}')
        order = Order.query.filter_by(id=self.or_id_v).first()
        assert order.status == StatusEnum.IN_PROGRESS

        resp = self.client.post(f'/cancel_order?id={order.id}')
        assert resp.status_code == 200
        assert resp.json.get("status") == "cancelled"

        order = Order.query.filter_by(id=self.or_id_v).first()
        assert order.status == StatusEnum.CANCELLED

    def test_cancel_order_negative(self):
        '''
        Create client with valid name and phone number
        Create driver with valid name, car number and phone number
        Create order with valid client name and price
        Be sure order is not None and status is NOT_ACCEPTED

        Execute /cancel_order POST method with invalid order id
        Response code should be 200
        Relevant error messages for each attribute with "error" key should be in response 
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_car_number_v,
        _phone_number=self.dr_phone_v)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price_v)
        assert order is not None
        assert order.status == StatusEnum.NOT_ACCEPTED

        for id_inv in self.ids_inv:
            resp = self.client.post(f'/cancel_order?id={id_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Order id is not valid"
        
        resp = self.client.post(f'/cancel_order')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'id' is a required property"

    def test_finish_order(self):
        '''
        Create client with valid name and phone number
        Create driver with valid name, car number and phone number
        Create order with valid client name and price
        Be sure order is not None and status is NOT_ACCEPTED

        Execute /accept_order POST method with valid order id and valid driver id
        Response code should be 200
        Be sure order status is IN_PROGRESS

        Execute /finish_order POST method with valid order id
        Response code should be 200
        "done" status with "status" key should be in response     
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_car_number_v,
        _phone_number=self.dr_phone_v)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price_v)
        assert order is not None
        assert order.status == StatusEnum.NOT_ACCEPTED

        resp = self.client.post(f'/accept_order?id={order.id}&driver_id={driver.id}')
        assert resp.status_code == 200
        assert resp.json.get("status") == "in_progress"

        order = Order.query.filter_by(id=self.or_id_v).first()
        assert order.driver_id == 1
        assert order.status == StatusEnum.IN_PROGRESS

        resp = self.client.post(f'/finish_order?id={order.id}')
        assert resp.status_code == 200
        assert resp.json.get("status") == "done"

        order = Order.query.filter_by(id=self.or_id_v).first()
        assert order.driver_id == 1
        assert order.status == StatusEnum.DONE

    def test_finish_order_negative(self):
        '''
        Create client with valid name and phone number
        Create driver with valid name, car number and phone number
        Create order with valid client name and price
        Be sure order is not None and status is NOT_ACCEPTED

        Execute /accept_order POST method with valid order id and valid driver id
        Response code should be 200
        Be sure order status is IN_PROGRESS

        Execute /finish_order POST method with invalid order id
        Response code should be 200
        Relevant error messages for each attribute with "error" key should be in response 
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_car_number_v,
        _phone_number=self.dr_phone_v)
        assert driver is not None

        order = Order.add_order(_client_name=client.name, _price=self.or_price_v)
        assert order is not None
        assert order.status == StatusEnum.NOT_ACCEPTED

        resp = self.client.post(f'/accept_order?id={order.id}&driver_id={driver.id}')
        assert resp.status_code == 200
        assert resp.json.get("status") == "in_progress"

        order = Order.query.filter_by(id=1).first()
        assert order.driver_id == 1
        assert order.status == StatusEnum.IN_PROGRESS

        for id_inv in self.ids_inv:
            resp = self.client.post(f'/finish_order?id={id_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Order id is not valid"
        
        resp = self.client.post(f'/finish_order')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'id' is a required property"