import pytest
from models import Client

class TestClient:
    
    def test_add_client(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        
        assert client is not None
        
        assert client.name == "NoName"
        assert client.phone_number == "0000"
        
    def test_search_client(self):
        Client.add_client("NoName", "0000")
        client = Client.query.filter_by(name = "NoName").first()
        
        assert client is not None
        
        assert client.name == "NoName"
        assert client.phone_number == "0000"
        
    def test_delete_client(self):
        Client.add_client("NoName2", "0000")
        client = Client.query.filter_by(name = "NoName2").first()
        
        client_id = client.id
        assert client.name == "NoName2"
        assert client.phone_number == "0000"
        
        Client.delete_client(client_id)
        
        client = Client.query.filter_by(name = "NoName2").first()
        
        assert client == None