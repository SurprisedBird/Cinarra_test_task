from config import app
from models import *
from flask import request, jsonify, Response, json
import order_iteractions
import jsonschema
from schemas.client_schema import *
from schemas.driver_schema import *
from schemas.order_schema import *

#client
# -----------------------------------------------------------
@app.route('/add_client',  methods = ['POST'])
def add_client():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, add_client_schema)
    name = request.args.get('name')
    phone_number = request.args.get('phone_number')
    client = Client.add_client(name, phone_number)
    return jsonify({'client_name': client.name})

@app.route('/search_client',  methods = ['GET'])
def search_client():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, search_client_schema)
    name = request.args.get('name')
    client = Client.search_client(name)
    return jsonify({'client_name': client.name})

@app.route('/delete_client>',  methods = ['DELETE'])
def delete_client(id):
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, delete_client_schema)
    id = request.args.get('id', type=int)
    client = Client.delete_client(id)
    return jsonify("{'client_id': client.id}")

# -----------------------------------------------------------

#driver
# -----------------------------------------------------------

@app.route('/add_driver',  methods = ['POST'])
def add_driver():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, add_driver_schema)
    name = request.args.get('name')
    car_number = request.args.get('car_number')
    phone_number = request.args.get('phone_number')
    driver = Driver.add_driver(name, car_number, phone_number)
    return jsonify({'driver_name': driver.name})

@app.route('/search_driver',  methods = ['GET'])
def search_driver():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, search_driver_schema)
    name = request.args.get('name')
    driver = Driver.search_driver(name)
    return jsonify({'driver_name': driver.name})

@app.route('/delete_driver/<int:id>',  methods = ['DELETE'])
def delete_driver(id):
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, delete_driver_schema)
    driver = Driver.delete_driver(id)
    return jsonify({'driver_id': driver.id})

# -----------------------------------------------------------

#order
# -----------------------------------------------------------

@app.route('/add_order', methods = ['POST'])
def add_order():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, add_order_schema)
    name = request.args.get('name')
    price = request.args.get('price')
    client = Client.search_client(name)
    order = Order.add_order(_client_id=client.id, _price=price)
    return jsonify({'order_client_id': order.client_id})

@app.route('/search_order_by_client', methods = ['GET'])
def search_order_by_client():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, search_order_by_client_schema)
    name = request.args.get('name')
    order = Order.search_order_by_client(name)
    return jsonify({'order_id': order.id})

@app.route('/search_order_by_id', methods = ['GET'])
def search_order_by_id():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, search_order_by_id_schema)
    id = request.args.get('id')
    order = Order.search_order_by_id(id)
    return jsonify({'order_id': order.id})

@app.route('/change_order', methods = ['POST'])
def change_order():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, change_order_schema)
    id = request.args.get('id')
    change_message = Order.change_order(id, request.args)
    return jsonify({'change_message': change_message})

# -----------------------------------------------------------


#order_interactions
# -----------------------------------------------------------

@app.route('/accept_order', methods = ['POST'])
def accept_order():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, accept_order_schema)
    id = request.args.get('id')
    driver_id = request.args.get('driver_id')
    order_status = order_iteractions.accept_order(id, driver_id)
    return jsonify({'order_status': order_status})

@app.route('/cancel_order', methods = ['POST'])
def cancel_order():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, cancel_order_schema)
    id = request.args.get('id')
    order_status = order_iteractions.cancel_order(id)
    return jsonify({'order_status': order_status})

@app.route('/finish_order', methods = ['POST'])
def finish_order():
    request_data = request.args.to_dict()
    jsonschema.validate(request_data, finish_order_schema)
    id = request.args.get('id')
    order_status = order_iteractions.finish_order(id)
    return jsonify({'order_status': order_status})

# -----------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
    
