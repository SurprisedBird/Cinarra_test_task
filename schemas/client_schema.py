add_client_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-zA-Z\s]*$",
            "minLength": 1,
            "maxLength": 40,
            "error_msg": "Client name is not valid"
        },
        "phone_number" : {
            "type": "string",
            "pattern": "^[() \-\d+]*$",
            "minLength": 1,
            "maxLength": 20,
            "error_msg": "Client phone number is not valid"
        }
    },
    "required": ["name"]
}

search_client_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-zA-Z\s]*$",
            "minLength": 1,
            "maxLength": 40,
            "error_msg": "Client name is not valid"
        }
    },
    "required": ["name"]
}

delete_client_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
            "error_msg": "Client id is not valid"
        }
    },
    "required": ["id"]
}