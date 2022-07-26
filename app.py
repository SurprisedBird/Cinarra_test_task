from http import client
from config import app
from models import *
from flask import request, jsonify
import order_iteractions

if __name__ == '__main__':
    app.run(debug=True)
    
