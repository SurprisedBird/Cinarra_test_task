add_driver_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-zA-Z\s]*$",
            "minLength": 1,
            "maxLength": 40,
            "error_msg": "Driver name is not valid"
        },

        "car_number": {
            "type": "string",
            "pattern": "^[A-Z\d+]*$",
            "minLength": 1,
            "maxLength": 40,
            "error_msg": "Driver car number is not valid"
        },

        "phone_number" : {
            "type": "string",
            "pattern": "^[() \-\d+]*$",
            "minLength": 1,
            "maxLength": 20,
            "error_msg": "Driver phone number is not valid"
        }
    },
    "required": ["name"]
}

search_driver_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-zA-Z\s]*$",
            "minLength": 1,
            "maxLength": 40,
            "error_msg": "Driver name is not valid"
        }
    },
    "required": ["name"]
}

delete_driver_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
            "error_msg": "Driver id is not valid"
        }
    },
    "required": ["id"]
}