add_order_schema = {
    "type": "object",
    "properties": {
        "client_name": {
            "type": "string",
            "pattern": "^[a-zA-Z\s]*$",
            "minLength": 1,
            "maxLength": 40,
            "error_msg": "Client name is not valid"
        },
        "price" : {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
            "maxLength": 5,
            "error_msg": "Order price is not valid"
        }
    },
    "required": ["client_name", "price"]
}


search_order_by_client_schema = {
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


search_order_by_id_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
            "error_msg": "Order id is not valid"
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
            "error_msg": "Order id is not valid"
        },
        "client_id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
            "error_msg": "Client id is not valid"
        },
        "driver_id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
            "error_msg": "Driver id is not valid"
        },
        "created": {
            "type": "string",
            "pattern": "^[. \-\d+]*$",
            "minLength": 1,
            "maxLength": 10,
            "error_msg": "Order date is not valid"
        },
        "price": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
            "maxLength": 5,
            "error_msg": "Order price is not valid"
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
            "minLength": 1,
            "error_msg": "Order id is not valid"
        },
        "driver_id": {
            "type": "string",
            "pattern": "^\d+$",
            "minLength": 1,
            "error_msg": "Driver id is not valid"
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
            "minLength": 1,
            "error_msg": "Order id is not valid"
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
            "minLength": 1,
            "error_msg": "Order id is not valid"
        }
    },
    "required": ["id"]
}