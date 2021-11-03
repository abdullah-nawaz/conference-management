import json
import logging

from flask import request, Response

from conference_management_app import db
from conference_management_app.common.validate_json import validate_json
from conference_management_app.web.conferences import conference_management_conference
from conference_management_app.web.conferences.schemas import create_conference_schema

LOGGER = logging.getLogger(__name__)


@conference_management_conference.route('/conferences', methods=['GET'])
def get_conferences():
    """
    Get All Conferences
    """
    return Response(status=200, mimetype='application/json')


@conference_management_conference.route('/conferences/<conference_id>', methods=['GET'])
def get_conferences(conference_id):
    """
    Get Conferences with Conference ID
    """
    return Response(status=200, mimetype='application/json')


@conference_management_conference.route('/conferences', methods=['POST'])
@validate_json(create_conference_schema)
def add_conferences():
    """
    Add Conferences on Conference Management app
    """
    return Response(status=200, mimetype='application/json')


@conference_management_conference.route('/conferences/<conference_id>', methods=['PATCH'])
@validate_json(create_conference_schema)
def update_device(conference_id):
    """
    Update Conference.
    """
    return Response(status=202, mimetype="application/json")


@conference_management_conference.route('/conferences/<conference_id>', methods=['DELETE'])
def delete_conferences(conference_id):
    """
    Delete Conferences on Conference Management app
    """
    return Response(status=200, mimetype='application/json')
