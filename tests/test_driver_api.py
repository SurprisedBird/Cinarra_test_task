from http import client
import pytest
from app import app
from models import Driver

@pytest.fixture(autouse=True)
def run_before_test():
    Driver.clear_driver_table()

class TestDriverAPI:
    client = app.test_client()

    # Valid driver properties
    dr_name_v = "Any Driver"
    dr_phone_v = "3 095 9454583"
    dr_carnum_v = "BH4570"
    dr_id_v = 1

    # Invalid driver properties
    dr_names_inv = ["", "Any Driver1", "Any Driver^", "AbcdeAbcdeAbcdeAbcdeAbcdeAbcdeAbcdeAbcdeA"]
    dr_phones_inv = ["", "3 (099) 555-22-11a", "3 (099) 555-22-11$", "123456789012345678901"]
    dr_carnum_inv = ["", "BH 4570", "BH457@"]
    dr_ids_inv = ["1'", "1 "]

    def test_add_driver(self):
        '''
        Execute /add_driver POST method with valid name, valid car number, valid phone number
        Response code should be 200
        Added driver attributes in json format should be in response
        '''

        resp = self.client.post(f'/add_driver?name={self.dr_name_v}&car_number={self.dr_carnum_v}&phone_number={self.dr_phone_v}')
        assert resp.status_code == 200
        assert resp.json == {'id': 1, 'name': 'Any Driver', 'car_number': 'BH4570', 'phone_number': '3 095 9454583'}

    def test_add_driver_negative(self):
        '''
        Execute /add_driver_negative POST method with invalid name, invalid car number, invalid phone number and without name
        Response code should be 200
        Relevant error messages should be in response
        '''

        for name_inv in self.dr_names_inv:
            resp = self.client.post(f'/add_driver?name={name_inv}&car_number={self.dr_carnum_v}&phone_number={self.dr_phone_v}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Driver name is not valid"

        for car_num_inv in self.dr_carnum_inv:
            resp = self.client.post(f'/add_driver?name={self.dr_name_v}&car_number={car_num_inv}&phone_number={self.dr_phone_v}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Driver car number is not valid"

        for phone_inv in self.dr_phones_inv:
            resp = self.client.post(f'/add_driver?name={self.dr_name_v}&car_number={self.dr_carnum_v}&phone_number={phone_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Driver phone number is not valid"

        resp = self.client.post(f'/add_driver?phone_number={self.dr_phone_v}')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'name' is a required property"

    def test_search_driver(self):
        '''
        Execute /search_driver GET method with valid name
        Response code should be 200
        Found driver attributes in json format should be in response
        '''

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_carnum_v, _phone_number=self.dr_phone_v)
        assert driver is not None

        resp = self.client.get(f'/search_driver?name={self.dr_name_v}')
        assert resp.status_code == 200
        assert resp.json == {'id': 1, 'name': 'Any Driver', 'car_number': 'BH4570', 'phone_number': '3 095 9454583'}

    def test_search_driver_negative(self):
        '''
        Execute /search_driver GET method with invalid name and without name
        Response code should be 200
        Relevant error messages should be in response
        '''

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_carnum_v, _phone_number=self.dr_phone_v)
        assert driver is not None

        for name_inv in self.dr_names_inv:
            resp = self.client.get(f'/search_driver?name={name_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Driver name is not valid"

        resp = self.client.get(f'/search_driver')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'name' is a required property"

    def test_delete_driver(self):
        '''
        Execute /delete_driver DELETE method with valid driver id
        Response code should be 200
        "Driver is successfuly deleted" message with "success" key should be in response
        '''

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_carnum_v, _phone_number=self.dr_phone_v)
        assert driver is not None

        resp = self.client.delete(f'/delete_driver/{self.dr_id_v}')
        assert resp.status_code == 200
        assert resp.json.get("success") == "Driver is successfuly deleted"

    def test_delete_driver_negative(self):
        '''
        Execute /delete_driver_negative DELETE method with invalid driver id and without id
        Response code should be 200 if id is defined
        Response code should be 404 if id is not defined
        "Driver is not deleted or not existed" message with "error" key should be in response
        '''

        driver = Driver.add_driver(_name=self.dr_name_v, _car_number=self.dr_carnum_v, _phone_number=self.dr_phone_v)
        assert driver is not None

        for id in self.dr_ids_inv:
            resp = self.client.delete(f'/delete_driver/{id}')
            assert resp.status_code == 200
            assert resp.json.get("error") == 'Driver id is not valid'

        resp = self.client.delete(f'/delete_driver/{self.dr_id_v+1}')
        assert resp.status_code == 200
        assert resp.json.get("error") == "Driver is not deleted or not existed"

        resp = self.client.delete(f'/delete_driver/')
        assert resp.status_code == 404