from flask import Blueprint

conference_management_conference = Blueprint('conference_management_conference', __name__)

from conference_management_app.web.conferences import api
