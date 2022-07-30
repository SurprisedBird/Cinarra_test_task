add_client_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-zA-Z\s]*$",
            "minLength": 1,
            "maxLength": 100,
        },
        "phone_number" : {
            "type": "string",
            "pattern": "^[() \-\d+]*$",
            "minLength": 1,
            "maxLength": 20,
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
            "maxLength": 100,
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
        }
    },
    "required": ["id"]
}