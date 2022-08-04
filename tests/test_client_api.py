import pytest
from app import app
from models import Client

@pytest.fixture(autouse=True)
def run_before_test():
    Client.clear_client_table()

class TestClientAPI:
    client = app.test_client()

    # Valid client properties
    cl_name_v = "Any Client"
    cl_phone_v = "3 (099) 555-22-11"
    cl_id_v = 1

    # Invalid client properties
    cl_names_inv = ["", "Any Client1", "Any Client^", "AbcdeAbcdeAbcdeAbcdeAbcdeAbcdeAbcdeAbcdeA"]
    cl_phones_inv = ["", "3 (099) 555-22-11a", "3 (099) 555-22-11$", "123456789012345678901"]
    cl_ids_inv = ["1@", "1 "]

    def test_add_client(self):
        '''
        Execute /add_client POST method with valid name and valid phone number
        Response code should be 200
        Added client attributes in json format should be in response
        '''

        resp = self.client.post(f'/add_client?name={self.cl_name_v}&phone_number={self.cl_phone_v}')
        assert resp.status_code == 200
        assert resp.json == {'id': 1, 'name': 'Any Client', 'phone_number': '3 (099) 555-22-11'}

    def test_add_client_negative(self):
        '''
        Execute /add_client POST method with invalid name, invalid phone number and without name
        Response code should be 200
        Relevant error messages should be in response
        '''

        for name_inv in self.cl_names_inv:
            resp = self.client.post(f'/add_client?name={name_inv}&phone_number={self.cl_phone_v}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Client name is not valid"

        for phone_inv in self.cl_phones_inv:
            resp = self.client.post(f'/add_client?name={self.cl_name_v}&phone_number={phone_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Client phone number is not valid"

        resp = self.client.post(f'/add_client?phone_number={self.cl_phone_v}')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'name' is a required property"

    def test_search_client(self):
        '''
        Execute /search_client GET method with valid name
        Response code should be 200
        Found client attributes in json format should be in response
        '''
        
        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        resp = self.client.get(f'/search_client?name={self.cl_name_v}')
        assert resp.status_code == 200
        assert resp.json == {'id': 1, 'name': 'Any Client', 'phone_number': '3 (099) 555-22-11'}

    def test_search_client_negative(self):
        '''
        Execute /search_client GET method with invalid name and without name
        Response code should be 200
        Relevant error messages should be in response
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        for name_inv in self.cl_names_inv:
            resp = self.client.get(f'/search_client?name={name_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == "Client name is not valid"

        resp = self.client.get(f'/search_client')
        assert resp.status_code == 200
        assert resp.json.get("error") == "'name' is a required property"

    def test_delete_client(self):
        '''
        Execute /delete_client DELETE method with valid client id
        Response code should be 200
        "Client is successfuly deleted" message with "success" key should be in response
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        resp = self.client.delete(f'/delete_client/{self.cl_id_v}')
        assert resp.status_code == 200
        assert resp.json.get("success") == "Client is successfuly deleted"

    def test_delete_client_negative(self):
        '''
        Execute /delete_client DELETE method with invalid client id and without id
        Response code should be 200 if id is defined
        Response code should be 404 if id is not defined
        "Client is not deleted or not existed" message with "error" key should be in response
        '''

        client = Client.add_client(_name=self.cl_name_v, _phone_number=self.cl_phone_v)
        assert client is not None

        for id_inv in self.cl_ids_inv:
            resp = self.client.delete(f'/delete_client/{id_inv}')
            assert resp.status_code == 200
            assert resp.json.get("error") == 'Client id is not valid'

        resp = self.client.delete(f'/delete_client/{self.cl_id_v+1}')
        assert resp.status_code == 200
        assert resp.json.get("error") == "Client is not deleted or not existed"

        resp = self.client.delete(f'/delete_client/')
        assert resp.status_code == 404