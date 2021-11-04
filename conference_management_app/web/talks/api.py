import json
import logging
from datetime import timedelta

from flask import request, Response

from conference_management_app import db
from conference_management_app.common.utils import parse_timestamp
from conference_management_app.common.validate_json import validate_json
from conference_management_app.models import Talk, Conference
from conference_management_app.web.common.consts import INVALID_DATE_SELECTION, DEFAULT_LIMIT, MAX_PAGE_LIMIT, \
    TALK_WITH_SAME_TITLE_EXIST, TALK_NOT_FOUND, TALK_INVALID_DATA_PROVIDED, CONFERENCE_NOT_FOUND
from conference_management_app.web.talks import conference_management_talk
from conference_management_app.web.talks.schemas import create_talk_schema, talk_schema

LOGGER = logging.getLogger(__name__)


@conference_management_talk.route('/talks', methods=['GET'])
def get_talks():
    """
    Get All Talks
    """
    start = request.args.get('start', 1, type=int)
    limit = request.args.get('limit', DEFAULT_LIMIT, type=int)
    kwargs = dict()
    if request.args.get('conference_id'):
        kwargs["conference_id"] = request.args.get('conference_id')

    talks = db.session.query(Talk).filter_by(**kwargs).paginate(start, limit, False, MAX_PAGE_LIMIT)
    if not talks.items:
        return Response(status=204)

    talks_json = {
        "items": [talk.to_json() for talk in talks.items],
        "previous": talks.prev_num if talks.has_prev else None,
        "next": talks.next_num if talks.has_next else None,
        "pages": talks.pages
    }
    return Response(json.dumps(talks_json), status=200, mimetype='application/json')


@conference_management_talk.route('/talks/<talk_id>', methods=['GET'])
def get_talk(talk_id):
    """
    Get Talks with Talk ID
    """
    talk = db.session.query(Talk).filter_by(id=talk_id).first()
    if not talk:
        LOGGER.info(f"No Talk found with ID {talk}")
        return Response(TALK_NOT_FOUND, status=404)

    return Response(json.dumps(talk.to_json()), status=200, mimetype='application/json')


@conference_management_talk.route('/talks', methods=['POST'])
@validate_json(create_talk_schema)
def add_talks():
    """
    Add Talks on Talk Management app
    """
    data = request.get_json(force=True)

    conference = db.session.query(Conference).filter_by(id=data["conference"]['id']).first()
    if not conference:
        LOGGER.info(f"No Conference found with ID {data['conference']['id']}")
        return Response(CONFERENCE_NOT_FOUND, status=404)

    conference_start_date = conference.start_date
    conference_end_date = conference.end_date
    talk_end_date_time = parse_timestamp(data["date_and_time"]) + timedelta(minutes=data["duration"])

    if parse_timestamp(data["date_and_time"]) > conference_end_date or parse_timestamp(
            data["date_and_time"]) < conference_start_date or talk_end_date_time > conference_end_date:
        return Response(INVALID_DATE_SELECTION, status=400)

    if db.session.query(Talk).filter_by(title=data["title"], conference_id=data['conference']['id']).first():
        return Response(TALK_WITH_SAME_TITLE_EXIST, status=409)

    for talk in conference.talks.all():
        talk_start = talk.date_and_time
        talk_end = talk.date_and_time + timedelta(minutes=talk.duration)
        if talk_start <= parse_timestamp(data["date_and_time"]) < talk_end:
            return Response(INVALID_DATE_SELECTION, status=400)

    talk = Talk.from_json_body(data)
    conference.talks.append(talk)
    db.session.commit()

    return Response(json.dumps(talk.to_json()), status=200, mimetype='application/json')


@conference_management_talk.route('/talks/<talk_id>', methods=['PATCH'])
@validate_json(talk_schema)
def update_talk(talk_id):
    """
    Update Talk.
    """
    data = request.get_json(force=True)

    if not data:
        return Response(TALK_INVALID_DATA_PROVIDED, status=400)

    talk = db.session.query(Talk).filter_by(id=talk_id).first()
    if not talk:
        LOGGER.info(f"No Talk found with ID {talk_id}")
        return Response(TALK_NOT_FOUND, status=404)

    talk.update_from_json(data)
    conference = talk.conference
    if (talk.date_and_time + timedelta(minutes=talk.duration)) > conference.end_date or talk.date_and_time < conference.start_date:
        return Response(INVALID_DATE_SELECTION, status=400)

    db.session.commit()
    return Response(json.dumps(talk.to_json()), status=200, mimetype="application/json")


@conference_management_talk.route('/talks/<talk_id>', methods=['DELETE'])
def delete_talks(talk_id):
    """
    Delete Talks on Talk Management app
    """
    talk = db.session.query(Talk).filter_by(id=talk_id).first()
    if not talk:
        LOGGER.info(f"No Talk found with ID {talk}")
        return Response(TALK_NOT_FOUND, status=404)

    db.session.delete(talk)
    db.session.commit()
    return Response(status=200, mimetype='application/json')
