import logging
from functools import wraps

from flask import Response, request
from jsonschema import FormatChecker, ValidationError, validate

from conference_management_app.common.consts import SCHEMA_VALIDATION_INVALID_DETAIL

LOGGER = logging.getLogger(__name__)


def validate_json(schema=None):
    """Validate input data regardless of the content type whether its a valid json or not"""

    def json_decorator(func):
        @wraps(func)
        def json_validator(*args, **kwargs):
            data = request.get_json(force=True)
            if not data:
                return Response(status=400)
            if schema:
                try:
                    validate(data, schema, format_checker=FormatChecker())
                except ValidationError as e:
                    if e.path:
                        msg = SCHEMA_VALIDATION_INVALID_DETAIL.format(
                            path=e.path.pop(),
                            value=e.instance,
                            value_type=e.instance.__class__.__name__,
                            message=e.message,
                            schema_type=e.schema.get("type"),
                            api_url=request.path,
                            validator=e.validator,
                            function_name=func.__name__,
                        )
                    else:
                        msg = e.message
                    LOGGER.info(msg)
                    return Response(status=400)

            return func(*args, **kwargs)

        return json_validator

    return json_decorator
