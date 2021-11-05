talk_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string", "minLength": 1},
        "duration": {"type": "integer", "minimum": 1, "maximum": 60},
        "date_and_time": {"type": "string", "minLength": 1},
    }
}

create_talk_schema = {
    "definitions": {
        "talk": talk_schema,
        "conference": {
            "type": "object",
            "properties": {
                "conference": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "minLength": 32, "maxLength": 32}
                    },
                    "required": ["id"]
                }
            },
            "required": ["conference"]
        }
    },
    "allOf": [
        {"$ref": "#/definitions/talk"},
        {"$ref": "#/definitions/conference"},
        {"required": ["title", "duration", "date_and_time", "conference"]}
    ]
}
