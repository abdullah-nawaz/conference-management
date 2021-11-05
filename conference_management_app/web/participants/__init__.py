from flask import Blueprint

conference_management_participant = Blueprint('conference_management_participant', __name__)

from conference_management_app.web.participants import api
