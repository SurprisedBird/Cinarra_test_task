add_driver_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string",
                "minLength": 1},
        "phone_number" : {"type": "string",
                "minLength": 1}
    },
    "required": ["name"]
}

delete_driver_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string",
        "minLength": 1}
    },
    "required": ["id"]
}

search_driver_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string",
        "minLength": 1}
    },
    "required": ["name"]
}


