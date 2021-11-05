import json
import logging

from flask import request, Response

from conference_management_app import db
from conference_management_app.common.utils import parse_timestamp
from conference_management_app.common.validate_json import validate_json
from conference_management_app.models import Conference
from conference_management_app.web.common.consts import INVALID_DATE_SELECTION, DEFAULT_LIMIT, MAX_PAGE_LIMIT, \
    CONFERENCE_WITH_SAME_TITLE_EXIST, CONFERENCE_NOT_FOUND, CONFERENCE_INVALID_DATA_PROVIDED
from conference_management_app.web.conferences import conference_management_conference
from conference_management_app.web.conferences.schemas import create_conference_schema, conference_schema

LOGGER = logging.getLogger(__name__)


@conference_management_conference.route('/conferences', methods=['GET'])
def get_conferences():
    """
    Get All Conferences
    """
    start = request.args.get('start', 1, type=int)
    limit = request.args.get('limit', DEFAULT_LIMIT, type=int)
    kwargs = dict()
    if request.args.get('start_date'):
        kwargs["start_date"] = request.args.get('start_date')
    elif request.args.get('end_date'):
        kwargs["end_date"] = request.args.get('end_date')

    conferences = db.session.query(Conference).filter_by(**kwargs).paginate(
        start, limit, False, MAX_PAGE_LIMIT)

    if not conferences.items:
        return Response(status=204)

    conferences_json = {
        "items": [conference.to_json() for conference in conferences.items],
        "previous": conferences.prev_num if conferences.has_prev else None,
        "next": conferences.next_num if conferences.has_next else None,
        "pages": conferences.pages
    }
    return Response(json.dumps(conferences_json), status=200, mimetype='application/json')


@conference_management_conference.route('/conferences/<conference_id>', methods=['GET'])
def get_conference(conference_id):
    """
    Get Conferences with Conference ID
    """
    conference = db.session.query(Conference).filter_by(id=conference_id).first()
    if not conference:
        LOGGER.info(f"No Conference found with ID {conference_id}")
        return Response(CONFERENCE_NOT_FOUND, status=404)

    return Response(json.dumps(conference.to_json()), status=200, mimetype='application/json')


@conference_management_conference.route('/conferences', methods=['POST'])
@validate_json(create_conference_schema)
def add_conferences():
    """
    Add Conferences on Conference Management app
    """
    data = request.get_json(force=True)

    start_date = parse_timestamp(data["start_date"])
    end_date = parse_timestamp(data["end_date"])

    if start_date >= end_date:
        return Response(INVALID_DATE_SELECTION, status=400)

    if db.session.query(Conference).filter_by(title=data["title"]).first():
        return Response(CONFERENCE_WITH_SAME_TITLE_EXIST, status=409)

    conference = Conference.from_json_body(data)
    db.session.add(conference)
    db.session.commit()

    return Response(json.dumps(conference.to_json()), status=200, mimetype='application/json')


@conference_management_conference.route('/conferences/<conference_id>', methods=['PATCH'])
@validate_json(conference_schema)
def update_conference(conference_id):
    """
    Update Conference.
    """
    data = request.get_json(force=True)

    if not data:
        return Response(CONFERENCE_INVALID_DATA_PROVIDED, status=400)

    conference = db.session.query(Conference).filter_by(id=conference_id).first()
    if not conference:
        LOGGER.info(f"No Conference found with ID {conference_id}")
        return Response(CONFERENCE_NOT_FOUND, status=404)

    conference.update_from_json(data)
    if conference.start_date > conference.end_date:
        return Response(INVALID_DATE_SELECTION, status=400)

    db.session.commit()
    return Response(json.dumps(conference.to_json()), status=200, mimetype="application/json")


@conference_management_conference.route('/conferences/<conference_id>', methods=['DELETE'])
def delete_conferences(conference_id):
    """
    Delete Conferences on Conference Management app
    """
    conference = db.session.query(Conference).filter_by(id=conference_id).first()
    if not conference:
        LOGGER.info(f"No Conference found with ID {conference_id}")
        return Response(CONFERENCE_NOT_FOUND, status=404)

    db.session.delete(conference)
    db.session.commit()
    return Response(status=200, mimetype='application/json')
