import pytest
import datetime
import order_iteractions
from models import Order, Client, Driver, StatusEnum

class TestOrder:
    
    def test_add_order(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        client_id = client.id
        
        order = Order.add_order(client_id, 400)
        
        assert order is not None
        
        assert order.client_id == client_id
        assert order.price == 400
        assert order.status == StatusEnum.NOT_ACCEPTED
        
    def test_search_order_by_client(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        client_id = client.id
        
        Order.add_order(client_id, 400)
        
        order = Order.search_order_by_client(client.name)
        
        assert order is not None
        
        assert order.client_id == client_id
        assert order.price == 400
        
    def test_search_order_by_id(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        client_id = client.id
        
        order = Order.add_order(client_id, 400)
        order_id = order.id
        
        order = Order.search_order_by_id(order_id)
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id
        
    def test_change_order_client(self):
        Client.add_client("NoName1", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        first_client_id = client.id
        
        Client.add_client("NoName1", "0000")
        client = Client.query.filter_by(name = "NoName1").first()
        second_client_id = client.id
        
        order = Order.add_order(first_client_id, 400)
        order_id = order.id
        
        order = Order.search_order_by_id(order_id)
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == first_client_id
        assert order.status == StatusEnum.NOT_ACCEPTED
        
        Order.change_order(order_id, {"client_id" : second_client_id})
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == second_client_id
        assert order.status == StatusEnum.NOT_ACCEPTED
        
    def test_change_order_driver(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        client_id = client.id
        
        Driver.add_driver("NoNameDriver", "ВН2222", "0000")
        driver = Driver.query.filter_by(name = "NoNameDriver").first()
        driver_id = driver.id
        
        order = Order.add_order(client_id, 400)
        order_id = order.id
        
        order = Order.search_order_by_id(order_id)
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id
        assert order.driver_id == None
        assert order.status == StatusEnum.NOT_ACCEPTED
        
        Order.change_order(order_id, {"driver_id" : driver_id})
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id
        assert order.driver_id == driver_id
        assert order.status == StatusEnum.NOT_ACCEPTED
        
    def test_change_order_created(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        client_id = client.id
        
        order = Order.add_order(client_id, 400)
        order_id = order.id
        
        order = Order.search_order_by_id(order_id)
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id
        assert order.status == StatusEnum.NOT_ACCEPTED
        
        Order.change_order(order_id, {"created" : datetime.datetime(2022, 9, 13, 0, 40, 18)})
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id
        assert order.created == datetime.datetime(2022, 9, 13, 0, 40, 18)
        assert order.status == StatusEnum.NOT_ACCEPTED
        
    def test_change_order_created(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        client_id = client.id
        
        order = Order.add_order(client_id, 400)
        order_id = order.id
        
        order = Order.search_order_by_id(order_id)
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id
        assert order.status == StatusEnum.NOT_ACCEPTED
        
        order_created = order.created
        
        Order.change_order(order_id, {"created" : datetime.datetime(2022, 9, 13, 0, 40, 18)})
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id
        assert order.created == datetime.datetime(2022, 9, 13, 0, 40, 18)
        assert order.status == StatusEnum.NOT_ACCEPTED
        
    def test_change_order_price(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        client_id = client.id
        
        order = Order.add_order(client_id, 400)
        order_id = order.id
        
        order = Order.search_order_by_id(order_id)
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id
        
        Order.change_order(order_id, {"price" : 1000})
        
        assert order is not None
        
        assert order.id == order_id
        assert order.client_id == client_id
        assert order.price == 1000
        
    def test_accept_order(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        client_id = client.id
        
        Driver.add_driver("NoNameDriver", "ВН2222", "0000")
        driver = Driver.query.filter_by(name = "NoNameDriver").first()
        driver_id = driver.id
        
        order = Order.add_order(client_id, 400)
        order_id = order.id
        
        status = order_iteractions.accept_order(order_id, driver_id)
        
        assert status == 'in_progress'
        
    def test_cancel_order(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        client_id = client.id
        
        order = Order.add_order(client_id, 400)
        order_id = order.id
        
        status = order_iteractions.cancel_order(order_id)
        
        assert status == 'cancelled'
        
    def test_finish_order(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        client_id = client.id
        
        Driver.add_driver("NoNameDriver", "ВН2222", "0000")
        driver = Driver.query.filter_by(name = "NoNameDriver").first()
        driver_id = driver.id
        
        order = Order.add_order(client_id, 400)
        order_id = order.id
        
        order_iteractions.accept_order(order_id, driver_id)
        
        status = order_iteractions.finish_order(order_id)
        
        assert status == 'done'