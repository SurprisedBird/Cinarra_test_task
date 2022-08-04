import pytest
from models import Client

@pytest.fixture(autouse=True)
def run_before_test():
    Client.clear_client_table()

class TestClient:
    cl_name = "Any Client"
    cl_phone = "+3 (099) 333-55-22"

    cl_name_negative = "Any Client Negative"
    cl_id_negative = 2

    def test_add_client(self):
        '''
        Execute add_client("Any Client", "+3 (099) 333-55-22")
        Client should be not None
        Client name should be "Any Client"
        Client phone number should be "+3 (099) 333-55-22"
        '''

        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.query.filter_by(name=self.cl_name).first()

        assert client is not None
        assert client.name == "Any Client"
        assert client.phone_number == "+3 (099) 333-55-22"
        
    def test_search_client(self):
        '''
        Create client by add_client("Any Client", "+3 (099) 333-55-22")
        Execute search_client("Any Client")
        Client should be not None
        Client name should be "Any Client"
        Client phone number should be "+3 (099) 333-55-22"
        '''

        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.search_client(_name=self.cl_name)
        
        assert client is not None
        assert client.name == "Any Client"
        assert client.phone_number == "+3 (099) 333-55-22"

    def test_search_client_negative(self):
        '''
        Create client by add_client("Any Client", "+3 (099) 333-55-22")
        Execute search_client("Any Client Negative")
        Client with this name should not found and should be None
        '''

        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.search_client(_name=self.cl_name_negative)
        
        assert client is None

    def test_delete_client(self):
        '''
        Create client by add_client("Any Client", "+3 (099) 333-55-22")
        Save client id
        Be sure client is not None
        Execute delete_client(client_id)
        Client should be deleted and equaled to None
        delete_client(client_id) returns True
        '''

        Client.add_client(_name=self.cl_name, _phone_number=self.cl_phone)
        client = Client.query.filter_by(name=self.cl_name).first()
        client_id = client.id

        assert client is not None
        
        is_successful = Client.delete_client(client_id)
        client = Client.query.filter_by(id=client_id).first()
        
        assert client is None
        assert is_successful is True

    def test_delete_client_negative(self):
        '''
        Create client by add_client("Any Client", "+3 (099) 333-55-22")
        Be sure client is not None
        Execute delete_client(client_id_negative)
        Client should not be deleted and not equaled to None
        delete_client(client_id) returns False
        '''

        Client.add_client(self.cl_name, self.cl_phone)
        client = Client.query.filter_by(name=self.cl_name).first()

        assert client is not None
        
        is_successful = Client.delete_client(self.cl_id_negative)
        client = Client.query.filter_by(name=self.cl_name).first()
    
        assert client is not None
        assert is_successful is False
