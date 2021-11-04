conference_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string", "minLength": 1},
        "start_date": {"type": "string", "minLength": 1},
        "end_date": {"type": "string", "minLength": 1}

    }
}

create_conference_schema = {
    "definitions": {
        "conference": conference_schema
    },
    "allOf": [
        {"$ref": "#/definitions/conference"},
        {"required": ["title", "start_date", "end_date"]}
    ]
}
