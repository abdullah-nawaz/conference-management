from flask import Blueprint

conference_management_talk = Blueprint('conference_management_talk', __name__)

from conference_management_app.web.talks import api
