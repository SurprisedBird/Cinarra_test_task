import pytest
from models import Driver

class TestDriver:
    
    def test_add_driver(self):
        Driver.add_driver("NoNameDriver", "ВН2222", "0000")
        driver = Driver.query.filter_by(name = "NoNameDriver").first()
        
        assert driver is not None
        
        assert driver.name == "NoNameDriver"
        assert driver.phone_number == "0000"
        
    def test_search_driver(self):
        Driver.add_driver("NoNameDriver", "ВН2222", "0000")
        driver = Driver.query.filter_by(name = "NoNameDriver").first()
        
        assert driver is not None
        
        assert driver.name == "NoNameDriver"
        assert driver.phone_number == "0000"
        
    def test_delete_driver(self):
        Driver.add_driver("NoNameDriver1", "ВН2222", "0000")
        driver = Driver.query.filter_by(name = "NoNameDriver1").first()
        
        driver_id = driver.id
        assert driver.name == "NoNameDriver1"
        assert driver.phone_number == "0000"
        
        Driver.delete_driver(driver_id)
        
        driver = Driver.query.filter_by(name = "NoNameDriver1").first()
        
        assert driver == None