from config import app
from models import *
from flask import request, jsonify, Response, json
import order_iteractions
import jsonschema
from schemas.client_schema import *
from schemas.driver_schema import *
from schemas.order_schema import *

def is_valid(request_data, schema):
    try:
        result = jsonschema.validate(request_data, schema)
        return result
    except jsonschema.exceptions.ValidationError as result:
        return result

#client
# -----------------------------------------------------------
@app.route('/add_client',  methods = ['POST'])
def add_client():
    request_data = request.args.to_dict()
    
    result = is_valid(request_data, add_client_schema)
    if result is not None:
        return str(result)
    
    name = request.args.get('name')
    phone_number = request.args.get('phone_number')
    client = Client.add_client(name, phone_number)

    if client is None:
        return "Client is not added"
    else:
        return client.as_dict()

@app.route('/search_client',  methods = ['GET'])
def search_client():
    request_data = request.args.to_dict()
    
    result = is_valid(request_data, search_client_schema)
    if result is not None:
        return str(result)
    
    name = request.args.get('name')
    client = Client.search_client(name)
    
    if client is None:
        return "Client is not found"
    else:
        return client.as_dict()

@app.route('/delete_client/<id>',  methods = ['DELETE'])
def delete_client(id): 
    result = is_valid({"id": id}, delete_client_schema)
    if result is not None:
        return str(result)
    
    is_successful = Client.delete_client(id)
    
    if is_successful:
        return "Client is successfuly deleted"
    else:
        return f"Client is not deleted or not existed"

# -----------------------------------------------------------

#driver
# -----------------------------------------------------------

@app.route('/add_driver',  methods = ['POST'])
def add_driver():
    request_data = request.args.to_dict()

    result = is_valid(request_data, add_driver_schema)
    if result is not None:
        return str(result)
    
    name = request.args.get('name')
    car_number = request.args.get('car_number')
    phone_number = request.args.get('phone_number')
    driver = Driver.add_driver(name, car_number, phone_number)

    if driver is None:
        return "Driver is not added"
    else:
        return driver.as_dict()

@app.route('/search_driver',  methods = ['GET'])
def search_driver():
    request_data = request.args.to_dict()

    result = is_valid(request_data, search_driver_schema)
    if result is not None:
        return str(result)
    
    name = request.args.get('name')
    driver = Driver.search_driver(name)

    if driver is None:
        return "Driver is not found"
    else:
        return driver.as_dict()

@app.route('/delete_driver/<id>',  methods = ['DELETE'])
def delete_driver(id):
    result = is_valid({"id": id}, delete_driver_schema)
    if result is not None:
        return str(result)
    
    is_successful = Driver.delete_driver(id)

    if is_successful:
        return "Driver is successfuly deleted"
    else:
        return f"Driver is not deleted or not existed"

# -----------------------------------------------------------

#order
# -----------------------------------------------------------

@app.route('/add_order', methods = ['POST'])
def add_order():
    request_data = request.args.to_dict()

    result = is_valid(request_data, add_order_schema)
    if result is not None:
        return str(result)
    
    name = request.args.get('name')
    price = request.args.get('price')
    client = Client.search_client(name)
    
    if client is None:
        return "Order is not added. Client is not found."
    
    order = Order.add_order(_client_id=client.id, _price=price)

    if order is None:
        return "Order is not added"
    else:
        return order.as_dict()

@app.route('/search_order_by_client', methods = ['GET'])
def search_order_by_client():
    request_data = request.args.to_dict()

    result = is_valid(request_data, search_order_by_client_schema)
    if result is not None:
        return str(result)

    name = request.args.get('name')
    order = Order.search_order_by_client(name)

    if order is None:
        return "Order is not existed"
    else:
        return order.as_dict()

@app.route('/search_order_by_id', methods = ['GET'])
def search_order_by_id():
    request_data = request.args.to_dict()

    result = is_valid(request_data, search_order_by_id_schema)
    if result is not None:
        return str(result)

    id = request.args.get('id')
    order = Order.search_order_by_id(id)

    if order is None:
        return "Order is not existed"
    else:
        return order.as_dict()

@app.route('/change_order', methods = ['POST'])
def change_order():
    request_data = request.args.to_dict()

    result = is_valid(request_data, change_order_schema)
    if result is not None:
        return str(result)

    id = request.args.get('id')
    change_message = Order.change_order(id, request.args)
    
    return change_message

# -----------------------------------------------------------


#order_interactions
# -----------------------------------------------------------

@app.route('/accept_order', methods = ['POST'])
def accept_order():
    request_data = request.args.to_dict()

    result = is_valid(request_data, accept_order_schema)
    if result is not None:
        return str(result)

    id = request.args.get('id')
    driver_id = request.args.get('driver_id')
    order = order_iteractions.accept_order(id, driver_id)

    if order is None:
        return "Order status is not changed"
    else:
        return order.as_dict()

@app.route('/cancel_order', methods = ['POST'])
def cancel_order():
    request_data = request.args.to_dict()

    result = is_valid(request_data, cancel_order_schema)
    if result is not None:
        return str(result)
    
    id = request.args.get('id')
    order = order_iteractions.cancel_order(id)

    if order is None:
        return "Order status is not changed"
    else:
        return order.as_dict()

@app.route('/finish_order', methods = ['POST'])
def finish_order():
    request_data = request.args.to_dict()

    result = is_valid(request_data, finish_order_schema)
    if result is not None:
        return str(result)
    
    id = request.args.get('id')
    order = order_iteractions.finish_order(id)

    if order is None:
        return "Order status is not changed"
    else:
        return order.as_dict()

# -----------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
    
