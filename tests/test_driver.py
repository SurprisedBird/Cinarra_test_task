import pytest
from models import Driver

@pytest.fixture(autouse=True)
def run_before_test():
    Driver.clear_driver_table()
    yield
    Driver.clear_driver_table()

class TestDriver:
    dr_name = "Any Driver"
    dr_carnum = "AB0000YZ"
    dr_phone = "+3 (099) 333-55-22"

    dr_name_negative = "Any Client Negative"
    dr_id_negative = 2
    
    def test_add_driver(self):
        '''
        Execute add_driver("Any Driver", "AB0000YZ", "+3 (099) 333-55-22")
        Driver should be not None
        Driver name should be "Any Driver"
        Driver car number should be "AB0000YZ"
        Driver phone number should be "+3 (099) 333-55-22"
        '''

        Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum,
        _phone_number=self.dr_phone)
        driver = Driver.query.filter_by(name=self.dr_name).first()
        
        assert driver is not None
        
        assert driver.name == "Any Driver"
        assert driver.car_number == "AB0000YZ"
        assert driver.phone_number == "+3 (099) 333-55-22"
        
    def test_search_driver(self):
        '''
        Create driver by add_driver("Any Driver", "AB0000YZ", "+3 (099) 333-55-22")
        Execute search_driver("Any Driver")
        Driver name should be "Any Driver"
        Driver car number should be "AB0000YZ"
        Driver phone number should be "+3 (099) 333-55-22"
        '''

        Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum,
        _phone_number=self.dr_phone)
        driver = Driver.search_driver(_name=self.dr_name)
        
        assert driver is not None
        
        assert driver.name == "Any Driver"
        assert driver.car_number == "AB0000YZ"
        assert driver.phone_number == "+3 (099) 333-55-22"

    def test_search_driver_negative(self):
        '''
        Create driver by add_driver("Any Driver", "AB0000YZ", "+3 (099) 333-55-22")
        Execute search_driver("Any Driver Negative")
        Driver with this name should not found and should be None
        '''

        Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum, _phone_number=self.dr_carnum)
        driver = Driver.search_driver(_name=self.dr_name_negative)
        
        assert driver is None

    def test_delete_driver(self):
        '''
        Create driver by add_driver("Any Driver", "AB0000YZ", "+3 (099) 333-55-22")
        Save driver id
        Be sure driver is not None
        Execute delete_driver(driver_id)
        Driver should be deleted and equaled to None
        delete_client(client_id) returns True
        '''

        Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum, _phone_number=self.dr_phone)
        driver = Driver.query.filter_by(name=self.dr_name).first()
        driver_id = driver.id

        assert driver is not None
        
        is_successful = Driver.delete_driver(driver_id)
        driver = Driver.query.filter_by(id=driver_id).first()
        
        assert driver is None
        assert is_successful is True

    def test_delete_driver_negative(self):
        '''
        Create driver by add_driver("Any Driver", "AB0000YZ", "+3 (099) 333-55-22")
        Be sure driver is not None
        Execute delete_driver(driver_id_negative)
        Driver should not be deleted and not equaled to None
        delete_driver(driver_id) returns False
        '''

        Driver.add_driver(_name=self.dr_name, _car_number=self.dr_carnum,
        _phone_number=self.dr_phone)
        driver = Driver.query.filter_by(name=self.dr_name).first()

        assert driver is not None
        
        is_successful = Driver.delete_driver(self.dr_id_negative)
        driver = Driver.query.filter_by(name=self.dr_name).first()
    
        assert driver is not None
        assert is_successful is False
        