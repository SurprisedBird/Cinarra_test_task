add_order_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string",
                "minLength": 1},
        "price" : {"type": "string",
                "minLength": 1}
    },
    "required": ["name", "price"]
}


search_order_by_client_schema = {
    "type": "object",
    "properties": {
        "client_name": {"type": "string",
        "minLength": 1}
    },
    "required": ["client_name"]
}


search_order_by_id_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string",
        "minLength": 1}
    },
    "required": ["id"]
}

change_order_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string",
        "minLength": 1},
        "client_id": {"type": "string",
        "minLength": 1},
        "driver_id": {"type": "string",
        "minLength": 1},
        "created": {"type": "string",
        "minLength": 1},
        "price": {"type": "string",
        "minLength": 1},
    },
    "required": ["id"]
}

accept_order_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string",
        "minLength": 1},
        "driver_id": {"type": "string",
        "minLength": 1}
    },
    "required": ["id", "driver_id"]
}

cancel_order_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string",
        "minLength": 1}
    },
    "required": ["id"]
}

finish_order_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string",
        "minLength": 1}
    },
    "required": ["id"]
}