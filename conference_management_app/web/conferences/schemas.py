conference_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string", "minLength": 1},
        "start_data": {"type": "string", "minLength": 1},
        "end_data": {"type": "string", "minLength": 1}

    }
}

create_conference_schema = {
    "definitions": {
        "conference": conference_schema
    },
    "allOf": [
        {"$ref": "#/definitions/conference"},
        {"required": ["title", "start_data", "end_data"]}
    ]
}
