create_speaker_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"type": "string", "minLength": 1, "maxLength": 255},
        "talk": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "minLength": 32, "maxLength": 32}
            },
            "required": ["id"]
        },
        "speaker": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "minLength": 32, "maxLength": 32}
            },
            "required": ["id"]
        }
    },
    "oneOf": [
        {
            "required": ["username", "email"]
        },
        {
            "required": ["speaker"]
        }
    ],
    "required": ["talk"]
}
