from flask import Blueprint

conference_management_speaker = Blueprint('conference_management_speaker', __name__)

from conference_management_app.web.speakers import api
