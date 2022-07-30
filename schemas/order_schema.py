add_order_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-zA-Z\s]*$",
            "minLength": 1,
            "maxLength": 100,
        },
        "price" : {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
            "maxLength": 5,
        }
    },
    "required": ["name", "price"]
}


search_order_by_client_schema = {
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


search_order_by_id_schema = {
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

change_order_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
        },
        "client_id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1
        },
        "driver_id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1
        },
        "created": {
            "type": "string",
            "minLength": 1
        },
        "price": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
            "maxLength": 5,
        },
    },
    "required": ["id"]
}

accept_order_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1
        },
        "driver_id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1
        }
    },
    "required": ["id", "driver_id"]
}

cancel_order_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1
        }
    },
    "required": ["id"]
}

finish_order_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1
        }
    },
    "required": ["id"]
}